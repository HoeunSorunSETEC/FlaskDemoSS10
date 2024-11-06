from flask import render_template, redirect, url_for, flash, request, session, current_app
from .forms import RegistrationForm
from .models import User, PasswordReset  # Adjust based on your actual models
from . import db, mail  # Import db and mail from the current package
from flask_mail import Message
import random
import string
from datetime import datetime, timedelta

def generate_verification_code():
    """Generate a random 6-digit verification code."""
    return ''.join(random.choices(string.digits, k=6))

@current_app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email is already registered. Please log in.", "danger")
            return redirect(url_for("login"))

        # Create a new user entry (not yet activated)
        new_user = User(
            email=form.email.data,
            password=form.password.data  # In production, consider hashing the password
        )
        db.session.add(new_user)
        db.session.commit()

        # Generate verification code and save it with an expiry time
        code = generate_verification_code()
        expiry = datetime.utcnow() + timedelta(minutes=3)  # Code expires in 3 minutes
        new_user.verification_code = code
        new_user.code_expiry = expiry
        db.session.commit()

        # Send verification email
        msg = Message("Your Verification Code", recipients=[form.email.data])
        msg.body = f"Your verification code is {code}. This code will expire in 3 minutes."
        mail.send(msg)

        flash("A verification code has been sent to your email. Please enter it to complete registration.", "info")
        # Store user id in session for verifying later
        session['user_id'] = new_user.id
        return redirect(url_for("verify"))

    return render_template("register.html", form=form)

@current_app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        user_id = session.get("user_id")
        if not user_id:
            flash("Session expired. Please register again.", "danger")
            return redirect(url_for("register"))

        code = request.form.get("code")
        user = User.query.get(user_id)

        if user and user.verification_code == code and user.code_expiry > datetime.utcnow():
            # Verification successful, activate user
            user.is_verified = True
            user.verification_code = None  # Clear the code
            user.code_expiry = None
            db.session.commit()
            flash("Your account has been successfully verified. Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash("Invalid or expired code. Please try again.", "danger")

    return render_template("verify.html")
