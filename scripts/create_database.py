import os
import sqlite3
import numpy as np
import pandas as pd


def array_to_dataframe(array, variable):
    keys = ["evals", "problem_id", "instance",
            "k_component", "epsilon", variable]
    values = []
    problem_ids = [1, 16, 23]
    epsilons = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.5, ""]
    for j in range(20006):
        for m in range(3):
            for n in range(8):
                k = m*8+n
                values += [[j, problem_ids[m], 1,
                            20, epsilons[n], array[0][j][k]]]
    df = pd.DataFrame(values, columns=keys)
    return df


def read_atom_array(table_name):
    result = np.zeros((1, 20006, 24))
    tables = ["raw_y", "corrected", "cumulative_corrected",
              "F", "CR", "CS", "ED"]
    index = tables.index(table_name)
    for run in range(1, 11):
        print(run)
        matrix = np.load(f"data/L-SHADE_mirror/atom_array/{index}_{run}.npy")
        if table_name == "raw_y":
            min_value = matrix[:, 0, :]
            for i in range(20006):
                min_value = np.minimum(min_value, matrix[:, i, :])
                matrix[:, i, :] = min_value
        result += matrix / 10
    return result


if __name__ == "__main__":
    table_names = ["raw_y", "corrected", "cumulative_corrected",
                   "F", "CR", "CS", "ED"]
    conn = sqlite3.connect("data/L-SHADE_mirror/atom_data.db")
    cursor = conn.cursor()
    for table_name in table_names:
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{table_name}'")
        if cursor.fetchone():
            cursor.execute(f"drop table {table_name}")
        table_values = read_atom_array(table_name)
        df = array_to_dataframe(table_values, table_name)
        df.to_sql(table_name, conn, index=False)
        print(table_name)
