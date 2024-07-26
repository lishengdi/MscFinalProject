from Vehicle import Vehicle,Task
from ServiceNode import Node
class Server:
    def __init__(self):
        self.Nodes=[]
        self.Tasks=[]
        self.vehicle=[]
        self.avgLatency=0
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
