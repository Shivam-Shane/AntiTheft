import socket
import ssl
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from logger import logging
from utility import read_yaml
from files_selectory import get_most_recent_files
from mail_body_creation import mail_body

class MailSender():
    """
        MailSender class provides methods to send messages to a specific email address
        using SMTP protocol.
        Attributes:
        config (dict): A dictionary containing SMTP server details and email credentials.
        SENDER_NAME_VALUE (str): The name of the sender.
        SENDER_EMAIL (str): The email address of the sender.
        server_connection (smtplib.SMTP): The SMTP connection object.

    """
    def __init__(self):
        self.config = read_yaml("config.yaml")
        self.SENDER_EMAIL = self.config.get('SMTP_USERNAME')
        self.server_connection = None
        self.connect_to_smtp_server()

    def connect_to_smtp_server(self):
        try:
            logging.debug(f"Connecting to SMTP server {self.config.get('SMTP_SERVER')}")
            self.server_connection = smtplib.SMTP(self.config["SMTP_SERVER"], self.config["SMTP_PORT"])
            self.server_connection.starttls()
            self.server_connection.login(self.config["SMTP_USERNAME"], self.config["SMTP_PASSWORD"])
            logging.info("Successfully authenticated to SMTP server")
        except (socket.gaierror, socket.timeout) as net_err:
            logging.error(f"Network issue while connecting to SMTP server: {str(net_err)}")
            raise RuntimeError("Network issue while connecting to SMTP server: " + str(net_err))
        except ssl.SSLError as ssl_err:
            logging.error(f"SSL error while connecting to SMTP server: {str(ssl_err)}")
            raise RuntimeError("SSL error while connecting to SMTP server: " + str(ssl_err))
        except smtplib.SMTPException as smtp_err:
            logging.error(f"SMTP error: {str(smtp_err)}")
            raise RuntimeError("SMTP error: " + str(smtp_err))

    def send_mail(self,capture_time):
        """
        Send an email with the specified capture time/location and other details and recent files.
        Args: Capture time: The time when the events was recorded
        Returns: None 
        """
        # Get the most recent files (image, audio, video)
        directory="captures"
        extensions = ['.jpg', '.avi', '.wav']  # Add more extensions if needed
        recent_files = get_most_recent_files(directory, extensions)
        recipient_email = self.config.get('recipient_email')  # Replace with recipient's email address
        subject = '⚠️ Failed Login Attempt Detected on Your System'
        body = mail_body(capture_time)

        try:
            # Set up the MIME message
            msg = MIMEMultipart()
            msg['From'] = self.SENDER_EMAIL
            msg['To'] = recipient_email
            msg['Subject'] = subject
            
            # Add body to email
            msg.attach(MIMEText(body, 'html'))

            # Attach the most recent files
            for ext, file_path in recent_files.items():
                if os.path.exists(file_path):
                    part = MIMEBase('application', 'octet-stream')
                    with open(file_path, 'rb') as f:
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                    msg.attach(part)
                else:
                    logging.warning(f"File not found: {file_path}")
                    return 

            # Send the email
            self.server_connection.sendmail(self.SENDER_EMAIL, recipient_email, msg.as_string())
            logging.info(f"Email sent successfully to {recipient_email}")

        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")