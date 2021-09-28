from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BlogField
from wtforms.validators import Required,Email
from ..models import User
from wtforms import ValidationError
class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField(' input your Username',validators = [Required()])
    password = PasswordField('Password',validators = [Required()])
    Blog = BlogField  ('blog',validators =[Required()]) 
    def validate_email(self,data_field):
        if User.query.filter_by(email =data_field.data).first():
            raise ValidationError('There  exists an account with that email')
    def validate_username(self,data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That Username is already exists')
class Loginblog(FlaskForm):
    username = StringField('Your username',validators=[Required()])
    password = PasswordField('Password',validators =[Required()])
    

