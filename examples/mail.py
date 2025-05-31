import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Your Gmail credentials
sender_email = "coder0214h@gmail.com"
app_password = "plntlhhlylazxsih"  # From Google App Password

# Send email to yourself
receiver_email = sender_email  # 👈 Sending to yourself

# Create the message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test Email to Myself"

# Body of the email
body = "Hello! This is a test email sent to myself using Gmail's SMTP server."
message.attach(MIMEText(body, "plain"))

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  #
    server.login(sender_email, app_password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("✅ Email sent to yourself successfully!")
    server.quit()
except Exception as e:
    print("❌ Error:", e)