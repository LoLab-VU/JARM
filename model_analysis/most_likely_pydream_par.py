import numpy as np

chain0 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_0_100000.npy')
chain1 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_1_100000.npy')
chain2 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_2_100000.npy')
chain3 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_3_100000.npy')
chain4 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_4_100000.npy')
# chain5 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_5_300000.npy')
# chain6 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_6_300000.npy')
# chain7 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_7_300000.npy')
# chain8 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_8_300000.npy')
# chain9 = np.load('pydream_results/jnk3_dreamzs_5chain_sampled_params_chain_9_300000.npy')

total_iterations = chain0.shape[0]
burnin = int(total_iterations / 2)
samples = np.concatenate((chain0[burnin:, :], chain1[burnin:, :], chain2[burnin:, :],
                          chain3[burnin:, :], chain4[burnin:, :]))

u, indices, counts = np.unique(samples, return_index=True, return_counts=True, axis=0)

max_idx = np.argmax(counts)

np.save('most_likely_par_100000.npy', u[max_idx])
