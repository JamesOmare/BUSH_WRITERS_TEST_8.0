import os
import secrets
import PIL.Image
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify, current_app
from ..models.accounts import Account
from ..models.images import Image
from ..auth.form_fields import Seller_Profile_Form
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


@main.route('/user_profile')
@login_required
def user_profile():
    accounts = Account.query.filter_by(user_id = current_user.id).all()
    return render_template('user_profile.html', accounts = accounts, account_holder = current_user)


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

# def save_default(form)


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
        image = seller_form.image.data
        price = seller_form.account_value.data
        

        if image:
            secure_file = secure_filename(image.filename)
            image_file = save_picture(secure_file)
        else:
            image_file = None

        if date > date.today():
            flash("Invalid creation date entered", 'success')
            return redirect(url_for('main.seller'))

        account_entry = Account(
            account_name=name,
            account_type=category,
            brand=brand,
            price=price,
            description=description,
            account_creation_date=date,
            image_file=image_file,
            user = current_user
        )

        db.session.add(account_entry)
        db.session.commit()

        return redirect(url_for("main.viewpage"))

    return render_template('seller_prompt2.html', form=seller_form)
