import os
import sqlite3
import numpy as np
import pandas as pd

if __name__ == "__main__":
    if not os.path.exists("results/cumulative_corrected/"):
        os.mkdir("results/cumulative_corrected/")
    table_name = "cumulative_corrected"
    conn = sqlite3.connect("data/atom_data.db")
    cursor = conn.cursor()
    cursor.execute(f"select name from sqlite_master where type='table' and \
        name='{table_name}'")
    if cursor.fetchone():
        cursor.execute(f"drop table {table_name}")
    corrected = np.load("data/corrected.npy")
    cumulative_corrected = np.zeros(corrected.shape)
    for j in range(1, 100002):
        cumulative_corrected[:, j, :] = \
            cumulative_corrected[:, j-1, :] + corrected[:, j, :]
    np.save(f"data/{table_name}.npy", cumulative_corrected)
