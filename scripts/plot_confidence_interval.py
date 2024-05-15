import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def hash_bin(x):
    result = [None for _ in range(x[-1])]
    for e in x:
        result[e-1] = e
    marker = result[-1]
    for i in range(x[-1]):
        if result[-i-1] == None:
            result[-i-1] = marker
        else:
            marker = result[-i-1]
    return result


def hash_y(x_hash, variable, k_components):
    df = pd.read_sql_query(
        f"select evals, problem_id, epsilon, {variable} from {variable} where \
            k_component='{k_components}';", conn)
    df["evals"] = df.evals.map(lambda x: x_hash[x])
    if variable != "raw_y":
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
    title_dict = {
        "raw_y": "Best-so-far f(x)",
        "corrected": "Probability of generating infeasible solution",
        "cumulative_corrected": "Proportion of infeasible solutions",
        "F": "Change of F",
        "CR": "Change of CR",
        "CS": "Change of CS",
        "ED": "Change of ED",
    }
    if not os.path.exists(f"results/{title_dict[variable]}/"):
        os.mkdir(f"results/{title_dict[variable]}/")
    epsilons = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.5, ""]
    linestyles = ["dashed", "dashed", "solid", (0, (5, 1)),  # densely dashed
                  (0, (3, 1, 1, 1)),  # densely dashdotted
                  "dashed", "dashdot", "dotted",]
    colors = ["#440154", "#414487", "#2a788e",
              "#22a884", "#7ad151", "#fde725", "red", "blue"]
    df_mean = hash_y(x_hash, variable, 20)
    # print(df_mean)
    for problem_id in [1, 16, 23]:
        plt.figure(figsize=(10, 6))
        df_temp = df_mean[(df_mean["problem_id"] == problem_id)]
        # print(df_temp)
        y_mean = df_temp.values
        peak_x = y_mean[np.argmax(y_mean[:, 3])][0]
        peak_y = np.max(y_mean[:, 3])
        for i in range(len(epsilons)):
            epsilon = epsilons[i]
            df_temp = df_mean[(df_mean["problem_id"] == problem_id) & (
                df_mean["epsilon"] == str(epsilon))]
            sns.lineplot(data=df_temp, x="evals", y=variable,
                         linestyle=linestyles[-i-1], color=colors[i],
                         label=f"problem: {problem_id}, epsilon: {epsilon}")
            print(f"problem: {problem_id}, epsilon: {epsilon} plotting done.")
        plt.xscale('log')
        plt.xlabel("Function Evaluations")
        plt.axvspan(0, 360, color='grey', alpha=0.5,
                    label='Initialization Population')
        if variable == "raw_y":
            # plt.ylim(10**-6, 10**2.7)
            plt.yscale('log')
            plt.ylabel("Best-so-far f(x) value")
            plt.legend(loc="lower left")
        elif variable == "corrected":
            # plt.ylim(-0.04, 1.04)
            plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
            plt.ylabel("Probability of Generating Infeasible Solution")
            plt.axvline(x=peak_x, color="grey", linestyle='--')
            plt.axhline(y=peak_y, color="grey", linestyle='--')
            plt.text(peak_x, peak_y, f"({peak_x:.0f}, {peak_y:.2%})",
                     verticalalignment="bottom", horizontalalignment="left")
            plt.legend(loc="lower left")
        elif variable == "cumulative_corrected":
            # plt.ylim(-0.04, 0.35)
            plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
            plt.ylabel("Proportion of Infeasible Solutions")
            plt.axvline(x=peak_x, color="grey", linestyle='--')
            plt.axhline(y=peak_y, color="grey", linestyle='--')
            plt.text(peak_x, peak_y, f"({peak_x:.0f}, {peak_y:.2%})",
                     verticalalignment="bottom", horizontalalignment="right")
            plt.legend(loc="upper left")
        elif variable in ["F", "CR", "CS", "ED"]:
            # plt.ylim(-0.04, 0.77)
            plt.legend()
        plt.title(f"{title_dict[variable]} when k_components is 20")
        plt.tight_layout()
        plt.savefig(f"results/{title_dict[variable]}/{problem_id}_20.png")
        plt.cla()


if __name__ == "__main__":
    conn = sqlite3.connect("data/L-SHADE_mirror/atom_data.db")
    unit = 100
    budget = 20006
    x = list(set(int(10**(i/unit))
                 for i in range(int(np.log10(budget)*unit)+1))) + [budget]
    x.sort()
    x_hash = hash_bin(x)
    plot(x_hash, "raw_y")
    plot(x_hash, "corrected")
    plot(x_hash, "cumulative_corrected")
    plot(x_hash, "F")
    plot(x_hash, "CR")
    plot(x_hash, "CS")
    plot(x_hash, "ED")
