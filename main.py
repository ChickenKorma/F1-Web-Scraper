from table_scraper import *

print("What year do you want to see? (2022, 2021 ... 1950)")
year_input = input()
#year_input = "2022"

print("What do you want to see from that year? (drivers, races, team, fastest-laps)")
type_input = input()
#type_input = "races"

getPage(year_input, type_input)

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