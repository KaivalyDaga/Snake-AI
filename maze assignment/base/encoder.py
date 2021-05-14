import argparse
parser = argparse.ArgumentParser()
from nltk import flatten


class ENCODER:
    def __init__(self, grid):
        # get states
        # every line of text in an array
        mylines = []
        # open file and close it after reading using with
        with open(grid, 'r') as myfile:
            for line in myfile:
                mylines.append(line)
        states = []
        # get states as linear list
        for i in range(len(mylines)):
            states.append(mylines[i].split())
        # converts to 1d array
        states = list(flatten(states))
        for j in range(len(states)):
            states[j] = int(states[j])
        # dim on nxn grid
        dim = len(mylines)
        # main logic
        source_ls = []
        dest_ls = []
        # global variables
        end_pos = None
        start_pos = None
        for i in range(dim * dim):
            if not (states[i] == 1):
                # states where protagonist can be are non wall
                if states[i] == 3:
                    # end state
                    end_pos = len(source_ls)
                source_ls.append(i)
                if states[i] == 2:
                    start_pos = len(source_ls)-1
        for j in range(len(source_ls)):
            if j == end_pos:
                # end can't be start state
                continue
            for k in range(4):
                # for the four actions N E S W
                if k == 0:
                    if (source_ls[j] - dim) in source_ls:
                        dest_ls.append(source_ls.index(source_ls[j]-dim))
                    # north
                    # checks for wall
                    elif states[source_ls[j]-dim] == 1:
                        dest_ls.append(source_ls.index(source_ls[j]))
                    # checks for end state
                    else:
                        dest_ls.append(end_pos)

                if k == 1:
                    # east
                    if (source_ls[j]+1) in source_ls:
                        dest_ls.append(source_ls.index(source_ls[j]+1))
                    elif states[source_ls[j]+1] == 1:
                        dest_ls.append(j)
                    else:
                        dest_ls.append(end_pos)
                if k == 2:
                    # south
                    if (source_ls[j]+dim) in source_ls:
                        dest_ls.append(source_ls.index(source_ls[j]+dim))
                    elif states[source_ls[j]+dim] == 1:
                        dest_ls.append(j)
                    else:
                        dest_ls.append(end_pos)
                if k == 3:
                    # west
                    if (source_ls[j]-1) in source_ls:
                        dest_ls.append(source_ls.index(source_ls[j]-1))
                    elif states[source_ls[j]-1] == 1:
                        dest_ls.append(j)
                    else:
                        dest_ls.append(end_pos)
        # copy list
        starting_states = list(source_ls)
        dest_counter = 0
        # del starting_states[end_pos]
        with open("mdpFile.txt", "w") as mdpfile:
            # write mode overwrites
            mdpfile.write("numStates %s\n" % (len(source_ls)))
            mdpfile.write("actionStates 4\n")
            mdpfile.write("start %s\n" % start_pos)
            mdpfile.write("end %s\n" % end_pos)
            for num1 in range(len(starting_states)):
                if num1 == end_pos:
                    continue
                for num2 in range(4):
                    mdpfile.write("transition %s %s %s -1 1\n" % (num1, num2, dest_ls[dest_counter*4+num2]))
                dest_counter = dest_counter + 1
            mdpfile.write("mdptype episodic\n")
            mdpfile.write("discount 1")
        with open("variables_needed.txt", "w") as file1:
            file1.write("%s " % start_pos)
            file1.write("%s " % end_pos)
            for i in range(len(dest_ls)):
                file1.write("%s " % dest_ls[i])


if __name__ == "__main__":
    # command-line arguments
    parser.add_argument("--grid", type=str, default="C:/Users/Sanjay/Desktop/college/snakeAI_proj/maze assignment/base/data/maze/grid10.txt")
    args = parser.parse_args()

    encoder_obj = ENCODER(args.grid)
