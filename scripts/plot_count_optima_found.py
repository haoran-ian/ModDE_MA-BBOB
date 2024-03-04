import os
import json
import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def create_table():
    records = []
    keys = ["boundaries", "problem_id", "run", "best_y"]
    folders = os.listdir("logger/")
    for folder in folders:
        weights, xopt = int(folder.split("_")[-2]), int(folder.split("_")[-1])
        bounds = int((xopt-weights)/50)
        files = os.listdir("logger/{}".format(folder))
        for f in files:
            if f[-4:] == "json":
                json_file = "logger/{}/{}".format(folder, f)
        json_read = open(json_file, 'r')
        info = json.load(json_read)
        runs = info["scenarios"][0]["runs"]
        for i in range(25):
            records += [[bounds, weights, i, runs[i]["best"]["y"]]]
        json_read.close()
    return pd.DataFrame(records, columns=keys)


if __name__ == "__main__":
    table_name = "best_y"
    conn = sqlite3.connect("data/atom_data.db")
    cursor = conn.cursor()
    cursor.execute(f"select name from sqlite_master where type='table' and \
        name='{table_name}'")
    if not cursor.fetchone():
        df = create_table()
        df.to_sql(table_name, conn, index=False)
    df = pd.read_sql_query(
        "select boundaries, problem_id, run, best_y from best_y;", conn)
    df["optima found"] = df.apply(
        lambda x: "true" if x.best_y < 10**-8 else "false", axis=1)
    print(df)
    sns.countplot(df, x="boundaries", hue="optima found", orient="x")
    plt.xlabel("the number of boundaries that optimal solutions are close to")
    plt.title(
        "The count of whether the optimal solutions are found through all runs")
    plt.savefig("results/best_y.png")
