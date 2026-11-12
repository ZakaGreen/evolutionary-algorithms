import genetic_all as ga
import numpy as np
import random
import matplotlib.pyplot as plt
import math

def check_constraints(x):
    total = np.sum(x)
    print("Constraints:")
    print(f"  P1: sum <= 10_000_000: {total <= 10_000_000}")
    print(f"  P2: x1 + x2 <= 2_500_000: {x[0] + x[1] <= 2_500_000}")
    print(f"  P3: x4 >= x5: {x[3] >= x[4]}")
    print(f"  P4: x3 + x4 <= 0.5 * total: {x[2] + x[3] <= 0.5 * total}")
    print(f"  P5: x_i >= 0: {np.all(x >= 0)}")
    return

def revenue(x):
    coeffs = np.array([0.04, 0.07, 0.11, 0.06, 0.05])
    return np.dot(coeffs, x)

#Mŕtva pokuta
def mrtv(jedinec):
    total = np.sum(jedinec)
    if (
        (total > 10_000_000) or
        (jedinec[0] + jedinec[1] > 2_500_000) or
        (jedinec[3] < jedinec[4]) or
        (jedinec[2] + jedinec[3] > 0.5*total) or
        (np.any(jedinec < 0))
    ):
        return 1_500_000
    else:
        return 0

#Stupňová pokuta
def stup(jedinec):
    p = 0
    total = np.sum(jedinec)
    if (total > 10_000_000):
        p += 1
    if (jedinec[0] + jedinec[1] > 2_500_000):
        p += 1
    if (jedinec[3] < jedinec[4]):
        p += 1
    if (jedinec[2] + jedinec[3] > 0.5*total):
        p += 1
    if (np.any(jedinec < 0)):
        p += 1
    return 300_000 * p

#Pokuta úmerná miere porušenia obmedzení
def umer(jedinec):
    p = 0
    total = np.sum(jedinec)
    if (total > 10_000_000):
        p += (total - 10_000_000)
    if (jedinec[0] + jedinec[1] > 2_500_000):
        p += (jedinec[0] + jedinec[1] - 2_500_000)
    if (jedinec[3] < jedinec[4]):
        p += (jedinec[4] - jedinec[3])
    if (jedinec[2] + jedinec[3] > 0.5 * total):
        p += (jedinec[2] + jedinec[3] - 0.5 * total)
    if (np.any(jedinec < 0)):
        for i in jedinec:
            if (i < 0):
                p += -i
    return p

def fitness(pop):
    coeffs = np.array([0.04, 0.07, 0.11, 0.06, 0.05])
    fit = np.zeros(pop.shape[0], dtype=int)

    for ind in range(pop.shape[0]):
        revenue = np.dot(coeffs, pop[ind])
        fit[ind] = revenue

    return fit

def fitness_mrtrv(pop):
    coeffs = np.array([0.04, 0.07, 0.11, 0.06, 0.05])
    fit_mrtv = np.zeros(pop.shape[0], dtype=int)
    for ind in range(pop.shape[0]):
        revenue = np.dot(coeffs, pop[ind])
        fit_mrtv[ind] = revenue - mrtv(pop[ind])

    return fit_mrtv

def fitness_stup(pop):
    coeffs = np.array([0.04, 0.07, 0.11, 0.06, 0.05])
    fit_stup = np.zeros(pop.shape[0], dtype=int)

    for ind in range(pop.shape[0]):
        revenue = np.dot(coeffs, pop[ind])
        fit_stup[ind] = revenue - mrtv(pop[ind])

    return fit_stup

def fitness_umer(pop):
    coeffs = np.array([0.04, 0.07, 0.11, 0.06, 0.05])
    fit_umer = np.zeros(pop.shape[0], dtype=int)

    for ind in range(pop.shape[0]):
        revenue = np.dot(coeffs, pop[ind])
        fit_umer[ind] = revenue - mrtv(pop[ind])

    return fit_umer

