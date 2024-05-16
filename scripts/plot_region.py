import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    epsilons = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.5]
    plt.style.use("seaborn-v0_8-darkgrid")
    for problem_id in [1, 16, 23]:
        bounds = []
        fig, axs = plt.subplots(5, 4, figsize=(15, 13))
        axs = axs.ravel()
        for epsilon in epsilons:
            data = np.loadtxt(
                f"data/search_region/{problem_id}_1_{epsilon}.txt")
            bounds += [data.tolist()]
        bounds = np.array(bounds)
        for i in range(20):
            min_values = bounds[:, i, 0]
            max_values = bounds[:, i, 1]
            lengths = [max_val - min_val for max_val,
                        min_val in zip(max_values, min_values)]
            starts = min_values
            labels = [str(epsilon) for epsilon in epsilons]
            axs[i].barh(labels, lengths, left=starts)
            axs[i].set_title(f"dimension {i+1}")
        fig.suptitle(f"Search Region of Problem {problem_id}")
        plt.tight_layout()
        plt.savefig(f"results/region/{problem_id}.png")
        plt.cla()
