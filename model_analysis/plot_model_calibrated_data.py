# Importing libraries
from jnk3_no_ask1 import model
import numpy as np
import matplotlib.pyplot as plt
from pysb.simulator import ScipyOdeSimulator
import pandas as pd
from equilibration_function import pre_equilibration
import matplotlib
plt.rc('axes', labelsize=18)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=16)    # fontsize of the tick labels
plt.rc('ytick', labelsize=16)    # fontsize of the tick labels

# Loading fitted parameters
param_values = np.array([p.value for p in model.parameters])
# idx_pars_calibrate = [1, 5, 9, 11, 15, 17, 23, 25, 27, 31, 35, 36, 37, 38, 39, 41, 43] #pydream
# idx_pars_calibrate = [5, 9, 11, 15, 17, 23, 25, 27, 31, 35, 36, 37, 38, 39, 41, 43] #pydream2
idx_pars_calibrate = [1, 5, 9, 11, 15, 17, 19, 23, 25, 27, 31, 35, 36, 37, 38, 39, 41, 43] #pydream3
rates_of_interest_mask = [i in idx_pars_calibrate for i, par in enumerate(model.parameters)]

fitted_pars = np.load('most_likely_par_100000_3.npy')
# param_values[rates_of_interest_mask] = 10 ** fitted_pars

# exp_data = pd.read_csv('../../data/exp_data_arrestin_normalization_1h_138max.csv')
exp_data = pd.read_csv('../data/exp_data_3min.csv')

ignore = 0

# Index of Initial conditions of Arrestin
arrestin_idx = [44]
jnk3_initial_value = 0.6  # total jnk3
jnk3_initial_idxs = [47, 48, 49]
kcat_idx = [36, 37]

tspan = np.linspace(0, exp_data['Time (secs)'].values[-(ignore+1)], 121)
ignore = -len(exp_data['Time (secs)'].values)
t_exp_mask = [idx in exp_data['Time (secs)'].values[:] for idx in tspan]
solver = ScipyOdeSimulator(model, tspan=tspan)


