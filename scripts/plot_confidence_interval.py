import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


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


def hash_y(x_hash, variable, k_components):
    df = pd.read_sql_query(
        f"select evals, problem_id, epsilon, {variable} from {variable} where \
            k_component='{k_components}';", conn)
    df["evals"] = df.evals.map(lambda x: x_hash[x])
    df = df[df["evals"] > 360]
    if variable == "CS":
        df[variable] = df[variable].replace(0., 1.)
    df_mean = df.groupby(["evals", "problem_id", "epsilon"])[
        variable].mean().reset_index()
    if variable == "raw_y":
        df_mean[variable] = df_mean[variable]
    elif variable == "corrected":
        df_mean[variable] = df_mean[variable]
    elif variable == "cumulative_corrected":
        df_mean[variable] = df_mean[variable] / 20006
    return df_mean


def plot(x_hash, variable):
    if not os.path.exists(f"results/{variable}/"):
        os.mkdir(f"results/{variable}/")
    df_mean = hash_y(x_hash, variable, 20)
    y_mean = df_mean.values
    # peak_x = y_mean[np.argmax(y_mean[:, 1])][0]
    # peak_y = np.max(y_mean[:, 1])
    for problem_id in [1, 16, 23]:
        for epsilon in [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]:
            df_temp = df_mean[(df_mean["problem_id"] == problem_id) & (
                df_mean["epsilon"] == epsilon)]
            # .groupby(
                    # ["evals"])[variable].mean().reset_index()
            sns.lineplot(data=df_temp, x="evals", y=variable,
                         label=f"problem: {problem_id}, epsilon: {epsilon}")
            print(f"problem: {problem_id}, epsilon: {epsilon} plotting done.")
        plt.xscale('log')
        plt.xlabel("Function Evaluations")
        if variable == "raw_y":
            # plt.ylim(10**-6, 10**2.7)
            plt.yscale('log')
            plt.ylabel("Best-so-far f(x) value")
            plt.legend(loc="lower left")
            plt.title(f"Best-so-far f(x) value when k_components is 20")
        # elif variable == "corrected":
        #     plt.ylim(-0.04, 1.04)
        #     plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        #     plt.ylabel("Probability of Generating Infeasible Solution")
        #     plt.axvline(x=peak_x, color="grey", linestyle='--')
        #     plt.axhline(y=peak_y, color="grey", linestyle='--')
        #     plt.text(peak_x, peak_y, f"({peak_x:.0f}, {peak_y:.2%})",
        #                 verticalalignment="bottom", horizontalalignment="left")
        #     plt.legend(loc="upper left")
        #     if i > 1:
        #         plt.title(
        #             f"Probability of generating infeasible solution where optima \nare close to the bound in {i} dimensions")
        #     else:
        #         plt.title(
        #             f"Probability of generating infeasible solution where optima \nare close to the bound in {i} dimension")
        # elif variable == "cumulative_corrected":
        #     plt.ylim(-0.04, 0.35)
        #     plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
        #     plt.ylabel("Proportion of Infeasible Solutions")
        #     plt.axvline(x=peak_x, color="grey", linestyle='--')
        #     plt.axhline(y=peak_y, color="grey", linestyle='--')
        #     plt.text(peak_x, peak_y, f"({peak_x:.0f}, {peak_y:.2%})",
        #                 verticalalignment="bottom", horizontalalignment="right")
        #     plt.legend(loc="upper left")
        #     if i > 1:
        #         plt.title(
        #             f"Proportion of infeasible solutions where optima \nare close to the bound in {i} dimensions")
        #     else:
        #         plt.title(
        #             f"Proportion of infeasible solutions where optima \nare close to the bound in {i} dimension")
        # elif variable == "F":
        #     plt.ylim(-0.04, 0.77)
        #     plt.legend(loc="upper left")
        #     if i > 1:
        #         plt.title(
        #             f"Change of F where optima are close to the bound in {i} dimensions")
        #     else:
        #         plt.title(
        #             f"Change of F where optima are close to the bound in {i} dimension")
        # elif variable == "CR":
        #     plt.ylim(-0.04, 1.0)
        #     plt.legend(loc="upper left")
        #     if i > 1:
        #         plt.title(
        #             f"Change of CR where optima are close to the bound in {i} dimensions")
        #     else:
        #         plt.title(
        #             f"Change of CR where optima are close to the bound in {i} dimension")
        # elif variable == "CS":
        #     # plt.ylim(-0.04, 0.9)
        #     plt.ylim(-0.04, 1.1)
        #     plt.legend(loc="upper left")
        #     if i > 1:
        #         plt.title(
        #             f"Change of CS where optima are close to the bound in {i} dimensions")
        #     else:
        #         plt.title(
        #             f"Change of CS where optima are close to the bound in {i} dimension")
        # elif variable == "ED":
        #     plt.ylim(-0.04, 1.8)
        #     plt.legend(loc="upper left")
        #     if i > 1:
        #         plt.title(
        #             f"Change of ED where optima are close to the bound in {i} dimensions")
        #     else:
        #         plt.title(
        #             f"Change of ED where optima are close to the bound in {i} dimension")
        plt.savefig(f"results/{variable}/{problem_id}_20.png")
        plt.cla()


if __name__ == "__main__":
    conn = sqlite3.connect("data/L-SHADE_mirror/atom_data.db")
    unit = 100
    budget = 20006
    x = list(set(int(10**(i/unit))
             for i in range(int(np.log10(budget)*unit)+2)))
    x.sort()
    x_hash = hash_bin(x)
    plot(x_hash, "raw_y")
    # plot(x_hash, "corrected")
    # plot(x_hash, "cumulative_corrected")
    # plot(x_hash, "F")
    # plot(x_hash, "CR")
    # plot(x_hash, "CS")
    # plot(x_hash, "ED")
