import random

#region INPUT DATA (you can modify these variables)

debo_prices = {
    "BASE": 825,
    "PRI": 2470,
    "DUO": 7400,
    "TRI": 20600,
    "TET": 99000,
    "PEN": 300000
}
cron_price = 3
downgrade_chance = 0.4
success_chances = {
    "PRI": 0.9,
    "DUO": 0.5,
    "TRI": 0.4,
    "TET": 0.3,
    "PEN": 0.12
}

num_simulations = 1000000
start_level = "TRI"
goal_level = "TET"

#endregion

#region other variables

crons_required = {
    "PRI": 95,
    "DUO": 288,
    "TRI": 865,
    "TET": 2405,
    "PEN": 11548
}
levels = [
    "BASE",
    "PRI",
    "DUO",
    "TRI",
    "TET",
    "PEN"
]

#endregion

#region functions

'''
    Calculates the final cost of enhancement.
    Parameters:
        start_level (string): Initial level of enhancement (BASE, PRI, DUO...)
        debos_used (int): Total debos used for the enhancement.
        crons_used (int): Total crons used for the enhancement.
    Returns:
        int: Total cost of the enhancement (in silvers).
'''
def calculate_cost(start_level, debos_used, crons_used):
    start_cost = debo_prices[start_level] * 1000000 if start_level != "BASE" else 0
    return 1000000 * ((debos_used * debo_prices["BASE"]) + (crons_used * cron_price)) + start_cost

'''
    Formats a given number into a string (1234567 -> 1.234.567)
    Parameters:
        number (int): Number to format.
    Returns:
        string: Formatted number.
'''
def format_num(number):
    return "{:,}".format(number).replace(",", ".")

'''
    Simulates a quantity (num_simulations) of ehnancements starting at start_level to goal_lever.
    Parameters:
        start_level (string): Initial level of enhancement (BASE, PRI, DUO...)
        goal_level (string): Goal level of enhancement (TRI, TET, PEN...)
        num_simulations (int): Number of simulations.
    Returns:
        list: List containing all data from every enhancement (number, enhancement info, debos used, crons used, cost)
'''
def simulate_enhancements(start_level, goal_level, num_simulations):
    results = []
    curr_simulation = 1
    update_interval = num_simulations // 100

    for curr_simulation in range(1, num_simulations + 1):
        curr_level = start_level
        debos_used = 0
        crons_used = 0
        while curr_level != goal_level:
            curr_level, debos_used, crons_used = enhance(levels[levels.index(curr_level) + 1], debos_used, crons_used)
        results.append(f"{curr_simulation};{start_level}->{goal_level};{debos_used};{format_num(crons_used)};{format_num(calculate_cost(start_level, debos_used, crons_used))}")
        if curr_simulation % update_interval == 0:
            progress = (curr_simulation / num_simulations) * 100
            print(f"Progreso: {progress:.2f}%", end='\r')

    return results

'''

    Parameters:
        level (string): Level to enhance (PRI, DUO, TRI...)
        debos_used (int): Current amount of debos used.
        crons_used (int): Current amount of crons used.
    Returns:
        string, int, int: Returns result level, debos used after enhancement, crons used after enhancement.
'''
def enhance(level, debos_used, crons_used):
    enhance_result = random.random()
    is_downgrade = random.random() < downgrade_chance
    crons_used += crons_required[level]
    if enhance_result < success_chances[level]:
        debos_used += 1
        return level, debos_used, crons_used
    elif not is_downgrade:
        debos_used += 1
        return levels[levels.index(level) - 1], debos_used, crons_used
    else:
        if level == levels[1]:
            debos_used += 2
            return levels[0], debos_used, crons_used
        else:
            debos_used += 1
            return levels[levels.index(level) - 2], debos_used, crons_used

'''
    Sorts the simulation results list by cost in ascending order.
    Parameters:
        simulation_results (list): List containing all data from every enhancement (number, enhancement info, debos used, crons used, cost)
'''
def sort_by_cost(simulation_results):
    simulation_results.sort(key=lambda line: int(line.split(';')[-1].replace('.', '')))

'''
    Saves all content from a list into a file.
    Parameters:
        filename (string): Filename name.
        data (list): List containing data you want to save.
'''
def save_to_file(filename, data):
    with open(filename, 'w') as file:
        for line in data:
            file.write(line + "\n")

'''
    Returns the list item corresponding to a given percentile of the cost of enhancement.
    Parameters:
        percentile (float): Number between 0 and 1.
        data (list): List containing all data from every enhancement (number, enhancement info, debos used, crons used, cost)
    Returns:
        string: String containing all data from a given percentile of cost (number, enhancement info, debos used, crons used, cost)
'''
def get_percentile_amount(percentile, data):
    return data[int(len(data) * percentile)]

'''
    Calculates the average cost of all the enhancements in the simulation.
    Parameters:
        simulation_data (list): List containing all data from every enhancement (number, enhancement info, debos used, crons used, cost)
    Returns:
        int: Average cost.
'''
def average_cost(simulation_results):
    total_cost = 0
    for result in simulation_results:
        cost = int(result.split(';')[-1].replace('.', ''))
        total_cost += cost

    return total_cost / len(simulation_results) if simulation_results else 0

'''
    Prints simulation data, average cost, and each 10th percentile of the cost to enhance.
    Parameters:
        simulation_results (list): List containing all data ordered by cost from every enhancement (number, enhancement info, debos used, crons used, cost)
'''
def print_simulation_data(simulation_results):
    debos_width = max(len(str(result.split(';')[2])) for result in simulation_results)
    crons_width = max(len(result.split(';')[3]) for result in simulation_results)
    silver_width = max(len(result.split(';')[4]) for result in simulation_results)

    print(f"Debo price: {debo_prices['BASE']}m silver\nCron price: {cron_price}m silver")
    print(f"Number of simulations: {format_num(num_simulations)}")
    print(f"{start_level}->{goal_level} average cost: {format_num(average_cost(simulation_results))} silver")
    print(f"-- PERCENTILES --")
    for i in range(1, 10):
        data = str(get_percentile_amount(i/10,simulation_results)).split(";")
        print(f"{i}0% -> {data[2].rjust(debos_width)} debos | {data[3].rjust(crons_width)} crons | {data[4].rjust(silver_width)} silver")

#endregion       

results = simulate_enhancements(start_level, goal_level, num_simulations)
sort_by_cost(results)
print_simulation_data(results)