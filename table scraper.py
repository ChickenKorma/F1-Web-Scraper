from msilib.schema import tables
import requests
from bs4 import BeautifulSoup

def getPage(year, type):
    URL = f"https://www.formula1.com/en/results.html/{year}/{type}.html"
    page = requests.get(URL)

    global soup
    soup = BeautifulSoup(page.content, "html.parser")

def getTable():
    table = soup.find("table", class_="resultsarchive-table")
    table_body = table.find("tbody")

    global table_elements
    table_elements = table_body.find_all("tr")

def driversStandings():
    getTable()
    
    for driver in table_elements:
        cells = driver.find_all("td")

        position = cells[1].text

        name_element = cells[2]
        name_spans = name_element.find_all("span")
        name = f"{name_spans[0].text} {name_spans[1].text} ({name_spans[2].text})"

        nationality = cells[3].text

        team_element = cells[4]
        team = team_element.find("a").text

        points = cells[5].text

        print(f"Position: {position}")
        print(f"Name: {name}")
        print(f"Nationality: {nationality}")
        print(f"Team: {team}")
        print(f"Points: {points}")
        print()

def raceResults():
    getTable()
    
    for race in table_elements:
        cells = race.find_all("td")

        grand_prix_element = cells[1]
        grand_prix = grand_prix_element.find("a").text.strip()

        date = cells[2].text

        winner_element = cells[3]
        winner_spans = winner_element.find_all("span")
        winner = f"{winner_spans[0].text} {winner_spans[1].text} ({winner_spans[2].text})"

        team = cells[4].text

        laps = cells[5].text

        time = cells[6].text

        print(f"Grand Prix: {grand_prix}")
        print(f"Date: {date}")
        print(f"Winner: {winner}")
        print(f"Team: {team}")
        print(f"Laps: {laps}")
        print(f"Time: {time}")
        print()

print("What year do you want to see? (2022, 2021 ... 1950)")
year_input = input()

#print("What do you want to see from that year? (drivers, races, team, fastest-laps)")
#type_input = input()
type_input = "races"

getPage(year_input, type_input)
#driversStandings()
raceResults()


#To get race progression:
#   Go to the year page
#   Gather list of races from html
#   Cycle through list of pages
#   Obtain grand prix name by the URL
#   Use table scraping as normal
