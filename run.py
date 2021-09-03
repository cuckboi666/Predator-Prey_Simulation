from random import randint  

import matplotlib.animation as animation 
import matplotlib.pyplot as plt 
import numpy as np 

from agents import Bunny, Fox 

def create_world(h, w, n_bunnies, speed_bunny_min, speed_bunny_max, visibility_bunny, gestChance_bunny, 
                gestStatus_bunny, gestNumber_bunny, age_bunny, n_foxes, speed_fox, visibility_fox, huntStatus_fox, age_fox, 
                hunger_fox, hungerThresMin_fox, hungerThresMax_fox, hungerReward_fox, maxHunger_fox, gestChance_fox, 
                gestStatus_fox, gestNumber_fox):
                state = np.zeros((h, w)) 
                liveAgents = {} 
                for i in range(1, n_bunnies + 1):
                    x = randint(0, w - 1) 
                    y = randint(0, h - 1) 
                    state[y][x] = i 
                    liveAgents[i] = Bunny(x, y, randint(speed_bunny_min, speed_bunny_max), visibility_bunny, gestChance_bunny, gestStatus_bunny, gestNumber_bunny, age_bunny) 



                for j in range(n_bunnies + 1, n_bunnies + 1 + n_foxes): 
                    x = randint(0, w - 1) 
                    y = randint(0, h - 1) 
                    state[y][x] = j 
                    liveAgents[j] = Fox(x, y, speed_fox, visibility_fox, age_fox, huntStatus_fox, hunger_fox, hungerThresMin_fox, hungerThresMax_fox, hungerReward_fox, maxHunger_fox, gestChance_fox, gestStatus_fox, gestNumber_fox) 


                return state, liveAgents 

def update_state(state, liveAgents): 
    state = np.zeros((len(state), len(state[0]))) 
    for key, agent in liveAgents.items(): 
        x = agent.x 
        y = agent.y 
        state[y][x] = key 
    return state 

def step(t, state, liveAgents): 
    for key, agent in liveAgents.copy().items(): 
        agent.act(t, state, liveAgents, age_fox) 
    return update_state(state, liveAgents) 

def export(liveAgents):
    XBunnies = []  
    YBunnies = [] 
    XFoxes = [] 
    YFoxes = [] 
    for agent in liveAgents.values(): 
        if isinstance(agent, Bunny): 
            XBunnies.append(agent.x) 
            YBunnies.append(agent.y) 
        elif isinstance(agent, Fox): 
            XFoxes.append(agent.x) 
            YFoxes.append(agent.y) 
    return XBunnies, YBunnies, XFoxes, YFoxes 

def count(liveAgents): 
    liveBunnies = 0 
    liveFoxes = 0 
    speed = 0 
    for agent in liveAgents.values(): 
        if isinstance(agent, Bunny): 
            liveBunnies += 1 
            speed += agent.speed 
        else: 
            liveFoxes += 1 
    return liveBunnies, liveFoxes, speed/max(liveBunnies, 0.1) 

# intialize dem vars 
w = 50  # width of world
h = 50  # height of world 
n_bunnies = 100     # number of bunnies 
speed_bunny_max = 9 # max bunny speed
speed_bunny_min = 2 # min bunny speed 
visibility_bunny = 10 # vision range of bunnies 
gestChance_bunny = 0.0008 # reproductive chance (0 - no reproduction / 1 - reproduction)
gestStatus_bunny = 0 
gestNumber_bunny = 3    # bunnies created per reproduction 
age_bunny = 5000 
n_foxes = 6     # number of foxes intially 
speed_fox = 4 
visibility_fox = 100    # vision range of fox 
age_fox = 800 
huntStatus_fox = 0 # 0 - no hunt / 1 - hunting
hunger_fox = 250   
hungerThresMin_fox = 350 
hungerThresMax_fox = 450    # hunger >= agent stops hunting 
hungerReward_fox = 150 # hungerreward per kill 
maxHunger_fox = 500     # hunger max limit 
gestChance_fox = 0.0004     # chance foxes reproduce 
gestStatus_fox = 0 
gestNumber_fox = 1  # foxes created in reproduction 

