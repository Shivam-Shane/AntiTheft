import re
from location import location_details
from logger import logging
import socket

def mail_body(capture_time):
    """
    Function  to create a mail body with html encoding for better view rendering
    Args: Capture_time
    Returns: body  Mail body to be mailed with all the details
    """
    system_name = socket.gethostname()
    location = location_details()
    # Generate Google Maps link (assuming location contains lat and lon keys)
    # Extract latitude and longitude using regex
    match_lat = re.search(r"Latitude:\s*([\d.]+)", location)
    match_lon = re.search(r"Longitude:\s*([\d.]+)", location)
    maps_link = f"https://www.google.com/maps/place/{match_lat.group(1)},{match_lon.group(1)}" 
    logging.debug(maps_link)
    body=f"""
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
            </head>
            <body style="font-family: Arial, sans-serif; background-color: #2d2828; color: #333; margin: 0; padding: 0;">
                <div style="background-color: #1f1212; margin: 20px auto; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); max-width: 600px;">
                    <div style="text-align: center; padding: 10px 0;">
                        <h2 style="color: #d9534f;">⚠️ Security Alert: Failed Login Attempt Detected</h2>
                    </div>
                    <p style="font-family: Arial, sans-serif;  color: #f1ecec;">Dear User,</p>
                    <p style="font-family: Arial, sans-serif;  color: #f1ecec;">Anti Theft detected a failed login attempt on your {system_name}. Please review the attached evidence and take necessary precautions.</p>
                    <p style="font-family: Arial, sans-serif;  color: #f1ecec;"><strong>Capture Time:</strong> {capture_time}</p>
                    <p style="font-family: Arial, sans-serif;  color: #f1ecec;"><strong>Location Details:</strong></p>
                    <pre style="background: #045819; padding: 10px; color: #f1ecec; border: 1px solid #ddd; border-radius: 5px;">{location}</pre>
                    <a href="{maps_link}" 
                    style="display: inline-block; background-color: #007bff; color: #ffffff; padding: 10px 20px; border-radius: 5px; text-decoration: none; margin: 20px 0; font-size: 16px;" 
                    target="_blank">View Location in Google Maps</a>
                    <p style="font-family: Arial, sans-serif;  color: #f1ecec;">If your device is online, you can track its current location using the link below</p>
                    <a href="https://support.microsoft.com/en-us/account-billing/find-and-lock-a-lost-windows-device-890bf25e-b8ba-d3fe-8253-e98a12f26316" target="_blank">Link</a>
                    <p style="color: red;"><em>Note: If you did not initiate this attempt, please consider securing your system immediately.</em></p>
                    <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #888;">
                        <p>This email was sent by the AntiTheft system. You can turn off these emails inside the app.</p>
                        <p>This is an automated email. Please do not reply.</p>
                    </div>
                </div>
            </body>
        </html>

    """
    return body