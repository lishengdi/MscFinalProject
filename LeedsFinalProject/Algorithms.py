from CentreServer import Server
from ServiceNode import Node
from Vehicle import Vehicle
import numpy as np
import random

#stage 3 relay node secection
def relay_node_selection(task,server):
    vehicle=server.get_vehicle_via_task(task)
    candidate_nodes=server.find_node_nearby(vehicle)
    found_flag=False
    for node in candidate_nodes:
        estimated_passing_time=server.estimated_passing_time(vehicle,node)
        if estimated_passing_time >= task.res_size/node.bandwidth:
            found_flag=True
            node.relay(task)
            node.res_return(task)
            vehicle.received_or_completde()
            vehicle.received_or_completde(task,server)
            break
    if not found_flag:
        pass
        # relay_node_selection(task,server)


#stage 2 offloading_node_selection
def Offloading_node_selection(task,server):
    # Initialize parameters
    alpha = 0.1  # Learning rate
    gamma = 0.9  # Discount factor
    epsilon = 1.0  # Exploration rate
    epsilon_decay = 0.99
    min_epsilon = 0.01
    num_episodes = 1000
    threshold_speed=100
    # Define the ranges for state space dimensions
    task_size_range = 50000
    speed_range = 120
    position_range = 5000
    rsu_resource_range = 3000
    uav_resource_range = 2000

    # Initialize Q-table
    state_space = (task_size_range, speed_range, position_range, rsu_resource_range, uav_resource_range)
    action_space = [0, 1]  # 0: RSU, 1: UAV
    Q_table = np.zeros(state_space + (len(action_space),))


    # get_vehicle_status:
    vehicle=server.get_vehicle_via_task(task)
    # get candidate nodes
    candidate_nodes=server.find_node_nearby(vehicle)
    candidate_uav=candidate_nodes[0]
    candidate_rsu=candidate_uav
    for n in candidate_nodes:
        if n.type=="U":
            candidate_uav=n
            break
        if n.type=="R":
            candidate_rsu=n

    def RSU_compute(task):
        candidate_rsu.take(task)

    def UAV_compute(task):
        candidate_uav.take(task)

    def calculate_reward(processing_time, deadline):
        # Reward based on whether the task meets the deadline
        return 1 if processing_time <= deadline else -1

    def offload_to_RSU(task, speed,vehicle_location,rsu_resource):
        if speed < threshold_speed:
            RSU_compute(task)
            processing_time = candidate_rsu.get_estimated_processing_time(task)
            reward = calculate_reward(processing_time, task.mtt)
            next_state = [task.size, vehicle.velocity, vehicle.location, candidate_rsu.recource,
                          candidate_uav.resource]
            return reward, next_state
        else:
            return -1, None  # Penalty for moving out of RSU range

    def offload_to_UAV(task, speed,vehicle_location,uav_resource):
        UAV_compute(task)
        processing_time = candidate_uav.get_estimated_processing_time(task)
        reward = calculate_reward(processing_time, task.mtt)
        next_state = [task.size, vehicle.velocity, vehicle.location, candidate_rsu.recource,
                          candidate_uav.resource]
        return reward, next_state

    # Simulation loop
    for episode in range(num_episodes):
        # task = task
        vehicle=server.get_vehicle_via_task(task)
        state = [task.size, vehicle.velocity, vehicle.location, candidate_rsu.recource,
                          candidate_uav.resource]

        done = False
        while not done:
            if random.random() < epsilon:
                action = random.choice(action_space)  # Exploration
            else:
                action = np.argmax(Q_table[tuple(state)])  # Exploitation

            if action == 0:  # RSU
                reward, next_state = offload_to_RSU(task, state[2], state[3], state[4])
            else:  # UAV
                reward, next_state = offload_to_UAV(task, state[2], state[3], state[5])

            if next_state is not None:
                best_next_action = np.argmax(Q_table[tuple(next_state)])
                Q_table[tuple(state)][action] = Q_table[tuple(state)][action] + alpha * (
                            reward + gamma * Q_table[tuple(next_state)][best_next_action] - Q_table[tuple(state)][
                        action])
                state = next_state
            else:
                done = True

        if epsilon > min_epsilon:
            epsilon *= epsilon_decay

#stage 1 decide whether to offloading
def OffloadingDecision(task,server):
    vehicle=server.get_vehicle_via_task(task)
    R_remain=vehicle.resource
    J_mrr=task.res_req
    J_dl=task.mtt
    if R_remain>=J_mrr:
        estimated_processing_time=vehicle.get_estimated_processing_time(task)
        task.turnoverTime_estimatedOnVehicle=estimated_processing_time
        if estimated_processing_time <= J_dl:
            vehicle.take(task,server)
        else:
            Offloading_node_selection(task,server)
    else:
        Offloading_node_selection(task,server)

