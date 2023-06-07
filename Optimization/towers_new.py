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
ward = "Barnet"
officers = 10
budget = officers * 2

# Adding stuff
data = pd.read_csv("../data/full_data.csv")

crimecounts = list(data.groupby("LSOA code_x").count()["Median 2011/12"]*10)
LSOAs = {}
for i, el in enumerate(crimecounts):
    LSOAs[i] = [1, el]


place, cost, population = gp.multidict(LSOAs)


# MIP  model formulation
m = gp.Model("Police Distributions")

build = m.addVars(len(place), vtype=GRB.INTEGER, lb=0, ub=2, name="Hours here")

m.addConstr(build.prod(cost) <= budget, name="budget")

m.setObjective(build.prod(population), GRB.MAXIMIZE)

m.optimize()

for el in build:
    if build[el].x > 0:
        print("LSOA: ", el, "| Hours: ", build[el].x)
