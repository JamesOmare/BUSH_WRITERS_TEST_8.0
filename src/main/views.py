import os
import secrets
import requests
import json
from requests.auth import HTTPBasicAuth
import base64
import logging
from datetime import datetime
import PIL.Image
from flask import (Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app, abort, Response,
                   copy_current_request_context)
from ..models.accounts import Account
from ..models.users import User
from ..models.notification import Notification
from ..models.complaints import Complaints
from ..models.images import Image
from ..models.confirmation import Confirmation
from ..models.account_credentials import Account_Credentials
from ..models.payment import Payment
from ..models.subscription_list import Subscription
from ..auth.form_fields import (Seller_Profile_Form, Account_Images, Update_User_Account, Payment_Method, 
                                Complaint, Confirmation_Form, Seller_Account_Details, Search, FilteredSearch,
                                Mpesa_Confirm, Contact_Us, Order_By, Seller_Complete_Account_Details, Accept_Account,
                                Upload_Images, Full_Purchase, Partial_Purchase)
from ..utils import db, mail
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_, desc, asc
from datetime import date
from werkzeug.utils import secure_filename
from decouple import config
import phonenumbers
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from flask_mail import Message 
from http import HTTPStatus

# configure logging
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


main = Blueprint('main', __name__)

# Custom Functions
def save_picture_thumbnail(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pics', picture_fn)

    output_size = (125, 125)
    img = PIL.Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn

def save_pictures(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/account_images', picture_fn)

    img = PIL.Image.open(form_picture)
    img.save(picture_path)

    return picture_fn

def save_file_credentials(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/file_credentials', picture_fn)

    img = PIL.Image.open(form_picture)
    img.save(picture_path)

    return picture_fn


@main.route('/search', methods = ['POST', 'GET'])
def search_results():
    search_form = Search()
    filter_form = FilteredSearch()
    purchase_form = Payment_Method()
    order_by_form = Order_By()
    page = request.args.get('page', 1, type=int)
    accounts = Account.query.filter_by(status = 0).paginate(page=page, per_page=10, error_out=False)

    if request.method == 'POST':

        if search_form.validate_on_submit():
            # get data from submitted form
            keyword = search_form.keyword.data
            print(keyword)
    
            # query the database
            searched_accounts = Account.query.filter(Account.description.like('%' + keyword + '%')).paginate(page=page, per_page=10, error_out=False)    
            return render_template('search.html', form = search_form, logged_in_user=current_user, keyword = keyword, account = searched_accounts, purchase_form = purchase_form, order = order_by_form, filter_form = filter_form)
        
    return render_template('search.html', form = search_form, logged_in_user=current_user, account = accounts, purchase_form = purchase_form, order = order_by_form, filter_form = filter_form)

@main.route('/about_us', methods = ['GET', 'POST'])
def about_us():
    return render_template('about_us.html')

@main.route('/', methods = ['GET', 'POST'])
def viewpage():
    page = request.args.get('page', 1, type=int)
    account = Account.query.filter_by(status = 0).paginate(page=page, per_page=10, error_out=False)
    search_form = Search()
    filter_form = FilteredSearch()
    purchase_form = Payment_Method()
    order_by_form = Order_By()

    if current_user.is_anonymous:
        notification = False

    if current_user.is_authenticated:
        buyer_msg = Notification.query.filter_by(buyer_id = current_user.id).first()
        seller_msg = Notification.query.filter_by(seller_id = current_user.id).first()

        #check if notifications exist
        notification = True if buyer_msg or seller_msg else False
    
   
    if request.method == 'POST':
        if purchase_form.validate_on_submit():
            account_id = purchase_form.info.data
            payment_method = purchase_form.payment_method.data
            account_seller = Account.query.filter_by(account_id = account_id).first()
            if payment_method == 'Mpesa':
                buyer_id = current_user.id
                seller_id = account_seller.user_id
                return redirect(url_for('main.mpesa_payment', payment_method = payment_method, product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
            elif payment_method == 'Paypal':
                buyer_id = current_user.id
                seller_id = account_seller.user_id
                return redirect(url_for('main.paypal_payment', payment_method = payment_method, product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
            else:
                return render_template('404.html'), 404

        elif order_by_form.validate_on_submit():
            order_item = order_by_form.account_type.data
            if order_item == "highest_price":
                account = Account.query.filter_by(status = 0).order_by(Account.price.desc()).paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            elif order_item == "lowest_price":
                account = Account.query.filter_by(status = 0).order_by(Account.price.asc()).paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            elif order_item == "date_posted_old":
                account = Account.query.filter_by(status = 0).order_by(Account.time_posted.asc()).paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            elif order_item == "date_posted_new":
                account = Account.query.filter_by(status = 0).order_by(Account.time_posted.desc()).paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            
            return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, notification = notification)
        
        elif filter_form.validate_on_submit():
            article_ac = filter_form.article_ac.data
            academic_ac = filter_form.academic_ac.data
            blogging_ac = filter_form.blogging_ac.data
            price_range_a = filter_form.price_range_a.data
            price_range_b = filter_form.price_range_b.data

                
            if article_ac and academic_ac and blogging_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "ARTICLE_ACCOUNT" and "BLOGGING_ACCOUNT" and "ACADEMIC_WRITING_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            
            elif not article_ac and academic_ac and blogging_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "BLOGGING_ACCOUNT" and "ACADEMIC_WRITING_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)

            elif not academic_ac and article_ac and blogging_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "ARTICLE_ACCOUNT" and "BLOGGING_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            
            elif not blogging_ac and article_ac and academic_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "ARTICLE_ACCOUNT" and "ACADEMIC_WRITING_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)

            elif not article_ac and not academic_ac and blogging_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "BLOGGING_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            
            elif not article_ac and not blogging_ac and academic_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "ACADEMIC_WRITING_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)

            elif not academic_ac and not blogging_ac and article_ac and price_range_a and price_range_b:
                account_ = Account.query.filter_by(status = 0).filter((Account.account_type == "ARTICLE_ACCOUNT")).filter((Account.price >= price_range_a) & (Account.price <= price_range_b))
                account = account_.paginate(page=page, per_page=10, error_out=False)
                return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)
            
            else:
                print(filter_form.form_errors)

    return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form, order = order_by_form, filter_form = filter_form, notification = notification)

@main.route('/product_view/<item_id>', methods=['GET', 'POST'])
def product_view(item_id):
    account = Account.query.filter_by(account_id = item_id).first()
    images = Image.query.filter_by(account_id = item_id).all()
    purchase_form = Payment_Method()
    upload_form = Upload_Images()
   
    if request.method == 'POST':
        if purchase_form.submit.data and purchase_form.validate_on_submit():
            account_id = purchase_form.info.data
            payment_method = purchase_form.payment_method.data
            account_seller = Account.query.filter_by(account_id = account_id).first()
            if payment_method == 'Mpesa':
                buyer_id = current_user.id
                seller_id = account_seller.user_id
                return redirect(url_for('main.mpesa_payment', payment_method = payment_method, product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
            elif payment_method == 'Paypal':
                buyer_id = current_user.id
                seller_id = account_seller.user_id
                return redirect(url_for('main.paypal_payment', product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
            else:
                return render_template('404.html'), 404

        elif upload_form.upload.data and upload_form.validate_on_submit():
            uploaded_images = upload_form.photo.data
            account_id = upload_form.account_id.data
            

            
            if uploaded_images:
                # Filter Image
                image_file = save_pictures(uploaded_images)

                # Save record
                image_entry = Image(
                    image_files = image_file,
                    user_id = current_user.id,
                    account_id = account_id
                )
                db.session.add(image_entry)
                db.session.commit()
            return render_template('product_view.html', account = account, images = images, purchase_form = purchase_form, upload_form = upload_form)

        else:
            print(upload_form.form_errors)
            print("here")

    
    return render_template('product_view.html', account = account, images = images, purchase_form = purchase_form, upload_form = upload_form)


@main.route('/user_profile/<id>')
@login_required
def user_profile(id):
    user = User.query.filter_by(id = id).first()
    buyer_msg = Notification.query.filter_by(buyer_id = id).first()
    seller_msg = Notification.query.filter_by(seller_id = id).first()

    #check if notifications exist
    notification = True if buyer_msg or seller_msg else False
   
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    return render_template('user_profile.html', accounts = accounts, account_holder = user, notification = notification)

@main.route('/contact_us', methods=['GET', 'POST'])
def contact_us():
    form = Contact_Us()
    if request.method == 'POST' and form.validate_on_submit():
        sender_name = form.sender_name.data
        sender_email = form.sender_email.data
        subject = form.subject.data
        message = form.message.data

        msg = Message(subject, 
                    sender= (sender_email),
                    recipients=["jamesmwafrica254@gmail.com"]
                    )
        msg.body = message
        mail.send(msg)
    
        flash("Message sent successfully", "success")

        subscription_entry = Subscription(
            client_email = sender_email
        )

        db.session.add(subscription_entry)
        db.session.commit()

    return render_template('contact_us.html', form = form)


@main.route('/guide')
def guide():
    return render_template('guide.html')
  


@main.route('/new_seller', methods=['GET', 'POST'])
@login_required
def seller():
    seller_form = Seller_Profile_Form()
    
    if request.method == 'POST':
        if seller_form.validate_on_submit():
            name = seller_form.account_name.data
            brand = seller_form.account_brand.data
            category = seller_form.account_type.data
            description = seller_form.account_description.data
            date = seller_form.account_creation_date.data
            images = seller_form.images.data
            price = seller_form.account_value.data

            

            account_entry = Account(
                account_name=name,
                account_type=category,
                brand=brand,
                price=price,
                description=description,
                account_creation_date=date,
                user = current_user,

            )

            db.session.add(account_entry)
            db.session.commit()
        
            latest_ac = Account.query.filter_by(user_id = current_user.id).order_by(Account.time_posted.asc()).first()
            
           
            if images:
                for image in images:
                    # Filter Image
                    image_file = save_pictures(image)

                    # Save record
                    image_entry = Image(
                        image_files = image_file,
                        user_id = current_user.id,
                        account_id = latest_ac.account_id
                    )
                    db.session.add(image_entry)
                db.session.commit()

            return redirect(url_for("main.viewpage"))

        else:
            print(seller_form.form_errors)

    return render_template('test_seller_form.html', form = seller_form)

@main.route('/update', methods = ['GET', 'POST'])
def update_profile():
    update_form = Update_User_Account()
    if update_form.validate_on_submit():
        email = update_form.email.data
        firstname = update_form.first_name.data
        lastname = update_form.last_name.data
        phone_number = update_form.phone.data
        profile_description = update_form.profile_details.data
        profile_image = update_form.profile_image.data
        if profile_image:
            picture_file = save_picture_thumbnail(profile_image)
            current_user.profile_photo = picture_file
        current_user.username = firstname + " " + lastname
        current_user.email = email
        current_user.phone_number = phone_number
        current_user.profile_description = profile_description
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.user_profile', id = current_user.id))
    elif request.method == 'GET':
        my_username = fr"{current_user.username}"
        first_name, last_name = my_username.split()
        update_form.first_name.data = first_name
        update_form.last_name.data = last_name
        update_form.email.data = current_user.email
        update_form.phone.data = current_user.phone_number
        update_form.profile_details.data = current_user.profile_description
        update_form.profile_image.data = current_user.profile_photo
    image_file = url_for('static', filename='images/profile_pics/' + current_user.profile_photo)
    return render_template('update_account_form.html', title='Account',
                           image_file=image_file, form=update_form)


@main.route('/chat_page/<id>', methods = ['GET', 'POST'])
@login_required
def chat(id):
    buyer_msg = Notification.query.filter_by(buyer_id = id).all()
    seller_msg = Notification.query.filter_by(seller_id = id).all()
    account_credentials = Account_Credentials.query.filter_by(buyer_id = id).all()
    buyer_form = Complaint()
    seller_form = Seller_Account_Details()
    accept_form = Accept_Account()
    seller_form_complete = Seller_Complete_Account_Details()
    purchase_completion = Full_Purchase()
    partial_completion = Partial_Purchase()
    file_names = []
    if buyer_msg and seller_msg:
        if request.method == 'POST':
            if buyer_form.submit.data and buyer_form.validate_on_submit():
                seller_id = buyer_form.seller_id.data
                account_id = buyer_form.account_id.data
                reason = buyer_form.reason.data
                extended_reason = buyer_form.extended_reason.data

                if not extended_reason:
                    extended_reason = None

                complaint_entry = Complaints(
                    buyer_id = current_user.id,
                    seller_id = seller_id,
                    account_id = account_id,
                    reason = reason,
                    further_description = extended_reason
                )

                db.session.add(complaint_entry)
                db.session.commit()
                
                flash('Successfully sent complaint to admin, purchase status updated!', 'success')

                return render_template('chat.html', buyer_msg =  buyer_msg, form = buyer_form, accept_form = accept_form)

            elif seller_form.submit.data and seller_form.validate_on_submit():
                buyer_id = seller_form.buyer_id.data
                account_id = seller_form.account_id.data
                account_email = seller_form.account_email.data
                account_url = seller_form.account_url.data
                account_passphrase = seller_form.account_passphrase.data

                credentials_entry = Account_Credentials(
                    seller_id = current_user.id,
                    buyer_id = buyer_id,
                    account_id = account_id,
                    account_email = account_email,
                    account_url = account_url,
                    account_passphrase = account_passphrase

                )

                db.session.add(credentials_entry)
                db.session.commit()
                flash('Successfully sent account credential details to admin, Please wait for account verification!', 'success')
                return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form)

            elif accept_form.accept.data and accept_form.validate_on_submit():
                seller_id = accept_form.seller_id.data
                account_id = accept_form.account_id.data

                alert = Notification.query.filter_by(account_id = account_id).first()
                updated_type = 3
                alert.type = updated_type
                db.session.commit()
                
                flash('Account Purchase Confirmation approved.', 'success')
                return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form)


        else:
            return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form, seller_form_complete = seller_form_complete)
    
    elif buyer_msg and not seller_msg:
        if account_credentials:
            if request.method == 'POST': 
                if buyer_form.submit.data and buyer_form.validate_on_submit():
                    seller_id = buyer_form.seller_id.data
                    account_id = buyer_form.account_id.data
                    reason = buyer_form.reason.data
                    extended_reason = buyer_form.extended_reason.data

                    if not extended_reason:
                        extended_reason = None


                    complaint_entry = Complaints(
                        buyer_id = current_user.id,
                        account_id = account_id,
                        seller_id = seller_id,
                        reason = reason,
                        further_description = extended_reason
                    )

                    db.session.add(complaint_entry)
                    db.session.commit()
                    logging.info(f'Successfully sent complaint to the admin.')

                    # update buyer notification status
                    alert = Notification.query.filter_by(account_id = account_id).first()
                    print('Alert is: ', alert ,'\n', 'Seller id is: ', seller_id)
                    updated_type = 4
                    alert.type = updated_type
                    db.session.commit()
                    logging.info(f'Successfully updated the notification to status "4"(Failed purchase alert)\n which will notify the seller that their account has been rejected .')

                    flash('Successfully sent complaint to admin, purchase status updated!', 'success')
                    return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form, accounts = account_credentials, accept_form = accept_form)

                elif accept_form.accept.data and accept_form.validate_on_submit():
                    seller_id = accept_form.seller_id.data
                    account_id = accept_form.account_id.data

                    alert = Notification.query.filter_by(account_id = account_id).first()
                    updated_type = 3
                    alert.type = updated_type
                    db.session.commit()

                    logging.info(f'Successfully updated notification to status "3"(Successful purchase alert).')
                    
                    flash('Account Purchase Confirmation approved.', 'success')
                    return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form) 

                elif purchase_completion.completed.data and purchase_completion.validate_on_submit():
                    seller_id = accept_form.seller_id.data
                    account_id = accept_form.account_id.data

                    alert = Notification.query.filter_by(account_id = account_id).first()
                    updated_type = 5
                    alert.type = updated_type
                    db.session.commit()

                    logging.info(f'Successfully updated notification to status "5" which indicates completion of purchase process by the buyer.')
                    
                    flash('Account Purchase Process Completed. Thank you', 'success')
                    flash('You are higly advised to change account credentials at this point', 'error')
                    return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form, purchase_completion = purchase_completion, partial_completion = partial_completion) 

                elif partial_completion.additional_info.data and partial_completion.validate_on_submit():
                    seller_id = accept_form.seller_id.data
                    account_id = accept_form.account_id.data

                    alert = Notification.query.filter_by(account_id = account_id).first()
                    updated_type = 6
                    alert.type = updated_type
                    db.session.commit()

                    logging.info(f'Successfully updated notification to status "6" where the seller is notified to send additional account credentials for the final purchase step.')
                    
                    flash('Successfully sent to the admin. Please wait while we get in contact with the buyer to request additional account credentials.', 'success')
                    return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form, purchase_completion = purchase_completion, partial_completion = partial_completion) 
                
            return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form, accounts = account_credentials, accept_form = accept_form, purchase_completion = purchase_completion, partial_completion = partial_completion)


        else:
            return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form, accept_form = accept_form)
    

    elif seller_msg and not buyer_msg:
        if request.method == 'POST' and seller_form.submit.data and seller_form.validate_on_submit():
            buyer_id = seller_form.buyer_id.data
            account_id = seller_form.account_id.data
            account_email = seller_form.account_email.data
            account_url = seller_form.account_url.data
            account_passphrase = seller_form.account_passphrase.data

            credentials_entry = Account_Credentials(
                seller_id = current_user.id,
                buyer_id = buyer_id,
                account_id = account_id,
                account_email = account_email,
                account_url = account_url,
                account_passphrase = account_passphrase

            )

            db.session.add(credentials_entry)
            db.session.commit()
            logging.info(f'Successfully sent account credentials to the buyer.')

            alert = Notification.query.filter_by(account_id = account_id).first()
            updated_type = 2
            alert.type = updated_type
            db.session.commit()
            logging.info(f'Successfully updated notification status to "2"(Account credentials added alert) which will alert the buyer with the account credentials i.e email, hyperlink for the buyer to decide to purchase or reject account.')

            flash('Successfully sent account credential details to admin, Please wait for account verification!', 'success')
            return render_template('chat.html', seller_msg = seller_msg, seller_form = seller_form, seller_form_complete = seller_form_complete)

        elif request.method == 'POST' and seller_form_complete.submit.data and seller_form_complete.validate_on_submit():
                seller_id = seller_form_complete.seller_id.data
                account_id = seller_form_complete.account_id.data
                account_cerificate = seller_form_complete.account_cerificate.data
                account_license = seller_form_complete.account_license.data
                other_documents = seller_form_complete.other.data

                # if photo:
                #     filename = secure_filename(photo.filename)
                #     file_names.append(filename)
                #     photos.save(photo)

                # ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

                # def allowed_file(filename):
                #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

                # for file in account_cerificate:
                #     if file and allowed_file(file.filename):
                #         filename = secure_filename(file.filename)
                #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # flash('File(s) successfully uploaded')

                
                
                flash('Account Purchase Confirmation approved.', 'success')
                return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form, accept_form = accept_form) 

        return render_template('chat.html', seller_msg = seller_msg, seller_form = seller_form, seller_form_complete = seller_form_complete)


    elif not buyer_msg and not seller_msg:
        return render_template('chat.html')

   




