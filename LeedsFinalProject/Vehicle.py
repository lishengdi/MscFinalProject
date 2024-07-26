import uuid
class Task:
    def __init__(self,ID,res_req,size,priority,mtt,timestamp):
        self.priority=property
        self.id=ID
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
    def __init__(self,loc,speed):
        self.id=uuid.uuid4()
        self.cpower=1000
        self.location=loc
        self.velocity=speed
        self.resource=1000

    def cpower_update(self):
        self.cpower=self.cpower-(1000-self.resource)*0.5

    def recover(self,task):
        self.resource+=task.res_req
        self.cpower+=task.res_req*0.5
        if self.resource>1000:
            self.resource=1000
        if self.cpower>1000:
            self.cpower=1000


    def take(self,task:Task):
        #update info
        task.undertaker="V"
        task.status=3
        self.resource-=task.res_req
        self.cpower_update()
        print(f"vehicleID:{self.id},take the job NO:{task.id},remain cpower:{self.cpower},remain resource:{self.resource}")
        task.timeConsumeUpdate(task.size/self.cpower)


