#!/usr/bin/env python
# coding: utf-8

# This is a module to find the best count of items for transporters.
# In this notebook it will be solved a linear problem with the library PulP (https://coin-or.github.io/pulp)
#
# Description:
# The problem is like a knapsack problem.
# There is one warehouse with hardware and far away one new office without hardware.
# This office needs to be equipped. For this exists transporters like trucks.
# The job is to find the most efficient loading for the transporters with hardware for the first delivery.
# All available hardware items have a weight, a utility value and a maximum of count.
# The transporters have a maximum load capacity, which limits the weight of their driver and items.
#
# For more information look at https://github.com/sourceunit/delivery_optimization

# Requirements:
# python=3.7.6
# pandas=1.2.1
# pulp=2.4
import pandas as pd
import pulp as pl
from sys import exit



def delivery_optimization(trucks_max_loadings,
                          drivers_weights,
                          items_csv_file,
                          trucks_measuring_unit='kg',
                          drivers_measuring_unit='kg',
                          csv_delimiter=';',
                          column_mapping_required=False,
                          columns_mapping={}):
    """Main function which process a optimization by parameters.

    :param trucks_max_loadings: trucks (count and) max loading weights like [1100, 1100] (for kg)
    :type trucks_max_loadings: list
    :param drivers_weights: drivers weight like [72.4, 85.7] (for kg)
    :type drivers_weights: list
    :param items_csv_file: path to the csv file with all items with columns: name, max_count, weight, utility
    :type items_csv_file: str
    :param trucks_measuring_unit: can be 'kg' or 'gram'
    :param drivers_measuring_unit: can be 'kg' or 'gram'
    :param csv_delimiter: delimiter of the csv columns, default ';'
    :param column_mapping_required: if False, the column names in the csv must be name, max_count, weight, utility
                                    if True, the column names from csv will be changed by columns_mapping below
    :param columns_mapping: the csv column names mapped to name, max_count, weight and utility
                            like {"<required column>" : "<mapping csv column>"}
    :return:
    """

    if len(trucks_max_loadings) != len(drivers_weights):
        print("The count of trucks must be equal to the count of drivers!")
        exit(1)


    # Calculate the possible loads for the trucks

    # If necessary, converting kg to gram for the trucks max loading and drivers weight.
    if trucks_measuring_unit == 'kg':
        trucks_max_loadings_gram = [max_load*1000 for max_load in trucks_max_loadings]
    else:
        trucks_max_loadings_gram = trucks_max_loadings

    if drivers_measuring_unit == 'kg':
        drivers_weights_gram = [weight*1000 for weight in drivers_weights]
    else:
        drivers_weights_gram = drivers_weights


    # Subtract the drivers weights from trucks max loading weight.
    trucks_possible_loads = [max_load - driver_weight
                             for max_load,driver_weight
                             in zip(trucks_max_loadings_gram, drivers_weights_gram)]

    print("\nTrucks max possible items loadings: ")
    for i, max_load in enumerate(trucks_possible_loads):
        print("Truck {}: {} gram".format(i, max_load))


    # Read the data from csv file into a dataframe by pandas.
    df_items = pd.read_csv(items_csv_file, delimiter=csv_delimiter, decimal='.')

    # Map the column names if required
    if column_mapping_required and columns_mapping is not None:
        df_items.rename(columns = {origin_name : new_name for new_name, origin_name in columns_mapping.items()},
                        inplace=True)


    # Start with pulp action

    # Create a new LpProblem from pulp.
    # The LpProblem should maximize a objective function, which will be set later.
    prob = pl.LpProblem("Delivery_Problem",pl.LpMaximize)


    items_names = df_items['name'].tolist()

    # Create LpVariables from pulp for optimizing.
    # The values of this variables will be changed by the solver included in pulp to optimize the objective function.
    # Set variables to optimize as items count, lower bound = 0 and as Integer numbers
    # create optimizeable variables for each item for each truck as a list of dicts
    lp_trucks_items = [pl.LpVariable.dicts("Truck {}".format(truck_number), items_names, lowBound=0, cat='Integer')
                       for truck_number in range(len(trucks_possible_loads))]


    # Adding main objective function
    #
    # Construct a objective function and add it to the LpProblem.
    # The objective function will be calculated repeatedly to adjust the LpVariables to maximize itself.
    #
    # For the objective function we calculate the total sum of utility for the items on the trucks.
    # To do this, we multiply the utility value of the item by its count from the LpVariable.
    # We do that with each item on each truck and get the sum of all.
    prob += pl.lpSum([
        item['utility'] * lp_truck_items[item['name']]
        for _, item in df_items.iterrows()
        for lp_truck_items in lp_trucks_items
    ])


    # Adding constraints

    # Adding max capacity constraints
    #
    # We have a limit of load for each truck, what we can implement as constraints.
    # Instead of taking the total sum as in the objective function, here we create a separate constraint for each truck.
    # To do this, we multiply the weight of the item by its count from the LpVariable.
    # We do that with each item on one truck and get the sum of its weight.
    # Then we add a new constraint where the sum of weight must be lower or equal
    # to the truck max possible load (which we got further up).
    # Repeat for all trucks.

    # for each truck get the possible load
    for truck_number, truck_possible_load in enumerate(trucks_possible_loads):
        lp_truck_items = lp_trucks_items[truck_number]
        # multiply the weight of the item with its count on the truck
        lp_sum = pl.lpSum([float(item['weight']) * lp_truck_items[item['name']] for _, item in df_items.iterrows()])
        # set the constraint, that the sum of weights on the truck must be lower or equal to his possible load
        prob += lp_sum <= truck_possible_load


    # Adding item max count constraints
    #
    # Like the max possible load above it exists also a limit by the max count of each item type.
    # This limit applies one item type over all trucks.
    # So we go through the item list and get the count of it from each truck by the LpVariables in `lp_trucks_items`.
    # We sum the count over all trucks and add a new constraint
    # where it must be lower or equal to the defined max count.
    # Repeat for all items.
    for _, item in df_items.iterrows():
        total_item_count = sum([lp_truck_items[item['name']] for lp_truck_items in lp_trucks_items])
        prob += total_item_count <= item['max_count']


    # Try to solve the defined problem
    #
    # It can be set a certain solver from the pulp library.
    # We set the msg parameter to False, because it disables the solvers output to stdout
    print("\nStart solving...", end='')
    prob.solve(pl.getSolver('PULP_CBC_CMD', msg=False))
    print("done\n")

    # Show the status of solving.
    print("Result status:", pl.LpStatus[prob.status])


    # Convert results to own data structure
    #
    # Because of the subdivide by upper name in the dicts has each LpVariable name a string as prefix like "Truck_1_".
    # Furthermore the library has replaced all whitespaces in the variable names by underscores.
    # So we can not use the original item name as key to get the value of a item.
    #
    # To make easy access we make a own result list for each truck.
    # In this list we add a dictionary for all items on the respective truck.
    # Because the division for each truck, we can remove the prefix on all variables.
    # Just the replaced whitespaces are taken and handled later.
    # The result values keep.

    # get optimized variables
    result_variables = prob.variables()
    # create a result list for the trucks
    result_trucks_items = []
    # for each truck add his items
    for truck_number in range(len(trucks_possible_loads)):
        prefix_len = len("Truck_{}_".format(truck_number))
        # create a result item dict for this truck
        truck_items = {var.name[prefix_len:] : var.varValue     # remove the prefix of truck in the name
                       for var in result_variables
                       # get only the items from the current truck
                       if var.name.startswith("Truck_{}_".format(truck_number))}
        # add count of items for this truck to result list
        result_trucks_items.insert(truck_number, truck_items)


    # Show each truck with containing driver weight and item count from results
    print("\nResult count for each item:")

    for truck_number, result_truck_items in enumerate(result_trucks_items):
        # increase the number of truck by 1 to skip the index 0 (only for presentation)
        # also divide the weight of driver by 1000 to get kg from gram
        print("\nTruck {} with driver weight {}kg:".format(truck_number+1, drivers_weights_gram[truck_number]/1000))
        for item_name, item_count in result_truck_items.items():
            # show only the items which counts are greater 0
            if item_count > 0:
                # replace underscores from pulp with whitespaces for better readability
                print("{:<25} = {:>10}".format(item_name.replace('_', ' '), item_count))

    print("")

    # Show possible loads of trucks
    for truck_number, truck_possible_load in enumerate(trucks_possible_loads):
        print("Allowed weight for truck {} (with included driver): {} gram or {} kg".format(
            truck_number+1,
            truck_possible_load,
            truck_possible_load / 1000))

    print("")

    # Show total weights of trucks containing items
    #
    # To get the total sum of weight for each truck and the chosen count of items,
    # we go through each truck from our own result list `result_trucks_items`.
    # We multiply the weight of item with the count from truck results.
    #
    # Because the library has replaced all whitespaces in the variable names by underscores,
    # we access the result value by do this with the origin name too and use it as key.
    #
    # Notice: We can not just replace all underscores with whitespaces,
    # because a origin name could contain a underscore too.

    # for each truck
    for truck_number, result_truck_items in enumerate(result_trucks_items):
        # calculate the total sum of weight for each item
        total_truck_weight = sum([
            item_count * item['weight']
            for item_name, item_count in result_truck_items.items()
            for _,item in df_items.iterrows()
            # the item names from pulp have replaced whitespaces ' ' with underscore '_'
            # to compare we must do this too
            if item['name'].replace(' ', '_') == item_name
        ])
        print("Total weight of truck {}: {} gram or {} kg".format(truck_number+1,
                                                                  total_truck_weight,
                                                                  total_truck_weight/1000))

    print("")

    # Show the total value of utility over all trucks and items

    # print the end value of the objective function, in our case the sum of utility from all picked items
    result_utility = pl.value(prob.objective)
    print("The total utility value (rounded to 2 decimal places) of picked items in both trucks is: {}".
          format(round(result_utility, 2)))

    print("\nProcess completed.")


