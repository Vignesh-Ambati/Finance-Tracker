from flask import current_app
from flask_mail import Message
from app.extensions import mail

class EmailService:
    @staticmethod
    def send_email(to, subject, body, html=None):
        try:
            # Skip gracefully if mail server credentials are not configured
            mail_server = current_app.config.get('MAIL_SERVER')
            mail_user = current_app.config.get('MAIL_USERNAME')
            if not mail_server or not mail_user:
                print(f"[EmailService] Mail server/username not configured in .env. Skipped sending email to {to}.")
                return False

            msg = Message(
                subject=subject,
                recipients=[to],
                body=body,
                html=html,
                sender=current_app.config.get('MAIL_DEFAULT_SENDER')
            )
            mail.send(msg)
            return True
        except Exception as e:
            print(f"[EmailService] Error sending email to {to}: {e}")
            return False

    @staticmethod
    def send_password_reset(user, token, frontend_url):
        clean_url = frontend_url.rstrip('/')
        reset_url = f"{clean_url}/reset-password/{token}"
        subject = "Password Reset - Finance Tracker"
        body = f"Hello {user.username},\n\nPlease use this link to reset your password:\n{reset_url}\n\nIf you did not request this, please ignore this email."
        html = f"<p>Hello {user.username},</p><p>Please use this link to reset your password:</p><p><a href='{reset_url}'>{reset_url}</a></p>"
        return EmailService.send_email(user.email, subject, body, html)

    @staticmethod
    def send_monthly_reminder(user, loans_summary):
        subject = "Monthly Interest Reminder - Finance Tracker"
        body = f"Hello {user.username},\n\nHere is your monthly interest reminder:\n\n{loans_summary}"
        return EmailService.send_email(user.email, subject, body)
