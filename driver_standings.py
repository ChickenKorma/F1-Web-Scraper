import requests
from bs4 import BeautifulSoup

URL = "https://www.formula1.com/en/results.html/2022/drivers.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

drivers_table = soup.find("table", class_="resultsarchive-table")
drivers_table_body = drivers_table.find("tbody")
drivers = drivers_table_body.find_all("tr")

for driver in drivers:
    table_elements = driver.find_all("td")

    position = table_elements[1].text

    name_element = table_elements[2]
    name_spans = name_element.find_all("span")
    name = f"{name_spans[0].text} {name_spans[1].text} ({name_spans[2].text})"

    nationality = table_elements[3].text

    team_element = table_elements[4]
    team = team_element.find("a").text

    points = table_elements[5].text

    print(f"Position: {position}")
    print(f"Name: {name}")
    print(f"Nationality: {nationality}")
    print(f"Team: {team}")
    print(f"Points: {points}")
    print()

    
    #print(driver.text.strip())
