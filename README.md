# Schelling's model of segregation

## Introduction

Schelling's model of segregation is an agent-based model developed by economist Thomas Schelling in 1971. This model demonstrates how even mild preferences for neighbors of the same type (e.g., race, ethnicity, income level) can lead to high levels of segregation at the societal level. The model consists of the following key elements:

- **Two types of agents** representing different groups, initially randomly distributed on a grid.
- **Satisfaction condition**: Agents are satisfied if at least a certain fraction (the "tolerance threshold") of their neighbors are of the same type.
- **Movement**: In each round, unsatisfied agents move to the nearest vacant spot where they would be satisfied.
- **Termination**: The simulation continues until all agents are satisfied or a stable configuration is reached.

In his work, Schelling used two types of coins as the agents of the model. Since I have a background in physics and there is often a silly and somewhat funny rivalry between physicists and engineers, I will use the neighborhoods of physicists and engineers in this model instead of those coins.

At the end, I will also explore some methods of preventing segregation, such as variable thresholds or introducing third stabilizer agents that appear to reduce segregation.

## Basic Segregation Model of Schelling

In this method, I used a grid of size of 20, here the neighbors were two types and intially randomly placed in the grid. The threshold for moving of each agent in the grid is 0.4, meaning, when number of neighbors of different type exceeds this threshold then, the agent will move to other places with neighborhood satisfaction below 0.4. As you can see in the animation, the perfect segregation pattern emerges after 500 iterations. Each type had 50 agents in the grid and the total number of agents are 100.

![Basic Schelling Model](src/plots/schelling_model.gif)

## Schelling Segregation Model with Stabilizer Agents

I introduced a new type of agents to the neighborhood, called stabilizer agents. There are the agents that both our initial types are satisfied when they are neighbors. As you can see in the animation below, even introducing small number of stabilizer agents to the neighbors, can prevent the perfect segregation as seen before. When agents of each type are neighbors with stabilizer agents, since the threshold for moving is not met, agents decided to not to move, resulting a diverse neighborhood. 

![Schelling Model with stabilizer Agents](src/plots/schelling_model_stabilizers.gif)

## Schelling Segregation Model with cost of moving

I also explored a case, in which movements of agents have costs. In this first I used Manhatan Distance as our metric, and then introduced a cost threshold for moving. This method incorporates both Stabilizer agents and moving cost in a grid with Manhatan Distance as its metric. The result was not what I expected and here more work should be done. 

As you can see in the animation, some agents gets replaced by moving agents which is not quite correct. Anyways in the future I will explore this case in a better way.

![Schelling Model with cost for moving](src/plots/schelling_model_moving_cost.gif)