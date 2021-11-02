from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField,IntegerField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField('Remember Me')
    submit = SubmitField('Login')





class RegistrationForm(FlaskForm):
	first_name = StringField('First Name', 
					validators=[DataRequired(), Length(min =2, max=30)])
	last_name = StringField('Last Name', 
					validators=[DataRequired(), Length(min =2, max=30)])
	email = StringField('Email', 
				validators=[DataRequired(), Email()])
	# contact = IntegerField('Contact No.', 
	# 			validators=[DataRequired(), Length(min =5, max=30)])
	password = PasswordField('Password',
				 validators = [DataRequired(), Length(min=8, max=20)])
	confirm_password = PasswordField('Confirm Password',
								validators = [DataRequired(),EqualTo('password')])

	submit = SubmitField('Sign Up')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user:
			raise ValidationError('That email is taken')




class UpdateProfileForm(FlaskForm):
	first_name = StringField('First Name', 
					validators=[DataRequired(), Length(min =2, max=30)])
	last_name = StringField('Last Name', 
					validators=[DataRequired(), Length(min =2, max=30)])
	email = StringField('Email', 
				validators=[DataRequired(), Email()])
	# contact = IntegerField('Contact No.', 
	# 			validators=[DataRequired(), Length(min =5, max=30)])
	
	submit = SubmitField('Update Profile')

	def validate_email(self, email):
		if email.data!= current_user.email:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('That email is taken')



class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('New Post')