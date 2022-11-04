from flask_admin.contrib.sqla import ModelView
from src import db, admin
from src.models.users import User
from src.models.accounts import Account
from src.models.confirmation import Confirmation
from src.models.account_credentials import Account_Credentials
from wtforms.fields import SelectField, PasswordField, StringField
from flask_admin import Admin, BaseView, expose, Admin, AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from flask import g, url_for, flash, request, render_template
from flask_admin.actions import action
from sqlalchemy.sql import func
from ..auth.form_fields import AdminForm, Payment_Status
from ..models.messages import Message
from ..models.complaints import Complaints

# class AdminAuthentication(object):
#     def is_accessible(self):
#         return g.user.is_authenticated and g.user.is_admin()

# class BaseModelView(AdminAuthentication, ModelView):
#     pass



# class IndexView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/index.html')

class OnProgressView(ModelView):
    can_delete = False
    can_create = False

    list_template = 'admin/add2.html'
    edit_template = 'admin/edit.html'

    #  Override to allow POSTS
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        return super(OnProgressView, self).index_view()
    
    def render(self, template, **kwargs):
        # we are only interested in our custom list page
        if template == 'admin/add2.html':
            
            def get_counting_query(self):
                return self.session.query(func.count('*')).filter(self.model.status==1).scalar()
            
            kwargs['number'] = get_counting_query(self)
                        


        return super(OnProgressView, self).render(template, **kwargs)
    
    _status_choices = [(choice, label) for choice, label in [
        (Account.STATUS_AVAILABLE, 'Available'),
        (Account.STATUS_ON_PROGRESS, 'On_Progress'),
        (Account.STATUS_VERIFICATION_STAGE, 'Verification_Stage'),
        (Account.STATUS_SUCCESSFUL_STAGE, 'Successful_Stage'),
        (Account.STATUS_DISPUTED_STAGE, 'Disputed_Stage'),
    ]]
    column_choices = {
    'status': _status_choices,
    }

    form_ajax_refs = {
        'user': {
        'fields': (User.username, User.email),
        },
    }

    column_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user']
    column_searchable_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user.email', 'user.phone_number']
    column_filters = ['account_id','status', 'account_creation_date', 'time_posted',User.username, User.email, User.phone_number, User.active ]
    
    # column_editable_list = ['status']
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['status']
    form_overrides = {'status': SelectField}
    can_export = True
    export_types = ['csv', 'xlsx']

    def get_query(self):
      return self.session.query(self.model).filter(self.model.status==1)

    

    
class VerificationView(ModelView):
    can_delete = False
    can_create = False
    
    _status_choices = [(choice, label) for choice, label in [
        (Account.STATUS_AVAILABLE, 'Available'),
        (Account.STATUS_ON_PROGRESS, 'On_Progress'),
        (Account.STATUS_VERIFICATION_STAGE, 'Verification_Stage'),
        (Account.STATUS_SUCCESSFUL_STAGE, 'Successful_Stage'),
        (Account.STATUS_DISPUTED_STAGE, 'Disputed_Stage'),
    ]]
    column_choices = {
    'status': _status_choices,
    }

    form_ajax_refs = {
        'user': {
        'fields': (User.username, User.email),
        },
    }

    column_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user']
    column_searchable_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user.email', 'user.phone_number']
    column_filters = ['account_id','status', 'account_creation_date', 'time_posted',User.username, User.email, User.phone_number, User.active ]
    
    # column_editable_list = ['status']
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['status']
    form_overrides = {'status': SelectField}
    can_export = True
    export_types = ['csv', 'xlsx']

    def get_query(self):
      return self.session.query(self.model).filter(self.model.status==2)

