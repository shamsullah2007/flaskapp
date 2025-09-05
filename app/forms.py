from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,DateTimeField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from datetime import datetime
from flask_login import current_user
from app.models import User,Post



class Regform(FlaskForm):
    
    user_name=StringField("username",validators=[DataRequired(),Length(min=6 , max=20)])
    email=StringField("email",validators=[DataRequired(),Email()])
    password=PasswordField("password",validators=[DataRequired(),Length(min=6 , max=20)])
    confirm_password=PasswordField("confirm_password", validators=[DataRequired(),Length(min=6,max=20),EqualTo('password')])
    submit=SubmitField("sign up")

    def validate_user_name(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("this username is allready exist")
        

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("this email is allready exist")
        



class Logform(FlaskForm):
    user_name=StringField("username",validators=[DataRequired()])
    email=StringField("email",validators=[DataRequired(),Email()])
    password=PasswordField("username",validators=[DataRequired(),Length(min=6 , max=20)])
    # confirm_password=PasswordField("confirm_password", validators=[DataRequired(),Length(min=6,max=10),EqualTo])
    remember=BooleanField("remember me")
    submit=SubmitField("login")


class PostForm(FlaskForm):
    title=StringField("title",validators=[DataRequired(),Length(min=4)])
    content=TextAreaField("content",validators=[DataRequired()])
    publish=SubmitField("publish")

class UpdateAccount(FlaskForm):
    username=StringField("username",validators=[DataRequired()])
    email=StringField('email',validators=[Email()])
    picture=FileField("upload a porfile pic" , validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField('Update')
    

    def validate_username(self,username):
        if username.data !=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('this username already take try differnt one')
  
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is already registered. Please choose another one.")

