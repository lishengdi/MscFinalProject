import uuid
from Vehicle import Task,Vehicle
class Node:
    def __init__(self,env,type,loc):
        self.id=uuid.uuid4()
        self.type=type # "U":UAV, "R": RSU
        self.location=loc
        self.radius=50 if type=="R" else self.radius=30
        self.resource=300 if type=="R" else self.resource=200
        self.cpower=300 if type=="R" else self.resource=200
        self.bandwidth=10000
        self.speed=0 if type=="R" else self.speed=150

    def cpower_update(self):
        if self.type=="U":
            self.cpower=self.cpower-(1000-self.resource)*0.5
        if self.type=="R":
            self.cpower=self.cpower-(1000-self.resource)*0.4

    def take(self,task:Task,server):
        #update info
        task.undertaker="V"
        task.status=2
        self.resource-=task.res_req
        self.cpower_update()
        print(f"vehicleID:{self.id},take the job NO:{task.id},remain cpower:{self.cpower},remain resource:{self.resource}")
        task.turnoverTime_real=task.size/self.cpower
        server.update_task_status_lists()


    def relay(self,task:Task):
        task.stageUpdate(status=2,undertaker=self.type)
        task.timeConsumeUpdate(task.res_size*2/self.bandwidth)
    def res_return(self,task:Task):
        task.stageUpdate(status=3,undertaker=self.type)
        task.timeConsumeUpdate(task.res_size/ self.bandwidth)
    def recover(self, task):
        self.resource += task.res_req
        self.cpower += task.res_req * 0.5
        if self.type=="U":
            if self.resource > 200:
                self.resource =200
            if self.cpower > 200:
                self.cpower = 200
        if self.type=="R":
            if self.resource > 300:
                self.resource =300
            if self.cpower > 300:
                self.cpower = 300

    def get_estimated_processing_time(self,task:Task):
        return task.size/self.cpower


