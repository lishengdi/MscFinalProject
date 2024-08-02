import simpy

class Vehicle:
    def __init__(self, env, name, server, rsu, drone):
        self.env = env
        self.name = name
        self.server = server
        self.rsu = rsu
        self.drone = drone
        self.action = env.process(self.run())

    def run(self):
        while True:
            # Simulate sending data to RSU
            print(f'{self.name} sending data to RSU at {self.env.now}')
            yield self.env.process(self.send_data(self.rsu))

            # Simulate processing data at RSU
            print(f'{self.name} waiting for RSU processing at {self.env.now}')
            yield self.env.timeout(2)

            # Simulate sending data to Central Server
            print(f'{self.name} sending data to Central Server at {self.env.now}')
            yield self.env.process(self.send_data(self.server))

            # Simulate sending data to Drone
            print(f'{self.name} sending data to Drone at {self.env.now}')
            yield self.env.process(self.send_data(self.drone))

            # Wait before next communication cycle
            yield self.env.timeout(5)

    def send_data(self, node):
        with node.request() as req:
            yield req
            yield self.env.timeout(1)
            print(f'{self.name} finished sending data to {node.name} at {self.env.now}')

class Server:
    def __init__(self, env, name, capacity):
        self.env = env
        self.name = name
        self.resource = simpy.Resource(env, capacity=capacity)

    def request(self):
        return self.resource.request()

env = simpy.Environment()

# Create RSU, Drones and Server
rsu_units = [Server(env, f'RSU_{i}', 1) for i in range(4)]
drone_units = [Server(env, f'Drone_{i}', 1) for i in range(4)]
central_server = Server(env, 'CentralServer', 1)

# Create Vehicles
vehicles = [Vehicle(env, f'Vehicle_{i}', central_server, rsu_units[i % 4], drone_units[i % 4]) for i in range(10)]

# Run the simulation
env.run(until=30)
