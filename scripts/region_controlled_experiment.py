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
    k_components = int(args['k_components'])
    bound_corr = args['bound_corr']

    # define the problems' dimensions, number of sets of weights and iids,
    # budget, and runs for algorithm
    ndim = 20
    budget = 1000 * ndim
    r_N_init = 18
    r_arc = 2.6
    p = 0.11
    H = 6
    runs = 10
    problem_ids = [1, 16, 23]
    # generate problems
    problems = [ioh.get_problem(problem_id, 1, ndim, ioh.ProblemClass.BBOB) for
                problem_id in problem_ids]
    # generate search region
    epsilons = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1]
    # epsilons = [0.5]
    for prob in problems:
        xopt = prob.optimum.x
        lb = [-5. for _ in range(ndim)]
        ub = [5. for _ in range(ndim)]
        abs_diff_with_neg5 = np.abs(xopt - lb)
        abs_diff_with_5 = np.abs(xopt - ub)
        min_abs_diff = np.minimum(abs_diff_with_neg5, abs_diff_with_5)
        sorted_indices = np.argsort(min_abs_diff)
        sorted_values = min_abs_diff[sorted_indices]
        sorted_xopt = xopt[sorted_indices]
        components = sorted_indices[:k_components]
        for epsilon in epsilons:
            search_region = np.array([[lb[i], ub[i]] for i in range(ndim)])
            for j in components:
                if np.abs(xopt[j] - lb[j]) <= np.abs(xopt[j] - ub[j]):
                    search_region[j][0] = xopt[j] - \
                        (ub[j] - xopt[j]) * epsilon / (1 - epsilon)
                    search_region[j][1] = ub[j]
                else:
                    search_region[j][0] = lb[j]
                    search_region[j][1] = xopt[j] + \
                        (xopt[j] - lb[j]) * epsilon / (1 - epsilon)
            problem_id = prob.meta_data.problem_id
            np.savetxt(f"data/search_region/{problem_id}_{1}_{epsilon}.txt",
                       search_region)
    # experiment
    for problem_id in problem_ids:
        for epsilon in epsilons:
            obj = LSHADE_interface(bound_corr, r_N_init, r_arc, p, H, budget)
            info = f"problem id: {problem_id}, k components: {k_components}, \
                bound_corr: {bound_corr}, epsilon: {epsilon}"
            print(info)
            problem = ioh.get_problem(
                problem_id, 1, ndim, ioh.ProblemClass.BBOB)
            bounds = np.loadtxt(
                f"data/search_region/{problem_id}_1_{epsilon}.txt")
            problem.bounds.lb = bounds.T[0]
            problem.bounds.ub = bounds.T[1]
            logger_params = dict(
                triggers=[ioh.logger.trigger.ALWAYS,
                          ioh.logger.trigger.ON_VIOLATION],
                additional_properties=[],
                root="data/L-SHADE_mirror/",
                folder_name=f"L-SHADE_mirror_{problem_id}_{epsilon}",
                algorithm_name=f"L-SHADE_mirror_{problem_id}_{epsilon}",
                algorithm_info=info,
                store_positions=True,
            )
            logger = ioh.logger.Analyzer(**logger_params)
            # logger.set_experiment_attributes({'SDIS': 'Saturate'})
            logger.watch(obj, ['corrected', 'cumulative_corrected',
                               'F', 'CR', 'CS', 'ED'])
            logger.reset()
            problem.attach_logger(logger)
            for _ in range(runs):
                obj(problem)
                problem.reset()

    # # experiment
    # for problem_id in problem_ids:
    #     obj = LSHADE_interface(bound_corr, r_N_init, r_arc, p, H, budget)
    #     info = f"problem id: {problem_id}, k components: {k_components}, \
    #         bound_corr: {bound_corr}"
    #     print(info)
    #     problem = ioh.get_problem(problem_id, 1, ndim, ioh.ProblemClass.BBOB)
    #     logger_params = dict(
    #         triggers=[ioh.logger.trigger.ALWAYS,
    #                     ioh.logger.trigger.ON_VIOLATION],
    #         additional_properties=[],
    #         root="data/L-SHADE_mirror/",
    #         folder_name=f"L-SHADE_mirror_{problem_id}_",
    #         algorithm_name=f"L-SHADE_mirror_{problem_id}_",
    #         algorithm_info=info,
    #         store_positions=True,
    #     )
    #     logger = ioh.logger.Analyzer(**logger_params)
    #     # logger.set_experiment_attributes({'SDIS': 'Saturate'})
    #     logger.watch(obj, ['corrected', 'cumulative_corrected',
    #                         'F', 'CR', 'CS', 'ED'])
    #     logger.reset()
    #     problem.attach_logger(logger)
    #     for _ in range(runs):
    #         obj(problem)
    #         problem.reset()
