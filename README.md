# AntiTheft

An advanced AntiTheft system designed to protect your laptop, deter unauthorized access, and assist in recovering your lost device quickly.

## Overview

**AntiTheft** captures crucial evidence like images, audio, and video of anyone attempting unauthorized access to your system by entering a wrong password. It also sends location details and alerts to your email, ensuring you remain informed about any intrusion attempts.

## Features

- **Capture Evidence**: Automatically records the intruder's image, audio, and video upon a wrong password attempt.
- **Location Tracking**: Retrieves and sends the system's location using hardware-level GPS (if available).
- **Alert Notifications**: Sends email alerts containing captured media and location information.
- **Automated Execution**: Script activates when the system locks and stops when it unlocks.
- **Error Handling**: Includes robust mechanisms to handle runtime issues and ensure reliable operation.

## Requirements

- **Python 3.11+**
- **Gmail App Password** for sending email notifications.
- **Additional Libraries**: Install dependencies listed in `requirements.txt`.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/Shivam-Shane/AntiTheft.git
    cd AntiTheft
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Settings**
   - Edit the `Config.yaml` file to include your email credentials and other configurations as required.

$Config.yaml file preview$

 ***Set up the IMAP connection***
- IMAP_SERVER: imap.gmail.com
- IMAP_PORT: 993
- SMTP_SERVER: smtp.gmail.com
- SMTP_PORT: 587

***Set up your email credentials***
- SMTP_USERNAME: yourgmail@gmail.com
- SMTP_PASSWORD: Gmail_App_Password

***Name of the Email Sender***
- SENDER_NAME: YourName
- recipient_email: yourgmail@gmail.com

4. **Run the Script**
    ```bash
    python AntiTheft.py
    ```

5. **Automate with Task Scheduler (Windows)**
   - Schedule the script to run automatically when your system locks using the Windows Task Scheduler.

## Usage

1. Ensure the script is configured and running in the background or set up as a scheduled task.
2. On a wrong password attempt:
   - The system captures the intruder's image, audio, and video.
   - An alert email is sent to your registered email with the collected evidence and the system's location.

## Logs

All events and errors are logged for monitoring and troubleshooting. Logs are stored in the `logs/` directory.

## Future Enhancements

- **Customizable UI**: Enable users to personalize alert preferences and other settings through a graphical interface.
- **More functionality** To prevents further access to system if wrong password is provided, continue mail attempts if failed. 
- **Enhanced Error Handling**: Improve messaging and response times for better user experience.

## Contribution

Contributions are welcome! Fork this repository, submit pull requests, or report issues. Help improve functionality and make the system more robust.

## License

This project is licensed under the Apache License. See the LICENSE file for details.

## Contact

For questions, suggestions, or support, reach out at **sk0551460@gmail.com**.

## Support the Project

Help support continued development and improvements:

- **Follow on LinkedIn**: Stay connected for updates – [LinkedIn Profile](https://www.linkedin.com/in/shivam-2641081a0/)
- **Buy Me a Coffee**: Appreciate the project? [Buy Me a Coffee](https://buymeacoffee.com/shivamshane)
