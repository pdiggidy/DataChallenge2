#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2023 Kajetan Knopp <kajetan@knopp.com.pl>
#
# Distributed under terms of the MIT license.

"""
Cell towers implementation.
"""



import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# tested with Gurobi v9.0.0 and Python 3.7.0

# Parameters
budget = 250

# Adding stuff
data = pd.read_csv("../data/full_data.csv")

crimecounts = list(data.groupby("LSOA code_x").count()["Median 2011/12"]*10)
LSOAs = {}
cov = {}
for i, el in enumerate(crimecounts):
    LSOAs[i] = el
    cov[i] = [{i}, 1, el]

regions, population = gp.multidict(LSOAs)

sites, coverage, cost, population = gp.multidict(cov)


# MIP  model formulation
m = gp.Model("cell_tower")

build = m.addVars(len(regions), vtype=GRB.INTEGER, lb=1, ub=6, name="Build")
is_covered = m.addVars(len(regions), vtype=GRB.BINARY, lb=1, name="Is_covered")

m.addConstr(build.prod(cost) <= budget, name="budget")



m.setObjective(is_covered.prod(population), GRB.MAXIMIZE)

m.optimize()
