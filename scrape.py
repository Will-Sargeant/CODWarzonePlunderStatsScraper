from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from time import sleep
import csv


### functions 
def parse_text(unparsed):
    parsed = unparsed.get_text().lstrip('\n\r\n').lstrip('\n\r\n ').rstrip('\n\r\n').rstrip('\n\r\n ')
    return parsed

def scrape (player_name, plarform, driver):
    overview_url = f"https://cod.tracker.gg/warzone/profile/{platform}/{player_name}/overview"

    driver.get(overview_url)
    # need to sleep for 5 sec to let page finish loading before pulling dynamic content
    sleep(4)
    #accept cookies pop-up if it occurs 
    try:
        driver.find_element_by_xpath('//*[@id="onetrust-accept-btn-handler"]').click()
    except NoSuchElementException:
        pass

    #extraxt page html
    overview_url_html = driver.page_source
    #Create Soup
    soup = BeautifulSoup(overview_url_html, 'html.parser')

    match = soup.find_all("div", {"class": "segment-stats card bordered responsive"})[2]

    ### lists of attributes / values
    attributes = []
    values = []

    ### add user 
    attributes.append('User')
    values.append(player_name)

    ### Get total number of games
    total_games = match.find("div", {"class": "title-stats"}).find("span", {"class": "matches"})
    total_num_games = str(parse_text(total_games).split()[0])

    try:
        attributes.append('Games Played')
        values.append(total_num_games)
    except AttributeError:
        pass

    ## Get stats from Plunder section
    stats = match.find_all("div", {"class": "numbers"})
    for stat in stats:  
        name = stat.find("span", {"class": "name"})
        value = stat.find("span", {"class": "value"})
        
        try:
            if (parse_text(name)) in attributes:
                name = str((parse_text(name)))+"_"
                attributes.append(name)
                values.append(parse_text(value))
            else:
                attributes.append(parse_text(name))
                values.append(parse_text(value))
        except AttributeError:
            pass

    ## Combine into dict
    plunder_dict = dict(zip(attributes, values))
    output.append(plunder_dict)


## Script

driver = webdriver.Chrome(executable_path='/Users/sargeantw/Desktop/my project/project_env/bin/chromedriver')

player_names = ["sargeboi", "Calijohns", "Norrington123", "McGuv", "goonerSP", "jp0792"]
platform = "psn"

output = []

for player_name in player_names: 
    scrape(player_name, platform, driver)

field_names = list(output[0].keys())

with open('output.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(output)

print("csv created")
print(output)

driver.close()