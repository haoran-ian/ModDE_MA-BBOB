import os
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if not os.path.exists("results/corrected/"):
        os.mkdir("results/corrected/")
    df = pd.read_csv("data/csv/correctd.csv")
    values = df.values
    for i in range(21):
        plt.plot(values[i])
        plt.savefig("results/corrected/{}.png".format(i))
        plt.cla()