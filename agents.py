import functools 
from copy import deepcopy 
from math import sqrt, inf 
from random import randint, random 

@functools.lru_cache(maxsize=128, typed=False) 
def distance(x1, y1, x2, y2): 
    """
    Measures distance b/t 2 agents
    :param agent1, agent2: animals (bunny / fox) 
    :type agent1, agent2: Objexs 
    :return: distance
    :rtype: Float 
    """

    x_dist = x1 - x2 
    y_dist = y1 - y2 
    return sqrt((x_dist*x_dist) + (y_dist*y_dist)) 

def unit_vector(agent1, agent2): 
    """
    Returns unit vector from agent1 to agent2 
    :param agent1, agent2: animal bunny/fox 
    :type agent1, agent: objex 
    :return: unit vector (x, y) 
    :rtype: tuple 
    """ 
    
    d = max(distance(agent1.x, agent1.y, agent2.x, agent2.y), 0.1) 
    return (agent2.x - agent1.x)/d, (agent2.y - agent1.y)/d

def legal_move(move, state): 
    """
    Checks move if possible and not OOB 
    :param move: next potential pos for agent (x, y) 
    :type move: tuple 
    :param state: state, 2d array of size h*w with 0 if spot is empty 
    :type state: array 
    :return: True if legal 
    :rtype: Bool
    """ 

    yMax = len(state) 
    xMax = len(state[0]) 
    return 0 <= move[0] < xMax and 0 <= move[1] < yMax 

def move_towards(agent, agentT, state, direction): 

    xU, yU = unit_vector(agent, agentT) 
    if abs(xU) >= abs(yU): 
        if xU > 0: 
            xU = 1*direction 
        else: 
            xU = -1*direction 
        move = (agent.x + xU, agent.y) 
        if legal_move(move, state): 
            (agent.x, agent.y) = move 
        else: 
            random_movement(agent, state) 
    
    else: 
        if yU > 0: 
            yU = 1*direction 
        else:
            yU = -1*direction 
        move = (agent.x, agent.y + yU) 
        if legal_move(move, state): 
            (agent.x, agent.y) = move 
        else: 
            random_movement(agent, state) 

def random_movement(agent, state, moves=None): 

    x = agent.x 
    y = agent.y 
    moves = moves or [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] 
    move = moves.pop(randint(0, len(moves)-1)) 
    if legal_move(move, state): 
        (agent.x, agent.y) = move 
    else: 
        random_movement(agent, state, moves) 


def detect_prey(agent, liveAgents, is_prey): 

    minPrey = None 
    minDist = inf 
    minKey = None 
    for key, prey in liveAgents.items(): 
        if prey.IS_PREY == is_prey and prey != agent and prey.x - agent.x <= agent.visibility and prey.y - agent.y <= agent.visibility: 
            dist = distance(agent.x, agent.y, prey.x, prey.y)  
            if minDist > dist <= agent.visibility: 
                minPrey = prey 
                minDist = dist 
                minKey = key 
    return minPrey, minKey 

class Animal: 
    def __init__(self, x, y, speed, visibility, gestChance, gestStatus, gestNumber, age): 
        self.x = x 
        self.y = y 
        self.speed = speed 
        self.visibility = visibility 
        self.gestChance = gestChance 
        self.gestStatus = gestStatus 
        self.gestNumber = gestNumber 
        self.age = age 

