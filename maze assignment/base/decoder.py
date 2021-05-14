import argparse

parser = argparse.ArgumentParser()


class DECODER:

    def __init__(self, val_policy):
        # get state values and best actions
        myLines = []
        myActions = []
        directions = []
        # stores start_pos, end_pos, dest_ls
        variables_ls = []
        dest_ls = []
        with open("variables_needed.txt", "r") as file1:
            for line in file1:
                variables_ls.append(line)
        variables1_ls = variables_ls[0].split()
        start_pos = int(variables1_ls[0])
        end_pos = int(variables1_ls[1])
        for i in range(2, len(variables1_ls)):
            dest_ls.append(int(variables1_ls[i]))

        with open(val_policy, "r") as policyfile:
            for line in policyfile:
                myLines.append(line)
            for element in myLines:
                temp = element.split()
                # only want actions
                myActions.append(temp[1])
        for i in range(len(myActions)):
            myActions[i] = int(myActions[i])
        # for starting state
        if start_pos < end_pos:
            self.giveActionName(myActions[start_pos], directions)
            curr_pos = dest_ls[start_pos*4+myActions[start_pos]]
        else:
            self.giveActionName(myActions[start_pos], directions)
            curr_pos = dest_ls[start_pos*4-4+myActions[start_pos]]

        while True:
            if curr_pos == end_pos:
                break
            if curr_pos < end_pos:
                self.giveActionName(myActions[curr_pos], directions)
                curr_pos = dest_ls[curr_pos * 4 + myActions[curr_pos]]
            else:
                self.giveActionName(myActions[curr_pos], directions)
                curr_pos = dest_ls[curr_pos * 4 - 4 + myActions[curr_pos]]

        sol_file = open("solution.txt", "w")
        for i in range(len(directions)):
            print(directions[i], end=" ", file=sol_file)
        sol_file.close()

    def giveActionName(self, action_num, directions):
        if action_num == 0:
            directions.append("N")
        if action_num == 1:
            directions.append("E")
        if action_num == 2:
            directions.append("S")
        if action_num == 3:
            directions.append("W")


if __name__ == "__main__":
    # command-line arguments
    parser.add_argument("--val_policy", type=str, default="C:/Users/Sanjay/Desktop/college/snakeAI_proj/maze assignment/base/value_and_policy_file.txt")
    args = parser.parse_args()

    encoder_obj = DECODER(args.val_policy)
