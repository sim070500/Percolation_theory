import numpy as np
import matplotlib.pyplot as plt
import question1 as toolkit


def questionA1(prob, PBC = False):
    
    L = 10**5

    test_lattice = rng.uniform(0, 1, L)
    test_lattice = np.where(test_lattice<prob, 1, 0)
    union_set = toolkit.union_1d(test_lattice, PBC)
    union_set.perform_union()
    union_set.get_unique_cluster()

    cluster_stat = {}
    for keys, group in union_set.unique_sets.items():
        group_size = len(group)
        if group_size in list(cluster_stat.keys()):
            cluster_stat[group_size] += 1
        else:
            cluster_stat[group_size] = 1
        # print(keys, group)
    all_size = np.array(list(cluster_stat.keys()))
    all_number = np.array(list(cluster_stat.values()))
    # all_number_prob = all_number/np.sum(all_number)
    all_number_prob = all_number/L
    return all_size, all_number_prob

def questionA2(prob, rng):
    L = 10**5
    test_lattice = rng.uniform(0, 1, L)
    test_lattice = np.where(test_lattice<prob, 1, 0)
    union_set = toolkit.union_1d(test_lattice)
    union_set.perform_union()
    union_set.get_unique_cluster()

    cluster_stat = {}
    for keys, group in union_set.unique_sets.items():
        group_size = len(group)
        if group_size in list(cluster_stat.keys()):
            cluster_stat[group_size] += 1
        else:
            cluster_stat[group_size] = 1
        # print(keys, group)
    all_size = np.array(list(cluster_stat.keys()))
    all_number = np.array(list(cluster_stat.values()))
    all_number_prob = all_number/L

    avgs = np.sum(all_size*all_number_prob)/np.sum(all_number_prob)
    chi = np.sum(all_size**2*all_number_prob)/np.sum(all_size*all_number_prob)

    random_point = rng.choice(union_set.sites, 10**4)
    random_size = []
    for point in random_point:
        point_set = union_set.find_set(point)
        random_size.append(len(union_set.unique_sets[point_set]))
    

    random_point_2 = rng.choice(list(union_set.unique_sets.keys()), 10**4)
    random_size_2 = []
    for point in random_point_2:
        
        random_size_2.append(len(union_set.unique_sets[point]))
    
    
    second_chi_mean = (np.mean(random_size))
    second_avg_mean = (np.mean(random_size_2))


    return avgs, chi, second_avg_mean, second_chi_mean


def questionA3(prob, L, rng):
    N = 10**5
    test_lattice = rng.uniform(0, 1, (N, L))
    test_lattice = np.where(test_lattice<prob, 1, 0)

    site_number = np.sum(test_lattice, axis = 1)
    full_occupied = np.where(site_number == L, 1, 0)
    full_occupied_number = np.sum(full_occupied)
    return full_occupied_number/N


def questionA4(a, b, L, rng):
    test_lattice = rng.uniform(0, 1, L)
    test_site = np.zeros(L)
    pi = b/(1-a+b)
    for i in range(0, L):
        if i == 0:
            test_site[i] = 1 if test_lattice[i] < pi else 0
        else:
            if test_site[i-1] == 1:
                test_site[i] = 1 if test_lattice[i] < a else 0
            if test_site[i-1] == 0:
                test_site[i] = 1 if test_lattice[i] < b else 0
    union_set = toolkit.union_1d(test_site)
    union_set.perform_union()
    union_set.get_unique_cluster()
    cluster_stat = {}
    for keys, group in union_set.unique_sets.items():
        group_size = len(group)
        if group_size in list(cluster_stat.keys()):
            cluster_stat[group_size] += 1
        else:
            cluster_stat[group_size] = 1
        # print(keys, group)
    all_size = np.array(list(cluster_stat.keys()))
    all_number = np.array(list(cluster_stat.values()))
    all_number_prob = all_number/L

    chi = np.sum(all_size**2*all_number_prob)/np.sum(all_size*all_number_prob)
    avgs = np.sum(all_size*all_number_prob)/np.sum(all_number_prob)
    return all_size, all_number_prob, chi, pi, avgs
    





seed = 42
rng = np.random.default_rng(seed)


