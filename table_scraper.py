import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

url_prefix = "https://www.formula1.com"

#Requests desired page html and creates global soup object
def getGenericPage(year, type):
    URL = f"https://www.formula1.com/en/results.html/{year}/{type}.html"
    page = requests.get(URL)

    global soup
    soup = BeautifulSoup(page.content, "html.parser")

#Requests specific page html and creates global soup object
def getSpecificPage(URL):
    page = requests.get(URL)

    global soup
    soup = BeautifulSoup(page.content, "html.parser")

#Parses html to extract table rows into table_elements
def getTable():
    table = soup.find("table", class_="resultsarchive-table")
    table_body = table.find("tbody")

    global table_elements
    table_elements = table_body.find_all("tr")

#Parses html to find the race list and extracts cells into race_list
def getRaceList():
    list_wrapper = soup.find_all("div", class_="resultsarchive-filter-wrap")[2]
    list = list_wrapper.find("ul")
    list_elements = list.find_all("li")

    race_list = []

    for race in list_elements:
        link_element = race.find("a")
        link = url_prefix + link_element["href"]

        grand_prix = link_element.find("span").text

        #print(f"Grand Prix: {grand_prix}")
        #print(f"Link: {link}")

        race_info = [grand_prix, link]
        race_list.append(race_info)

    return race_list


#Parses table_elements to return list of drivers and associated data
def driversStandings(year):
    getGenericPage(year, "drivers")
    getTable()
    
    driver_list = []

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

        #print(f"Position: {position}")
        #print(f"Name: {name}")
        #print(f"Nationality: {nationality}")
        #print(f"Team: {team}")
        #print(f"Points: {points}")
        #print()

        driver_info = [position, name, nationality, team, points]
        driver_list.append(driver_info)

    return driver_list

#Generates list of races that season and parses html in each to return list of drivers and associated data
def raceResults(year):
    getGenericPage(year, "races")
    races = getRaceList()

    race_list = []
    
    for race in races:
        if race[0] == "All":
            continue

        getSpecificPage(race[1])
        getTable()
        
        race_details = soup.find("p", class_ = "date")
        race_details_elements = race_details.find_all("span")
        race_date = f"{race_details_elements[0].text} - {race_details_elements[1].text}"
        race_name_parts = race_details_elements[2].text.split(", ")
        track_name = race_name_parts[0]
        region_name = race_name_parts[1]

        driver_list = []

        for driver in table_elements:
            cells = driver.find_all("td")

            position = cells[1].text

            number = cells[2].text

            name_element = cells[3]
            name_spans = name_element.find_all("span")
            name = f"{name_spans[0].text} {name_spans[1].text} ({name_spans[2].text})"

            team = cells[4].text

            laps = cells[5].text

            time = cells[6].text

            points = cells[7].text

            #print(f"Position: {position}")
            #print(f"Name: {name}")
            #print(f"Nationality: {nationality}")
            #print(f"Team: {team}")
            #print(f"Points: {points}")
            #print()

            driver_info = [position, number, name, team, laps, time, points]
            driver_list.append(driver_info)

        race_info = [track_name, region_name, race[0], race_date, driver_list]

        race_list.append(race_info)

    return race_list

def scrapeDrivers(start, stop):
    for year in range(start, stop + 1, 1):
        full_path = os.getcwd() + "/Data/driver_standings/"

        if not os.path.isdir(full_path):
            os.mkdir(full_path)

        drivers = driversStandings(year)

        data_frame = pd.DataFrame(drivers)
        data_frame.columns = ["Position", "Name", "Nationality", "Team", "Points"]
        data_frame.to_csv(f"Data/driver_standings/{year}.csv", index = False)

def scrapeRaces(start, stop):
    for year in range(start, stop + 1, 1):
        full_path = os.getcwd() + f"/Data/race_results/{year}/"

        if not os.path.isdir(full_path):
            os.mkdir(full_path)

        races = raceResults(year)

        race_list = []

        for race in races:
            race_list.append([race[0], race[1], race[2], race[3]])

            data_frame = pd.DataFrame(race[4])
            data_frame.columns = ["Position", "Number", "Name", "Team", "Laps", "Time", "Points"]
            data_frame.to_csv(f"Data/race_results/{year}/{race[2]}.csv", index = False)

        data_frame = pd.DataFrame(race_list)
        data_frame.columns = ["Track", "Region", "Country/Race", "Date"]
        data_frame.to_csv(f"Data/race_results/{year}/_races.csv", index = False)

#Determines desired data by user input
print("What data do you want to scrape? (drivers, races)")
type_input = input()

print("What year do you want to start from? (2022, 2021 ... 1950)")
start_input = int(input())

print("What year do you want to stop at? (2022, 2021 ... 1950)")
stop_input = int(input())

#Performs web scraping to obtain data
match type_input:
    case "drivers":
        scrapeDrivers(start_input, stop_input)

    case "races":
        scrapeRaces(start_input, stop_input)


