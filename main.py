from table_scraper import *

#Determines desired data by user input
print("What year do you want to see? (2022, 2021 ... 1950)")
year_input = input()

print("What do you want to see from that year? (drivers, races, team, fastest-laps)")
type_input = input()

#Initialises html soup object
getPage(year_input, type_input)

#Performs web scraping to obtain data
match type_input:
    case "drivers":
        driversStandings()

    case "races":
        raceResults()


#To get race progression:
#   Go to the year page
#   Gather list of races from html
#   Cycle through list of pages
#   Obtain grand prix name by the URL
#   Use table scraping as normal