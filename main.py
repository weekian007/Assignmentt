import requests

import Admin
import User
import Customer
import shelve
import jwt


from flask import Flask, render_template, request, redirect, url_for,session
from flask_rbac import RBAC
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from Forms import CreateCustomerForm, CreateAdminForm
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField,validators
from wtforms.validators import InputRequired,Email,Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Idontknowman'
app.config["SESSION_PERMANENT"] = False
app.secret_key = "secret"
app.config["SESSION_TYPE"] = "filesystem"
secret = "WKGAY"



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'


@app.route('/get/')
def get():
    return session.get('key','not set')


@app.route('/')
def index():
    return render_template('home.html')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=4,max=20)])
    password = PasswordField('Password',validators=[InputRequired(),Length(min=8,max=20)])
    remember = BooleanField('Remember me')


# @app.route('', methods=["GET","POST"]) # delete the methods if you do not think that any form will send a request to your app route/webpage
# def insertName():
#     if "adminSession" in session or "userSession" in session:
#         if "adminSession" in session:
#             userSession = session["adminSession"]
#         else:
#             userSession = session["userSession"]
#
#         userFound, accGoodStanding, accType, imagesrcPath = general_page_open_file(userSession)
#
#         if userFound and accGoodStanding:
#             if accType == "Teacher":
#                 teacherUID = userSession
#             else:
#                 teacherUID = ""
#             return render_template('users/general/page.html', accType=accType, imagesrcPath=imagesrcPath, teacherUID=teacherUID)
#         else:
#             print("Admin/User account is not found or is not active/banned.")
#             session.clear()
#             return render_template("users/general/page.html", accType="Guest")
#             # return redirect(url_for("insertName"))
#     else:
#         return render_template("users/general/page.html", accType="Guest")

@app.route('/', methods=['GET'])
def match():
    form = LoginForm



