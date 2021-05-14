import argparse
parser = argparse.ArgumentParser()
import numpy as np
import sys
from itertools import groupby


class PLANNER:
    def __init__(self, mdp, algorithm):
        if algorithm == "vi":
            self.getData(mdp)

    def getData(self, mdp):
        # every line of text in an array
        mylines = []
        # open file and close it after reading using with
        with open(mdp, 'r') as myfile:
            for line in myfile:
                mylines.append(line)
        # getting numActions S
        numStates_ls = mylines[0].split()
        del numStates_ls[0]
        S = int(numStates_ls[0])
        # getting numActions A
        numActions_ls = mylines[1].split()
        del numActions_ls[0]
        A = int(numActions_ls[0])
        # getting discount
        discount_ls = mylines[len(mylines)-1].split()
        del discount_ls[0]
        discount = float(discount_ls[0])
        # val array initialised to 0
        val_new = [0] * S
        assoc_action = [0] * S
        # getting end
        end_ls = mylines[3].split()
        del end_ls[0]
        if end_ls[0] == "-1":
            # no end elements
            del end_ls[0]

        source = []
        dest = []
        prob = []
        action = []
        reward = []
        cnt_transitions = len(mylines) - 6
        for i in range(4, len(mylines) - 2):
            transition_ls = mylines[i].split()
            del transition_ls[0]
            source.append(int(transition_ls[0]))
            action.append(int(transition_ls[1]))
            dest.append(int(transition_ls[2]))
            reward.append(float(transition_ls[3]))
            prob.append(float(transition_ls[4]))
        self.ValueIteration(source, action, dest, reward, prob, S, A, discount, val_new, cnt_transitions, assoc_action)

    def ValueIteration(self, source, action, dest, reward, prob, S, A, discount, val_new, cnt_transitions, assoc_action):
        eachTransitionValues = []
        # type: np.ndarray
        groupedActions = []
        for key, group in groupby(action):
            groupedActions.append(list(group))

        # dummy value
        val_old = [1.22] * S

        while not self.checkConvergence(val_old, val_new):
            # copy list not reference to memory location
            val_old = val_new[:]
            curr_source = None
            source_cnt = 0
            transitions_done = 0
            # initializing list
            temp_val = [0]
            for i in range(cnt_transitions):
                if source[i] == curr_source:
                    continue
                else:
                    curr_source = source[i]
                    del eachTransitionValues[:]
                    for r in range(cnt_transitions):
                        eachTransitionValues.append(prob[r] * (reward[r] + discount * val_new[dest[r]]))
                    del temp_val[:]
                    # j is action number for a specific source state
                    for j in range(A):
                        # sum of value functions for each action of a state
                        val_sum = float(0)
                        # find appropriate element number in groupedActions list
                        for k in range(len(groupedActions[source_cnt * A + j])):
                            val_sum = val_sum + eachTransitionValues[transitions_done]
                            transitions_done = transitions_done + 1
                        temp_val.append(val_sum)
                        # temp_val stores val_sum for each action associated with a state
                    val_new[curr_source] = max(temp_val)
                    assoc_action[curr_source] = temp_val.index(val_new[curr_source])
                    source_cnt = source_cnt + 1
        with open("value_and_policy_file.txt", "w") as plannerfile:
            for num in range(S):
                plannerfile.write("%s %s\n" % (val_new[num], assoc_action[num]))

    def checkConvergence(self, val_old, val_new):
        return np.allclose(val_new, val_old,  rtol=0, atol=1e-11)


if __name__ == "__main__":
    # command-line arguments
    parser.add_argument("--mdp", type=str, default="C:/Users/Sanjay/Desktop/college/snakeAI_proj/maze assignment/base/mdpFile.txt")
    parser.add_argument("--algorithm", type=str, default="vi")

    args = parser.parse_args()
    if not (args.algorithm == "vi"):
        print("Algorithm should be Value Iteration")
        sys.exit(0)

    # main object
    main_object = PLANNER(args.mdp, args.algorithm)
