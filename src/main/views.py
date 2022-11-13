import os
import secrets
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
import PIL.Image
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app
from ..models.accounts import Account
from ..models.users import User
from ..models.messages import Message
from ..models.complaints import Complaints
from ..models.images import Image
from ..models.confirmation import Confirmation
from ..models.account_credentials import Account_Credentials
from ..auth.form_fields import (Seller_Profile_Form, Account_Images, Update_User_Account, Payment_Method, 
                                Complaint, Confirmation_Form, Seller_Account_Details, Search, FilteredSearch)
from ..utils import db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import and_, desc,asc
from datetime import date
from werkzeug.utils import secure_filename
from decouple import config

main = Blueprint('main', __name__)


@main.route('/search', methods = ['POST', 'GET'])
def search_results():
    form = Search()
    filter_form = FilteredSearch()
    purchase_form = Payment_Method()
    page = request.args.get('page', 1, type=int)
    accounts = Account.query.filter_by(status = 0)
    if form.validate_on_submit():
        # get data from submitted form
        keyword = form.keyword.data

        # query the database
        accounts = accounts.filter(Account.description.like('%' + keyword + '%'))
        accounts = accounts.order_by(Account.account_type).paginate(page=page, per_page=10)
        return render_template('search.html', form = form, logged_in_user=current_user, keyword = keyword, account = accounts, purchase_form = purchase_form)

    # if filter_form.validate_on_submit():
    #     article_ac = filter_form.article_ac.data
    #     academic_ac = filter_form.academic_ac.data
    #     blogging_ac = filter_form.blogging_ac.data
    #     date_from = filter_form.date_from.data
    #     date_to = filter_form.date_to.data
    #     price_range_a = filter_form.price_range_a.data
    #     price_range_b = filter_form.price_range_b.data

    #     # if article_ac and academic_ac and blogging_ac and date_from and date_to and price_range_a and price_range_b:

    #     # elif not article_ac and academic_ac and blogging_ac and date_from and date_to and price_range_a and price_range_b:

    #     # elif not article_ac and not academic_ac and not blogging_ac and date_from and date_to and price_range_a and price_range_b:

    #     # elif not article_ac and not academic_ac and not blogging_ac and not date_from and date_to and price_range_a and price_range_b:

    #     if article_ac and academic_ac and blogging_ac:
    #         if date_from or date_to:
    #             if price_range_a or price_range_b:
            
    #         elif price_range_a or price_range_b:

    #         else:
    #             accounts = accounts.all()
    #             return render_template('search.html', form = form, filter_form = filter_form, logged_in_user=current_user, accounts = accounts)
    #     elif not article_ac and academic_ac and blogging_ac:
    #         if date_from or date_to:
    #             if price_range_a or price_range_b:

    #     elif not article_ac and not academic_ac and blogging_ac:
    #         if date_from or date_to:
    #             if price_range_a or price_range_b:
        
    #     elif not article_ac and not academic_ac and not blogging_ac:
    #         if date_from or date_to:
    #             if price_range_a or price_range_b:

            

    return render_template('search.html', form = form, logged_in_user=current_user, account = accounts, purchase_form = purchase_form)