def show_items_efficiency(items_csv_file,
                          csv_delimiter=';',
                          column_mapping_required=False,
                          columns_mapping={},
                          output_on=True):
    """Calculate a value of efficiency by utility / weight

    :param items_csv_file: path to csv with items
    :type items_csv_file: str
    :param csv_delimiter: delimiter of the csv columns, default ';'
    :param column_mapping_required: True or False to switch the column mapping on or off
    :param columns_mapping: dict with required column names (name,max_count,weight,utility) as keys
                            and mapping file column names as values
    :param output_on: switch the printed output on or off
    :return: items_efficiency_ordered: sorted dict with item names as keys and efficiency as value
    """

    # Read the data from csv file into a dataframe by pandas.
    df_items = pd.read_csv(items_csv_file, delimiter=csv_delimiter, decimal='.')

    # Map the column names if required
    if column_mapping_required and columns_mapping is not None:
        df_items.rename(columns={origin_name: new_name for new_name, origin_name in columns_mapping.items()},
                        inplace=True)

    items_efficiency = {item['name']: item['utility'] / item['weight'] for _, item in df_items.iterrows()}

    items_efficiency_ordered = dict(sorted(items_efficiency.items(), key=lambda e: e[1], reverse=True))

    if output_on:
        print("Efficients ordered:\n")
        # for more readability its multiplied by 1000
        for name, efficiency in items_efficiency_ordered.items():
            print("{:<25}: {}".format(name, round(efficiency * 1000, 2)))

    return items_efficiency_ordered


