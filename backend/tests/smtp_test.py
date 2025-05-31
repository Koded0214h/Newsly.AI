import smtplib
from email.mime.text import MIMEText

def send_test_email():
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    sender_email = "coder0214h@gmail.com"
    app_password = "onuopumpcgbwolbo"
    receiver_email = "coder0214h@gmail.com"

    message = MIMEText("This is a test email from SMTP test script.")
    message["Subject"] = "SMTP Test Email"
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Failed to send test email: {e}")

if __name__ == "__main__":
    send_test_email()
