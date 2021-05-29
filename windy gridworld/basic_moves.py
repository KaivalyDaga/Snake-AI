"""
This employs the SARSA algorithm
"""
import numpy as np
import matplotlib.pyplot as plt

"""
grid data, editable values
Height is the x axis and width is the y axis
"""
grid_width = 10
grid_height = 7
wind = [0, 0, 0, 1, 1, 1, 2, 2, 1, 0]
# action values
up = 0
down = 1
left = 2
right = 3
# exploration probability
epsilon = 0.1
# step size
alpha = 0.5
reward = -1
start = [3, 0]
end = [3, 7]
actions = [up, down, left, right]


class Windy:
    def __init__(self):
        """
        Initialises the grid parameters
        """
        # initialise q values as zero, 4 actions
        sar_q_value = np.zeros((grid_height, grid_width, 4), dtype=float)
        max_episodes = 500
        self.main_logic(sar_q_value, max_episodes)

    def main_logic(self, sar_q_value, max_episodes):
        """
        :param sar_q_value: sar_q_value for each state action pair
        :param max_episodes: maximum number of runs
        :return: plot and optimal policy
        """
        ep_num = 0
        # stores number of sar_steps taken for completion of each episode
        sar_steps = []
        while ep_num < max_episodes:
            sar_steps.append(self.episode(sar_q_value))
            ep_num = ep_num + 1
        # stores cumulative sum in each element
        sar_steps = np.add.accumulate(sar_steps)
        # arange gives uniform array
        plt.plot(sar_steps, np.arange(1, len(sar_steps) + 1))
        plt.xlabel("Time steps")
        plt.ylabel("Episodes")
        plt.savefig("Plot(basic_moves).png")
        plt.close()

        # display the optimal policy
        optimal_policy = []
        for i in range(0, grid_height):
            optimal_policy.append([])
            for j in range(0, grid_width):
                if [i, j] == end:
                    # G is the end state
                    optimal_policy[-1].append('G')
                    continue
                bestAction = np.argmax(sar_q_value[i, j, :])
                if bestAction == up:
                    optimal_policy[-1].append('U')
                elif bestAction == down:
                    optimal_policy[-1].append('D')
                elif bestAction == left:
                    optimal_policy[-1].append('L')
                elif bestAction == right:
                    optimal_policy[-1].append('R')
        print('Optimal policy is:')
        for row in optimal_policy:
            print(row)

    def episode(self, sar_q_value):
        """
        :param sar_q_value: values of state action pairs
        :return: number of sar_steps taken to reach the end
        """
        time_sar_steps = 0
        # initialize starting state
        sar_curr_state = start
        # choose one action, using epsilon greedy
        # equivalent to 1 coin toss with epsilon as prob of true
        if np.random.binomial(1, epsilon) == 1:
            # explores with random action with epsilon probability
            # can allow it to choose the best action too as probability is already low
            action = np.random.choice(actions)
        else:
            # known best action
            # curr state has x and y coordinates
            action = np.argmax(sar_q_value[sar_curr_state[0], sar_curr_state[1], :])
        # keep going until get to the goal state, ensures that the end state is always zero
        while sar_curr_state != end:
            # function for returning the next pos
            next_state = self.step(sar_curr_state, action)
            # choose action A' for S' using sar_q_value and epsilon greedy
            if np.random.binomial(1, epsilon) == 1:
                next_action = np.random.choice(actions)
            else:
                next_action = np.argmax(sar_q_value[next_state[0], next_state[1], :])

            # Sarsa update
            sar_q_value[sar_curr_state[0], sar_curr_state[1], action] += \
                alpha * (reward + sar_q_value[next_state[0], next_state[1], next_action] -
                         sar_q_value[sar_curr_state[0], sar_curr_state[1], action])
            # discount was 1
            sar_curr_state = next_state
            action = next_action
            time_sar_steps += 1
        return time_sar_steps

    def step(self, sar_curr_state, action):
        """
        :param sar_curr_state: starting position/sar_curr_state
        :param action: 4 of the possible actions
        :return: subsequent position
        """
        i, j = sar_curr_state
        # use max,min functions to take care of bounds
        if action == up:
            # don't have to worry about downward boundary as wind is only upwards
            return [max(i - 1 - wind[j], 0), j]
        elif action == down:
            # worry about both top and bottom boundaries
            return [max(min(i + 1 - wind[j], grid_height - 1), 0), j]
        elif action == left:
            # first wind and then left/right
            return [max(i - wind[j], 0), max(j - 1, 0)]
        elif action == right:
            return [max(i - wind[j], 0), min(j + 1, grid_width - 1)]
        else:
            assert False


if __name__ == "__main__":
    main_object = Windy()