#paypal operations
def paypal_capture_function(order_id):
    post_route = f"/v2/checkout/orders/{order_id}/capture"
    paypal_capture_url = config('PAYPAL_API_URL') + post_route
    basic_auth = HTTPBasicAuth(config('PAYPAL_BUSINESS_CLIENT_ID'), config('PAYPAL_BUSINESS_SECRET'))
    headers = {
        "Content-Type": "application/json",
    }
    response = requests.post(url=paypal_capture_url, headers=headers, auth=basic_auth)
    response.raise_for_status()
    json_data = response.json()
    return json_data
 
def is_approved_payment(captured_payment):
    status = captured_payment.get("status")
    amount = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get("value")
    currency_code = captured_payment.get("purchase_units")[0].get("payments").get("captures")[0].get("amount").get(
        "currency_code")
    print(f"Payment happened. Details: {status}, {amount}, {currency_code}")
    if status == "COMPLETED":
        return True
    else:
        return False

@main.route("/paypal_payment/<product_id>/<buyer_id>/<seller_id>")
@login_required
def paypal_payment(product_id, buyer_id, seller_id):
    return render_template("paypal_payment.html", paypal_business_client_id=config('PAYPAL_BUSINESS_CLIENT_ID'),
                           price=config('IB_TAX_APP_PRICE'), currency=config('IB_TAX_APP_PRICE_CURRENCY'), product_id = product_id, buyer_id=buyer_id, seller_id = seller_id)
    
    