@main.route('/', methods = ['GET', 'POST'])
def viewpage():
    page = request.args.get('page', 1, type=int)
    account = Account.query.filter_by(status = 0).paginate(page=page, per_page=10)
    search_form = Search()
    purchase_form = Payment_Method()
   
    if request.method == 'POST' and purchase_form.validate_on_submit():
        account_id = purchase_form.info.data
        payment_method = purchase_form.payment_method.data
        account_seller = Account.query.filter_by(account_id = account_id).first()
        if payment_method == 'Mpesa':
            buyer_id = current_user.id
            seller_id = account_seller.user_id
            return redirect(url_for('main.mpesa_payment', product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
        elif payment_method == 'Paypal':
            buyer_id = current_user.id
            seller_id = account_seller.user_id
            return redirect(url_for('main.paypal_payment', product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
        else:
            return render_template('404.html'), 404
    return render_template('view.html', account=account, logged_in_user=current_user, purchase_form = purchase_form, form = search_form)

@main.route('/product_view/<item_id>', methods=['GET', 'POST'])
def product_view(item_id):
    account = Account.query.filter_by(account_id = item_id).first()
    images = Image.query.filter_by(account_id = item_id).all()
    purchase_form = Payment_Method()
   
    if request.method == 'POST' and purchase_form.validate_on_submit():
        account_id = purchase_form.info.data
        payment_method = purchase_form.payment_method.data
        account_seller = Account.query.filter_by(account_id = account_id).first()
        if payment_method == 'Mpesa':
            buyer_id = current_user.id
            seller_id = account_seller.user_id
            return redirect(url_for('main.mpesa_payment', product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
        elif payment_method == 'Paypal':
            buyer_id = current_user.id
            seller_id = account_seller.user_id
            return redirect(url_for('main.paypal_payment', product_id = account_id, buyer_id = buyer_id, seller_id = seller_id))
        else:
            return render_template('404.html'), 404

    # print("Account ID: ",current_user.account_id)
    return render_template('product_view.html', account = account, images = images, purchase_form = purchase_form)


@main.route('/user_profile/<id>')
@login_required
def user_profile(id):
    user = User.query.filter_by(id = id).first()
    msg = Message.query.filter_by(user_id = id).first()

    # if msg:
    #     notification = True
    # else:
    #     notification = False
    notification = True if msg else False

    # if current_user.id != user.id:
    #     flash('You do not have permission to enter this page', category='error')
    #     return redirect(url_for('auth.login'))
    
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    return render_template('user_profile.html', accounts = accounts, account_holder = user, notification = notification)
  


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





@main.route('/new_seller', methods=['GET', 'POST'])
@login_required
def seller():
    seller_form = Seller_Profile_Form()
    
    if request.method == 'POST' and seller_form.validate_on_submit():
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

    return render_template('seller_form.html', form=seller_form)

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
    buyer_msg = Message.query.filter_by(buyer_id = id).all()
    seller_msg = Message.query.filter_by(seller_id = id).all()
    account_credentials = Account_Credentials.query.filter_by(buyer_id = id).all()
    buyer_form = Complaint()
    seller_form = Seller_Account_Details()
    if buyer_msg and seller_msg:
        if request.method == 'POST' and buyer_form.validate_on_submit():
            seller_id = buyer_form.seller_id.data
            user_number = buyer_form.buyer_phone_number.data
            seller_number = buyer_form.seller_phone_number.data
            reason = buyer_form.reason.data
            extended_reason = buyer_form.extended_reason.data

            if not extended_reason:
                extended_reason = None

            complaint_entry = Complaints(
                buyer_id = current_user.id,
                seller_id = seller_id,
                buyer_number = user_number,
                seller_number = seller_number,
                reason = reason,
                further_description = extended_reason
            )

            db.session.add(complaint_entry)
            db.session.commit()
            flash('Successfully sent complaint to admin, purchase status updated!', 'success')

            return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form)

        elif request.method == 'POST' and seller_form.validate_on_submit():
            buyer_id = seller_form.buyer_id.data
            account_id = seller_form.account_id.data
            account_name = seller_form.account_name.data
            account_type = seller_form.account_type.data
            account_email = seller_form.account_email.data
            account_url = seller_form.account_url.data
            account_passphrase = seller_form.account_passphrase.data

            credentials_entry = Account_Credentials(
                seller_id = current_user.id,
                buyer_id = buyer_id,
                account_name = account_name,
                account_type = account_type,
                account_email = account_email,
                account_url = account_url,
                account_passphrase = account_passphrase

            )

            db.session.add(credentials_entry)
            db.session.commit()
            flash('Successfully sent account credential details to admin, Please wait for account verification!', 'success')
            return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form)
        else:
            if seller_msg:
                return render_template('chat.html', buyer_msg = buyer_msg, seller_msg = seller_msg, form = buyer_form, seller_form = seller_form)
            return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form)
    
    elif buyer_msg and not seller_msg:
        if account_credentials:
            if request.method == 'POST' and buyer_form.validate_on_submit():
                user_number = buyer_form.buyer_phone_number.data
                seller_number = buyer_form.seller_phone_number.data
                reason = buyer_form.reason.data
                extended_reason = buyer_form.extended_reason.data

                if not extended_reason:
                    extended_reason = None

                complaint_entry = Complaints(
                    buyer_id = current_user.id,
                    buyer_number = user_number,
                    seller_number = seller_number,
                    reason = reason,
                    further_description = extended_reason
                )

                db.session.add(complaint_entry)
                db.session.commit()
                flash('Successfully sent complaint to admin, purchase status updated!', 'success')

                return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form, accounts = account_credentials)
            return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form, accounts = account_credentials)
        else:
            return render_template('chat.html', buyer_msg = buyer_msg, form = buyer_form)
    

    elif seller_msg and not buyer_msg:
        if request.method == 'POST' and seller_form.validate_on_submit():
            buyer_id = seller_form.buyer_id.data
            account_id = seller_form.account_id.data
            account_name = seller_form.account_name.data
            account_type = seller_form.account_type.data
            account_email = seller_form.account_email.data
            account_url = seller_form.account_url.data
            account_passphrase = seller_form.account_passphrase.data

            credentials_entry = Account_Credentials(
                seller_id = current_user.id,
                buyer_id = buyer_id,
                account_id = account_id,
                account_name = account_name,
                account_type = account_type,
                account_email = account_email,
                account_url = account_url,
                account_passphrase = account_passphrase

            )

            db.session.add(credentials_entry)
            db.session.commit()

            alert = Message.query.filter_by(account_id = account_id).first()
            print('Previous_Account_Type:', alert.type)
            updated_type = 2
            alert.type = updated_type
            db.session.commit()
            print('Current_Account_Type:', alert.type)
            flash('Successfully sent account credential details to admin, Please wait for account verification!', 'success')
            return render_template('chat.html', seller_msg = seller_msg, seller_form = seller_form)
        return render_template('chat.html', seller_msg = seller_msg, seller_form = seller_form)


    elif not buyer_msg and not seller_msg:
        return render_template('chat.html')

    # else:
    #     return render_template('chat.html')




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

@main.route("/payment")
@login_required
def paypal_payment():
    return render_template("paypal_payment.html", paypal_business_client_id=config('PAYPAL_BUSINESS_CLIENT_ID'),
                           price=config('IB_TAX_APP_PRICE'), currency=config('IB_TAX_APP_PRICE_CURRENCY'))

@main.route("/payment/<order_id>/capture", methods=["POST"])
@login_required
def capture_payment(order_id):  # Checks and confirms payment
    captured_payment = paypal_capture_function(order_id)
    # print(captured_payment)
    if is_approved_payment(captured_payment):
        # Do something (for example Update user field)
        pass
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


@main.route('/payment/<product_id>/<payment_method>', methods = ['GET', 'POST'])
@login_required
def mpesa_payment(product_id, payment_method):
    account = Account.query.filter_by(account_id = product_id).first()

    if payment_method == 'Mpesa':
        return render_template()
    
    return render_template('payment.html', account = account)


my_endpoint = 'https://cdbf-102-2-160-42.in.ngrok.io'


# Initialize M-PESA Express request
# /pay?phone=&amount=1
@main.route('/pay')
@login_required
def MpesaExpress():
    amount = request.args.get('amount')
    phone = request.args.get('phone')

    endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    access_token = getAccesstoken()
    headers = {
        "Authorization": "Bearer %s" % access_token
    }
    Timestamp = datetime.now()
    times = Timestamp.strftime('%Y%m%d%H%M%S')
    password = '174379' + 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919' + times
    password = base64.b64encode(password.encode('utf-8')).decode()

    data = {
        "BusinessShortCode" : "174379",
        "Password": password,
        "Timestamp": times,
        "TransactionType": "CustomerBuyGoodsOnline",
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": my_endpoint + "/lnmo-callback",
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount

    }

    res = requests.post(endpoint, json = data, headers = headers)
    return res.json()


#consume M-PESA Express callback
@main.route('/lnmo-callback', methods=['POST'])
@login_required
def incoming():
    data = request.get_json()
    print(data)
    return "OK"


@main.route('/on_progress/<product_id>', methods = ['POST', 'GET'])
@login_required
def on_progress(product_id):
    account = Account.query.filter_by(account_id = product_id).first()
    confirmation_form = Confirmation_Form()

    if request.method == 'POST' and confirmation_form.validate_on_submit():
        msg = confirmation_form.confirmation_msg.data

        message = Confirmation(
            buyer_id = current_user.id,
            confirmation_msg = msg,
            buyer_email = current_user.email,
            seller_id = account.user_id,
            account_id = account.account_id
        )

        db.session.add(message)
        db.session.commit()

        flash('Confirmation message send to admin sucessfully, please wait.', 'success')
        return render_template('confirmation_message.html', form = confirmation_form)
    return render_template('confirmation2.html', form = confirmation_form)

# @main.route('/verification_stage/<product_id>', methods = ['POST', 'GET'])
# def verification_stage(product_id):
#     if request.method == 'POST':





