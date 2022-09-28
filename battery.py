import time
import datetime

import psutil
from winotify import Notification, audio

APP_ID = "Power Alert!"
ICON_PATH = r"C:\Users\YONI\Documents\Projects\My Projects\battery\icon.png"
TIME_DELTA = datetime.timedelta(minutes=5)


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


last_battery_status = psutil.sensors_battery().power_plugged
prev_notification_time = None

while True:
    current_battery_status = psutil.sensors_battery().power_plugged

    if not current_battery_status and not last_battery_status:
        if prev_notification_time is not None:
            now = datetime.datetime.now()
            time_gap = now - prev_notification_time

            if time_gap >= TIME_DELTA:
                reminder_toast = reminderToast()
                reminder_toast.show()

                prev_notification_time = now

    if last_battery_status != current_battery_status:

        toast = createToast(current_battery_status)
        toast.show()

        if not current_battery_status:
            prev_notification_time = datetime.datetime.now()

    last_battery_status = current_battery_status

    time.sleep(30)
    print("watching for battery status change")