def run_example():
    """Run a example what comes from a coding challenge by 'get in it'"""

    print("\nRun a example with parameters of the coding challenge from get in it and BWI.\n")
    print("Predefined parameters:")
    print("Truck count: 2")
    print("Truck 1 weight: 1100kg")
    print("Truck 2 weight: 1100kg")
    print("Driver 1 weight: 72.4kg")
    print("Driver 2 weight: 85.7kg")
    print("Items from file ./items.csv")
    print("---------------------------------------------------------------")

    # trucks count and max loading weight
    trucks_max_loadings = [1100, 1100]
    # can be 'kg' or 'gram'
    trucks_measuring_unit = 'kg'
    # drivers weight
    drivers_weights = [72.4, 85.7]
    # can be 'kg' or 'gram'
    drivers_measuring_unit = 'kg'

    # path to the csv file with all items
    items_csv_file = './items.csv'
    # if False, the column names in the csv must be name, max_count, weight, utility
    # if True, the column names from csv will be changed by columns_mapping below
    column_mapping_required = True
    # the csv column names mapped to name, max_count, weight and utility
    # "<required column>" : ""<mapping csv column>""
    columns_mapping = {
        'name': 'name',
        'max_count': 'required count',
        'weight': 'weight in gram',
        'utility': 'utility'
    }
    # delimiter of the csv columns
    csv_delimiter = ';'

    # start example run
    delivery_optimization(trucks_max_loadings,
                          drivers_weights,
                          items_csv_file,
                          trucks_measuring_unit,
                          drivers_measuring_unit,
                          csv_delimiter,
                          column_mapping_required,
                          columns_mapping)


if __name__ == "__main__":
    run_example()