problist = [0.5, 0.8, 0.95]
# fig, ax = plt.subplots(1, 3)
# fig.set_size_inches(11, 6)
# for i in range(0, len(problist)):
#     prob = problist[i]
#     all_size, all_number_prob = questionA1(prob)
#     ax[i].semilogy(all_size, all_number_prob, 'ro', label = 'Numerical result (Open)')
#     ax[i].semilogy(all_size, (1-prob)**2 * prob**all_size, 'bs', label = 'Theoretical result')
#     ax[i].set_title("Prob = %.2f" %(prob))    
#     # ax[i].legend(loc = 1)
#     avg = np.sum(all_size*all_number_prob)
#     print("Avg = %.2f, p = %.2f" % (avg, prob))
#     ax[i].set_title(r'$\sum_s sn_s$ ='+ '%.2f' %(avg) + '. Prob = %.2f' %(prob))

# for i in range(0, len(problist)):
#     prob = problist[i]
#     all_size, all_number_prob = questionA1(prob, PBC=True)
#     ax[i].semilogy(all_size, all_number_prob, 'gv', fillstyle = 'none', linestyle = 'None', label = 'Numerical result (Periodic)')
    
        
#     ax[i].legend(loc = 1)


"""
# ===== A2
problist  = np.linspace(0.1, 1, 10, endpoint=False)
avglist = []
chilist = []
second_chi_mean_list = []
second_avg_mean_list = []

for prob in problist :
    
    avgs, chi, second_avg_mean, second_chi_mean = questionA2(prob, rng)
    print(prob, avgs, chi, second_avg_mean, second_chi_mean)
    avglist.append(avgs)
    chilist.append(chi)
    second_chi_mean_list.append(second_chi_mean)
    second_avg_mean_list.append(second_avg_mean)
plt.plot(problist, avglist, 'ro', fillstyle = 'none', linestyle = 'None')
plt.plot(problist, chilist, 'bs', fillstyle = 'none', linestyle = 'None')
plt.plot(problist, second_avg_mean_list, 'gv', fillstyle = 'none', linestyle = 'None')
plt.plot(problist, second_chi_mean_list, 'm^', fillstyle = 'none', linestyle = 'None')
plotfun1 = 1/(1-problist)
plotfun2 = (1+problist)/(1-problist)
plt.plot(problist, plotfun1, 'k--')
plt.plot(problist, plotfun2, 'k-.')
plt.show()
"""



"""
# ===== A3
fig, ax = plt.subplots(1, 2)
fig.set_size_inches(11, 6)
Llist = [10, 30, 100, 300]
# Llist = [300]
problist = np.linspace(0.9, 1, 300, endpoint=False)

for L in Llist:
    
    span_prob = []
    for prob in problist:
        span_prob.append(questionA3(prob, L, rng))
    span_prob = np.array(span_prob)
    half_index = np.where(span_prob<0.5)[0][-1]
    half_prob = 0.5*(problist[half_index]+problist[half_index+1])
    print(L, half_prob)
    ax[0].plot(problist, span_prob)
    ax[1].loglog(L, 1-half_prob, 'ro')

Llist = np.array(Llist)
ax[1].loglog(Llist, 1-1/(2**(1/Llist)), 'k--')
# print(result_prob)
plt.show()
"""

fig, ax = plt.subplots(1, 2)
fig.set_size_inches(11, 6)

L = 10**5
a, b = 0.9, 0.1
all_size, all_number_prob, chi, pi, avgs = questionA4(a, b, L, rng)
theo_ns = (1-pi)*b*a**(all_size-1)*(1-a)
ax[0].semilogy(all_size, all_number_prob, 'ro')
ax[0].semilogy(all_size, theo_ns, 'k--')
a, b = 0.5, 0.5
all_size, all_number_prob, chi, pi, avgs = questionA4(a, b, L, rng)
theo_ns = (1-pi)*b*a**(all_size-1)*(1-a)
ax[0].semilogy(all_size, all_number_prob, 'bs')
ax[0].semilogy(all_size, theo_ns, 'k--')
a, b = 0.1, 0.9
all_size, all_number_prob, chi, pi, avgs = questionA4(a, b, L, rng)
theo_ns = (1-pi)*b*a**(all_size-1)*(1-a)
ax[0].semilogy(all_size, all_number_prob, 'gv')
ax[0].semilogy(all_size, theo_ns, 'k--')


avglist = []
chilist = []
problist  = np.linspace(0.1, 1, 10, endpoint=False)


for a in problist :
    b = np.random.uniform(0, 1)
    
    all_size, all_number_prob, chi, pi, avgs = questionA4(a, b, L, rng)

    avglist.append(avgs)
    chilist.append(chi)
ax[1].plot(problist, avglist, 'o', fillstyle = 'none', linestyle = 'None')
ax[1].plot(problist, 1/(1-problist), 'k--')
ax[1].plot(problist, chilist, 's', fillstyle = 'none', linestyle = 'None')
ax[1].plot(problist, (1+problist)/(1-problist), 'k-.')
plt.show()