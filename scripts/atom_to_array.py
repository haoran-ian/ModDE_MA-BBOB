import os
import sys
import time
import numpy as np
import pandas as pd


def parse_atom(df, array, problem_id, epsilon, variable):
    values = df.values
    m = [1, 16, 23].index(problem_id)
    n = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1].index(epsilon)
    index = m*6+n
    for j in range(20006):
        if j < values.shape[0]:
            if j > 360:
                array[0][j][index] = values[j][variable]
            else:
                if variable == 0:
                    array[0][j][index] = values[j][variable]
                else:
                    array[0][j][index] = 0.
        else:
            array[0][j][index] = array[0][j-1][index]
    return array


if __name__ == "__main__":
    start_time = time.time()
    if not os.path.exists("data/L-SHADE_mirror/atom_array/"):
        os.mkdir("data/L-SHADE_mirror/atom_array/")
    variable = int(sys.argv[1])
    runs = int(sys.argv[2])
    array = np.zeros((1, 20006, 18))
    for problem_id in [1, 16, 23]:
        for epsilon in [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]:
            file_path = f"data/L-SHADE_mirror/atom_runs/{problem_id}_1_20_{epsilon}_runs_{runs}.csv"
            if not os.path.exists(file_path):
                print(f"Don't exist: {file_path}")
                continue
            df = pd.read_csv(file_path)
            array = parse_atom(df, array, problem_id, epsilon, variable)
    np.save(f"data/L-SHADE_mirror/atom_array/{variable}_{runs}.npy", array)
    end_time = time.time()
    print(f"{(end_time-start_time)/60} mins")
