import os
import secrets
import PIL.Image
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app
from ..models.accounts import Account
from ..models.users import User
from ..models.messages import Message
from ..models.complaints import Complaints
from ..models.images import Image
from ..auth.form_fields import Seller_Profile_Form, Account_Images, Update_User_Account, Complaint
from ..utils import db
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
from werkzeug.utils import secure_filename


main = Blueprint('main', __name__)


@main.route('/view')
def homepage():
    return render_template('view.html')


@main.route('/')
def viewpage():
    account = Account.query.all()
    return render_template('view2.html', account=account, logged_in_user=current_user)

@main.route('/product_view')
def product_view():
    return render_template('product_view.html')


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

    if current_user.id != user.id:
        flash('You do not have permission to enter this page', category='error')
        return redirect(url_for('auth.login'))
    else:
        accounts = Account.query.filter_by(user_id = current_user.id).all()
        print(notification)
        return render_template('user_profile.html', accounts = accounts, account_holder = current_user, notification = notification)
  


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images/profile_pics', picture_fn)

    output_size = (125, 125)
    img = PIL.Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_fn




@main.route('/new_seller', methods=['GET', 'POST'])
@login_required
def seller():
    seller_form = Seller_Profile_Form()
    # image_files = Account_Images()
    if request.method == 'POST' and seller_form.validate_on_submit():
        name = seller_form.account_name.data
        brand = seller_form.account_brand.data
        category = seller_form.account_type.data
        description = seller_form.account_description.data
        date = seller_form.account_creation_date.data
        # images = image_files.images.data
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
        # print('user_email: ',current_user.email, 'image_account_id: ', current_user.account)

        # print(images)
        # print('current user:',current_user)
        # if images:
        #     picture_file = save_picture(images)
        #     print(picture_file)
        
        #     single_entry = Image(
        #             image_files = picture_file,
        #             user = current_user,
        #             account = '2'
        #         )

        #     db.session.add(single_entry)
        #     db.session.commit()
        
        

        # if images:
        #     for image in images:
        #         print('second')
        #         save_picture(image)
        #         image_entry = Image(
        #             image_files = image
        #         )

        #         db.session.add(image_entry)
        #     db.session.commit()
               

        # else:
        #     image = None
        #     single_entry = Image(
        #         image_files = image
        #     )

        #     db.session.add(single_entry)
        #     db.session.commit()
        

        return redirect(url_for("main.viewpage"))

    return render_template('seller_prompt2.html', form=seller_form)

@main.route('/update', methods = ['GET', 'POST'])
def update_profile():
    update_form = Update_User_Account()
    if update_form.validate_on_submit():
        email = update_form.email.data
        firstname = update_form.first_name.data
        lastname = update_form.last_name.data
        phone_number = update_form.phone.data
        profile_image = update_form.profile_image.data
        if profile_image:
            picture_file = save_picture(profile_image)
            current_user.profile_photo = picture_file
        current_user.username = firstname + " " + lastname
        current_user.email = email
        current_user.phone_number = phone_number
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.user_profile'))
    elif request.method == 'GET':
        my_username = fr"{current_user.username}"
        first_name, last_name = my_username.split()
        update_form.first_name.data = first_name
        update_form.last_name.data = last_name
        update_form.email.data = current_user.email
        update_form.phone.data = current_user.phone_number
        update_form.profile_image.data = current_user.profile_photo
    image_file = url_for('static', filename='images/profile_pics/' + current_user.profile_photo)
    return render_template('update_account_form.html', title='Account',
                           image_file=image_file, form=update_form)


@main.route('/chat_page/<id>', methods = ['GET', 'POST'])
def chat(id):
    msg = Message.query.filter_by(user_id = id).all()
    form = Complaint()
    if msg:
        if request.method == 'POST' and form.validate_on_submit():
            user_number = form.buyer_phone_number.data
            seller_number = form.seller_phone_number.data
            reason = form.reason.data
            extended_reason = form.extended_reason.data

            if not extended_reason:
                extended_reason = None

            complaint_entry = Complaints(
                user_id = current_user.id,
                buyer_number = user_number,
                seller_number = seller_number,
                reason = reason,
                further_description = extended_reason
            )

            db.session.add(complaint_entry)
            db.session.commit()
            flash('Successfully sent complaint to admin, purchase status updated!', 'success')

            return render_template('chat.html', msg = msg, form = form)
        else:
            return render_template('chat.html', msg = msg, form = form)

    else:
        return render_template('chat.html')
    
