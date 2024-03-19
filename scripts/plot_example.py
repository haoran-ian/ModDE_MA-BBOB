import os
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def average_x(bounds, problem_id, restricted=True):
    array = np.loadtxt(f"data/post_exp/{bounds}.txt")
    if not restricted:
        return array[problem_id][3]
    return array[problem_id][1]


def get_example(array, problem_id):
    records = []
    for bound_flag in range(2):
        for run in range(25):
            for eval_bin in range(200):
                dis_max = array[bound_flag][problem_id][run][eval_bin][0]
                dis_min = array[bound_flag][problem_id][run][eval_bin][1]
                dis_mean = array[bound_flag][problem_id][run][eval_bin][2]
                dis_median = array[bound_flag][problem_id][run][eval_bin][3]
                if dis_max == dis_min == dis_mean == dis_median == 0:
                    break
                records += [[bound_flag, problem_id, run, eval_bin *
                             500, dis_max, dis_min, dis_mean, dis_median]]
    df = pd.DataFrame(data=records, columns=["bound_flag", "problem_id", "run",
                                             "evals", "max", "min", "mean",
                                             "median"])
    return df


if __name__ == "__main__":
    if not os.path.exists("results/post_plots/"):
        os.mkdir("results/post_plots/")
    if not os.path.exists("results/post_plots/examples/"):
        os.mkdir("results/post_plots/examples/")
    bounds = int(sys.argv[1])
    if not os.path.exists(f"results/post_plots/examples/{bounds}/"):
        os.mkdir(f"results/post_plots/examples/{bounds}/")
    problem_id = np.random.randint(50)
    data = np.load(f"data/post_exp/{bounds}.npy")
    df = get_example(data, problem_id)
    df_restricted = df[df["bound_flag"] == 0]
    df_unrestricted = df[df["bound_flag"] == 1]
    if not df_restricted.empty:
        opt_x = average_x(bounds, problem_id)
        for run in range(25):
            df_plot = df_restricted[df_restricted["run"] == run]
            plt.figure(figsize=(10, 8))
            sns.lineplot(df_plot, x="evals", y="max", label="max")
            sns.lineplot(df_plot, x="evals", y="min", label="min")
            sns.lineplot(df_plot, x="evals", y="mean", label="mean")
            sns.lineplot(df_plot, x="evals", y="median", label="median")
            plt.axhline(opt_x, color='gray', linestyle='--', label="optima x")
            plt.ylim(-5.4, 5.4)
            plt.yticks(range(-5, 6, 1))
            plt.ylabel(f"actual value of $x$")
            title = f"Change of solutions in one restricted dimension during one run when restricted dimensions are {bounds}"
            plt.title(title)
            plt.legend()
            plt.savefig(
                f"results/post_plots/examples/{bounds}/restricted_{run}.png")
            plt.cla()
            plt.close()
    if not df_unrestricted.empty:
        opt_x = average_x(bounds, problem_id, restricted=False)
        for run in range(25):
            df_plot = df_unrestricted[df_unrestricted["run"] == run]
            plt.figure(figsize=(10, 8))
            sns.lineplot(df_plot, x="evals", y="max", label="max")
            sns.lineplot(df_plot, x="evals", y="min", label="min")
            sns.lineplot(df_plot, x="evals", y="mean", label="mean")
            sns.lineplot(df_plot, x="evals", y="median", label="median")
            plt.axhline(opt_x, color='gray', linestyle='--', label="optima x")
            plt.ylim(-5.4, 5.4)
            plt.yticks(range(-5, 6, 1))
            plt.ylabel(f"actual value of $x$")
            title = f"Change of solutions in one unrestricted dimension during one run when restricted dimensions are {bounds}"
            plt.title(title)
            plt.legend()
            plt.savefig(
                f"results/post_plots/examples/{bounds}/unrestricted_{run}.png")
            plt.cla()
            plt.close()
