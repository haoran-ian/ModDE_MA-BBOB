import ioh
import argparse
import numpy as np
from modde import ModularDE


class LSHADE_interface():
    def __init__(self, bound_corr, r_N_init, r_arc, p, H, budget):
        self.bound_corr = bound_corr
        self.r_N_init = r_N_init
        self.r_arc = r_arc
        self.p = p
        self.H = H
        self.budget = budget
        self.lshade = None

    def __call__(self, f):
        lambda_ = self.r_N_init*f.meta_data.n_variables
        archive_size = int(self.r_arc*self.r_N_init*f.meta_data.n_variables)
        self.lshade = ModularDE(f, budget=budget, base_sampler='uniform',
                                mutation_base='target',
                                mutation_reference='pbest',
                                bound_correction=self.bound_corr,
                                crossover='bin', lpsr=True,
                                lambda_=lambda_,
                                memory_size=self.H, use_archive=True,
                                archive_size=archive_size,
                                init_stats=True, adaptation_method_F='shade',
                                adaptation_method_CR='shade',
                                pbest_value=self.p)
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
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-n', '--near_bounds',
                        help='Determine how many dimesions of xopt are near to \
                            the boundaries', required=True)
    parser.add_argument('-i', '--index_params',
                        help='Indicate which set of weights and iids to be \
                            used when generating MA-BBOB', required=True)
    parser.add_argument('-b', '--bound_corr',
                        help='How to deal with the box-constraints. Choices: \
                            None, \"saturate\", \"unif_resample\", \"COTN\", \
                            \"toroidal\", \"mirror\", \"hvb\", \"expc_target\",\
                            \"expc_center\", \"exps\".', required=True)
    args = vars(parser.parse_args())
    number_of_dims_near_boundaries = int(args['near_bounds'])
    index_of_params_generating_problem = int(args['index_params'])
    boundary_correction = None if args['bound_corr'] == 'None' else args['bound_corr']
    # load xopt, weights, and iids for ioh.problem.ManyAffine
    xopts = np.loadtxt("data/xopts_20.txt")
    weights = np.loadtxt("data/weights.txt")
    iids = np.loadtxt("data/iids.txt").astype(np.int32)
    # define the problems' dimensions, number of sets of weights and iids,
    # budget, and runs for algorithm
    ndim = xopts.shape[1]
    nparams = weights.shape[0]
    budget = 5000 * ndim
    r_N_init = 18
    r_arc = 2.6
    p = 0.11
    H = 6
    runs = 25
    # generate problems
    xopt_index = (number_of_dims_near_boundaries) * nparams + \
        index_of_params_generating_problem
    problem = ioh.problem.ManyAffine(
        xopts[xopt_index],
        weights[index_of_params_generating_problem],
        iids[index_of_params_generating_problem],
        ndim)
    # problem.enforce_bounds(
    #     how=ioh.ConstraintEnforcement.SOFT,
    #     weight=1.0,
    #     exponent=1.0
    # )
    # experiment
    obj = LSHADE_interface('saturate', r_N_init, r_arc, p, H, budget)
    exp = ioh.Experiment(algorithm=obj,
                         fids=[1], iids=[1], dims=[20], reps=runs,
                         problem_class=ioh.ProblemClass.REAL,
                         njobs=12,
                         logged=True,
                         logger_triggers=[
                             ioh.logger.trigger.ALWAYS,
                             ioh.logger.trigger.ON_VIOLATION],
                         output_directory="./",
                         folder_name=f'L-SHADE_sat',
                         algorithm_name=f'L-SHADE',
                         store_positions=True,
                         experiment_attributes={'SDIS': 'Saturate'},
                         logged_attributes=[
                             'corrected', 'cumulative_corrected',
                             'F', 'CR', 'CS', 'ED'],
                         merge_output=True, zip_output=True, remove_data=True)
    exp.add_custom_problem(
        problem, "MA-BBOB_{}_{}".format(number_of_dims_near_boundaries,
                                        index_of_params_generating_problem))
    exp()
