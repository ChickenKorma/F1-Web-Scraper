import matplotlib.pyplot as plt
import numpy as np

def driverPoints(races, driver_name, year):
    driver_points = []

    for race in races:
        drivers = race[1]

        for driver in drivers:
            if driver_name in driver[2]:
                driver_points.append(float(driver[6]))

    #print(driver_points)
    plt.plot(np.arange(1, len(races) + 1), np.array(driver_points))
    plt.title(f"{driver_name} for the {year} season")
    plt.xlabel("Races")
    plt.ylabel("Points per Race")
    plt.show()
    
