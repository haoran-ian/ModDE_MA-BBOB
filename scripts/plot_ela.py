import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

from sklearn.preprocessing import MinMaxScaler


def plot(data, label):
    row_maxs = np.max(data, axis=1, keepdims=True)
    row_mins = np.min(data, axis=1, keepdims=True)
    data = (data - row_mins) / (row_maxs - row_mins)
    df = pd.DataFrame(data, columns=epsilons, index=problem_ids)
    sns.heatmap(df, square=True, cmap="viridis",
                annot=True, fmt=".2f", cbar=False)
    plt.title(
        f"{label} of ELA features between old and new domain. \nThe values of each row are normalized.")
    plt.tight_layout()
    plt.savefig(f"results/{label}.png")
    plt.close()
    print(df)


if __name__ == "__main__":
    problem_ids = [1, 16, 23]
    epsilons = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.5]
    df = pd.read_csv("data/ela_features.csv")
    cos_sim = np.zeros((3, 7))
    euc_dis = np.zeros((3, 7))
    for i in range(len(problem_ids)):
        a = df[(df["problem_id"] == problem_ids[i]) &
               (df["epsilon"] == 0.0)].values[0][2:]
        for j in range(len(epsilons)):
            b = df[(df["problem_id"] == problem_ids[i])
                   & (df["epsilon"] == epsilons[j])].values[0][2:]
            cosine_similarity = np.dot(
                a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            euclidean_distance = np.linalg.norm(a - b)
            cos_sim[i][j] = cosine_similarity
            euc_dis[i][j] = euclidean_distance
    plt.style.use("seaborn-v0_8-darkgrid")
    plot(cos_sim, "cosine_similarity")
    plot(euc_dis, "euclidean_distance")
