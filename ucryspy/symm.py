# Calculates the all posible combinations of the non-unit vectors of the vertices, face mid-points and edge mid-points of the constructed polyhedron
# Each of the triplet will eb considered as \vec{a}, \vec{b} and \vec{c} to evalute the direction of the lattic evectors
# i.e. \hat{a}, \hat{b} and \hat{c}

# INPUTS : all the non-unit vectors of the vertices, face mid-points and edge mid-points of the constructed polyhedron

import header
from condition_check import condition_check_func
from lattice_param import lattice_param_func

def symm_func(self, sorted_mod_positions_all):
    combin = header.combinations(header.np.array(sorted_mod_positions_all), 3)
    new_combin = []
    for comb in combin:
        new_combin.append(list(comb))

    # print('Sorting done')
    condition_check_func(self, new_combin)