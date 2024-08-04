import uuid
from CentreServer import Server
class Task:
    def __init__(self,ID,vehicleID,res_req,size,priority,mtt,timestamp,data):
        self.priority=priority
        self.id=ID
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
        self.data=data
    def stageUpdate(self,status,undertaker):
        self.status=status
        self.undertaker=undertaker
    def timeConsumeUpdate(self,timeConsumed):
        self.turnoverTime_real+=timeConsumed

class Vehicle:
    def __init__(self,loc,speed):
        self.id=uuid.uuid4()
        self.cpower=500
        self.location=loc
        self.velocity=speed
        self.resource=500

    def cpower_update(self):
        self.cpower=self.cpower-(1000-self.resource)*0.5

    def recover(self,task):
        self.resource+=task.res_req
        self.cpower+=task.res_req*0.5
        if self.resource>1000:
            self.resource=1000
        if self.cpower>1000:
            self.cpower=1000


    def take(self,task:Task,server):
        #update info
        task.undertaker="V"
        task.status=2
        self.resource-=task.res_req
        self.cpower_update()
        print(f"vehicleID:{self.id},take the job NO:{task.id},remain cpower:{self.cpower},remain resource:{self.resource}")
        task.timeConsumeUpdate(task.size/self.cpower)
        server.update_task_status_lists()

    def received_or_completde(self,task:Task,server):
        task.status=3
        server.update_task_status_lists()


    def get_estimated_processing_time(self, task: Task):
        return task.size / self.cpower