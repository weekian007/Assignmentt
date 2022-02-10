from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators, PasswordField
from wtforms.fields import EmailField, DateField


class CreateCustomerForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=150), validators.DataRequired()])
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    date_joined = DateField('Date Joined', format='%Y-%m-%d')
    address = TextAreaField('Mailing Address', [validators.length(max=200), validators.DataRequired()])
    membership = RadioField('Membership', choices=[('B', 'Basic'), ('S', 'Standard'), ('P', 'Premium')], default='F')
    remarks = TextAreaField('Remarks', [validators.Optional()])
    password = PasswordField(
        'Password', [validators.DataRequired(),
                     validators.Length(min=8),
                     validators.EqualTo('confirm',message='Password doesn´t match')])
    confirm = PasswordField('Confirm password')


class CreateAdminForm(Form):
    code = StringField('Username', [validators.Length(min=4, max=15), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()],choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    remarks = TextAreaField('Remarks', [validators.Optional()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    password = PasswordField(
        'Password', [validators.DataRequired(),
                     validators.Length(min=8),
                     validators.EqualTo('confirm',message='Password doesn´t match')])
    confirm = PasswordField('Repeat the password')