def display_sim_data(position):
    Y = np.copy(position)
    param_values[rates_of_interest_mask] = 10 ** Y

    pars1 = np.copy(param_values)
    pars2 = np.copy(param_values)

    # Pre-equilibration
    time_eq = np.linspace(0, 100, 100)
    pars_eq1 = np.copy(param_values)
    pars_eq2 = np.copy(param_values)

    pars_eq2[arrestin_idx] = 0
    pars_eq2[jnk3_initial_idxs] = [0.5958, 0, 0.0042]

    all_pars = np.stack((pars_eq1, pars_eq2))
    all_pars[:, kcat_idx] = 0  # Setting catalytic reactions to zero for pre-equilibration
    eq_conc = pre_equilibration(model, time_eq, all_pars)[1]

    # Simulating models with initials from pre-equilibration and parameters for condition with/without arrestin
    pars2[arrestin_idx] = 0
    pars2[jnk3_initial_idxs] = [0.5958, 0, 0.0042]
    sim = solver.run(param_values=[pars1, pars2], initials=eq_conc).all

    colors = ['#000000', '#E69F00', '#CC79A7', '#009E73', '#0072B2', '#D55E00']
    marker_a = 'v'
    marker_na = 'o'

    plt.plot(tspan, sim[0]['pTyr_jnk3'] / jnk3_initial_value, color=colors[0])
    plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pTyr_arrestin_avg'].values[:-ignore],
                 exp_data['pTyr_arrestin_std'].values[:-ignore],
                 linestyle='None', marker=marker_a, capsize=5, color=colors[0], label='p(Tyr)JNK3 exp')
    plt.plot(tspan, sim[0]['pThr_jnk3'] / jnk3_initial_value, color=colors[1])
    plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pThr_arrestin_avg'].values[:-ignore],
                 exp_data['pThr_arrestin_std'].values[:-ignore],
                 linestyle='None', marker=marker_a, capsize=5, color=colors[1], label='p(Thr)JNK3 exp')
    plt.plot(tspan, sim[0]['all_jnk3'] / jnk3_initial_value, color=colors[2])
    plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['ppjnk3_arrestin_avg'].values[:-ignore],
                 exp_data['ppjnk3_arrestin_std'].values[:-ignore],
                 linestyle='None', marker=marker_a, capsize=5, color=colors[2], label='ppJNK3 exp')

    plt.plot(tspan, sim[1]['pTyr_jnk3'] / jnk3_initial_value, color=colors[3])
    plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pTyr_noarrestin_avg'].values[:-ignore],
                 exp_data['pTyr_noarrestin_std'].values[:-ignore],
                 linestyle='None', marker=marker_na, capsize=5, color=colors[3], label='p(Tyr)JNK3 -Arr exp')
    plt.plot(tspan, sim[1]['pThr_jnk3'] / jnk3_initial_value, color=colors[4])
    plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pThr_noarrestin_avg'].values[:-ignore],
                 exp_data['pThr_noarrestin_std'].values[:-ignore],
                 linestyle='None', marker=marker_na, capsize=5, color=colors[4], label='p(Thr)JNK3 -Arr exp')
    plt.plot(tspan, sim[1]['all_jnk3'] / jnk3_initial_value, color=colors[5])
    plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['ppjnk3_noarrestin_avg'].values[:-ignore],
                 exp_data['ppjnk3_noarrestin_std'].values[:-ignore],
                 linestyle='None', marker=marker_na, capsize=5, color=colors[5], label='ppJNK3 -Arr exp')

    plt.xlabel('Time (s)')
    plt.ylabel('Conc (microM)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('calibrated_pydream_3.pdf', format='pdf', bbox_inches='tight')
    plt.show()


def display_data(data):
    linestyle = 'solid'
    marker_a = 'v'
    marker_na = 'o'
    markersize = 8
    colors = ['#000000', '#E69F00', '#CC79A7', '#009E73', '#0072B2', '#D55E00']
    loc = 4
    if data not in ['arrestin', 'no_arrestin', 'both']:
        raise ValueError('data value not accepted')

    if data == 'arrestin' or data == 'both':
        plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pTyr_arrestin_avg'].values[:-ignore],
                     exp_data['pTyr_arrestin_std'].values[:-ignore],
                     linestyle=linestyle, marker=marker_a, markersize=markersize,
                     capsize=5, color=colors[0], label='p(Tyr)JNK3 exp')

        plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pThr_arrestin_avg'].values[:-ignore],
                     exp_data['pThr_arrestin_std'].values[:-ignore],
                     linestyle=linestyle, marker=marker_a, markersize=markersize,
                     capsize=5, color=colors[1], label='p(Thr)JNK3 exp')

        plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['ppjnk3_arrestin_avg'].values[:-ignore],
                     exp_data['ppjnk3_arrestin_std'].values[:-ignore],
                     linestyle=linestyle, marker=marker_a, markersize=markersize,
                     capsize=5, color=colors[2], label='ppJNK3 exp')

    if data == 'no_arrestin' or data == 'both':
        plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pTyr_noarrestin_avg'].values[:-ignore],
                     exp_data['pTyr_noarrestin_std'].values[:-ignore],
                     linestyle=linestyle, marker=marker_na, markersize=markersize,
                     capsize=5, color=colors[3], label='p(Tyr)JNK3 -Arr exp')

        plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['pThr_noarrestin_avg'].values[:-ignore],
                     exp_data['pThr_noarrestin_std'].values[:-ignore],
                     linestyle=linestyle, marker=marker_na, markersize=markersize,
                     capsize=5, color=colors[4], label='p(Thr)JNK3 -Arr exp')

        plt.errorbar(exp_data['Time (secs)'].values[:-ignore], exp_data['ppjnk3_noarrestin_avg'].values[:-ignore],
                     exp_data['ppjnk3_noarrestin_std'].values[:-ignore],
                     linestyle=linestyle, marker=marker_na, markersize=markersize,
                     capsize=5, color=colors[5], label='ppJNK3 -Arr exp')

    plt.xlabel('Time (s)')
    plt.ylabel('Conc (microM)')
    plt.legend(loc=loc)
    plt.tight_layout()
    plt.savefig('jnk3_noASK1_pydream_data_{0}.pdf'.format(data), format='pdf')
    plt.show()


display_sim_data(fitted_pars)
# display_data(data='both')