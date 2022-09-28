##########################################
# battery: a script for windows 10 users #
##########################################

import time
import datetime

import psutil
from winotify import Notification, audio

# application id for the notification
APP_ID = "Power Alert!"
# absolute path of the icon
ICON_PATH = r"C:\path\icon.png"
# the minute difference between 'Lights OFF' reminders
TIME_DELTA = datetime.timedelta(minutes=5)

# function to create a toast object based on current battery status
def createToast(battery_status):
    battery = psutil.sensors_battery()

    toast = Notification(
        app_id=APP_ID,
        title="Lights ON!" if battery_status else "Lights OFF!",
        msg=f"Battery started recharging from {battery.percent}%" if battery_status else f"Battery stopped charging at {battery.percent}%", duration="short",
        icon=ICON_PATH
    )

    toast.set_audio(audio.Default, loop=False)
    return toast

# function to create a reminder toast object
def reminderToast():
    battery = psutil.sensors_battery()

    toast = Notification(
        app_id=APP_ID,
        title="Reminder",
        msg=f"Lights still OFF! Remaining battery life: {battery.percent}%",
        icon=ICON_PATH
    )

    toast.set_audio(audio.Default, loop=False)
    return toast

# previous battery status. used to compare with the current battery status
previous_battery_status = psutil.sensors_battery().power_plugged
# previous notification time. used to show reminder toasts with a 5 min gap
prev_notification_time = None

# an active listener with 30 seconds delay 
while True:
    # current battery status. used to compare with the previous battery status
    current_battery_status = psutil.sensors_battery().power_plugged

    # check if lights are still OFF
    if not current_battery_status and not previous_battery_status:
        # this works only if 'Lights OFF!' toast is shown first/ before
        if prev_notification_time is not None:
            now = datetime.datetime.now()
            time_gap = now - prev_notification_time
            # check if the minute difference is >= 5
            # if yes, show reminder toast
            if time_gap >= TIME_DELTA:
                reminder_toast = reminderToast()
                reminder_toast.show()

                prev_notification_time = now

    # check if battery status changed
    # if yes, show status update toast
    if previous_battery_status != current_battery_status:

        toast = createToast(current_battery_status)
        toast.show()

        # if the new status is 'Lights OFF!', set 'previous_battery_status' to the current time
        if not current_battery_status:
            prev_notification_time = datetime.datetime.now()

    # update the 'previous_battery_status' with the 'current_battery_status'
    previous_battery_status = current_battery_status

    # 30 seconds delay
    time.sleep(30)
    print("watching for battery status change")
