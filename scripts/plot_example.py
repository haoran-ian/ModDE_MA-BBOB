import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def average_x(bounds, restricted=True):
    array = np.loadtxt(f"data/post_exp/{bounds}.txt")
    if not restricted:
        return np.mean(array[:, 3]), np.mean(array[:, 3])
    array_positive = array[array[:, 1] > 0, 1]
    array_negtive = array[array[:, 1] < 0, 1]
    return np.mean(array_positive), np.mean(array_negtive)


def array_to_table(array, bounds):
    records = []
    positive_flag = []
    index_array = np.loadtxt(f"data/post_exp/{bounds}.txt")
    for i in range(50):
        if index_array[i][1] > 0:
            positive_flag += [1]
        else:
            positive_flag += [0]
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
                    records += [[bound_flag, problem_id,
                                 positive_flag[problem_id], run, eval_bin*500,
                                 dis_max, dis_min, dis_mean, dis_median]]
    df = pd.DataFrame(data=records, columns=["bound_flag", "problem_id",
                                             "positive_flag", "run", "evals",
                                             "max", "min", "mean", "median"])
    return df


if __name__ == "__main__":
    if not os.path.exists("results/post_plots/"):
        os.mkdir("results/post_plots/")
    if not os.path.exists("results/post_plots/restricted_positive/"):
        os.mkdir("results/post_plots/restricted_positive/")
    if not os.path.exists("results/post_plots/restricted_negtive/"):
        os.mkdir("results/post_plots/restricted_negtive/")
    if not os.path.exists("results/post_plots/unrestricted/"):
        os.mkdir("results/post_plots/unrestricted/")
    bounds = int(sys.argv[1])
    data = np.load(f"data/post_exp/{bounds}.npy")
    df = array_to_table(data, bounds)
    df_restricted_positive = df[(df["bound_flag"] == 0) & (
        df["positive_flag"] == 1)]
    df_restricted_negtive = df[(df["bound_flag"] == 0)
                               & (df["positive_flag"] == 0)]
    df_unrestricted = df[df["bound_flag"] == 1]
    if not df_restricted_positive.empty:
        mean_positive, _ = average_x(bounds)
        plt.figure(figsize=(10, 8))
        sns.lineplot(df_restricted_positive, x="evals", y="max", label="max")
        sns.lineplot(df_restricted_positive, x="evals", y="min", label="min")
        sns.lineplot(df_restricted_positive, x="evals", y="mean", label="mean")
        sns.lineplot(df_restricted_positive, x="evals",
                     y="median", label="median")
        plt.axhline(mean_positive, color='gray', linestyle='--', label="optima x")
        plt.ylim(-5.4, 5.4)
        plt.yticks(range(-5, 6, 1))
        plt.ylabel(f"actual value of $x$")
        title = f"Random dimension that the optima are close to (positive bounds)\n where optima are close to the bound in {bounds} dimension"
        title += "s" if bounds > 1 else ""
        plt.title(title)
        plt.legend()
        plt.savefig(
            f"results/post_plots/restricted_positive/{bounds}_restricted_positive.png")
        plt.cla()
    if not df_restricted_negtive.empty:
        _, mean_negtive = average_x(bounds)
        plt.figure(figsize=(10, 8))
        sns.lineplot(df_restricted_negtive, x="evals", y="max", label="max")
        sns.lineplot(df_restricted_negtive, x="evals", y="min", label="min")
        sns.lineplot(df_restricted_negtive, x="evals", y="mean", label="mean")
        sns.lineplot(df_restricted_negtive, x="evals",
                     y="median", label="median")
        plt.axhline(mean_negtive, color='gray', linestyle='--', label="optima x")
        plt.ylim(-5.4, 5.4)
        plt.yticks(range(-5, 6, 1))
        plt.ylabel(f"actual value of $x$")
        title = f"Random dimension that the optima are close to (negtive bounds)\n where optima are close to the bound in {bounds} dimension"
        title += "s" if bounds > 1 else ""
        plt.title(title)
        plt.legend()
        plt.savefig(
            f"results/post_plots/restricted_negtive/{bounds}_restricted_negtive.png")
        plt.cla()
    if not df_unrestricted.empty:
        x_mean, _ = average_x(bounds, restricted=False)
        plt.figure(figsize=(10, 8))
        sns.lineplot(df_unrestricted, x="evals", y="max", label="max")
        sns.lineplot(df_unrestricted, x="evals", y="min", label="min")
        sns.lineplot(df_unrestricted, x="evals", y="mean", label="mean")
        sns.lineplot(df_unrestricted, x="evals", y="median", label="median")
        plt.axhline(x_mean, color='gray', linestyle='--', label="optima x")
        plt.ylim(-5.4, 5.4)
        plt.yticks(range(-5, 6, 1))
        plt.ylabel(f"actual value of $x$")
        title = f"Random dimension that the optima are not close to\n where optima are close to the bound in {bounds} dimension"
        title += "s" if bounds > 1 else ""
        plt.title(title)
        plt.legend()
        plt.savefig(
            f"results/post_plots/unrestricted/{bounds}_unrestricted.png")
        plt.cla()
