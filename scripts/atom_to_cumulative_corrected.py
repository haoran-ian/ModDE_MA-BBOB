import pandas as pd

corrected = pd.read_csv("data/csv/correctd.csv")
corrected = corrected.values
cumulative_corrected = [[0 for _ in range(50)]
                        for _ in range(100002) for _ in range(21)]
for i in range(21):
    for j in range(100002):
        for k in range(50):
            if j > 0:
                cumulative_corrected[i][j][k] = corrected[i][j][k] + \
                    cumulative_corrected[i][j-1][k]
            else:
                cumulative_corrected[i][j][k] = corrected[i][j][k]
