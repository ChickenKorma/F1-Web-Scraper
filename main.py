from table_scraper import *
from graph_generator import *

#Determines desired data by user input
print("What year do you want to see? (2022, 2021 ... 1950)")
year_input = input()

print("What do you want to see from that year? (drivers, minimal race, full race)")
type_input = input()


#Performs web scraping to obtain data
match type_input:
    case "drivers":
        drivers = driversStandings(year_input)

    case "minimal race":
        races = basicRaceResults(year_input)

    case "full race":
        races = fullRaceResults(year_input)

        print("Which driver do you want to see?")
        driver = input()

        driverPoints(races, driver, year_input)


#To get race progression:
#   Go to the year page
#   Gather list of races from html
#   Cycle through list of pages
#   Obtain grand prix name by the URL
#   Use table scraping as normal