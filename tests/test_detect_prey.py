import agents 
import run 


def test_detect_prey(): 
    minPrey, minKey = agents.detect_prey(run.liveAgents[1], run.liveAgents, agents.Bunny.IS_PREY)
    assert isinstance(minPrey, agents.Bunny) 
    assert 0 <= minKey <= 100 


if __name__ == "__main__": 
    for i in range(100_000): 
        test_detect_prey() 
        