import ioh
import argparse
import numpy as np
from modde import ModularDE


class LSHADE_interface():
    def __init__(self, bound_corr, r_N_init, r_arc, p, H, budget):
        # It would be useful for maintainability if you add a short desciption of the variables, or give them more informative names (e.g. memory_size instead of H)
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
        self.lshade.run()  # I'm not sure if this will work properly with the property-logging, you might want to check this, otherwise use the ask-tell version

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
    parser.add_argument('-k', '--k_components',
                        help='Determine how many dimesions of xopt are near to \
                            the boundaries', required=True)
    parser.add_argument('-b', '--bound_corr',
                        help='How to deal with the box-constraints. Choices: \
                            None, \"saturate\", \"unif_resample\", \"COTN\", \
                            \"toroidal\", \"mirror\", \"hvb\", \"expc_target\",\
                            \"expc_center\", \"exps\".', required=True)
    args = vars(parser.parse_args())
    number_of_dims_near_boundaries = int(args['near_bounds'])
    boundary_correction = args['bound_corr']

    # define the problems' dimensions, number of sets of weights and iids,
    # budget, and runs for algorithm
    ndim = 20
    budget = 1000 * ndim
    r_N_init = 18
    r_arc = 2.6
    p = 0.11
    H = 6
    runs = 10
    # generate problems
    problems = [
        ioh.get_problems()
    ]
    # # experiment
    # obj = LSHADE_interface('saturate', r_N_init, r_arc, p, H, budget)

    # info = "index_of_params_generating_problem: {}, xopt_index: {}".format(
    #     index_of_params_generating_problem, xopt_index)
    # print(info)
    # logger_params = dict(
    #     triggers=[ioh.logger.trigger.ALWAYS, ioh.logger.trigger.ON_VIOLATION],
    #     additional_properties=[],
    #     root="./",
    #     folder_name='L-SHADE_sat_{}_{}'.format(
    #         index_of_params_generating_problem, xopt_index),
    #     algorithm_name=f'L-SHADE',
    #     algorithm_info=info,
    #     store_positions=True,
    # )
    # logger = ioh.logger.Analyzer(**logger_params)
    # logger.set_experiment_attributes({'SDIS': 'Saturate'})
    # logger.watch(obj,
    #              ['corrected', 'cumulative_corrected', 'F', 'CR', 'CS', 'ED'])
    # logger.reset()

    # # makes it easier to keep track of which function is which, can also use set_instance
    # problem_id = int(str(index_of_params_generating_problem).rjust(3, '0') +
    #                  str(xopt_index).rjust(3, '0')) + 1000000
    # print("Problem ID: {}".format(problem_id))
    # problem.set_id(problem_id)
    # problem.attach_logger(logger)
    # for _ in range(runs):
    #     obj(problem)
    #     problem.reset()
