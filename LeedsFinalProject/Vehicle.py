import uuid
from CentreServer import Server
import random
import numpy as np
import os
import time

class Task:
    def __init__(self,vehicleID,res_req,size,priority,mtt,timestamp):
        self.priority=priority
        self.id=uuid.uuid4()
        self.vehicleID=vehicleID
        self.res_req=res_req
        self.size=size
        self.mtt=mtt
        self.status=0 #0:waiting for process, 1:processed,2:relaying 3:Completed
        self.undertaker="V" #"V":vehicle, "U":UAV, "R": RSU
        self.turnoverTime_estimatedOnVehicle=0 # estimated processing time without offloading
        self.turnoverTime_real = 0
        self.returnViaRelay=False
        self.timeStamp=timestamp
        self.res_size=self.size*0.4

    def stageUpdate(self,status,undertaker):
        self.status=status
        self.undertaker=undertaker
    def timeConsumeUpdate(self,timeConsumed):
        self.turnoverTime_real+=timeConsumed

class Vehicle:
    def __init__(self,env,loc,speed,server):
        self.id=uuid.uuid4()
        self.cpower=500
        self.location=loc
        self.velocity=speed
        self.resource=500

    def cpower_update(self):
        self.cpower=self.cpower-(100-self.resource)*0.5

    def recover(self,task):
        self.resource+=task.res_req
        self.cpower+=task.res_req*0.5
        if self.resource>100:
            self.resource=100
        if self.cpower>100:
            self.cpower=100


    def take(self,task:Task,server):
        #update info
        task.undertaker="V"
        task.status=2
        self.resource-=task.res_req
        self.cpower_update()
        print(f"vehicleID:{self.id},take the job NO:{task.id},remain cpower:{self.cpower},remain resource:{self.resource}")
        task.timeConsumeUpdate(task.size/self.cpower)
        server.update_task_status_lists()
        self.recover(task)

    def received_or_completde(self,task:Task,server):
        task.status=3
        server.update_task_status_lists()

    def get_estimated_processing_time(self, task: Task):
        return task.size / self.cpower
    def run(self):
        while True:
            time.sleep(5)
            flag=random.randint(0,100)
            if flag %2==0:
                res=random.randint(0,300)
                priority=random.randint(1,4)
                mtt=random.randint(1000,2400)
                size=random.randint(1000,30000)
                new_task=Task(self.id,res,size,priority,mtt,time.time())
            else:
                continue
