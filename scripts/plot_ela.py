import pandas as pd
import seaborn as sns
import matplotlib.pylab as plt

from sklearn.preprocessing import MinMaxScaler

if __name__ == "__main__":
    for i in range(21):
        df = pd.read_csv(f"data/ELA_{i}.csv")
        df_mean = df.groupby("pid").mean()
        df_mean.drop("iteration", axis=1, inplace=True)
        scaler = MinMaxScaler()
        normalized_data = scaler.fit_transform(df_mean)
        normalized_df = pd.DataFrame(normalized_data, columns=df_mean.columns)
        plt.figure(figsize=(15, 13))
        sns.heatmap(normalized_df, cmap="viridis", square=True)
        plt.tight_layout()
        plt.savefig(f"results/ELA/{i}.png")