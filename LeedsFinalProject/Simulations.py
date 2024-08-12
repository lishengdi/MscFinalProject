import simpy
import Vehicle
import ServiceNode
import Algorithms
import CentreServer
import time
import random
import numpy as np

np.random.seed(42)
env = simpy.Environment()

NUM_Vehicle=50
Max_NUM_Tasks=100
NUM_RSU=10
NUM_UAV=10
speed_range = (-100, 100)
mean_speed1 = -50
mean_speed2 = 50
std_dev_speed = 20


vehicle_positions = np.random.uniform(0, 1000, NUM_Vehicle)

vehicle_speeds1 = np.random.normal(mean_speed1, std_dev_speed, NUM_Vehicle // 2)
vehicle_speeds2 = np.random.normal(mean_speed2, std_dev_speed, NUM_Vehicle // 2)
vehicle_speeds = np.concatenate((vehicle_speeds1, vehicle_speeds2))

#build and start centre Server
centre_server=CentreServer.Server(env)
centre_server.run()

#create vehicle
for i in range(NUM_Vehicle):
    centre_server.vehicles.append(
        Vehicle.Vehicle(env,vehicle_positions[i],vehicle_speeds[i],centre_server)
    )
    centre_server.vehicles[i].run()

#create and start Nodes
for i in range(NUM_RSU):
    centre_server.Nodes.append(ServiceNode.Node(env,"R",np.random.randint(0,1000)))
for i in range(NUM_RSU):
    centre_server.Nodes.append(ServiceNode.Node(env,"U",np.random.randint(0,1000)))
for i in range(NUM_UAV+NUM_RSU):
    centre_server.Nodes[i].run()

# Run the simulation
env.run(until=100)

print(f"Current System Average Latency: {centre_server.avgLatency}")


