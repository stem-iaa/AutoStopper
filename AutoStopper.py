git #!/usr/bin/python3

import psutil
import datetime
from gi.repository import Notify, Gtk
import time
import os


class AutoStopper:
    STOP_THRESHOLD = 8.0  # cpu percent
    SHUTDOWN_TIMEOUT = 2  # minutes
    NOTIFICATION_TIMEOUT =1  # minutes

    def __init__(self):
        self.below_threshold_time = None
        self.notification = None

        Notify.init("AutoStopper")

    def stop_idle_timer(self):
        print("stopped idle timer")
        self.below_threshold_time = None
        self.notification = None

    def start(self):
        while True:
            cpu_percent = psutil.cpu_percent()
            print(cpu_percent)
            if cpu_percent < AutoStopper.STOP_THRESHOLD:
                if self.below_threshold_time:
                    notification_compare = self.below_threshold_time + \
                                           datetime.timedelta(minutes=AutoStopper.NOTIFICATION_TIMEOUT)
                    if notification_compare < datetime.datetime.now() and not self.notification:
                        title = "AutoStopper Engaged"
                        body = "AutoStopper has determined that this virtual machine is idle. If no activity is " \
                               "detected, AutoStopper will shutdown this machine."
                        self.notification = Notify.Notification.new(title, body)
                        self.notification.set_timeout(Notify.EXPIRES_NEVER)

                        self.notification.show()
                        print("notification popped")

                    shutdown_compare = self.below_threshold_time + \
                                       datetime.timedelta(minutes=AutoStopper.SHUTDOWN_TIMEOUT)
                    if shutdown_compare < datetime.datetime.now():
                        os.system("shutdown now")
                        print("shutdown")
                        return
                else:
                    self.below_threshold_time = datetime.datetime.now()
                    print("started idle timer")
            else:
                self.stop_idle_timer()

            time.sleep(1)


if __name__ == "__main__":
    AutoStopper().start()

    '''
    Notify.init("AutoStopper")
    Notify.Notification.new("test notification").show()
    '''
