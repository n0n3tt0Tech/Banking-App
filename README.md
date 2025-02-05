

# Django Banking App

## Overview

Welcome to **Banking App**, a Django-based web application with various user functionalities. The app allows users to register, log in, manage a personal balance, perform transactions, and make bill payments securely. Admin users can manage users and monitor activities.

## Features

### User Features:
- **Registration & Login**: Users can register and log in to their accounts.
- **User Dashboard**: Displays the user's balance and recent transactions.
- **Money Transfer**: Allows users to transfer money to different banks.
- **Bill Payments**: Users can pay their bills securely using their balance.
- **Transaction History**: Users can view their past transactions.

### Admin Features:
- **Admin Dashboard**: Admins can monitor user activity and balance.
- **User Management**: Admins can delete user accounts.
- **Security**: Features include session management, login attempts protection, and more.

## Installation & Setup

### Requirements:
- Python 3.8+
- Django 5.1+
- PostgreSQL or SQLite database
- Allauth for authentication

### Installation Steps:

1. Clone the repository:
    ```bash
    https://github.com/n0n3tt0Tech/Banking-App.git
    cd Banking-App
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the database:
    - Create a database in PostgreSQL or use SQLite for development.
    - Modify the `DATABASES` setting in `settings.py` if necessary.

4. Run migrations:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser (for admin access):
    ```bash
    python manage.py createsuperuser (set username and password. Don't add email)
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

7. Visit the app at `http://127.0.0.1:8000/`.

## Usage

### User Registration

- Navigate to the **register** page to sign up. Once registered, you will be automatically logged in and redirected to your user dashboard.

### Money Transfer

- Use the **transfer_money** page to transfer funds to an external bank. Input the bank name, account number, and amount.

### Bill Payment

- On the **pay_bills** page, select the bill type and enter the amount to pay.

### Admin Features

- Admin users can access the **admin_dashboard** to view and manage user data.
- Admins can delete users through the **delete_user** functionality.

## Security Features

- **Password Validation**: Enforces strong password policies to prevent weak passwords and improve security.
- **CSRF Protection**: Protects against CSRF attacks by ensuring requests are from trusted sources.
- **Content Security Policy (CSP)**: CSP headers are implemented to prevent XSS attacks by restricting content sources.
- **Session Rotation**: Sessions are automatically rotated every 2 minutes to prevent session fixation.
- **Session Security**: Ensures cookies are secure, HTTPOnly, and have SameSite attribute for added protection.
- **Account Lockout**: Accounts are locked after multiple failed login attempts, preventing brute-force attacks.
- **SQL Injection Prevention**: Uses Django ORM to safely handle user input, preventing SQL injection.
- **HTTPS and SSL Encryption**: Ensures all data transmitted between client and server is encrypted.
- **Admin Access Control**: Restricts access to admin pages to authorized users only.
- **User Role Management**: Assigns user roles and restricts access to sensitive features based on roles.
- **XSS Prevention**: Automatically escapes output in templates to prevent Cross-Site Scripting (XSS) attacks.
- **X-Frame-Options Header**: Prevents the app from being embedded in iframes to mitigate clickjacking.
- **Referrer Policy**: Restricts the sending of referrer data to prevent leakage of sensitive information.
- **Logging and Monitoring**: Logs key security events to help monitor and detect potential threats.
- **Role-based Access Control (RBAC)**: Restricts access to resources based on the user's role.

## Files Overview

- **views.py**: Contains view functions for handling user registration, login, transactions, money transfer, bill payment, and admin actions.
- **models.py**: Defines the `Profile` and `Transaction` models for storing user data and transactions.
- **forms.py**: Contains the `RegistrationForm` for user signup.
- **settings.py**: Configures project settings, including database, security, and third-party apps like Allauth.
- **middleware.py**: Implements custom middleware for CSP headers and session auto-rotation.

## URL Structure

Here’s a list of key URLs in the application:

- `/` - Home page
- `/register/` - User registration page
- `/login/` - Login page
- `/user_dashboard/` - User dashboard
- `/transactions/` - View transaction history
- `/transfer/` - Transfer money to an external bank
- `/pay_bills/` - Pay bills from your balance
- `/admin_dashboard/` - Admin dashboard (admin users only)
- `/delete_user/<username>/` - Delete user (admin only)

## Troubleshooting

### Common Issues:

- **404 Error on Dashboard**: Ensure you’re logged in before accessing the dashboard.
- **Session Expiry**: If your session expires, log in again and continue your work.

### Debugging Tips:

- Check logs in `django.log` for detailed error information.
- Use `python manage.py shell` to test individual queries and database access.

## Contributing

Feel free to fork the repository and submit pull requests for bug fixes or new features. Please ensure you write tests for any new functionality.

## License

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


---

