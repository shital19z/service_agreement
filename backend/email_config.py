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
        print(f"✅ Password reset email sent successfully to {to_email}!")
    except Exception as e:
        print(f"❌ Error sending password reset email: {e}")


def send_share_email(to_email: str, share_link: str, client_name: str):
    """Send email with shared agreement link"""
    # --- Configuration ---
    smtp_server = "smtp.gmail.com"
    port = 587 
    login = "gunadhya.ai@gmail.com"
    password = "zdsn pelr qywo uexl" 
    sender_email = "gunadhya.ai@gmail.com"
    receiver_email = to_email

    # Create the root message and set the headers
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Agreement Shared: {client_name}"
    message["From"] = f"Agreement Portal <{sender_email}>"
    message["To"] = receiver_email

    # Plain-text version
    text = f"""
Hi there,


Click the link below to view the agreement:
{share_link}

This link will expire in 7 days.

Thank you,
Agreement Portal Team
    """

    # HTML version
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 10px;">
          <h2 style="color: #4facfe;">Agreement Shared</h2>
          <p>Hi there,</p>

          <p>Click the button below to view the agreement:</p>
          <p style="text-align: center;">
            <a href="{share_link}" 
               style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                      color: white; 
                      padding: 12px 24px; 
                      text-decoration: none; 
                      border-radius: 8px; 
                      display: inline-block;
                      font-weight: 600;">
               View Agreement
            </a>
          </p>
          <p style="font-size: 12px; color: #666;">This link will expire in 7 days.</p>
          <p style="font-size: 12px; color: #666;">If you did not expect this email, you can safely ignore it.</p>
          <br>
          <p>Thank you,<br>Agreement Portal Team</p>
        </div>
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
        print(f"✅ Share email sent successfully to {to_email}!")
        return True
    except Exception as e:
        print(f"❌ Error sending share email: {e}")
        return False