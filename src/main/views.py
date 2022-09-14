from crypt import methods
from flask import Blueprint, redirect, render_template, request, flash, url_for, jsonify
from ..models.accounts import Account
from ..utils import db
from flask_login import login_user, logout_user, login_required, current_user

main = Blueprint('main', __name__)


@main.route('/view')
def homepage():
    return render_template('view.html')

@main.route('/')
def viewpage():
    account = Account.query.all()
    return render_template('view2.html', account = account, logged_in_user = current_user)

@main.route('/new', methods=['GET', 'POST'])
def create():
    context = {
        'min_price' : 1000,
        'max_price' : 10000
    }
    
    if request.method == 'GET':
        return render_template('create_account.html', **context)
    else:
        account_type = request.form["account_type"]
        price = request.form["price"]
        description = request.form['description']

        account_types = ['ARTICLE_ACCOUNT', 'ACADEMIC_WRITING_ACCOUNT', 'BLOGGING_ACCOUNT']

        #ensure only three types of accounts are submitted
        if account_type not in account_types:
            return render_template('create_account.html')


        new_entry = Account(
            account_type = account_type,
            price = price,
            description = description
        )

        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("main.viewpage"))

@main.route('/new_seller', methods=['GET', 'POST'])
def seller():
    
    # context = {
    #     'min_price' : 1000,
    #     'max_price' : 10000
    # }
    
    # if request.method == 'GET':
    #     return render_template('create_account.html', **context)
    # else:
    #     account_type = request.form["account_type"]
    #     price = request.form["price"]
    #     description = request.form['description']

    #     account_types = ['ARTICLE_ACCOUNT', 'ACADEMIC_WRITING_ACCOUNT', 'BLOGGING_ACCOUNT']

    #     #ensure only three types of accounts are submitted
    #     if account_type not in account_types:
    #         return render_template('create_account.html')


    #     new_entry = Account(
    #         account_type = account_type,
    #         price = price,
    #         description = description
    #     )

    #     db.session.add(new_entry)
    #     db.session.commit()

        return render_template('seller_prompt.html')

