#! /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2023 Kajetan Knopp <kajetan@knopp.com.pl>
#
# Distributed under terms of the MIT license.

"""
ILP implementation.
"""



import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# tested with Gurobi v9.0.0 and Python 3.7.0

# Adding stuff
wards = pd.read_csv("../DC2Data/Ward_assignments.csv")

# Parameters
ward_selection = set(list(wards["Ward"]))

result = []

ward_data = pd.read_csv("../predictions.csv")
ward_data_range = ward_data[["Ward", ward_data.columns[1]]].rename({ward_data.columns[1]: "Values"}, axis=1)
print(ward_data_range)
all_crimes = sum(ward_data_range["Values"].values.tolist())

for ward in ward_selection:
    data = pd.read_csv("../data/full_data.csv")

    crimes_ward = float(ward_data_range[ward_data["Ward"] == ward]["Values"])
    officers = int(crimes_ward/all_crimes*200)
    budget = officers

    LSOA_in_ward = wards.loc[wards.Ward == ward, :].dropna(axis=1).values.flatten().tolist()[1:]

    data = data[data["LSOA code_x"].isin(LSOA_in_ward)]
    crimecounts = list(data.groupby("LSOA code_x").count()["Median 2011/12"]*10)

    LSOAs = {}
    for i, el in enumerate(crimecounts):
        LSOAs[i] = [1, el]


    place, cost, population = gp.multidict(LSOAs)


    # MIP  model formulation
    m = gp.Model("Police Distributions")

    build = m.addVars(len(place), vtype=GRB.INTEGER, lb=0, ub=4, name="Hours here")

    m.addConstr(build.prod(cost) <= budget, name="budget")

    m.setObjective(build.prod(population), GRB.MAXIMIZE)

    m.optimize()

    for i,el in enumerate(build):
        result.append([LSOA_in_ward[i], build[el].x])
        if build[el].x > 0:
            print("LSOA: ", LSOA_in_ward[i], "| Officers: ", build[el].x)

result = pd.DataFrame(result, columns=["LSOA", "Officers"]).groupby("LSOA").sum()
result.to_csv("../DC2Data/result_ILP.csv")