def one_generation(pop, space, mode, amp, pokuta):
    # fit = fitness(pop)
    match pokuta:
        case 0: #Mŕtva pokuta

            fit = fitness_mrtrv(pop)
            elite, _ = ga.selbest(pop, fit, [1] * 30, reverse=True)  # elitarny vyber
            parents, _ = ga.seltourn(pop, fit, 70, reverse=True)
            # parents_2, _ = ga.selrand(pop, fit, 10) #nahodny vyber
            # parents = np.vstack([parents_1, parents_2])
            kids = parents.copy()
            ga.intmedx(kids, 0.1, mode)  # medzialne krizenie
            kids = ga.mutx(kids, 0.05, space)  # obycajna(globalna) mutacia
            kids = ga.muta(kids, 0.2, amp, space)  # aditivna(lokalna) mutacia
            pop_next = np.vstack([elite, kids])
            fit = fitness_mrtrv(pop_next)
            return pop_next, fit

        case 1: #Stupňová pokuta

            fit = fitness_stup(pop)
            elite, _ = ga.selbest(pop, fit, [1] * 30, reverse=True)  # elitarny vyber
            parents, _ = ga.seltourn(pop, fit, 70, reverse=True)
            # parents_2, _ = ga.selrand(pop, fit, 10) #nahodny vyber
            # parents = np.vstack([parents_1, parents_2])
            kids = parents.copy()
            ga.intmedx(kids, 0.1, mode)  # medzialne krizenie
            kids = ga.mutx(kids, 0.05, space)  # obycajna(globalna) mutacia
            kids = ga.muta(kids, 0.2, amp, space)  # aditivna(lokalna) mutacia
            pop_next = np.vstack([elite, kids])
            fit = fitness_stup(pop_next)
            return pop_next, fit

        case 2: #Pokuta úmerná miere porušenia obmedzení

            fit = fitness_umer(pop)
            elite, _ = ga.selbest(pop, fit, [1] * 30, reverse=True)  # elitarny vyber
            parents, _ = ga.seltourn(pop, fit, 70, reverse=True)
            # parents_2, _ = ga.selrand(pop, fit, 10) #nahodny vyber
            # parents = np.vstack([parents_1, parents_2])
            kids = parents.copy()
            ga.intmedx(kids, 0.1, mode)  # medzialne krizenie
            kids = ga.mutx(kids, 0.05, space)  # obycajna(globalna) mutacia
            kids = ga.muta(kids, 0.2, amp, space)  # aditivna(lokalna) mutacia
            pop_next = np.vstack([elite, kids])
            fit = fitness_umer(pop_next)
            return pop_next, fit

        case _:

            fit = fitness(pop)
            elite, _ = ga.selbest(pop, fit, [1] * 30, reverse=True)  # elitarny vyber
            parents, _ = ga.seltourn(pop, fit, 70, reverse=True)
            #parents_2, _ = ga.selrand(pop, fit, 10) #nahodny vyber
            #parents = np.vstack([parents_1, parents_2])
            kids = parents.copy()
            #kids = ga.crossov(parents.copy(), 2, mode) #obycajne krizenie
            ga.intmedx(kids, 0.1, mode)  # medzialne krizenie
            kids = ga.mutx(kids, 0.05, space)  # obycajna(globalna) mutacia
            kids = ga.muta(kids, 0.2, amp, space)  # aditivna(lokalna) mutacia
            pop_next = np.vstack([elite, kids])
            fit = fitness(pop_next)
            return pop_next, fit


nvar = 5

lower, upper = 0, 3_000_000
space = ga.uniform_space(nvar, lower, upper) # Generuje space s rovnakymi obmedzeniami pre vsetky geny
                                             # [[0, 0, ..., 0], [ 10000000, 10000000, ..., 10000000]]

pop_size = 100
ngen = 1000     # pocet generacii
n_runs = 5

mode = 0
#mut_rate = 0.05
amp = np.array([1000000]*5, dtype=int) # +-10 ku kazdemu genu


# ---------------------------
# VIAC SPUSTENI + GRAF
# ---------------------------

final_best_priebehy = np.empty((3, ngen))

for pokuta in range(3):
    plt.figure()

    best_best_jedinec = np.empty((n_runs, nvar), dtype=int)
    best_best_fit = np.empty(n_runs, dtype=int)
    best_best_priebeh = np.empty((n_runs, ngen))

    for run in range(n_runs):
        print(f"Pokuta: {pokuta}")
        pop = ga.genrpop(pop_size, space)
        best_fit = np.empty(ngen, dtype=int)
        best_jedinec = np.empty((ngen, nvar), dtype=int)

        for g in range(ngen):
            pop, Fit = one_generation(pop, space, mode, amp, pokuta)
            best_fit[g] = Fit.max()
            best_jedinec[g][:] = pop[Fit.argmax()]

        ind_best = best_fit.argmax()

        best_best_fit[run] = best_fit[ind_best]
        best_best_jedinec[run][:] = best_jedinec[ind_best][:]
        best_best_priebeh[run][:] = best_fit[:]

        print("Najlepsia generacia:", ind_best)
        print("Fit_best:", best_fit[ind_best])
        print("X_best (5D):")
        print(best_jedinec[ind_best][:])
        print()

        plt.plot(np.arange(1, ngen + 1), best_fit)

    ind_best_best = best_best_fit.argmax()
    print("THE BEST OF THE BEST Fit:",  best_best_fit[ind_best_best])
    print("THE BEST OF THE BEST X:", best_best_jedinec[ind_best_best][:])
    print("  Revenue:", revenue(best_best_jedinec[ind_best_best][:]))
    check_constraints(best_best_jedinec[ind_best_best][:])
    print()

    final_best_priebehy[pokuta][:] = best_best_priebeh[ind_best_best][:]

    plt.xlabel("generation")
    plt.ylabel("F(x)")
    plt.title(f"Pokuta {pokuta}")
    plt.xlim(1, ngen)
    plt.grid(True)
    plt.show()

# ---------------------------
# FINALNY POROVNAVACI GRAF
# ---------------------------
plt.figure()
plt.plot(np.arange(1, ngen + 1), final_best_priebehy[0], label="Mrtva pokuta")
plt.plot(np.arange(1, ngen + 1), final_best_priebehy[1], label="Stupnovita pokuta")
plt.plot(np.arange(1, ngen + 1), final_best_priebehy[2], label="Umerna pokuta")

plt.xlabel("generation")
plt.ylabel("F(x)")
plt.title("Finalny porovnavaci graf")
plt.xlim(1, ngen)
plt.grid(True)
plt.legend()
plt.show()