class SucessView(ModelView):
    can_delete = False
    can_create = False
    
    _status_choices = [(choice, label) for choice, label in [
        (Account.STATUS_AVAILABLE, 'Available'),
        (Account.STATUS_ON_PROGRESS, 'On_Progress'),
        (Account.STATUS_VERIFICATION_STAGE, 'Verification_Stage'),
        (Account.STATUS_SUCCESSFUL_STAGE, 'Successful_Stage'),
        (Account.STATUS_DISPUTED_STAGE, 'Disputed_Stage'),
    ]]
    column_choices = {
    'status': _status_choices,
    }

    form_ajax_refs = {
        'user': {
        'fields': (User.username, User.email),
        },
    }

    column_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user']
    column_searchable_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user.email', 'user.phone_number', 'user.username']
    column_filters = ['account_id','status', 'account_creation_date', 'time_posted', User.username, User.email, User.phone_number, User.active ]
    
    # column_editable_list = ['status']
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['status']
    form_overrides = {'status': SelectField}
    can_export = True
    export_types = ['csv', 'xlsx']

    def get_query(self):
      return self.session.query(self.model).filter(self.model.status==3)

class DisputedView(ModelView):
    # @expose('/')
    # def custom(self):
    #     return self.render('admin/add.html')
    can_delete = False
    can_create = False
    list_template = 'admin/add.html'
    edit_template = 'admin/edit.html'

    #  Override to allow POSTS
    @expose('/', methods=('GET', 'POST'))
    def index_view(self):
        return super(DisputedView, self).index_view()
    
    def render(self, template, **kwargs):
        # we are only interested in our custom list page
        if template == 'admin/add.html':
            
            def get_counting_query(self):
                return self.session.query(func.count('*')).filter(self.model.status==4).scalar()
            
            kwargs['number'] = get_counting_query(self)
                        


        return super(DisputedView, self).render(template, **kwargs)
    
    _status_choices = [(choice, label) for choice, label in [
        (Account.STATUS_AVAILABLE, 'Available'),
        (Account.STATUS_ON_PROGRESS, 'On_Progress'),
        (Account.STATUS_VERIFICATION_STAGE, 'Verification_Stage'),
        (Account.STATUS_SUCCESSFUL_STAGE, 'Successful_Stage'),
        (Account.STATUS_DISPUTED_STAGE, 'Disputed_Stage'),
    ]]
    column_choices = {
    'status': _status_choices,
    }

    form_ajax_refs = {
        'user': {
        'fields': (User.username, User.email),
        },
    }

    column_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user']
    column_searchable_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user.email', 'user.phone_number']
    column_filters = ['account_id','status', 'account_creation_date', 'time_posted',User.username, User.email, User.phone_number, User.active ]
    
    # column_editable_list = ['status']
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['status']
    form_overrides = {'status': SelectField}
    can_export = True
    export_types = ['csv', 'xlsx']

    def get_query(self):
      return self.session.query(self.model).filter(self.model.status==4)


    def get_count_query(self):
      return self.session.query(func.count('*')).filter(self.model.status==4)

    @expose('/claims')
    # @login_required
    # @has_role('admin')
    def second_page(self):
        complaints = Complaints.query.all()
        if not complaints:
            complaints = None
        return self.render('admin/complaint_claims.html', claims = complaints)


# class UserView(ModelView):
#     @action('approve', 'Approve', 'Are you sure you want to approve selected users?')
#     def action_approve(self, ids):
#         try:
#             query = User.query.filter(User.id.in_(ids))

#             count = 0
#             for user in query.all():
#                 if user.approve():
#                     count += 1

#             flash(ngettext('User was successfully approved.',
#                            '%(count)s users were successfully approved.',
#                            count,
#                            count=count))
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 raise

#             flash(gettext('Failed to approve users. %(error)s', error=str(ex)), 'error')

# class MyView(BaseView):
#     @expose('/')
#     def index(self):
#         return 'Hello World!'

