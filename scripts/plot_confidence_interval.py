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


def hash_y(x_hash, variable, boundaries):
    df = pd.read_sql_query(
        f"select evals, problem_id, {variable} from {variable} where \
            boundaries='{boundaries}';", conn)
    df["evals"] = df.evals.map(lambda x: x_hash[x])
    df_mean = df.groupby(["evals", "problem_id"])[
        variable].mean().reset_index()
    if variable == "raw_y":
        df_mean[variable] = df_mean[variable]
    elif variable == "corrected":
        df_mean[variable] = df_mean[variable] / 25
    elif variable == "cumulative_corrected":
        df_mean[variable] = df_mean[variable] / 100002
    return df_mean


def plot(x_hash, variable):
    if not os.path.exists(f"results/{variable}/"):
        os.mkdir(f"results/{variable}/")
    for i in range(21):
        print(i)
        df_mean = hash_y(x_hash, variable, i)
        y_mean = df_mean.groupby(["evals"])[
            variable].mean().reset_index().values
        peak_x = y_mean[np.argmax(y_mean[:, 1])][0]
        peak_y = np.max(y_mean[:, 1])
        sns.lineplot(data=df_mean, x="evals", y=variable, label="L-SHADE")
        plt.xscale('log')
        plt.xlabel("Function Evaluations")
        if variable == "raw_y":
            plt.yscale('log')
            plt.ylabel("Best-so-far-f(x)-value")
            plt.legend(loc="lower left")
            if i > 1:
                plt.title(
                    f"Expected target value when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Expected target value when proximate boundary is {i}")
        elif variable == "corrected":
            plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
            plt.ylabel("Probability of Generating Infeasible Solution")
            plt.axvline(x=peak_x, color="grey", linestyle='--')
            plt.axhline(y=peak_y, color="grey", linestyle='--')
            plt.text(peak_x, peak_y, f"({peak_x:.0f}, {peak_y:.2%})",
                     verticalalignment="bottom", horizontalalignment="left")
            plt.legend(loc="upper left")
            if i > 1:
                plt.title(
                    f"Probability of generating infeasible solution \n\
                        when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Probability of generating infeasible solution \n\
                        when proximate boundary is {i}")
        elif variable == "cumulative_corrected":
            plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
            plt.ylabel("Proportion of Infeasible Solutions")
            plt.axvline(x=peak_x, color="grey", linestyle='--')
            plt.axhline(y=peak_y, color="grey", linestyle='--')
            plt.text(peak_x, peak_y, f"({peak_x:.0f}, {peak_y:.2%})",
                     verticalalignment="bottom", horizontalalignment="right")
            plt.legend(loc="upper left")
            if i > 1:
                plt.title(
                    f"Proportion of infeasible solutions \n\
                        when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Proportion of infeasible solutions \n\
                        when proximate boundary is {i}")
        elif variable == "F":
            plt.legend(loc="upper left")
            if i > 1:
                plt.title(
                    f"Change of F when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Change of F when proximate boundary is {i}")
        elif variable == "CR":
            plt.legend(loc="upper left")
            if i > 1:
                plt.title(
                    f"Change of CR when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Change of CR when proximate boundary is {i}")
        elif variable == "CS":
            plt.legend(loc="upper left")
            if i > 1:
                plt.title(
                    f"Change of CS when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Change of CS when proximate boundary is {i}")
        elif variable == "ED":
            plt.legend(loc="upper left")
            if i > 1:
                plt.title(
                    f"Change of ED when proximate boundaries are {i}")
            else:
                plt.title(
                    f"Change of ED when proximate boundary is {i}")
        plt.savefig(f"results/{variable}/{i}.png")
        plt.cla()


if __name__ == "__main__":
    conn = sqlite3.connect("data/atom_data.db")
    unit = 100
    x = list(set(int(10**(i/unit)) for i in range(5*unit+1)))
    x.sort()
    x_hash = hash_bin(x)
    # plot(x_hash, "raw_y")
    # plot(x_hash, "corrected")
    # plot(x_hash, "cumulative_corrected")
    # plot(x_hash, "F")
    # plot(x_hash, "CR")
    plot(x_hash, "CS")
    plot(x_hash, "ED")
