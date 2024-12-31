import win32evtlog
import win32evtlogutil

from datetime import datetime, timedelta
from evidance_capturing import capture_evidence
from mail_sender import MailSender
from files_cleanup import delete_old_files
from logger import logging


def monitor_failed_logins():
    """
    Continues Monitor the failed logins attempt on system using windows event viewer logs,
    Args: None
    Returns: None
    """

    server = 'localhost'
    log_type = 'Security'
    mail_sender = MailSender()
    # Open the event log
    handle = win32evtlog.OpenEventLog(server, log_type)
    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    try:
        if not handle:
            logging.error("Failed to open Event Log. Handle is invalid.")
            return
        while True:
            try:
                events = win32evtlog.ReadEventLog(handle, flags, 0)
                if events:
                    for event in events:
                        current_time = datetime.now()

                        if event.EventID == 4625:  # Event ID for failed login
                            event_time = event.TimeGenerated
                            if current_time - event_time <= timedelta(seconds=10):  # Only process recent events
                                event_time.strftime('%Y-%m-%d %H:%M:%S')

                                # Log the failed login
                                win32evtlogutil.SafeFormatMessage(event, log_type)
                                logging.info(f"Failed login detected")

                                # Trigger evidence capture and cleanup
                                capture_evidence()
                                mail_sender.send_mail(event_time.strftime('%Y-%m-%d %H:%M:%S'))
                                delete_old_files('captures')  # Delete old files after sending an email

                        elif event.EventID == 4624:  # Event ID for successful login
                            event_time = event.TimeGenerated
                            description = event.StringInserts  # Event details
                            logon_type = description[8]  # Logon type
                            # logon type determine the type of logon happening on system like on keyboard, remote, internet and other
                            if current_time - event_time <= timedelta(seconds=15) and logon_type == '7':
                                logging.info("System Logon Detected, Exiting Anti Theft")
                                return

            except KeyboardInterrupt:
                logging.warning("Monitoring stopped by user.")
                break
            except Exception as e:
                pass
    finally:
            win32evtlog.CloseEventLog(handle)
            
if __name__ == '__main__':
    logging.info(f"Monitoring Laptop Anti Theft Starts... at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    monitor_failed_logins()