import os
import ioh
import time
import numpy as np
import pandas as pd

from pyDOE import lhs
from pflacco.classical_ela_features import calculate_dispersion
from pflacco.classical_ela_features import calculate_ela_distribution
from pflacco.classical_ela_features import calculate_ela_level
from pflacco.classical_ela_features import calculate_ela_meta
from pflacco.classical_ela_features import calculate_information_content
from pflacco.classical_ela_features import calculate_nbc
from pflacco.classical_ela_features import calculate_pca


def calculate_features(X, y):
    keys = []
    values = []
    disp = calculate_dispersion(X, y)
    keys += list(disp.keys())[:-1]
    values += list(disp.values())[:-1]
    ela_distr = calculate_ela_distribution(X, y)
    keys += list(ela_distr.keys())[:-1]
    values += list(ela_distr.values())[:-1]
    ela_level = calculate_ela_level(X, y)
    keys += list(ela_level.keys())[:-1]
    values += list(ela_level.values())[:-1]
    ela_meta = calculate_ela_meta(X, y)
    keys += list(ela_meta.keys())[:-1]
    values += list(ela_meta.values())[:-1]
    ic = calculate_information_content(X, y)
    keys += list(ic.keys())[:-1]
    values += list(ic.values())[:-1]
    nbc = calculate_nbc(X, y)
    keys += list(nbc.keys())[:-1]
    values += list(nbc.values())[:-1]
    pca = calculate_pca(X, y)
    keys += list(pca.keys())[:-1]
    values += list(pca.values())[:-1]
    return keys, values


def ela_experiment(prob, epsilon):
    if epsilon != 0.0:
        bounds = np.loadtxt(f"data/search_region/{problem_id}_1_{epsilon}.txt")
        prob.bounds.lb = bounds[:, 0]
        prob.bounds.ub = bounds[:, 1]
    lhs_matrix = lhs(20, samples=10000)
    min_values = prob.bounds.lb
    max_values = prob.bounds.ub
    scaled_samples = np.zeros_like(lhs_matrix)
    for i in range(20):
        scaled_samples[:, i] = lhs_matrix[:, i] * \
            (max_values[i] - min_values[i]) + min_values[i]
    return calculate_features(scaled_samples, prob(scaled_samples))


if __name__ == "__main__":
    ndim = 20
    dataset_values = []
    epsilons = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.5, 0.0]
    for problem_id in [1, 16, 23]:
        for epsilon in epsilons:
            print(f"Problem {problem_id}, epsilon {epsilon}")
            prob = ioh.get_problem(problem_id, 1, ndim, ioh.ProblemClass.BBOB)
            keys, values = ela_experiment(prob, epsilon)
            dataset_values += [[problem_id, epsilon] + values]
    dataset_keys = ["problem_id", "epsilon"] + keys
    dataset = pd.DataFrame(dataset_values, columns=dataset_keys)
    dataset.to_csv("data/ela_features.csv", index=False)
