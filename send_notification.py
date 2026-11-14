import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart




EMAIL_USER = "m.baldauf04@gmail.com"
EMAIL_PASSWORD = "dksn utdl lwmq bvai "

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SOIL_MOISTURE_THRESHOLD = 30 


# Carrier SMS gateways
SMS_GATEWAYS = {
    "t-mobile": "tmomail.net",
    "tmobile": "tmomail.net",
    "verizon": "vtext.com",
    "att": "txt.att.net",
}


def send_email(recipient_email, subject, body):
    """
    Send a normal email.
    """

    try:
        msg = MIMEMultipart()

        msg["From"] = EMAIL_USER
        msg["To"] = recipient_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(
                EMAIL_USER,
                recipient_email,
                msg.as_string()
            )

        print(f"Email sent to {recipient_email}")
        return True

    except Exception as e:
        print(f"Email failed: {e}")
        return False



def send_sms(phone_number, carrier, message):
    """
    Send SMS using carrier email gateway.
    """

    # Remove formatting
    clean_number = (
        phone_number
        .replace("+", "")
        .replace("-", "")
        .replace(" ", "")
    )

    carrier = carrier.lower().strip()

    if carrier not in SMS_GATEWAYS:
        print(f"Unknown carrier: {carrier}")
        return False

    sms_email = f"{clean_number}@{SMS_GATEWAYS[carrier]}"

    return send_email(
        sms_email,
        "",
        message
    )



def send_soil_alert(soil_moisture):

    if soil_moisture < SOIL_MOISTURE_THRESHOLD:

        message = (
            "ALERT!\n\n"
            f"Soil moisture is low.\n"
            f"Current reading: {soil_value}\n"
            "Please water the plant."
        )