# change font sizse for plt 
size = 8 
small_size = 6 
plt.rc('font', size=size)  #control default text size 
plt.rc('axes', titlesize=size)  # fontsize of axes title 
plt.rc('axes', labelsize=small_size)    # fontsize of x and y 
plt.rc('xtick', labelsize=small_size) # fontsize of X tick 
plt.rc('ytick', labelsize=small_size)   # fontsize of Y tick 
plt.rc('legend', fontsize=small_size) # legend fontsize 
plt.rc('figure', titlesize=small_size) 

# setting up plots 
fig = plt.figure() 
ax1 = plt.subplot(221, title="Ecosystem (blue=bunny; red=fox)", xlabel="x (-)", ylabel="y (-)")
plt.xlim(0, w) 
plt.ylim(0, h) 
bunnies, = ax1.plot([], [], 'bo', ms=3) 
foxes, = ax1.plot([], [], 'ro', ms=3) 

# plot to study evo of avg speed of bunnies OT
ax2 = plt.subplot(224, title="average speed of bunnies over time (red=fox speed)", xlabel="time (-)", ylabel="speed (less is faster) (-)")
plt.xlim(0, 5000) 
plt.ylim(7, 2) 
plt.plot([0, 5000], [speed_fox, speed_fox], color='r')
speedData, = ax2.plot([], []) 


ax3 = plt.subplot(222, title="Population over time", xlabel="time (-)", ylabel="population (-)") 
plt.xlim(0, 5000) 
plt.ylim(0, 200) 
popBunnyData, = ax3.plot([], []) 
popFoxData, = ax3.plot([], [], color='r') 

fig.tight_layout(pad=1.5) 

def init(): 
    """ initialize animation """  
    bunnies.set_data([], []) 
    foxes.set_data([], []) 
    popBunnyData.set_data([], [])
    popFoxData.set_data([], []) 
    speedData.set_data([], []) 
    return bunnies, foxes, popBunnyData, popFoxData, speedData,


# craete new world 
(state, liveAgents)  = create_world(w, h, n_bunnies, 
                                    speed_bunny_min, speed_bunny_max, visibility_bunny, gestChance_bunny, gestStatus_bunny, 
                                    gestNumber_bunny, age_bunny, n_foxes, speed_fox, visibility_fox, age_fox, huntStatus_fox, 
                                    hunger_fox, hungerThresMin_fox, hungerThresMax_fox, hungerReward_fox, maxHunger_fox, 
                                    gestChance_fox, gestStatus_fox, gestNumber_fox) 

t = 0   # time 
T = [] 
popBunnyList = [] 
popFoxList = [] 
speedList = [] 

# animate fxn 

def animate(_): 
    global t, state, liveAgents 
    state = step(t, state, liveAgents)  # execute steps 
    t += 1      # increment time 
    T.append(t)     # time lsit for plt 

    totalCount = count(liveAgents) 
    popBunnyList.append(totalCount[0]) 
    popFoxList.append(totalCount[1]) 
    speedList.append(totalCount[2]) 

     # export pos of agents for plt 
    (Xbunnies, Ybunnies, XFoxes, YFoxes) = export(liveAgents) 

    # Set data for animation 
    bunnies.set_data(Xbunnies, Ybunnies) 
    foxes.set_data(XFoxes, YFoxes) 
    popBunnyData.set_data(T, popBunnyList) 
    speedData.set_data(T, speedList) 

    return bunnies, foxes, popBunnyData, popFoxData, speedData, 


if __name__ == "__main__": 

    # Animation 
    ani = animation.FuncAnimation(fig, animate, frames=600, interval=5, blit=True, init_func=init) 

    plt.show() 











                
