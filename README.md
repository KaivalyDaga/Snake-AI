# Snake-AI

This repository contains the files and the code for my WnCC Summer of Code - 2021 Project (Snake AI)

In this project, I built the very popular Nokia Snake Game from scratch and then implemented basic Reinforcement Learning (RL) techniques to help the snake master the game and get really high scores. The RL agent is capable of learning on its own by exploring its environment to determine the best action to take in a certain situation.
___
## Basic Game Demo
This is a keyboard controlled version of the game. 
You can find the basic game demo [here](https://drive.google.com/file/d/1CNqgc_5zQGanXpYcHHVvlu6Re66HdskK/view?usp=drivesdk)
___

## Assignment 1 - Maze Assignment
Worked on this assignment during the first week of May '21. 

In this assignment, I had to implement a maze solver using Value Iteration. The program doesn't use memory efficient methods and is computationally heavy. The last 10x10 grid took >30 min to run. The objective of the assignment was to check the understanding that I developed with the help of David Silver's RL lectures of Barton and Sutton's book (in resources at the end) and to also get some hands on coding practice.

The assignment has two parts, in the first part we use the value iteration algorithm on an MDP. And in the second part we model our maze as an MDP and then attempt to solve it. 
In the data folder, you'll find the data for the maze as well as the mdp. You'll find more details in the assignment link. Ignore the linear programming and howard policy iteration part.

[Link to Assignment 1](https://www.cse.iitb.ac.in/~shivaram/teaching/old/cs747-a2020/pa-2/programming-assignment-2.html)

The generateMDP.py file generates a random MDP of the prescribed format.

The planner.py file runs the Value Iteration algorithm and assigns a value to each element which can then be used for further analysis.

The encoder.py file encodes the maze which is represented using the numbers- 0,1,2,3 as an MDP.

The decoder.py file then understands the output of the planner file and decides the shortest path between given points of a given maze.

The value_and_policy_file.txt and variables_needed.txt files are needed during the execution of the code.

The MazeVerifyOutput.py and PlannerVerifyOutput.py files check the output of the encoder and the planner files for the given data at once.

Visualize.py generates an image of the maze - with or without the shortest path 

Solution.txt contains the solution for the shortest path in case of the given maze files

You can view the image of the solution in case of the 10x10 maze using gridFile.png

___
## Assignment 2 - Sutton & Barto's Windy Gridworld using Model-free control
In this assignment, we solve the Windy Gridworld problem using different Model-free approaches - SARSA(0), Q-Learning, Expected-SARSA, Dyna-Q. Dyna-Q proves to be the best, outperforming all the other algorithms while Q-Learning and Expected-SARSA have similar performances. I plan on adding an implemention of SARSA(&lambda;) and comparing it with other approaches listed above.  
[Sutton & Barto](https://www.andrew.cmu.edu/course/10-703/textbook/BartoSutton.pdf)  
[Link to the Assignment 2](https://www.cse.iitb.ac.in/~shivaram/teaching/old/cs747-a2020/pa-2/programming-assignment-3.html)
___

## Simple Tabular RL Agent
I have added a simple Tabular RL agent to play the Snake Game. The game has an extremely large state space representation and we must use a reduced representation to make the task feasible.
### State Space
My representation uses 7 bits of information to describe the current state of the snake:
* 4 bits of information to define the relative position of the fruit with respect to the head of the snake
* 3 bits of information for obstacles right in front of the head, to the immediate right and left of the head

### Action Space
The snake has 3 possible actions:
* Do nothing: The snake continues to move in the same direction
* Turn right: The snake turns right to change its direction
* Turn left: The snake turns left to change its direction

### Reward Scheme
I have used a fairly simple reward scheme that can be optimized to improve the performance of the agent:
* Reward of +5 if the snake moves closer to the fruit
* Reward of -5 if the snake moves away from the fruit
* Reward of +500 for eating the fruit
* Reward of -1000 for crashing  

### Hyperparameters
The starting learning rate and &epsilon; parameter for an &epsilon;-greedy policy are 0.5 and 0.01. Without decaying these hyperparameters, the training behaviour of the agent is extremely erratic. With annealing, the performance is more consistent. The agent has achieved a maximum score of 64. 
___

## Resources
[Resource Webpage](https://www.notion.so/SOC-Snake-AI-Project-471ff57983a24f749ca0ec08df8c9472)
