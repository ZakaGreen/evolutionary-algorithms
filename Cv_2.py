import genetic_all as ga
import math
import numpy as np
import random
import matplotlib.pyplot as plt

def one_generation(pop, space, nsel, pts, mode, mut_rate, amp):
    fit = ga.testfn3c(pop)

    elite, _ = ga.selbest(pop, fit, [1,1,1,1], reverse=False) #elitarny vyber
    parents_1, _ = ga.seltourn(pop, fit, 56, reverse=False) #tournarny vyber
    #parents_2, _ = ga.selrand(pop, fit, 10) #nahodny vyber
    #parents = np.vstack([parents_1, parents_2])

    #kids = ga.crossov(parents.copy(), pts, mode) #obycajne krizenie
    kids = parents_1.copy()
    ga.intmedx(kids, 0.05, mode) #medzialne krizenie
    kids = ga.mutx(kids, mut_rate, space) #obycajna(globalna) mutacia
    kids = ga.muta(kids, mut_rate, amp, space) # aditivna(lokalna) mutacia

    pop_next = np.vstack([elite, kids])
    return pop_next, fit

nvar = 10
lower, upper = -1000, 1000
space = ga.uniform_space(nvar, lower, upper) # Generuje space s rovnakymi obmedzeniami pre vsetky geny
                                             # [[-1000, -1000, ..., -1000], [ 1000,  1000, ...,  1000]]

pop_size = 60
ngen = 500      # pocet generacii
n_runs = 3

nsel = 60        #  = pop_size, pocet jedincov berieme dalej po fitness
pts = 5          # pocet genov, ktore vykrizujeme
mode = 0
mut_rate = 0.05
amp = np.array([10]*10) # +-10 ku kazdemu genu

# ---------------------------
# VIAC SPUSTENI + GRAF
# ---------------------------
plt.figure()

for run in range(n_runs):
    pop = ga.genrpop(pop_size, space)
    best_fit = np.empty(ngen)
    best_jedinec = np.empty((ngen, nvar))

    for g in range(ngen):
        pop, Fit = one_generation(pop, space, nsel, pts, mode, mut_rate, amp)
        best_fit[g] = Fit.min()
        best_jedinec[g][:] = pop[Fit.argmin()]


    ind_best = best_fit.argmin()
    print("Najlepsia generacia:", ind_best)
    print("Fit_best:", best_fit[ind_best])
    print("X_best (10D):")
    print(best_jedinec[ind_best][:])
    print()

    plt.plot(np.arange(1, ngen + 1), best_fit)

plt.xlabel("generation")
plt.ylabel("F(x)")
plt.xlim(1, ngen)
plt.grid(True)
plt.show()

