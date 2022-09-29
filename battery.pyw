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
ICON_PATH = r"C:\Users\YONI\Documents\Projects\My Projects\battery\icon.png"
# the minute difference between 'Lights OFF' reminders
TIME_DELTA = datetime.timedelta(minutes=4, seconds=50)
# time to sleep
SLEEP_TIME = 15

# function to create a toast object based on current battery status
def showStatusChangeToast(battery_status):
    battery = psutil.sensors_battery()

    toast = Notification(
        app_id=APP_ID,
        title="Lights ON!" if battery_status else "Lights OFF!",
        msg=f"Battery started recharging from {battery.percent}%" if battery_status else f"Battery stopped charging at {battery.percent}%", duration="short",
        icon=ICON_PATH
    )

    toast.set_audio(audio.Default, loop=False)
    toast.show()

# function to create a reminder toast object
def showReminderToast():
    battery = psutil.sensors_battery()

    toast = Notification(
        app_id=APP_ID,
        title="Reminder",
        msg=f"Lights still OFF! Remaining battery life: {battery.percent}%",
        icon=ICON_PATH
    )

    toast.set_audio(audio.Default, loop=False)
    toast.show()

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
        print(prev_notification_time)
        if prev_notification_time is not None:
            now = datetime.datetime.now()
            time_gap = now - prev_notification_time
            # check if the minute difference is >= 5
            # if yes, show reminder toast
            print(time_gap, TIME_DELTA)
            if time_gap >= TIME_DELTA:
                
                showReminderToast()

                # set 'prev_notification_time' to 'now' after showing the toast
                prev_notification_time = now

    # check if battery status changed
    # if yes, show status update toast
    if previous_battery_status != current_battery_status:

        showStatusChangeToast(current_battery_status)

        # if the new status is 'Lights OFF!', set 'previous_battery_status' to the current time
        if not current_battery_status:
            prev_notification_time = datetime.datetime.now()

    # update the 'previous_battery_status' with the 'current_battery_status'
    previous_battery_status = current_battery_status

    # 15 seconds delay
    time.sleep(SLEEP_TIME)
    print("watching for battery status change")
