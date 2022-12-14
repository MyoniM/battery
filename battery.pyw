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
# types and attributes of toasts
# toast_type : {title, msg}
TOAST_TYPES = {
    'LIGHTS_ON': {'title': 'Lights ON!', 'msg': lambda batteryPercent : f'Battery started recharging from {batteryPercent}%'},
    'LIGHTS_OFF':  {'title': 'Lights OFF!', 'msg': lambda batteryPercent : f'Battery stopped charging at {batteryPercent}%'},
    'REMINDER':  {'title': 'Reminder!', 'msg': lambda batteryPercent : f'Lights still OFF! Remaining battery life: {batteryPercent}%'},
}

# function to create a toast object based on toast_type
def showToast(toast_type: str):
    battery = psutil.sensors_battery()
    batteryPercent = battery.percent

    toast = Notification(
        app_id = APP_ID,
        title = TOAST_TYPES[toast_type]['title'],
        msg = TOAST_TYPES[toast_type]['msg'](batteryPercent),
        icon = ICON_PATH
    )

    toast.set_audio(audio.Default, loop=False)
    toast.show()

# previous battery status. used to compare with the current battery status
previous_battery_status = psutil.sensors_battery().power_plugged
# previous notification time. used to show reminder toasts with a 5 min gap
prev_notification_time = None

# an active listener with SLEEP_TIME seconds delay 
while True:
    # current battery status. used to compare with the previous battery status
    current_battery_status = psutil.sensors_battery().power_plugged

    # check if lights are still OFF
    if not current_battery_status and not previous_battery_status:
        # this works only if 'Lights OFF!' toast is shown first/ at least once before
        if prev_notification_time is not None:
            now = datetime.datetime.now()
            time_gap = now - prev_notification_time
            # check if the minute difference is >= TIME_DELTA
            # if yes, show reminder toast
            if time_gap >= TIME_DELTA:
                
                showToast("REMINDER")

                # set 'prev_notification_time' to 'now' after showing the toast
                prev_notification_time = now

    # check if battery status changed
    # if yes, show status update toast
    if previous_battery_status != current_battery_status:

        # get the current toast_type from  current_battery_status
        toast_type = "LIGHTS_ON" if current_battery_status else "LIGHTS_OFF"
        showToast(toast_type)

        # if the new status is 'Lights OFF!', set 'prev_notification_time' to the current time
        if not current_battery_status:
            prev_notification_time = datetime.datetime.now()

    # update the 'previous_battery_status' with the 'current_battery_status'
    previous_battery_status = current_battery_status

    # SLEEP_TIME seconds delay
    time.sleep(SLEEP_TIME)
    print("watching for battery status change")
