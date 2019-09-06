
"""
Carwash example.

Covers:

- Waiting for other processes
- Resources: Resource

Scenario:
  A carwash has a limited number of washing machines and defines
  a washing processes that takes some (random) time.

  Car processes arrive at the carwash at a random time. If one washing
  machine is available, they start the washing process and wait for it
  to finish. If not, they wait until they an use one.

"""
import random

import simpy

import pandas as pd

import numpy as np

import matplotlib.pyplot as plt

import sys 

RANDOM_SEED = 42
NUM_MACHINES = 2                # Number of machines in the carwash
WASHTIME = 5                    # Minutes it takes to clean a car
T_INTER = 7                     # Create a car every ~7 minutes
SIM_TIME = 20                   # Simulation time in minutes

for i in range(len(sys.argv)):
    if sys.argv[i] == "-r":
        RANDOM_SEED = int(sys.argv[i+1])
    elif sys.argv[i] == "-m":
        NUM_MACHINES = int(sys.argv[i+1])
    elif sys.argv[i] == "-w":
        WASHTIME = int(sys.argv[i+1])
    elif sys.argv[i] == "-t":
        T_INTER = int(sys.argv[i+1])
    elif sys.argv[i] == "-s":
        SIM_TIME = int(sys.argv[i+1])
    else: pass
        






class Carwash(object):
    """A carwash has a limited number of machines (``NUM_MACHINES``) to
    clean cars in parallel.

    Cars have to request one of the machines. When they got one, they
    can start the washing processes and wait for it to finish (which
    takes ``washtime`` minutes).

    """
    def __init__(self, env, num_machines, washtime):
        self.env = env
        self.machine = simpy.Resource(env, num_machines)
        self.washtime = washtime

    def wash(self, car):
        """The washing processes. It takes a ``car`` processes and tries
        to clean it."""
        yield self.env.timeout(WASHTIME)
        print("Carwash removed %d%% of %s's dirt." %
              (random.randint(50, 99), car))


def car(env, name, cw):
    """The car process (each car has a ``name``) arrives at the carwash
    (``cw``) and requests a cleaning machine.

    It then starts the washing process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives at the carwash at %.2f.' % (name, env.now))
    with cw.machine.request() as request:
        yield request

        print('%s enters the carwash at %.2f.' % (name, env.now))
        yield env.process(cw.wash(name))

        print('%s leaves the carwash at %.2f.' % (name, env.now))


def setup(env, num_machines, washtime, t_inter):
    """Create a carwash, a number of initial cars and keep creating cars
    approx. every ``t_inter`` minutes."""
    # Create the carwash
    carwash = Carwash(env, num_machines, washtime)

    # Create 4 initial cars
    for i in range(4):
        env.process(car(env, 'Car %d' % i, carwash))

    # Create more cars while the simulation is running
    while True:
        yield env.timeout(random.randint(t_inter - 2, t_inter + 2))
        i += 1
        env.process(car(env, 'Car %d' % i, carwash))
"""
def test_run():
   
    thislist = []
    plt.plot(thislist,[5,6,7] )
    axes = plt.gca()
    axes.set_xlim([0,SIM_TIME])
    plt.show()

    df = df.cumsum()
    df.plot()
    plt.show()
    """
# Setup and start the simulation
print('Carwash')
#print('Check out http://youtu.be/fXXmeP9TvBg while simulating ... ;-)')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_MACHINES, WASHTIME, T_INTER))

test_run()
# Execute!
env.run(until=SIM_TIME)
