import requests
from bs4 import BeautifulSoup

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

#Parses table_elements to return list of races and associated data
def basicRaceResults(year):
    getGenericPage(year, "races")
    getTable()

    race_list = []
    
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

        #print(f"Grand Prix: {grand_prix}")
        #print(f"Date: {date}")
        #print(f"Winner: {winner}")
        #print(f"Team: {team}")
        #print(f"Laps: {laps}")
        #print(f"Time: {time}")
        #print()

        race_info = [grand_prix, date, winner, team, laps, time]
        race_list.append(race_info)

    return race_list

#Generates list of races that season and parses html in each to return list of drivers and associated data
def fullRaceResults(year):
    getGenericPage(year, "races")
    races = getRaceList()

    race_list = []
    
    for race in races:
        if race[0] == "All":
            continue

        getSpecificPage(race[1])
        getTable()
        
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

        race_info = [race[0], driver_list]

        race_list.append(race_info)

    return race_list