@app.route('/stafflogin', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('stafflogin.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.pop('username',None)
    logout_user()
    return redirect(url_for('/'))


@app.route('/userlogin',methods=['GET','POST'])
def user_login():
    error = None
    customer_dict = {}
    try:
        db = shelve.open('customer.db','r')
        customer_dict = db['Customers']
        db.close()
        customer_list = []
        for key in customer_dict:
            customer = customer_dict.get(key)
            customer_list.append(customer)
        dataUsername = customer.get_username()
        dataPassword = customer.get_password()
        if request.method == 'POST':
            try:
                attemptedUsername = request.form.get("username")
                attemptedPassword = request.form.get("password")
                if dataUsername == attemptedUsername:
                    if dataPassword == attemptedPassword:
                        encoded_jwt = jwt.encode({"username":attemptedUsername, "password":attemptedPassword},secret,algorithm="HS256")
                        # decoded_jwt = jwt.decode(encoded_jwt,secret,algorithms=["HS256"])
                        # session.__setitem__("token",encoded_jwt)
                        session["token"] = encoded_jwt
                        print(session["token"])

                        return redirect(url_for("profile"))
            except:
                print("Error 404")
                return redirect(url_for("user_login"))
    except:
        print("Error 404.")
        return redirect(url_for("user_login"))

    return render_template('userlogin.html', error=error)
        # if request.form['username'] != 'user' or request.form['password'] != 'user':
        #     error = 'Invalid Credentials. Please try again.'

    #     else:
    #         return redirect(url_for('homepage'))
    # return render_template('userlogin.html', error=error)

@app.route('/profile')
def profile():
    if session["token"] != " ":
        print("GOT TOKEN")

    return render_template('profile.html')

@app.route('/dashboard')
def dashboard():
    error = None
    return render_template('dashboard.html',error=error)


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        customer = Customer.Customer(create_customer_form.username.data, create_customer_form.name.data,
                            create_customer_form.gender.data, create_customer_form.membership.data,
                            create_customer_form.remarks.data,
                            create_customer_form.email.data, create_customer_form.date_joined.data,
                            create_customer_form.address.data,create_customer_form.password.data)

        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)


@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    create_admin_form = CreateAdminForm(request.form)
    # create_admin_form.confirm.data = create_admin_form.password.data
    if request.method == 'POST' and create_admin_form.validate():
        admin_dict = {}
        db = shelve.open('admin.db', 'c')

        try:
            admin_dict = db['Admin']
        except:
            print("Error in retrieving Admin from admin.db.")

        count_id = 1
        for key in admin_dict:
            count_id = key+1

        admin = Admin.Admin(create_admin_form.code.data,
                            create_admin_form.gender.data,create_admin_form.email.data
                            ,create_admin_form.remarks.data,create_admin_form.password.data)
        admin.set_admin_id(count_id)
        admin_dict[admin.get_admin_id()] = admin
        db['Admin'] = admin_dict

        db.close()

        return redirect(url_for('retrieve_admin'))
    return render_template('createAdmin.html', form=create_admin_form)

@app.route('/retrieveAdmin')
def retrieve_admin():
    admin_dict = {}
    try:
        db = shelve.open('admin.db', 'r')
        admin_dict = db['Admin']
        db.close()
    except:
        print("No admins in the directory.")
    admin_list = []
    for key in admin_dict:
        admin = admin_dict.get(key)
        admin_list.append(admin)

    return render_template('retrieveAdmin.html', count=len(admin_list), admin_list=admin_list)

@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    try:
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()
    except:
        print("No customers in the directory.")

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


@app.route('/updateAdmin/<int:id>', methods=['GET', 'POST'])
def update_admin(id):
    update_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST' and update_admin_form.validate():
        try:
            admin_dict = {}
            db = shelve.open('admin.db', 'w')
            admin_dict = db['Admin']
            admin = admin_dict.get(id)
            admin.set_code(update_admin_form.code.data)
            admin.set_gender(update_admin_form.gender.data)
            admin.set_email(update_admin_form.email.data)
            admin.set_remarks(update_admin_form.remarks.data)
            admin.set_password(update_admin_form.password.data)

            db['Admin'] = admin_dict
            db.close()

            return redirect(url_for('retrieve_admin'))
        except:
            admin_dict = {}
            db = shelve.open('admin.db', 'r')
            admin_dict = db['Admin']
            db.close()

            admin = admin_dict.get(id)
            update_admin_form.code.data = admin.get_code()
            update_admin_form.gender.data = admin.get_gender()
            update_admin_form.email.data = admin.get_email()
            update_admin_form.remarks.data = admin.get_remarks()
            update_admin_form.password.data = admin.get_password()

            return render_template('updateAdmin.html', form=update_admin_form)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        try:
            customers_dict = {}
            db = shelve.open('customer.db', 'w')
            customers_dict = db['Customers']
            customer = customers_dict.get(id)
            customer.set_first_name(update_customer_form.username.data)
            customer.set_last_name(update_customer_form.name.data)
            customer.set_gender(update_customer_form.gender.data)
            customer.set_membership(update_customer_form.membership.data)
            customer.set_remarks(update_customer_form.remarks.data)
            customer.set_email(update_customer_form.email.data)
            customer.set_date_joined(update_customer_form.date_joined.data)
            customer.set_address(update_customer_form.address.data)
            customer.set_password(update_customer_form.password.data)

            db['Customers'] = customers_dict
            db.close()

            return redirect(url_for('retrieve_customers'))
        except:
            print('Error updating customer into db')
    else:
        customers_dict = {}
        try:
            db = shelve.open('customer.db', 'r')
            customers_dict = db['Customers']
            db.close()

            customer = customers_dict.get(id)
            update_customer_form.username.data = customer.get_first_name()
            update_customer_form.name.data = customer.get_last_name()
            update_customer_form.gender.data = customer.get_gender()
            update_customer_form.membership.data = customer.get_membership()
            update_customer_form.remarks.data = customer.get_remarks()
            update_customer_form.email.data = customer.get_email()
            update_customer_form.address.data = customer.get_address()
            update_customer_form.date_joined.data = customer.get_date_joined()
            update_customer_form.password.data = customer.get_password()

            return render_template('updateCustomer.html', form=update_customer_form)
        except:
            print('Error retrieving customer from db')

    return redirect(url_for('retrieve_customers'))

@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer_dict = {}
    db = shelve.open('customer.db', 'w')
    customer_dict = db['Customers']

    customer_dict.pop(id)

    db['Customers'] = customer_dict
    db.close()

    return redirect(url_for('retrieve_customers'))

@app.route('/deleteAdmin/<int:id>', methods=['POST'])
def delete_admin(id):
    admin_dict = {}
    db = shelve.open('admin.db', 'w')
    admin_dict = db['Admin']

    admin_dict.pop(id)

    db['Admin'] = admin_dict
    db.close()

    return redirect(url_for('retrieve_admin'))


if __name__ == '__main__':
    # db.create_all(app=create_app())
    app.run(debug=True)
    Session(app)
