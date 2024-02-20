import os
import pandas as pd


def dataframe_to_csv(table_value, index_of_params_generating_problem,
                     xopt_index, runs):
    header = ["raw_y", "corrected", "cumulative_corrected", "F", "CR", "CS",
              "ED", "x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9",
              "x10", "x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18",
              "x19"]
    df = pd.DataFrame(table_value, columns=header)
    df.to_csv("data/atom_runs/{}_{}_runs_{}.csv".format(
        index_of_params_generating_problem, xopt_index, runs), index=False)


def split_dat(index_of_params_generating_problem, xopt_index):
    problem_id = int(str(index_of_params_generating_problem).rjust(3, '0') +
                     str(xopt_index).rjust(3, '0')) + 1000000
    file_path = "logger/L-SHADE_sat_{}_{}/data_f{}_ManyAffine/IOHprofiler_f{}_DIM20.dat".format(
        index_of_params_generating_problem, xopt_index, problem_id, problem_id)
    f = open(file_path, 'r')
    lines = f.readlines()
    table_value = []
    runs = 1
    for line in lines:
        if line[:11] == "evaluations":
            if table_value != []:
                dataframe_to_csv(table_value,
                                 index_of_params_generating_problem,
                                 xopt_index, runs)
                table_value = []
                runs += 1
        else:
            elements = line[:-2].split(" ")
            elements = [float(e) for e in elements[1:]]
            table_value += [elements]
    dataframe_to_csv(table_value, index_of_params_generating_problem,
                     xopt_index, runs)


if __name__ == "__main__":

    if not os.path.exists("data/atom_runs"):
        os.mkdir("data/atom_runs")

    for index_of_params_generating_problem in range(50):
        for i in range(21):
            xopt_index = i*50+index_of_params_generating_problem
            split_dat(index_of_params_generating_problem, xopt_index)
