from django.conf import settings
me=settings.EMAIL_HOST_USER
my_pass=settings.EMAIL_HOST_PASSWORD
# import the necessary components first
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail_otp(user_email,username,otp):
    message = MIMEMultipart("alternatives")
    message["Subject"] = "Verify Your Email"
    message["From"] = "Shop MS"
    message["To"] = user_email
    # write the text/plain part
    # write the HTML part
    html = f"""
    <html>
    <body>
        <h3>Hi {username},</h3>
        <p>Please use the OTP below to verify your email:</p>
        <p><strong style="font-size: 26px; color: #2e6edb;">[ {otp} ]</strong></p>
        <p>This OTP is valid for 15 minutes.</p>
        <h3>Thanks,<br>BackEnd Team</h3>
    </body>
    </html>
    """
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    part2 = MIMEText(html, "html")
    message.attach(part2)
    s=smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(me, my_pass)
    s.sendmail(
        me, user_email, message.as_string()
    )
    s.quit
