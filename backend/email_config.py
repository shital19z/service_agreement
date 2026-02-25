import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_reset_email(to_email: str, token: str):
    # --- Configuration ---
    smtp_server = "smtp.gmail.com"
    port = 587 
    login = "gunadhya.ai@gmail.com"
   
    password = "zdsn pelr qywo uexl" 
    sender_email = "gunadhya.ai@gmail.com"
    receiver_email = to_email

    # The actual link for the user
    reset_link = f"http://localhost:5173/reset-password?token={token}"

    # Create the root message and set the headers
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = f"Support Team <{sender_email}>"
    message["To"] = receiver_email

    # Plain-text version
    text = f"Hi there, click the link to reset your password: {reset_link}"

    # HTML version
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h3>Password Reset Request</h3>
        <p>Hi there,</p>
        <p>We received a request to reset your password. Please click the button below to proceed:</p>
        <p>
            <a href="{reset_link}" 
               style="background-color: #4facfe; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">
               Reset Password
            </a>
        </p>
        <p style="font-size: 12px; color: #666;">If you did not request this, please ignore this email.</p>
        <br>
        <p>Thank you,<br>The Team</p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(login, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully to {to_email}!")
    except Exception as e:
        print(f"Error sending email: {e}")