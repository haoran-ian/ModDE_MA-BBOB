import os
import sqlite3
import numpy as np
import pandas as pd


def array_to_dataframe(array, variable):
    keys = ["boundaries", "evals", "problem_id", variable]
    values = []
    for i in range(21):
        print(i)
        for j in range(100002):
            for k in range(50):
                values += [[i, j, k, array[i][j][k]]]
    df = pd.DataFrame(values, columns=keys)
    return df


def read_atom_array(table_name):
    result = np.zeros((21, 100002, 50))
    tables = ["raw_y", "corrected", "cumulative_corrected",
              "F", "CR", "CS", "ED"]
    index = tables.index(table_name)
    for run in range(1, 26):
        print(run)
        matrix = np.load(f"data/atom_array/{index}_{run}.npy")
        if table_name == "raw_y":
            min_value = matrix[:, 0, :]
            for i in range(100002):
                min_value = np.minimum(min_value, matrix[:, i, :])
                matrix[:, i, :] = min_value
        result += matrix / 25
    return result


if __name__ == "__main__":
    # table_name = "raw_y"
    # table_name = "corrected"
    # table_name = "cumulative_corrected"
    # table_name = "F"
    # table_name = "CR"
    # table_name = "CS"
    table_name = "ED"
    conn = sqlite3.connect("data/atom_data.db")
    cursor = conn.cursor()
    cursor.execute(f"select name from sqlite_master where type='table' and \
        name='{table_name}'")
    if cursor.fetchone():
        cursor.execute(f"drop table {table_name}")
    table_values = read_atom_array(table_name)
    df = array_to_dataframe(table_values, table_name)
    df.to_sql(table_name, conn, index=False)
