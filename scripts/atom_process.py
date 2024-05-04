import os
import pandas as pd


def dataframe_to_csv(table_value, problem_id, iid, k_component, epsilon, runs):
    header = ["raw_y", "corrected", "cumulative_corrected", "F", "CR", "CS",
              "ED", "x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9",
              "x10", "x11", "x12", "x13", "x14", "x15", "x16", "x17", "x18",
              "x19"]
    df = pd.DataFrame(table_value, columns=header)
    file_name = f"data/L-SHADE_mirror/atom_runs/{problem_id}_{iid}_{k_component}_{epsilon}_runs_{runs}.csv"
    print(file_name)
    df.to_csv(file_name, index=False)


def split_dat(problem_id, iid, k_component, epsilon):
    folder_path = f"data/L-SHADE_mirror/L-SHADE_mirror_{problem_id}_{epsilon}/"
    child_folder_path = os.listdir(folder_path)[0]
    file_path = os.listdir(folder_path + child_folder_path)[0]
    file_path = folder_path + child_folder_path + "/" + file_path
    f = open(file_path, 'r')
    lines = f.readlines()
    table_value = []
    runs = 1
    for line in lines:
        if line[:11] == "evaluations":
            if table_value != []:
                dataframe_to_csv(table_value, problem_id, iid,
                                 k_component, epsilon, runs)
                table_value = []
                runs += 1
        else:
            elements = line[:-2].split(" ")
            elements = [float(e) for e in elements[1:]]
            table_value += [elements]
    dataframe_to_csv(table_value, problem_id, iid, k_component, epsilon, runs)


if __name__ == "__main__":

    if not os.path.exists("data/L-SHADE_mirror/atom_runs"):
        os.mkdir("data/L-SHADE_mirror/atom_runs")

    for problem_id in [1, 16, 23]:
        for epsilon in [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]:
            split_dat(problem_id, 1, 20, epsilon)
