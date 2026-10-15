import numpy as np
import matplotlib.pyplot as plt

import numpy as np

import time

# Question-0-0


class union_1d:

    def __init__(self, mat, PBC=False):
        site_index = np.arange(1, mat.shape[0]+1)
        site_index = site_index[mat==1]
        self.sites = site_index.copy()
        # self.parant = site_index.copy()
        self.parent = {}
        self.size = {}
        
        if PBC:
            interaction = []
            for site, site_i in enumerate(site_index):
                self.parent[site_i] = site_i
                self.size[site_i] = 1
                if site_i+1 in site_index:
                    interaction.append(np.array([site_i, site_i+1]))
                if site_i-1 in site_index:
                    interaction.append(np.array([site_i, site_i-1]))
                if site_i == 1 and mat.shape[0] in site_index:
                    interaction.append(np.array([1, mat.shape[0]]))
                

        else:
            interaction = []
            for site, site_i in enumerate(site_index):
                self.parent[site_i] = site_i
                self.size[site_i] = 1
                if site_i+1 in site_index:
                    interaction.append(np.array([site_i, site_i+1]))
                if site_i-1 in site_index:
                    interaction.append(np.array([site_i, site_i-1]))
        self.pairs = interaction

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        else:
            self.parent[v] = self.find_set(self.parent[v]) 
            return self.find_set(self.parent[v])
             

    def union_sets(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        # print(a, b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b];
    def perform_union(self):
        for i in self.pairs:
            # print(i[0], i[1])
            self.union_sets(i[0], i[1])

    def get_unique_cluster(self):
        self.unique_sets = {}
        for node, parent in self.parent.items():
            root = self.find_set(node)
            if root not in self.unique_sets.keys():
                self.unique_sets[root] = [node]
            else:
                self.unique_sets[root].append(node)
            
class union_2d:

    def __init__(self, mat):
        site_index = np.arange(1, mat.size+1)
        site_index = site_index.reshape(mat.shape)
        self.site_index = site_index.copy()
        
        site_index = site_index[mat==1]
        
        mat_width = mat.shape[1]
        mat_heigh = mat.shape[0]

        
        self.parent = {}
        self.size = {}
        

        interaction = []
        for site, site_i in enumerate(site_index):
            self.parent[site_i] = site_i
            self.size[site_i] = 1
            if site_i+1 in site_index and site_i % mat_width != 0:
                interaction.append(np.array([site_i, site_i+1]))
            if site_i-1 in site_index and site_i % mat_width != 1:
                interaction.append(np.array([site_i, site_i-1]))
            if site_i+mat_width in site_index:
                interaction.append(np.array([site_i, site_i+mat_width]))
            if site_i-mat_width in site_index:
                interaction.append(np.array([site_i, site_i-mat_width]))
        self.pairs = interaction

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        else:
            self.parent[v] = self.find_set(self.parent[v]) 
            return self.find_set(self.parent[v])
             

    def union_sets(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        # print(a, b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b];
    def perform_union(self):
        for i in self.pairs:
            self.union_sets(i[0], i[1])

    def get_unique_cluster(self):
        self.unique_sets = {}
        for node, parent in self.parent.items():
            root = self.find_set(node)
            if root not in self.unique_sets.keys():
                self.unique_sets[root] = [node]
            else:
                self.unique_sets[root].append(node)         

class union_bond_percolation:

    def __init__(self, lattice_width, lattice_height, bond_prob, rng):
        lattice_point = np.arange(1, lattice_width*lattice_height+1)
        all_bounds = []
        for site, site_i in enumerate(lattice_point):
            if site_i+1 in lattice_point and site_i % lattice_width != 0:
                all_bounds.append(np.array([site_i, site_i+1]))
            if site_i+lattice_width in lattice_point:
                all_bounds.append(np.array([site_i, site_i+lattice_width]))

        selected_bound_index = rng.choice(len(all_bounds), size=int(bond_prob*len(all_bounds)), replace = False)
        selected_bound_point = np.array([])
        selected_interaction = []
        for index, bound in enumerate(selected_bound_index):
            selected_bound_point = np.append(selected_bound_point, all_bounds[bound])
            selected_interaction.append(all_bounds[bound])
        
        selected_bound_point = np.unique(selected_bound_point)
        

        
        site_index = selected_bound_point
        mat_width = lattice_width
        mat_heigh = lattice_height

        
        self.parent = {}
        self.size = {}

        for site, site_i in enumerate(selected_bound_point):
            self.parent[site_i] = site_i
            self.size[site_i] = 1

        
        self.pairs = selected_interaction

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        else:
            self.parent[v] = self.find_set(self.parent[v]) 
            return self.find_set(self.parent[v])
             

    def union_sets(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        # print(a, b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b];
    def perform_union(self):
        for i in self.pairs:
            self.union_sets(i[0], i[1])

    def get_unique_cluster(self):
        self.unique_sets = {}
        for node, parent in self.parent.items():
            root = self.find_set(node)
            if root not in self.unique_sets.keys():
                self.unique_sets[root] = [node]
            else:
                self.unique_sets[root].append(node)         

class percolation_arbitrary_bound:

    def __init__(self, selected_interaction, lattice_number):
        
        
        selected_bound_point = np.arange(1, lattice_number+1)

        
        self.parent = {}
        self.size = {}

        for site, site_i in enumerate(selected_bound_point):
            self.parent[site_i] = site_i
            self.size[site_i] = 1

        
        self.pairs = selected_interaction

    def find_set(self, v):
        if v == self.parent[v]:
            return v
        else:
            self.parent[v] = self.find_set(self.parent[v]) 
            return self.find_set(self.parent[v])
             

    def union_sets(self, a, b):
        a = self.find_set(a)
        b = self.find_set(b)
        # print(a, b)
        if a != b:
            if self.size[a] < self.size[b]:
                a, b = b, a
            self.parent[b] = a
            self.size[a] += self.size[b];
    def perform_union(self):
        for i in self.pairs:
            self.union_sets(i[0], i[1])

    def get_unique_cluster(self):
        self.unique_sets = {}
        for node, parent in self.parent.items():
            root = self.find_set(node)
            if root not in self.unique_sets.keys():
                self.unique_sets[root] = [node]
            else:
                self.unique_sets[root].append(node)         


# Question-0-1

class Create_init:
    def __init__(self, L):

        self.lattice = np.zeros((L, L))

    def empty(self):
        self.lattice[:] = 0

    def all_full(self):
        self.lattice[:] = 1

    def checkboard(self):
        self.empty()
        l_h, l_w = self.lattice.shape
        for i in range(0, l_w, 2):
            for j in range(0, l_h, 2):
                self.lattice[j, i] = 1
        for i in range(1, l_w, 2):
            for j in range(1, l_h, 2):
                self.lattice[j, i] = 1


    def snakelike(self):
        self.empty()
        l_h, l_w = self.lattice.shape
        for j in range(0, l_h, 2):
            self.lattice[j, :] = 1
        for j in range(1, l_h, 2):
            i = int(-0.5+(-1)**(int((j+1)/2))/2)
            self.lattice[j, i] = 1

    def two_diag(self):
        self.empty()
        l_h, l_w = self.lattice.shape
        self.lattice[0:int(l_h/2), 0:int(l_w/2)] = 1
        self.lattice[int(l_h/2):, int(l_w/2):] = 1


def plotallfigure(L):
    fig, ax = plt.subplots(2, 3)
    fig.set_size_inches(11, 6)



    Num_clusternum = []
    theoretical_num = []
    function_label = []

    pattern = Create_init(L)
    pattern.empty()
    union_set_2 = union_2d(pattern.lattice)
    union_set_2.perform_union()
    union_set_2.get_unique_cluster()
    ax[0, 0].imshow(pattern.lattice, clim=(0, 1))
    ax[0, 0].set_title("All empty. Cluster number = %d" % (len(union_set_2.unique_sets)))
    Num_clusternum.append(len(union_set_2.unique_sets))
    theoretical_num.append(0)
    function_label.append("Empty")

    pattern = Create_init(L)
    pattern.all_full()
    union_set_2 = union_2d(pattern.lattice)
    union_set_2.perform_union()
    union_set_2.get_unique_cluster()
    ax[0, 1].imshow(pattern.lattice, clim=(0, 1))
    ax[0, 1].set_title("All full. Cluster number = %d" % (len(union_set_2.unique_sets)))
    Num_clusternum.append(len(union_set_2.unique_sets))
    theoretical_num.append(1)
    function_label.append("All full")

    pattern = Create_init(L)
    pattern.checkboard()
    union_set_2 = union_2d(pattern.lattice)
    union_set_2.perform_union()
    union_set_2.get_unique_cluster()

    Num_clusternum.append(len(union_set_2.unique_sets))
    site_color = np.zeros(pattern.lattice.shape)
    for keys, group in union_set_2.unique_sets.items():
        for index in group:
            site_color[union_set_2.site_index == index] = keys
    ax[0, 2].imshow(site_color)
    ax[0, 2].set_title("Checkboard. Cluster number = %d" % (len(union_set_2.unique_sets)))
    if L%2 == 1:
        theoretical_num.append((L**2+1)/2)
    else:
        theoretical_num.append((L**2)/2)
    function_label.append("Checkboard")


    pattern = Create_init(L)
    pattern.snakelike()
    union_set_2 = union_2d(pattern.lattice)
    union_set_2.perform_union()
    union_set_2.get_unique_cluster()

    site_color = np.zeros(pattern.lattice.shape)
    for keys, group in union_set_2.unique_sets.items():
        for index in group:
            site_color[union_set_2.site_index == index] = keys
    ax[1, 0].imshow(site_color)
    ax[1, 0].set_title("Snake like. Cluster number = %d" % (len(union_set_2.unique_sets)))
    Num_clusternum.append(len(union_set_2.unique_sets))
    theoretical_num.append(1)
    function_label.append("Snake like")



    pattern = Create_init(L)
    pattern.two_diag()
    union_set_2 = union_2d(pattern.lattice)
    union_set_2.perform_union()
    union_set_2.get_unique_cluster()
    site_color = np.zeros(pattern.lattice.shape)
    for keys, group in union_set_2.unique_sets.items():
        for index in group:
            site_color[union_set_2.site_index == index] = keys
    print(site_color)
    ax[1, 1].imshow(site_color)
    ax[1, 1].set_title("Two Diagonal. Cluster number = %d" % (len(union_set_2.unique_sets)))
    Num_clusternum.append(len(union_set_2.unique_sets))
    theoretical_num.append(2)
    function_label.append("Two diag")



    ax[1, 2].plot(Num_clusternum, 'ro', fillstyle = 'none',linestyle = 'None', label='Numerical')
    ax[1, 2].plot(theoretical_num, 'bs', fillstyle = 'none',linestyle = 'None', label='Theoretical')

    ax[1, 2].set_xticks(np.arange(5))

    ax[1, 2].set_xticklabels(function_label)
    ax[1, 2].legend(loc = 1)

    fig.suptitle("L=%d" %(L))

    plt.show()

def testtime(L, prob):
    test_lattice = rng.uniform(0, 1, (L, L))
    test_lattice = np.where(test_lattice<prob, 1, 0)
    start = time.time()
    union_set_2 = union_2d(test_lattice)
    union_set_2.perform_union()
    union_set_2.get_unique_cluster()
    end = time.time()
    return end-start


# seed = 42
# rng = np.random.default_rng(seed)

L = 5
plotallfigure(L)


# prob = 0.6
# Llist  = 2**np.arange(6, 11)
# timelist = []
# for L in Llist:
#     print(L)
#     timelist.append(testtime(L, prob))

# plt.plot(np.log2(Llist), np.log2(timelist), 'ro')
# plt.show()



