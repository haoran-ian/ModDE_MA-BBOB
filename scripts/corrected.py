import os
import pandas as pd


def parse_corrected(df, tables_corrected, i, index_of_params_generating_problem):
    corrected_flags = df["corrected"].tolist()
    for j in range(len(corrected_flags)):
        if corrected_flags[j] == 1.0:
            tables_corrected[i][j][index_of_params_generating_problem] += 1
    return tables_corrected


if __name__ == "__main__":
    if not os.path.exists("data/csv/"):
        os.mkdir("data/csv/")
    tables_corrected = [
        [[0 for _ in range(50)] for _ in range(100002)] for _ in range(21)]
    for index_of_params_generating_problem in range(50):
        for i in range(21):
            for runs in range(1, 26):
                xopt_index = i*50+index_of_params_generating_problem
                file_path = "data/atom_runs/{}_{}_runs_{}.csv".format(
                    index_of_params_generating_problem, xopt_index, runs)
                if not os.path.exists(file_path):
                    print(file_path)
                    continue
                df = pd.read_csv(file_path)
                tables_corrected = parse_corrected(
                    df, tables_corrected, i, index_of_params_generating_problem)
    df_corrected = pd.DataFrame(tables_corrected)
    df_corrected.to_csv("data/csv/correctd.csv", index=False)
