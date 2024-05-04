import os
import ioh
import time
import numpy as np
import pandas as pd

from pflacco.sampling import create_initial_sample
from pflacco.classical_ela_features import calculate_dispersion
from pflacco.classical_ela_features import calculate_ela_distribution
from pflacco.classical_ela_features import calculate_ela_level
from pflacco.classical_ela_features import calculate_ela_meta
from pflacco.classical_ela_features import calculate_information_content
from pflacco.classical_ela_features import calculate_limo
from pflacco.classical_ela_features import calculate_nbc
from pflacco.classical_ela_features import calculate_pca


def load_problems():
    problems = []
    iids = np.loadtxt("data/iids.txt").astype(np.int32)
    weights = np.loadtxt("data/weights.txt")
    xopts = np.loadtxt("data/xopts_20.txt")
    nprob = iids.shape[0]
    for xopt_index in range(xopts.shape[0]):
        problem = ioh.problem.ManyAffine(
            xopts[xopt_index],
            weights[xopt_index % nprob],
            iids[xopt_index % nprob], 20)
        problems += [problem]
    return problems


def calculate_features(X, y, target):
    keys = []
    values = []
    if target == "disp":
        disp = calculate_dispersion(X, y)
        keys += list(disp.keys())[:-1]
        values += list(disp.values())[:-1]
    elif target == "ela_distr":
        ela_distr = calculate_ela_distribution(X, y)
        keys += list(ela_distr.keys())[:-1]
        values += list(ela_distr.values())[:-1]
    elif target == "ela_level":
        ela_level = calculate_ela_level(X, y)
        keys += list(ela_level.keys())[:-1]
        values += list(ela_level.values())[:-1]
    elif target == "ela_meta":
        ela_meta = calculate_ela_meta(X, y)
        keys += list(ela_meta.keys())[:-1]
        values += list(ela_meta.values())[:-1]
    elif target == "ic":
        ic = calculate_information_content(X, y)
        keys += list(ic.keys())[:-1]
        values += list(ic.values())[:-1]
    elif target == "limo":
        limo = calculate_limo(X, y, lower_bound=[-5. for _ in range(20)],
                              upper_bound=[5. for _ in range(20)])
        keys += ["limo.avg_length_norm", "limo.length_mean", "limo.ratio_mean"]
        values += [limo[keys[-3]], limo[keys[-2]], limo[keys[-1]]]
    elif target == "nbc":
        nbc = calculate_nbc(X, y)
        keys += list(nbc.keys())[:-1]
        values += list(nbc.values())[:-1]
    elif target == "pca":
        pca = calculate_pca(X, y)
        keys += list(pca.keys())[:-1]
        values += list(pca.values())[:-1]
    return keys, values


if __name__ == "__main__":
    if not os.path.exists("data/samplingX.npy"):
        samplingX = []
        for _ in range(100):
            X = create_initial_sample(20, lower_bound=-5, upper_bound=5)
            samplingX += X.values.tolist()
        samplingX = np.array(samplingX)
        np.save("data/samplingX.npy", samplingX)
    X = np.load("data/samplingX.npy")
    X = pd.DataFrame(X)
    problems = load_problems()
    dataset_keys = []
    dataset_values = []
    for bounds in range(1, 21):
        for pid in range(50):
            start_time = time.time()
            prob = problems[bounds*50+pid]
            y = X.apply(lambda x: prob(x), axis=1)
            y_norm = (y - y.min()) / (y.max() - y.min())
            for sampling in range(100):
                set_keys = ["pid", "iteration"]
                set_values = [pid, sampling]
                for feature in ["disp", "ela_distr", "ela_level", "ela_meta",
                                "ic", "nbc", "pca"]:
                    keys, values = calculate_features(
                        X[1000*sampling:1000*sampling+1000],
                        y[1000*sampling:1000*sampling+1000], feature)
                    set_keys += keys
                    set_values += values
                if dataset_keys == []:
                    dataset_keys = set_keys
                dataset_values += [set_values]
            end_time = time.time()
            print(
                f"Processing problem {pid} (boundaries {bounds}) in {end_time-start_time}s")
        df = pd.DataFrame(dataset_values, columns=dataset_keys)
        df.to_csv(f"data/ELA_{bounds}.csv", index=False)