class NotificationView(BaseView):
    @expose('/')
    def custom(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    # @login_required
    # @has_role('admin')
    def second_page(self):
        return self.render('admin/notification.html')

class FormView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def form(self):
        form = AdminForm()
        if request.method == 'POST':
            if form.validate_on_submit() == False:
                flash('All fields are required.', 'error')
                return self.render('admin/form.html', form=form)
            else:
                login_email = form.ac_login_email.data
                login_pass = form.ac_login_pass.data
                buyer_id = form.buyer_id.data
                account_id = form.account_id.data
                new_msg = Message(
                    login_password = login_pass,
                    login_email = login_email,
                    type = 2,
                    buyer_id = buyer_id,
                    account_id = account_id
                )

                db.session.add(new_msg)
                db.session.commit()
                flash('Message sent succcessfully to recipient', 'success')
                return self.render('admin/form.html', form = form)
        return self.render('admin/form.html', form = form)

            # elif form.type == 0:
            #     buyer_id = form.user_id.data
            #     account_id = form.account_id.data
            #     alert_message = form.intent_message.data
            #     purchase_intent_msg = Message(
            #         buyer_id = buyer_id,
            #         account_id = account_id,
            #         intent_message = alert_message
            #     )
            #     db.session.add(purchase_intent_msg)
            #     db.session.commit()
            #     flash('Message sent succcessfully to recipient', 'success')
            #     return self.render('admin/form.html', form = form)

            # elif form.type == 1:
            #     buyer_id = form.user_id.data
            #     account_id = form.account_id.data
            #     alert_message = form.purchase_verification_message.data
            #     purchase_verification_msg = Message(
            #         buyer_id = buyer_id,
            #         account_id = account_id,
            #         purchase_verification_message = alert_message
            #     )
            #     db.session.add(purchase_verification_msg)
            #     db.session.commit()
            #     flash('Message sent succcessfully to recipient', 'success')
            #     return self.render('admin/form.html', form = form)

            # elif form.type == 2:
            #     buyer_id = form.user_id.data
            #     account_id = form.account_id.data
            #     alert_message = form.successful_purchase.data
            #     successful_purchase_msg = Message(
            #         buyer_id = buyer_id,
            #         account_id = account_id,
            #         successful_purchase = alert_message
            #     )
            #     db.session.add(successful_purchase_msg)
            #     db.session.commit()
            #     flash('Message sent succcessfully to recipient', 'success')
            #     return self.render('admin/form.html', form = form)

            # elif form.type == 3:
            #     buyer_id = form.user_id.data
            #     account_id = form.account_id.data
            #     alert_message = form.failed_purchase.data
            #     failed_purchase_msg = Message(
            #         buyer_id = buyer_id,
            #         account_id = account_id,
            #         failed_purchase = alert_message
            #     )
            #     db.session.add(failed_purchase_msg)
            #     db.session.commit()
            #     flash('Message sent succcessfully to recipient', 'success')
            #     return self.render('admin/form.html', form = form)

            


class AccountModelView(ModelView):
    _status_choices = [(choice, label) for choice, label in [
        (Account.STATUS_AVAILABLE, 'Available'),
        (Account.STATUS_ON_PROGRESS, 'On_Progress'),
        (Account.STATUS_VERIFICATION_STAGE, 'Verification_Stage'),
        (Account.STATUS_SUCCESSFUL_STAGE, 'Successful_Stage'),
        (Account.STATUS_DISPUTED_STAGE, 'Disputed_Stage'),
    ]]
    column_choices = {
    'status': _status_choices,
    }

    column_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted']
    column_searchable_list = ['account_id', 'account_type', 'account_name', 'description', 'brand', 'price', 'status', 'account_creation_date', 'time_posted', 'user.email', 'user.phone_number']
    column_filters = ['status', 'account_creation_date', 'time_posted', Account.account_id, Account.account_name, Account.price, Account.status, User.id, User.username, User.email, User.phone_number, User.active, User.date_created ]
    form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
    }
    form_columns = ['account_type', 'account_name', 'description', 'brand', 'price', 'status']
    form_overrides = {'status': SelectField}
    can_export = True
    export_types = ['csv', 'xlsx']

   
    

