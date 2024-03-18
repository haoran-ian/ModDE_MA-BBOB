import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def array_to_table(array):
    records = []
    for bound_flag in range(2):
        for problem_id in range(50):
            for run in range(25):
                for eval_bin in range(200):
                    dis_max = array[bound_flag][problem_id][run][eval_bin][0]
                    dis_min = array[bound_flag][problem_id][run][eval_bin][1]
                    dis_mean = array[bound_flag][problem_id][run][eval_bin][2]
                    dis_median = array[bound_flag][problem_id][run][eval_bin][3]
                    if dis_max == dis_min == dis_mean == dis_median == 0:
                        break
                    records += [[bound_flag, problem_id, run, eval_bin*500,
                                 dis_max, dis_min, dis_mean, dis_median]]
    df = pd.DataFrame(data=records, columns=["bound_flag", "problem_id", "run",
                                             "evals", "max", "min", "mean",
                                             "median"])
    return df


if __name__ == "__main__":
    if not os.path.exists("results/post_exp/"):
        os.mkdir("results/post_exp/")
    bounds = int(sys.argv[1])
    data = np.load(f"data/post_exp/{bounds}.npy")
    df = array_to_table(array=data)
    df_0 = df[df["bound_flag"] == 0]
    df_1 = df[df["bound_flag"] == 1]
    if not df_0.empty:
        sns.lineplot(df_0, x="evals", y="max", label="max")
        sns.lineplot(df_0, x="evals", y="min", label="min")
        sns.lineplot(df_0, x="evals", y="mean", label="mean")
        sns.lineplot(df_0, x="evals", y="median", label="median")
        plt.ylim(-0.2, 5.2)
        plt.ylabel("distance to nearest lower/upper bound")
        title = f"Random dimesion that the optima are close to\n where optima are close to the bound in {bounds} dimension"
        title += "s" if bounds > 1 else ""
        plt.title(title)
        plt.savefig(f"results/post_exp/{bounds}_boundary.png")
        plt.cla()
    if not df_1.empty:
        sns.lineplot(df_1, x="evals", y="max", label="max")
        sns.lineplot(df_1, x="evals", y="min", label="min")
        sns.lineplot(df_1, x="evals", y="mean", label="mean")
        sns.lineplot(df_1, x="evals", y="median", label="median")
        plt.ylim(-0.2, 5.2)
        plt.ylabel("distance to nearest lower/upper bound")
        title = f"Random dimesion that the optima are not close to\n where optima are close to the bound in {bounds} dimension"
        title += "s" if bounds > 1 else ""
        plt.title(title)
        plt.savefig(f"results/post_exp/{bounds}_not_boundary.png")
        plt.cla()
