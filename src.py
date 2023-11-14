import ioh
import argparse
import numpy as np
from tqdm import trange
from modde import ModularDE


class LSHADE_interface():
    def __init__(self, bound_corr):
        self.bound_corr = bound_corr
        self.lshade = None

    def __call__(self, f):
        self.lshade = ModularDE(f, base_sampler='uniform',
                                mutation_base='target',
                                mutation_reference='pbest',
                                bound_correction=self.bound_corr,
                                crossover='bin', lpsr=True,
                                lambda_=18*f.meta_data.n_variables,
                                memory_size=6, use_archive=True,
                                archive_size=int(2.6*18*f.meta_data.n_variables),
                                init_stats=True, adaptation_method_F='shade',
                                adaptation_method_CR='shade',
                                pbest_value=0.11)
        self.lshade.run()

    @property
    def F(self):
        if self.lshade is None:
            return 0
        return self.lshade.parameters.stats.curr_F

    @property
    def CR(self):
        if self.lshade is None:
            return 0
        return self.lshade.parameters.stats.curr_CR

    @property
    def CS(self):
        if self.lshade is None:
            return 0
        return self.lshade.parameters.stats.CS

    @property
    def ED(self):
        if self.lshade is None:
            return 0
        return self.lshade.parameters.stats.ED

    @property
    def cumulative_corrected(self):
        if self.lshade is None:
            return 0
        return self.lshade.parameters.stats.corr_so_far

    @property
    def corrected(self):
        if self.lshade is None:
            return 0
        return self.lshade.parameters.stats.corrected


if __name__ == "__main__":
    # argparser
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--near_bounds',
                        help='Determine how many dimesions of xopt are near to \
                            the boundaries', required=True)
    parser.add_argument('-i', '--index_params',
                        help='Indicate which set of weights and iids to be \
                            used when generating MA-BBOB', required=True)
    args = vars(parser.parse_args())
    near_bounds = int(args['near_bounds'])
    index_params = int(args['index_params'])
    # load xopt, weights, and iids for ioh.problem.ManyAffine
    xopts = np.loadtxt("data/xopts_20.txt")
    weights = np.loadtxt("data/weights.txt")
    iids = np.loadtxt("data/iids.txt").astype(np.int32)
    # define the problems' dimensions, number of sets of weights and iids,
    # budget, and runs for algorithm
    ndim = xopts.shape[1]
    nparams = weights.shape[0]
    budget = 5000 * ndim
    runs = 25
    # generate problems
    xopt_index = (near_bounds-1)*nparams+index_params
    problem = ioh.problem.ManyAffine(
        xopts[xopt_index], weights[index_params], iids[index_params], ndim)
    # experiment
    print(problem.meta_data)
    obj = LSHADE_interface('saturate')
    exp = ioh.Experiment(algorithm=obj, fids=[1], iids=[1], dims=[20], reps=25,
                         problem_class=ioh.ProblemClass.REAL,
                         njobs=12, logger_triggers=[ioh.logger.trigger.ALWAYS],
                         logged=True, folder_name=f'L-SHADE_sat',
                         algorithm_name=f'L-SHADE', store_positions=True,
                         experiment_attributes={'SDIS': 'Saturate'},
                         logged_attributes=['corrected', 'cumulative_corrected',
                                            'F', 'CR', 'CS', 'ED'],
                         merge_output=True, zip_output=True, remove_data=True)
    exp.add_custom_problem(
        problem, "MA-BBOB_{}_{}".format(near_bounds, index_params))
    exp()