class Bunny(Animal): 
    """
    Bunny class variable details in run.py
    """ 
    IS_PREY = True 

    def age_creature(self, liveAgents): 
        self.age -= 1 # decrease age (if age <= 0 agent dies) 
        if self.age == 0: # kill agent when age reaches 0 
            for key, agent in liveAgents.items(): 
                if agent == self: 
                    liveAgents.pop(key, None) 
                    break 

    def handle_fox_in_area(self, state, liveAgents): 
        # scout for foxes in area 
        minFox, minFKey = detect_prey(self, liveAgents, Fox.IS_PREY) 
        if minFox is not None:  # if fox present, run 
            move_towards(self, minFox, state, -1) 
            return True 

    def doesnt_want_to_reproduce(self, state): 
        if self.gestStatus == 0: 
            self.gestStatus = int(random() < self.gestChance) 
            random_movement(self, state) 
            return True 

    def find_partner(self, state, liveAgents, age_bunny): 
        # if agent wants to fuck, find a fuckbuddy 
        minPrey, minKey = detect_prey(self, liveAgents, Bunny.IS_PREY) 
        if minPrey is not None: 
            move_towards(self, minPrey, state, 1) 
            if self.x == minPrey.x and self.y == minPrey.y:     # bunny found, reproduce 
                self.gestStatus = 0 
                maxKey = max(liveAgents) # find unassigned key in liveAgents for newborns 


                for i in range(self.gestNumber): 
                    # newborns replica of parents 
                    liveAgents[maxKey + i + 1] = Bunny( 
                        self.x, 
                        self.y, 
                        self.speed, 
                        self.visibility, 
                        self.gestChance, 
                        self.gestStatus, 
                        self.gestNumber, 
                        age_bunny   # reset age of newborns 
                    )
                return True 

    def act(self, t, state, liveAgents, age_bunny): 
        self.age_creature(liveAgents) 

        # agent can only act on some values of t (time), frequency of values are defined 
        if t % self.speed == 0: 
            if ( 
                not self.handle_fox_in_area(state, liveAgents) 
                and not self.doesnt_want_to_reproduce(state) 
                and not self.find_partner(state, liveAgents, age_bunny) 
            ): 
                random_movement(self, state) 

class Fox(Animal): 
    """
    Fox class, variables 
    """ 
    IS_PREY = False 

    def __init__(self, x, y, speed, visibility, age, huntStatus, hunger, hungerThresMin, hungerThresMax, hungerReward, maxHunger, 
                gestChance, gestStatus, gestNumber): 
        super(Fox, self).__init__(x, y, speed, visibility, gestChance, gestStatus, gestNumber, age) 
        self.huntStatus = huntStatus 
        self.hunger = hunger 
        self.hungerThresMin = hungerThresMin 
        self.hungerThresMax = hungerThresMax 
        self.hungerReward = hungerReward 
        self.maxHunger = maxHunger 

    def act(self, t, state, liveAgents, age_fox): 
        self.age -= 1 
        self.hunger -= 1 
        self.hunger = min(self.maxHunger, self.hunger) 
        if self.age == 0 or self.hunger == 0: 
            for key, agent in liveAgents.items(): 
                if agent == self: 
                    liveAgents.pop(key, None) 
                    break 
        # agent can only act on some values of t (time), frequency of values 
        if t % self.speed == 0: 
            if self.huntStatus == 0: 
                if self.hunger <= self.hungerThresMin: 
                    self.huntStatus = 1 
                if self.gestStatus == 1: 
                    minPrey, minKey = detect_prey(self, liveAgents, Fox.IS_PREY) 
                    if minPrey is not None: 
                        move_towards(self, minPrey, state, 1) 
                        if self.x == minPrey.x and self.y == minPrey.y: 
                            self.gestStatus = 0 
                            maxKey = max(liveAgents) 

                            for i in range(self.gestNumber): 
                                liveAgents[maxKey + i + 1] = deepcopy(self) 
                                # reset age of newborns 
                                liveAgents[maxKey + i + 1].age = age_fox 
                elif self.gestChance > random(): # random chance to reproduce 
                    self.gestStatus = 1 
            else:
                if self.hunger >= self.hungerThresMax: 
                    self.huntStatus = 0 
                minPrey, minKey = detect_prey( 
                    self, liveAgents, Bunny.IS_PREY) # find prey 
                if minPrey is not None: 
                    move_towards(self, minPrey, state, 1) 
                    if self.x == minPrey.x and self.y == minPrey.y: 
                        liveAgents.pop(minKey, None) 
                        self.hunger += self.hungerReward 


