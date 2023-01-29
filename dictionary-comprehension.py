import random

customers = ["Alex", "Bob", "Mavis", "Dave", "Flow", "Katie", "Nate"]
surnames = ["lnjsdfag", "adfag", "egh", "Bsfvut", "Ssdfsf", "Pefgret", "Sillyface"]
discounts = [12, 99, 194, 123, 234234, 2342, 23523, 0000.234]

new_dict = {customer: random.choice(discounts) for customer in customers}
# combine two iterables into one dictionary as key/value pairs
newer_dict = {customer: surname for (customer, surname) in zip(customers, surnames)}
# print(newer_dict)

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
temp_C = [30.5, 32.6, 31.8, 33.4, 29.8, 30.2, 29.9]
weekly_temperatures = {day: temp for (day, temp) in zip(days, temp_C)}
# print(weekly_temperatures["Wednesday"])

print(weekly_temperatures.items())

# for day in weekly_temperatures:
#     print(day)
# for temp in weekly_temperatures:
#     print(weekly_temperatures[temp])
# new_dict_temps = {day: temp for (day, temp) in (weekly_temperatures, weekly_temperatures[temp])}