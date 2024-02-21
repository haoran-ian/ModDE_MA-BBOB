import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def hash_bin(x):
    result = [None for _ in range(100002)]
    for e in x:
        result[e] = e
    marker = 100000
    for i in range(100002):
        if result[100001-i] == None:
            result[100001-i] = marker
        else:
            marker = result[100001-i]
    return result


if __name__ == "__main__":
    if not os.path.exists("results/corrected/"):
        os.mkdir("results/corrected/")
    conn = sqlite3.connect("data/atom_data.db")
    unit = 100
    x = list(set(int(10**(i/unit)) for i in range(5*unit+1)))
    x.sort()
    x_hash = hash_bin(x)
    for i in range(21):
        print(i)
        df = pd.read_sql_query("select evals, problem_id, corrected from \
            corrected where boundaries='{}';".format(i), conn)
        df["evals"] = df.evals.map(lambda x: x_hash[x])
        df_mean = df.groupby(['evals', 'problem_id'])[
            'corrected'].mean().reset_index()
        sns.lineplot(data=df_mean, x="evals", y="corrected")
        plt.title("corrected $x$ when proximate boundaries are {}".format(i))
        plt.savefig("results/corrected/{}.png".format(i))
        plt.cla()
