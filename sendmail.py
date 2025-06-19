import boto3
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# CONFIG
SENDER = "poornakallam414@gmail.com.com"
RECIPIENTS = ["poornakallam414@gmail.com"]
AWS_REGION = "us-east-1"
SUBJECT = "Automated Report"
BODY_TEXT = "Please find the attached results."

# Create SES client
client = boto3.client('ses', region_name=AWS_REGION)

# Build email with attachment
msg = MIMEMultipart()
msg['Subject'] = SUBJECT
msg['From'] = SENDER
msg['To'] = ", ".join(RECIPIENTS)

# Add body
msg.attach(MIMEText(BODY_TEXT, 'plain'))

# Attach the ZIP file
with open("results.zip", "rb") as file:
    part = MIMEBase('application', 'zip')
    part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="results.zip"')
    msg.attach(part)

# Send
response = client.send_raw_email(
    Source=SENDER,
    Destinations=RECIPIENTS,
    RawMessage={'Data': msg.as_string()}
)

print("Email sent! Message ID:", response['MessageId'])
