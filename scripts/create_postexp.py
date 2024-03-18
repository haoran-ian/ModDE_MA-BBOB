import os
import sys
import numpy as np
import pandas as pd


def min_distance(x):
    return min(abs(x - (-5.)), abs(x - 5.))


def post_exp(df, index_a, index_b, problem_id, run, output_file):
    # print(df)
    group_size = 500
    result_a = None
    result_b = None
    if index_a != None:
        df[f"x{index_a}"] = df[f"x{index_a}"].apply(min_distance)
        groups_a = df.groupby((df.index // group_size) + 1)[f"x{index_a}"]
        result_a = groups_a.agg(['max', 'min', 'mean', 'median']).values
        length = min(result_a.shape[0], 200)
        output_file[0][problem_id][run-1][:length, :] = result_a[:length, :]
    if index_b != None:
        df[f"x{index_b}"] = df[f"x{index_b}"].apply(min_distance)
        groups_b = df.groupby((df.index // group_size) + 1)[f"x{index_b}"]
        result_b = groups_b.agg(['max', 'min', 'mean', 'median']).values
        length = min(result_b.shape[0], 200)
        output_file[1][problem_id][run-1][:length, :] = result_b[:length, :]
    return output_file
    # pass


if __name__ == "__main__":
    if not os.path.exists("data/post_exp/"):
        os.mkdir("data/post_exp/")
    bounds = int(sys.argv[1])
    output_file = np.zeros((2, 50, 25, 200, 4))
    xopts = np.loadtxt("data/xopts_20.txt")
    for problem_id in range(50):
        print(f"Processing problem {problem_id}.")
        xopt_index = (bounds) * 50 + problem_id
        xopt = xopts[xopt_index]
        index_a = None
        index_b = None
        while (True):
            if bounds == 0:
                break
            index = np.random.randint(0, 20)
            if xopt[index] < -4.99 or xopt[index] > 4.99:
                index_a = index
                break
        while (True):
            if bounds == 20:
                break
            index = np.random.randint(0, 20)
            if xopt[index] > -4.99 and xopt[index] < 4.99:
                index_b = index
                break
        for run in (range(1, 26)):
            df = pd.read_csv(
                f"data/atom_runs/{problem_id}_{xopt_index}_runs_{run}.csv")
            output_file = post_exp(df, index_a, index_b,
                                   problem_id, run, output_file)
    np.save(f"data/post_exp/{bounds}.npy", output_file)
    # table_name = "best_y"
    # conn = sqlite3.connect("data/atom_data.db")
    # cursor = conn.cursor()
    # cursor.execute(f"select name from sqlite_master where type='table' and \
    #     name='{table_name}'")
    # if not cursor.fetchone():
    #     df = create_table()
    #     df.to_sql(table_name, conn, index=False)
    # df = pd.read_sql_query(
    #     "select boundaries, problem_id, run, best_y from best_y;", conn)
    # df["optima found"] = df.apply(
    #     lambda x: "true" if x.best_y < 10**-8 else "false", axis=1)
    # print(df)
    # sns.countplot(df, x="boundaries", hue="optima found", orient="x")
    # plt.xlabel("the number of boundaries that optimal solutions are close to")
    # plt.title(
    #     "The count of whether the optimal solutions are found through all runs")
    # plt.savefig("results/best_y.png")
