from math import sqrt
import invord as inv
import genetic_all as ga
import numpy as np
import random
import matplotlib.pyplot as plt

B = [[0, 0], [17, 100], [51, 15], [70, 62], [42, 25], [32, 17], [51, 64], [39, 45],
     [68, 89], [20, 19], [12, 87], [80, 37], [35, 82], [2, 15], [38, 95], [33, 50],
     [85, 52], [97, 27], [99, 10], [37, 67], [20, 82], [49, 0], [62, 14], [7, 60], [0, 0]] #25

def fitness(pop):
    Fit = []
    for individual in pop:
        fitness = 0
        for i in range(len(individual) - 1):
            index1 = int(individual[i])
            index2 = int(individual[i + 1])
            dlzka = sqrt((B[index2][0] - B[index1][0])**2 + (B[index2][1] - B[index1][1])**2)
            fitness += dlzka
        Fit.append(fitness)
    return np.array(Fit)


def perm_crossover(old_pop, pts_low, pts_high):
    shape = old_pop.shape #(18, 25)
    pair_list = list(range(shape[0])) #[0, 1, 2, .., 17]
    random.shuffle(pair_list) #[8, 3, 14, 11, .., 9]
    new_pop = np.zeros((shape[0], shape[1]), dtype=int)

    for cyk in range(int(shape[0] / 2)):
        kid_1 = [-1] * 25
        kid_2 = [-1] * 25
        i, j = pair_list[2 * cyk], pair_list[2 * cyk + 1] #[|8, 3|, |14, 11|, ..]
        kid_1[pts_low:pts_high] = old_pop[i][pts_low:pts_high]
        kid_2[pts_low:pts_high] = old_pop[j][pts_low:pts_high]
        for k in range(1, 24):
            if old_pop[j][k] in kid_1:
                continue
            else:
                for ind in range(1, 24):
                    if kid_1[ind] == -1:
                        kid_1[ind] = old_pop[j][k]
                        break
        for k in range(1, 24):
            if old_pop[i][k] in kid_2:
                continue
            else:
                for ind in range(1, 24):
                    if kid_2[ind] == -1:
                        kid_2[ind] = old_pop[i][k]
                        break
        kid_1[0], kid_1[24] = 0, 24
        kid_2[0], kid_2[24] = 0, 24
        new_pop[2 * cyk] = kid_1
        new_pop[2 * cyk + 1] = kid_2

    return new_pop


def one_generation(pop, mut_rate):
    fit = fitness(pop)
    elite, _ = ga.selbest(pop, fit, [1] * 2, reverse=False)  # elitarny vyber
    parents, _ = ga.seltourn(pop, fit, 98, reverse=False)
    #parents_2, _ = ga.selrand(pop, fit, 10) #nahodny vyber
    #parents = np.vstack([parents_1, parents_2])

    pts_low = random.randint(1, 22)
    pts_high = random.randint(pts_low + 1, 24)

    kids = perm_crossover(parents, pts_low, pts_high)
    # kids = perm_crossover(parents, 11, 18)

    ga.swapgen(kids[:, 1:24], 0.01)
    ga.swappart(kids[:, 1:24], 0.03)
    inner = kids[:, 1:24].copy()
    inner = inv.invord(inner, mut_rate)
    kids[:, 1:24] = inner

    pop_next = np.vstack([elite, kids])
    fit = fitness(pop_next)
    return pop_next, fit


pop_size = 100
ngen = 500     # pocet generacii
n_runs = 10

mode = 0
mut_rate = 0.05

# ---------------------------
# VIAC SPUSTENI + GRAF
# ---------------------------
plt.figure()
global_best_fit = float("inf")
global_best_path = None

for run in range(n_runs):
    mid_pop = ga.genrpop_perm(pop_size, 1, 23)
    pop = np.hstack((
        np.zeros((pop_size, 1), dtype=int),
        mid_pop,
        np.full((pop_size, 1), 24, dtype=int)
    ))
    best_fit = np.empty(ngen)
    best_jedinec = np.empty((ngen, 25), dtype=int)

    for g in range(ngen):
        pop, Fit = one_generation(pop, mut_rate)
        best_fit[g] = Fit.min()
        best_jedinec[g] = pop[Fit.argmin()]

    ind_best = best_fit.argmin()

    if best_fit[ind_best] < global_best_fit:
        global_best_fit = best_fit[ind_best]
        global_best_path = best_jedinec[ind_best].copy()

    print("Najlepsia generacia:", ind_best)
    print("Fit_best:", best_fit[ind_best])
    print("Path_best:")
    print(best_jedinec[ind_best][:])
    print()

    plt.plot(np.arange(1, ngen + 1), best_fit)

plt.xlabel("Generacia")
plt.ylabel("Best fitness")
plt.xlim(1, ngen)
plt.grid(True)
plt.show()

plt.figure()

path = global_best_path

for i in range(len(path) - 1):
    p1 = B[int(path[i])]
    p2 = B[int(path[i + 1])]
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]])

for i in range(len(B) - 1):
    plt.plot(B[i][0], B[i][1], 'o')
    plt.text(B[i][0] + 1, B[i][1] + 1, str(i + 1))

plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.axis("equal")
plt.show()