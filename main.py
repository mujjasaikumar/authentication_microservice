from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import random
from twilio.rest import Client
import twilio_keys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

my_email = "sample@gmail.com" # email through you have to send otp
my_password = 'app_password' 


# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()


# send otp to mobile number
def verify_mobile_otp(phone_number):
    client = Client(twilio_keys.account_sid, twilio_keys.auth_token)
    otp = ''.join(random.choices('0123456789', k=6))
    message = client.messages.create(
        body=f"Use this OTP to login: {otp}",
        from_=twilio_keys.twilio_number,
        to='+91'+phone_number
    )
    return otp


def verify_email_otp(email):
    otp = ''.join(random.choices('0123456789', k=6))
    # Set up the message
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = f"{email}"
    msg['Subject'] = "Email Verification"
    body = f"use this OTP to verify email: {otp}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # SMTP - Simple Mail Transfer Protocol
        connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email, to_addrs=f"{email}", msg=msg.as_string())
        connection.close()
        return otp
    except Exception as e:
        print(f"An error occurred: {e}")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get registration data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']

        # Generate email verification token
        otp = verify_email_otp(email)

        # Save user details and verification token to session
        session['registration_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'password': password,
        }
        session['otp_details'] = otp

        # Redirect to email verification page
        return redirect('/verify_email')
    return render_template('register.html')


@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        # Get verification token from the URL
        entered_otp = request.form.get('otp')

        # Get registration data from session
        registration_data = session.get('registration_data')

        # Check if verification token matches the one sent
        if session.get('otp_details') == entered_otp:
            # Save user details to the database
            new_user = User(**registration_data)
            db.session.add(new_user)
            db.session.commit()
            session.pop('registration_data')  # Clear registration data from session
            return jsonify({'message': 'User registered successfully'})
        else:
            return jsonify({'error': 'Invalid or expired verification token'})

    return render_template('verify_email.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone_number = request.form['phone_number']
        # Check if the phone number provided is not empty
        if phone_number:
            # Check if the phone number exists in the database
            user = User.query.filter_by(phone_number=phone_number).first()
            if user:
                # Generate OTP and store it in the session
                otp = verify_mobile_otp(phone_number)
                session['phone_number'] = phone_number
                session['otp'] = otp
                return redirect(url_for('otp_verification'))
            else:
                return jsonify({'error': 'Phone number does not exist'})
        else:
            return jsonify({'error': 'Phone number is required'})
    return render_template('login.html')


@app.route('/verify_mobile', methods=['GET', 'POST'])
def verify_mobile():
    if request.method == 'POST':
        entered_otp = request.form['otp']
        # Retrieve phone number and OTP from the session
        phone_number = session.get('phone_number')
        otp = session.get('otp')
        user = User.query.filter_by(phone_number=phone_number).first()
        if user and entered_otp == otp:
            # OTP verification successful
            return jsonify({'message': f'Logged in as {user.first_name} {user.last_name}'})
        else:
            return jsonify({'error': 'Incorrect OTP. Please try again'})
    return render_template('verify_mobile.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                session['email'] = email
                return redirect(url_for('update_details'))
            else:
                return jsonify({'error': 'Password incorrect'})
        else:
            return jsonify({'error': 'Email does not exist'})
    return render_template('update.html')


@app.route('/update_details', methods=['GET', 'POST'])
def update_details():
    if request.method == 'POST':
        email = session.get('email')
        # Retrieve the updated details
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            # Update the user's information
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.password = password
            db.session.commit()
            return jsonify({'message': 'User details updated successfully'})
        else:
            return jsonify({'error': 'User not found'})

    # Render the form template for GET requests
    return render_template('update_details.html')


if __name__ == '__main__':
    app.run(debug=True)