@main.route("/payment/<order_id>/capture/<product_id>/<buyer_id>/<seller_id>", methods=["POST"])
@login_required
def capture_payment(order_id, product_id, buyer_id, seller_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    if is_approved_payment(captured_payment):
        # Capture Payment Callback
        buyer_id = buyer_id
        seller_id = seller_id
        product_id = product_id
        transaction_id = captured_payment['id']
        transaction_status = captured_payment['status']
        paypal_email = captured_payment['payment_source']['paypal']['email_address']
        country_code = captured_payment['payment_source']['paypal']['address']['country_code']
        payment_currency = captured_payment['purchase_units'][0]['payments']['captures'][0]['amount']['currency_code']
        gross_payment = captured_payment['purchase_units'][0]['payments']['captures'][0]['amount']['value']
        paypal_fee = captured_payment['purchase_units'][0]['payments']['captures'][0]['seller_receivable_breakdown']['paypal_fee']['value']
        net_payment = captured_payment['purchase_units'][0]['payments']['captures'][0]['seller_receivable_breakdown']['net_amount']['value']
        datetime_str = captured_payment['purchase_units'][0]['payments']['captures'][0]['update_time']
        # A list containing multiple characters, that needs to be deleted from the string.
        list_of_chars = ['T', 'Z']
        # Filter multiple characters from string
        filtered_chars = filter(lambda item: item not in list_of_chars, datetime_str)
        # Join remaining characters in the filtered list
        sample_str = ''.join(filtered_chars)
        transaction_date = sample_str[0:10]
        transaction_time = sample_str[10:18]

        # add payment details to the database
        payment_data = Payment(
            buyer_id = buyer_id,
            seller_id = seller_id,
            product_id = product_id,
            status = transaction_status,
            payment_method = 'paypal',
            transaction_id = transaction_id,
            country_code = country_code,
            gross_pay = gross_payment,
            paypal_fee = paypal_fee,
            paypal_email = paypal_email,
            net_pay = net_payment,
            currency_paid = payment_currency,
            transaction_date = transaction_date,
            transaction_time = transaction_time
        )
        db.session.add(payment_data)
        db.session.commit()

        # change account status to on progess *verified since the payment is confirmed
        account = Account.query.filter_by(account_id = product_id).first()
        account.status = 2
        db.session.commit()

        # Update account status to verification stage
        account.status = 2
        db.session.commit()
        
        # display notification to user profile
        alert_message = True
        alert_type = 0
        alert = Notification(
            buyer_id = buyer_id,
            seller_id = seller_id,
            account_id = product_id,
            purchase_verification_message = alert_message,
            type = alert_type
        )

        db.session.add(alert)
        db.session.commit()
    return jsonify(captured_payment)



#mpesa operations

# get access token
def getAccesstoken():
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # make a get request using python requests liblary
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = r.json()['access_token']
    return access_token

# Initialize M-PESA Express request
def MpesaExpress(phone, amount, my_endpoint, product_id, buyer_id, seller_id):
    account = Account.query.filter_by(account_id = product_id).first()
    endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    access_token = getAccesstoken()
    headers = {
        "Authorization": "Bearer %s" % access_token
    }
    Timestamp = datetime.now()
    time = Timestamp.strftime('%Y%m%d%H%M%S')
    password = '174379' + 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919' + time
    password = base64.b64encode(password.encode('utf-8')).decode()
    data = {
        "BusinessShortCode" : "174379",
        "Password": password,
        "Timestamp": time,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": my_endpoint + f"/stk_callback/{product_id}/{buyer_id}/{seller_id}",
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount

    }
    if account.status != 0:
        flash('The account has already been purchased or is at a state of being transfered, Return to marketplace to view other accounts.', 'error')
    else:
        res = requests.post(endpoint, json = data, headers = headers)
        print("Server end transaction status: ", res.json())
        return res.json()


@main.route('/payment/<payment_method>/<product_id>/<buyer_id>/<seller_id>', methods = ['GET', 'POST'])
@login_required
def mpesa_payment(payment_method, product_id, buyer_id, seller_id):
    mpesa_form = Mpesa_Confirm()
    account = Account.query.filter_by(account_id = product_id).first()
    my_endpoint = "https://0e0f-154-157-176-217.in.ngrok.io"
    fee = 1
    total = fee
    if request.method == 'POST':
            unfilterd_number = request.form.get('number')
            if not unfilterd_number:
                flash('The number supplied is invalid', 'error')
            number = phonenumbers.parse(unfilterd_number, "KE")
            phone_number = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
            phone = phone_number.lstrip("+")
            amount = total
            MpesaExpress(phone,amount, my_endpoint, product_id, buyer_id, seller_id)
            account = Account.query.filter_by(account_id = product_id).first()
            if account.status == 2:
                flash('Mpesa confirmation code has been verified, please check your notitfications.', 'success')
        
    return render_template('payment.html', mpesa_form = mpesa_form, account = account, buyer_id = buyer_id, seller_id = seller_id)



@main.route('/refresh_url/<product_id>', methods = ['GET', 'POST'])
def refresh(product_id):
    account = Account.query.filter_by(account_id = product_id).first()
    if account.status == 2:
        return "accepted"
    else:
        return "rejected"
   


#consume M-PESA Express callback
@main.route('/stk_callback/<product_id>/<buyer_id>/<seller_id>', methods=['POST'])
def incoming(product_id, buyer_id, seller_id):
    if request.method == 'POST':
        unfiltered_data = request.get_json()
        filtered_data = str(unfiltered_data).replace("'", '"')
        data = json.loads(filtered_data)
        if unfiltered_data:
            filtered_data = str(unfiltered_data).replace("'", '"')
            data = json.loads(filtered_data)
            result_code = data['Body']['stkCallback']['ResultCode']
            if result_code == 0:
                buyer_id = buyer_id
                seller_id = seller_id
                product_id = product_id
                transaction_status = 'SUCCESS'
                transaction_id = data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
                gross_pay = data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
                payment_number = data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
                date_int = data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
                date_str =  str(date_int)
                date_object = datetime.strptime(date_str, '%Y%m%d%H%M%S').date()
                time_object = datetime.strptime(date_str, '%Y%m%d%H%M%S').time()
                transaction_date = str(date_object)
                transaction_time = str(time_object)


                # Store transaction result
                payment_data = Payment(
                        buyer_id = buyer_id,
                        seller_id = seller_id,
                        product_id = product_id,
                        status = transaction_status,
                        payment_method = 'mpesa',
                        transaction_id = transaction_id,
                        country_code = 'KE',
                        gross_pay = gross_pay,
                        mpesa_fee = 0,
                        net_pay = 0,
                        payment_number = payment_number,
                        currency_paid = 'KSH',
                        transaction_date = transaction_date,
                        transaction_time = transaction_time
                    )
                db.session.add(payment_data)
                db.session.commit()
            

                # change account status to on progess *verified since the payment is confirmed
                account = Account.query.filter_by(account_id = product_id).first()

                # change status from on progress to verification stage
                account.status = 2
                db.session.commit()

                # display notification to user profile
                alert_message = True
                alert_type = 0
                alert = Notification(
                    buyer_id = current_user.id,
                    seller_id = account.user_id,
                    account_id = account.account_id,
                    purchase_verification_message = alert_message,
                    type = alert_type
                )

                db.session.add(alert)
                db.session.commit()
                print('----------------------------------')
                print('status updated successfully 🤩')
                print('-----------------------------------')
               
                

            elif result_code == 1032:
                transaction_status = 'Cancelled By user'
                print(transaction_status)

            elif result_code == 2001:
                transaction_status = 'Wrong credentials entered'
                print(transaction_status)

            elif result_code == 17:
                transaction_status = 'A concurrent transaction is already taking place. Please wait'
                print(transaction_status)
            else:
                print('Some unknown result code.')

    return Response(status = 405)





@main.route('/on_progress/<product_id>', methods = ['POST', 'GET'])
@login_required
def on_progress(product_id):
    account = Account.query.filter_by(account_id = product_id).first()
    confirmation_form = Confirmation_Form()

    if request.method == 'POST' and confirmation_form.validate_on_submit():
        msg = confirmation_form.confirmation_msg.data
        confirmation_msg = msg[0:10]
        confirm_payment = Payment.query.filter_by(transaction_id = confirmation_msg).first()

        if confirm_payment:
            flash('Mpesa confirmation code has been verified, please check your notitfications.', 'success')

            # change status from on progress to verification stage
            account.status = 2
            db.session.commit()

            # display notification to user profile
            alert_message = True
            alert_type = 0
            alert = Notification(
                buyer_id = current_user.id,
                seller_id = account.user_id,
                account_id = account.account_id,
                purchase_verification_message = alert_message,
                type = alert_type
            )

            db.session.add(alert)
            db.session.commit()
            return redirect(url_for('main.chat', id = current_user.id))
        
        else:
            message = Confirmation(
                buyer_id = current_user.id,
                confirmation_msg = msg,
                buyer_email = current_user.email,
                seller_id = account.user_id,
                account_id = account.account_id
            )

            db.session.add(message)            

            try:
               
                db.session.commit()

            except IntegrityError:
                db.session.rollback()
                flash('Do not resend the message, kindly wait while we confirm the payment.', 'warning')

            except PendingRollbackError:
                db.session.rollback()
                flash('Do not resend the message, kindly wait while we confirm the payment.', 'warning')

            except:
                flash('Do not resend the message, kindly wait while we confirm the payment.', 'warning')

            else:
                flash('Confirmation message send to admin sucessfully, please wait.', 'success')


            return render_template('confirmation_message.html', form = confirmation_form)
    return render_template('confirmation_message.html', form = confirmation_form)



@main.route("/delete_notification", methods = ["POST"])
def delete_msg():
    if request.method == "POST":
        logging.info(f'Successfully received post request to delete notification by user of id {current_user.id}')
        ref = request.form.get('ref')

        if ref:
            notification = Notification.query.filter_by(id = ref).first()

            # delete notification
            db.session.delete(notification)
            db.session.commit()

            logging.info(f'Successfully deleted notification of id {ref} as prompted by user of id {current_user.id}')
            return Response(status = 204)
    
        logging.info(f'Failed to delete notification.')
        return abort(404, description="Resource not found")


@main.route("/delete_image", methods = ["POST"])
def delete_image():
    if request.method == "POST":
        logging.info(f'Successfully received post request to delete image by user of id {current_user.id}')
        ref = request.form.get('ref')
        print('ref id: ', ref)
        if ref:
            image = Image.query.filter_by(id = ref).first()

            # delete image
            db.session.delete(image)
            db.session.commit()

            logging.info(f'Successfully deleted image of id {ref} as prompted by user of id {current_user.id}')
            return Response(status = 204)
    
        logging.info(f'Failed to delete image.')
        return abort(404, description="Resource not found")


