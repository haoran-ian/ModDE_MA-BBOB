import os
import sys
import time
import numpy as np
import pandas as pd


def parse_atom(df, array, i, weights_index, variable):
    values = df.values
    for j in range(100002):
        if j < values.shape[0]:
            if j > 360:
                array[i][j][weights_index] = values[j][variable]
            else:
                if variable == 0:
                    array[i][j][weights_index] = values[j][variable]
                else:
                    array[i][j][weights_index] = 0.
        else:
            array[i][j][weights_index] = array[i][j-1][weights_index]
    return array


if __name__ == "__main__":
    start_time = time.time()
    if not os.path.exists("data/atom_array/"):
        os.mkdir("data/atom_array/")
    variable = int(sys.argv[1])
    runs = int(sys.argv[2])
    # for variable in range(7):
    #     for runs in range(1, 26):
    array = np.zeros((21, 100002, 50))
    for i in range(21):
        print(variable, runs, i)
        for weights_index in range(50):
            xopt_index = i*50+weights_index
            file_path = "data/atom_runs/{}_{}_runs_{}.csv".format(
                weights_index, xopt_index, runs)
            if not os.path.exists(file_path):
                print(f"Don't exist: {file_path}")
                continue
            df = pd.read_csv(file_path)
            array = parse_atom(df, array, i, weights_index, variable)
    np.save(f"data/atom_array/{variable}_{runs}.npy", array)
    end_time = time.time()
    print(f"{(end_time-start_time)/60} mins")