class UserModelView(ModelView):
    column_list = ['id', 'username', 'email', 'phone_number', 'profile_photo', 'active', 'date_created']
    column_searchable_list = ['id', 'username', 'email', 'phone_number', 'profile_photo', 'active', 'date_created', 'account.brand', 'account.price']
    column_filters = ['active',User.id, User.phone_number, User.date_created, Account.account_name, Account.price, Account.brand, Account.brand, Account.status, Account.account_id, Account.account_type, 'date_created']
    form_columns = ['id', 'username', 'admin', 'email', 'phone_number', 'password', 'profile_photo', 'active', 'date_created']
    form_extra_fields = {
    'password': PasswordField('New password'),
    }
    can_export = True
    export_types = ['csv', 'xlsx']
def on_model_change(self, form, model, is_created):
    if form.password.data:
        model.password_hash = User.make_password(form.password.data)
        return super(UserModelView, self).on_model_change(form, model, is_created)


class Confirmation_Message(BaseView):
    @expose('/', methods=('GET', 'POST'))
    # @login_required
    # @has_role('admin')
    def notification_page(self):
        confirmation = Confirmation.query.all()
        form = Payment_Status()
        if request.method == 'POST':
            if not confirmation:
                confirmation = None
            if form.validate_on_submit() == False:
                flash('All fields are required.', 'error')
                return self.render('admin/on_progress.html', form=form, confirmations = confirmation)
            else:
                confirmed = form.success.data
                rejected = form.failure.data
                account_id = form.account_id.data
                buyer_id = form.buyer_id.data
                seller_id = form.seller_id.data
                account = Account.query.filter_by(account_id = account_id).first()
                if confirmed:
                    print('Account status was: ', account.status, 'Account id: ', account_id)
                    account.status = 2
                    # db.session.refresh(account)
                    db.session.merge(account)
                    db.session.commit()
                    # print('Account session: ' , Account.query.session.connection().engine)
                    # print('db session: ', db.session.connection().engine)
                    # print(' ', Account.query.session == db.session)
                    # print(' ', Account.query.session.connection() == db.session.connection())
                    print('Account status now is: ',account.status)
                    # print(Account.query.session.connection().engine.url)
                    # print(db.session.connection().engine.url)
                    alert_message = True
                    alert_type = 0
                    alert = Message(
                        buyer_id = buyer_id,
                        seller_id = seller_id,
                        account_id = account_id,
                        purchase_verification_message = alert_message,
                        type = alert_type
                    )

                    db.session.add(alert)
                    db.session.commit()
                    flash('Status has been updated successfully', 'success')
                    return self.render('admin/on_progress.html', form = form, confirmations = confirmation)
                elif rejected:
                    print('Account Status is', account.status)
                    flash('The buyer will be notified of the purchase status', 'danger')
                    return self.render('admin/on_progress.html', form = form, confirmations = confirmation)
        return self.render('admin/on_progress.html', confirmations = confirmation, form = form)

class Rejected_Accounts(BaseView):
    @expose('/')
    # @login_required
    # @has_role('admin')
    def second_page(self):
        complaints = Complaints.query.all()
        if not complaints:
            complaints = None
        return self.render('admin/complaint_claims.html', claims = complaints)


class NotificationsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/notify.html')


admin.add_view(UserModelView(User, db.session))
admin.add_view(AccountModelView(Account, db.session))
path = op.join(op.dirname(__file__), '../static')
admin.add_view(FileAdmin(path, '/static/', name='Static Files'))
admin.add_view(NotificationView(name='Custom'))
admin.add_view(FormView(name='Forms'))
admin.add_view(OnProgressView(Account, db.session, name='On Progress', endpoint="on_progress"))
admin.add_view(VerificationView(Account, db.session, name='Verification Pending', endpoint="pending_verification"))
admin.add_view(SucessView(Account, db.session, name='Successful', endpoint="success"))
admin.add_view(DisputedView(Account, db.session, name='Disputed', endpoint="disputed"))
admin.add_view(Confirmation_Message(name = 'Confirmation Messeges', category="Incoming Messages"))
admin.add_view(Rejected_Accounts(name = 'Rejection Messeges', category="Incoming Messages"))