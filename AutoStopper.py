#!/usr/bin/python3

import psutil
import datetime
import time
import os
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient
import json


class AutoStopper:
    STOP_THRESHOLD = 1.0  # cpu percent
    SHUTDOWN_TIMEOUT = 1.0  # minutes

    def __init__(self):
        self.below_threshold_time = None

        self.config = json.load(open("config.json"))

        self.credentials = ServicePrincipalCredentials(
            client_id=self.config["client_id"],
            secret=self.config["secret"],
            tenant=self.config["tenant"]
        )

        self.vm_name = open("vm_name.txt").read()

        self.compute_client = ComputeManagementClient(self.credentials, self.config["subscription_id"])

    def stop_idle_timer(self):
        print("stopped idle timer")
        self.below_threshold_time = None

    def start(self):
        while True:
            cpu_percent = psutil.cpu_percent()
            print(cpu_percent)
            if cpu_percent < AutoStopper.STOP_THRESHOLD:
                if self.below_threshold_time:
                    shutdown_compare = self.below_threshold_time + \
                                       datetime.timedelta(minutes=AutoStopper.SHUTDOWN_TIMEOUT)
                    print(shutdown_compare, datetime.datetime.now())
                    if shutdown_compare < datetime.datetime.now():
                        print("shutdown")
                        async_vm_deallocate = self.compute_client.virtual_machines.deallocate(
                            self.config["group_name"],
                            self.vm_name
                        )
                        async_vm_deallocate.wait()
                else:
                    self.below_threshold_time = datetime.datetime.now()
                    print("started idle timer")
            else:
                self.stop_idle_timer()

            time.sleep(1)


if __name__ == "__main__":
    AutoStopper().start()
