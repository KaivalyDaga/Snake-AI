"""
This employs the SARSA, expected SARSA, Q-learning algorithms
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
        ql_steps = []
        esar_steps = []
        ql_q_value = sar_q_value
        esar_q_value = sar_q_value
        while ep_num < max_episodes:
            sar_steps.append(self.sar_episode(sar_q_value))
            ql_steps.append(self.ql_episode(ql_q_value))
            esar_steps.append(self.esar_episode(esar_q_value))
            ep_num = ep_num + 1
        # stores cumulative sum in each element
        sar_steps = np.add.accumulate(sar_steps)
        ql_steps = np.add.accumulate(ql_steps)
        esar_steps = np.add.accumulate(esar_steps)
        # arange gives uniform array
        plt.plot(sar_steps, np.arange(1, len(sar_steps) + 1), label="Sarsa")
        plt.plot(ql_steps, np.arange(1, len(sar_steps) + 1), label="Q-Learning")
        plt.plot(esar_steps, np.arange(1, len(esar_steps) + 1), label="Expected Sarsa")
        plt.xlabel("Time steps")
        plt.ylabel("Episodes")
        plt.legend()
        plt.savefig("Plot(diff_algos).png")
        plt.close()

    def sar_episode(self, sar_q_value):
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
            sar_action = np.random.choice(actions)
        else:
            # known best action
            # curr state has x and y coordinates
            sar_action = np.argmax(sar_q_value[sar_curr_state[0], sar_curr_state[1], :])
        # keep going until get to the goal state, ensures that the end state is always zero
        while sar_curr_state != end:
            # function for returning the next pos
            sar_next_state = self.step(sar_curr_state, sar_action)
            # choose action A' for S' using sar_q_value and epsilon greedy
            if np.random.binomial(1, epsilon) == 1:
                sar_next_action = np.random.choice(actions)
            else:
                sar_next_action = np.argmax(sar_q_value[sar_next_state[0], sar_next_state[1], :])

            # Sarsa update
            sar_q_value[sar_curr_state[0], sar_curr_state[1], sar_action] += \
                alpha * (reward + sar_q_value[sar_next_state[0], sar_next_state[1], sar_next_action] -
                         sar_q_value[sar_curr_state[0], sar_curr_state[1], sar_action])
            # discount was 1
            sar_curr_state = sar_next_state
            sar_action = sar_next_action
            time_sar_steps += 1
        return time_sar_steps

    def ql_episode(self, ql_q_value):
        """
        :param ql_q_value:
        :return: number of ql_steps required to reach the end state
        """
        time_ql_steps = 0
        # initialize starting state
        ql_curr_state = start
        # keep going until get to the goal state, ensures that the end state is always zero
        while ql_curr_state != end:
            # choose one action, using epsilon greedy
            # equivalent to 1 coin toss with epsilon as prob of true
            if np.random.binomial(1, epsilon) == 1:
                # explores with random action with epsilon probability
                # can allow it to choose the best action too as probability is already low
                ql_action = np.random.choice(actions)
            else:
                # known best action
                # curr state has x and y coordinates
                ql_action = np.argmax(ql_q_value[ql_curr_state[0], ql_curr_state[1], :])
            # function for returning the next pos
            ql_next_state = self.step(ql_curr_state, ql_action)
            # Q learning update
            ql_q_value[ql_curr_state[0], ql_curr_state[1], ql_action] += \
                alpha * (reward + max(ql_q_value[ql_next_state[0], ql_next_state[1], :]) -
                         ql_q_value[ql_curr_state[0], ql_curr_state[1], ql_action])
            # discount was 1
            ql_curr_state = ql_next_state
            time_ql_steps += 1
        return time_ql_steps

    def esar_episode(self, esar_q_value):
        """
        :param esar_q_value: values of state action pairs
        :return: number of esar_steps taken to reach the end
        """
        time_esar_steps = 0
        # initialize starting state
        esar_curr_state = start
        # choose one action, using epsilon greedy
        # equivalent to 1 coin toss with epsilon as prob of true
        if np.random.binomial(1, epsilon) == 1:
            # explores with random action with epsilon probability
            # can allow it to choose the best action too as probability is already low
            esar_action = np.random.choice(actions)
        else:
            # known best action
            # curr state has x and y coordinates
            esar_action = np.argmax(esar_q_value[esar_curr_state[0], esar_curr_state[1], :])
        # keep going until get to the goal state, ensures that the end state is always zero
        while esar_curr_state != end:
            # function for returning the next pos
            esar_next_state = self.step(esar_curr_state, esar_action)
            # choose action A' for S' using sar_q_value and epsilon greedy
            if np.random.binomial(1, epsilon) == 1:
                esar_next_action = np.random.choice(actions)
            else:
                esar_next_action = np.argmax(esar_q_value[esar_next_state[0], esar_next_state[1], :])
            # expected q value
            best_q_val = max(esar_q_value[esar_next_state[0], esar_next_state[1], :])
            exp_esar_q_value = (epsilon / 4 * np.sum(esar_q_value[esar_next_state[0], esar_next_state[1], :]) +
                                (1 - epsilon) * best_q_val)
            # Expected Sarsa update
            esar_q_value[esar_curr_state[0], esar_curr_state[1], esar_action] += \
                alpha * (reward + exp_esar_q_value -
                         esar_q_value[esar_curr_state[0], esar_curr_state[1], esar_action])
            # discount was 1
            esar_curr_state = esar_next_state
            esar_action = esar_next_action
            time_esar_steps += 1
        return time_esar_steps

    def step(self, sar_curr_state, sar_action):
        """
        :param sar_curr_state: starting position/sar_curr_state
        :param sar_action: 4 of the possible actions
        :return: subsequent position
        """
        i, j = sar_curr_state
        # use max,min functions to take care of bounds
        if sar_action == up:
            # don't have to worry about downward boundary as wind is only upwards
            return [max(i - 1 - wind[j], 0), j]
        elif sar_action == down:
            # worry about both top and bottom boundaries
            return [max(min(i + 1 - wind[j], grid_height - 1), 0), j]
        elif sar_action == left:
            # first wind and then left/right
            return [max(i - wind[j], 0), max(j - 1, 0)]
        elif sar_action == right:
            return [max(i - wind[j], 0), min(j + 1, grid_width - 1)]
        else:
            assert False


if __name__ == "__main__":
    main_object = Windy()
