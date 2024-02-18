
## Authentication Microservice Documentation

## Overview

The Authentication Microservice provides functionalities for user registration, login, and management. It utilizes Flask, SQLAlchemy, Twilio for SMS OTP, and SMTP for email OTP verification.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your_username/your_repository.git
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up Twilio account and obtain credentials.
4. Set up SMTP email service and configure credentials.

## Usage

### 1. Registration

- Endpoint: `/register`
- Method: `POST`
- Parameters:
  - `first_name`: First name of the user.
  - `last_name`: Last name of the user.
  - `email`: Email address of the user.
  - `phone_number`: Phone number of the user.
  - `password`: Password for the user account.
- Description: Registers a new user by sending email OTP verification.

### 2. Email Verification

- Endpoint: `/verify_email`
- Method: `POST`
- Parameters:
  - `otp`: One-time password sent to the user's email.
- Description: Verifies the email OTP to complete the user registration.

### 3. Login

- Endpoint: `/login`
- Method: `POST`
- Parameters:
  - `phone_number`: Phone number of the user.
- Description: Sends an SMS OTP to the user's phone for authentication.

### 4. OTP Verification

- Endpoint: `/otp_verification`
- Method: `POST`
- Parameters:
  - `otp`: One-time password sent to the user's phone.
- Description: Verifies the SMS OTP to authenticate the user.

### 5. Profile Update

- Endpoint: `/update`
- Method: `POST`
- Parameters:
  - `email`: Email address of the user.
  - `password`: Password for the user account.
- Description: Updates the user's profile details.

### 6. Profile Details Update

- Endpoint: `/update_details`
- Method: `POST`
- Parameters:
  - `first_name`: First name of the user.
  - `last_name`: Last name of the user.
  - `phone_number`: Phone number of the user.
  - `password`: Password for the user account.
- Description: Updates the user's profile details.

## Dependencies

- Flask
- SQLAlchemy
- Twilio
- SMTP

## Security Considerations

- Use HTTPS for secure communication.
- Implement proper input validation to prevent injection attacks.
- Protect sensitive data, such as passwords, with encryption.
- Use strong and unique OTPs for verification.

## Author

Your Name (Your Email)

---

Feel free to customize this documentation to include additional details or sections as needed.
