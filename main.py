#Change machine monitoring program 
#Mark Brotcke
#v1.5.5

import network
import time
import machine
import umail
from machine import Pin
from utime import sleep, localtime, time  # Import necessary functions from `utime`

# Pin assignments
LARGE_MACHINE_PIN = Pin(4, Pin.IN, Pin.PULL_UP)
SMALL_MACHINE_PIN = Pin(6, Pin.IN, Pin.PULL_UP)

# Wi-Fi Credentials
SSID = 'ssid here'
PASSWORD = 'wifi password here'

# Email settings
SMTP_SERVER = "smtp server here"
SMTP_PORT = 465  # Change to port 465 for SSL
SENDER_EMAIL = "email here"
SENDER_PASSWORD = "email password here"  # Use an app-specific password for Gmail
RECEIVER_EMAIL = "email here"

# Subject line for emails
SUBJECT_LARGE_MACHINE = "#1 Change Machine Down"
SUBJECT_SMALL_MACHINE = "#2 Change Machine Down"

# Email body template
BODY_TEMPLATE = """
Hello,

{machine_name} change machine is down.

Please check the machine and take any necessary actions.

Regards,
Raspberry Pi Monitor
"""

# Global variables to keep track of email sending limits for each pin
LAST_EMAIL_TIME_LARGE = None
LAST_EMAIL_TIME_SMALL = None
EMAIL_INTERVAL = 3600  # 1 hour in seconds

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        sleep(1)

    print(f"Connected to Wi-Fi: {wlan.ifconfig()}")

def send_initialization_email():
    subject = "Droste Change Machine monitoring system has started!"
    body = "Monitoring change machines at Droste Road has started."
    send_email(subject, body)

def main():
    global LAST_EMAIL_TIME_LARGE, LAST_EMAIL_TIME_SMALL

    # Connect to Wi-Fi
    connect_wifi()

    # Send initialization email
    send_initialization_email()

    try:
        while True:
            # Check pin states every 10 seconds
            large_machine_connected = not LARGE_MACHINE_PIN.value()
            small_machine_connected = not SMALL_MACHINE_PIN.value()

            # Send email if needed and within the 1-hour email limit for each pin
            if large_machine_connected and can_send_email(LAST_EMAIL_TIME_LARGE):
                send_email(SUBJECT_LARGE_MACHINE, BODY_TEMPLATE.format(machine_name="Large"))
                LAST_EMAIL_TIME_LARGE = time()  # Record the current time

            if small_machine_connected and can_send_email(LAST_EMAIL_TIME_SMALL):
                send_email(SUBJECT_SMALL_MACHINE, BODY_TEMPLATE.format(machine_name="Small"))
                LAST_EMAIL_TIME_SMALL = time()  # Record the current time

            # Print status if no machine issues detected
            if not (large_machine_connected or small_machine_connected):
                print(f"{localtime()} - Checked pins. No machines connected.")

            sleep(10)  # Sleep for 10 seconds before rechecking

    except KeyboardInterrupt:
        print("Exiting...")

def send_email(subject, body):
    try:
        # Set up the SMTP server with SSL on port 465
        smtp = umail.SMTP(SMTP_SERVER, SMTP_PORT, ssl=True)  # Set SSL to True
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Create the email message
        smtp.to(RECEIVER_EMAIL)
        smtp.write(f"Subject: {subject}\n")
        smtp.write(f"From: {SENDER_EMAIL}\n")
        smtp.write(f"To: {RECEIVER_EMAIL}\n")
        smtp.write(body)

        smtp.send()
        smtp.quit()

        print(f"Sent email: {subject}")

    except Exception as e:
        print(f"Error sending email: {e}")

def can_send_email(last_email_time):
    current_time = time()

    # Check if 1 hour (3600 seconds) has passed since the last email
    if last_email_time is None or (current_time - last_email_time) > EMAIL_INTERVAL:
        return True
    else:
        print("1 hour has not yet elapsed. Email will not be sent.")
        return False

if __name__ == "__main__":
    main()
