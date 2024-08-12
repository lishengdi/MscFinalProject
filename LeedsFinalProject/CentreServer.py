import Algorithms
from Vehicle import Vehicle,Task
from ServiceNode import Node
class Server:
    def __init__(self,env):
        self.Nodes=[]
        self.Tasks=[]
        self.vehicles=[]
        self.avgLatency=0
        self.Task_wait_for_decision=[]
        self.Task_under_processing = []
        self.Task_wait_returning = []
    def sort_tasks(self):
        self.Tasks.sort(reverse=True,key=lambda x:x.priority)
    def find_node_nearby(self,vehicle):
        res=[]
        if vehicle.velocity>0:
            for node in self.Nodes:
                if node.location>vehicle.location and (node.location-node.radius)<=vehicle.location:
                    res.append(node)
        if vehicle.velocity<0:
            for node in self.Nodes:
                if node.location<vehicle.location and (node.location+node.radius)>=vehicle.location:
                    res.append(node)
        if not res:
            for n in self.Nodes:
                if n.type=="U":
                    self.uav_move(n,vehicle.location)

        res.sort(key=lambda x:abs(x.location-vehicle.location))
        return res
    def update_task_status_lists(self):
        self.Task_wait_for_decision = []
        self.Task_under_processing = []
        self.Task_wait_for_returning = []
        self.Task_completed = []
        self.sort_tasks()
        for t in self.Tasks:
            if t.status==0:
                self.Task_wait_for_decision.append(t)
            if t.status==1:
                self.Task_under_processing.append(t)
            if t.status==2:
                self.Task_wait_for_returning.append(t)
            if t.status==3:
                self.Task_completed.append(t)

    def get_vehicle_via_task(self,task:Task):
        VID=task.vehicleID
        for v in self.vehicles:
            if v.id==VID:
                return v
    def estimated_passing_time(self,vehicle,node):

        if vehicle.velocity>0:
            return (node.location+node.radius-vehicle.location)/vehicle.velocity
        if vehicle.velocity<0:
            return (vehicle.location-node.location+node.radius)/vehicle.velocity

    def uav_move(self,node,new_loc):
        node.location=new_loc

    def run(self):
        while True:
            for t in self.Task_wait_for_decision:
                if t:
                    Algorithms.OffloadingDecision(t,self)
                else:
                    continue
            finish_count = 0
            time_sum = 0
            for t in self.Tasks:
                if t.status==3:
                    finish_count+=1
                    time_sum+=t.turnoverTime_real

            self.avgLatency=time_sum/finish_count