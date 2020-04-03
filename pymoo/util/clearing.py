import numpy as np


def func_select_by_objective(pop):
    F = pop.get("F")
    return F[:, 0].argmin()


def select_by_clearing(pop, D, n_select, func_select, eps=0.05):
    clearing = EpsilonClearing(D, eps)

    while len(clearing.selected()) < n_select:
        remaining = clearing.remaining()

        if len(remaining) == 0:
            clearing.reset()

        best = remaining[func_select(pop[remaining])]
        clearing.select(best)

    S = clearing.selected()
    return S


class EpsilonClearing:

    def __init__(self, D,
                 epsilon) -> None:
        super().__init__()
        self.D = D
        self.n = len(D)
        self.epsilon = epsilon

        self.S = []
        self.C = np.full(self.n, False)

    def remaining(self):
        return np.where(~self.C)[0]

    def has_remaining(self):
        return self.C.sum() != self.n

    def cleared(self):
        return self.C

    def selected(self):
        return self.S

    def reset(self):
        self.C = np.full(self.n, False)
        self.C[self.S] = True

    def select(self, k):
        self.S.append(k)
        self.C[k] = True

        less_than_epsilon = self.D[k] < self.epsilon
        self.C[less_than_epsilon] = True