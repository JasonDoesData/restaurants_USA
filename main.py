from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

class RestaurantScraper:
    def __init__(self, city, state):
        self.city = city
        self.state = state

    def start_scrape(self, city, state):
        time.sleep(5)
        more_places = driver.find_element(By.CLASS_NAME, "jRKCUd")
        more_places.click()

    def scrape_details(self, city, state, dictionary):
        time.sleep(3)
        citystate = f'{city}, {state}'
        restaurants_in_page = driver.find_elements(By.CLASS_NAME, "rllt__details")
        for element in restaurants_in_page:
            restaurant = element.find_element(By.CLASS_NAME,"OSrXXb").get_attribute('innerText')
            rating = element.find_element(By.CLASS_NAME, "Y0A0hc").get_attribute('innerText')[:3]
            rating = float(rating)
            left = element.find_element(By.CLASS_NAME, "Y0A0hc").get_attribute('innerText').index('(')
            right = element.find_element(By.CLASS_NAME, "Y0A0hc").get_attribute('innerText').index(')')
            num_reviews = element.find_element(By.CLASS_NAME, "Y0A0hc").get_attribute('innerText')[left+1:right]
            if 'K' in num_reviews:
                num_reviews = num_reviews.replace('K', '')
                if '.' in num_reviews:
                    num_reviews = num_reviews.replace('.', '')
                    num_reviews = float(num_reviews)
                    num_reviews *= 100
                    num_reviews = int(num_reviews)
                else:
                    num_reviews = float(num_reviews)
                    num_reviews *= 1000
                    num_reviews = int(num_reviews)
            else:
                num_reviews = int(num_reviews)
            dictionary[citystate].append((restaurant, rating, num_reviews))
        return dictionary

    def next_page(self, count, city, state, dictionary):
        next_page_class = driver.find_element(By.CLASS_NAME, "AaVjTc")
        next_page = next_page_class.find_elements(By.TAG_NAME, 'td')
        len_next_page = len(next_page) - 2

        while count < len_next_page:
            if next_page_class.find_element(By.ID, 'pnnext'):
                next_page_class.find_element(By.ID, 'pnnext').click()
                next_page = next_page_class.find_elements(By.TAG_NAME, 'td')
                len_next_page = len(next_page) - 2
                print(f'{count} {len_next_page}')
                time.sleep(3)
                self.scrape_details(city, state, dictionary)
                self.next_page(count+1, city, state, dictionary)


states = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

cities = [
    ["Birmingham", "Montgomery", "Mobile"],  # Alabama
    ["Anchorage", "Fairbanks", "Juneau"],  # Alaska
    ["Phoenix", "Tucson", "Mesa"],  # Arizona
    ["Little Rock", "Fort Smith", "Fayetteville"],  # Arkansas
    ["Los Angeles", "San Diego", "San Jose"],  # California
    ["Denver", "Colorado Springs", "Aurora"],  # Colorado
    ["Bridgeport", "New Haven", "Stamford"],  # Connecticut
    ["Wilmington", "Dover", "Newark"],  # Delaware
    ["Jacksonville", "Miami", "Tampa"],  # Florida
    ["Atlanta", "Augusta", "Columbus"],  # Georgia
    ["Honolulu", "Pearl City", "Hilo"],  # Hawaii
    ["Boise", "Meridian", "Nampa"],  # Idaho
    ["Chicago", "Aurora", "Rockford"],  # Illinois
    ["Indianapolis", "Fort Wayne", "Evansville"],  # Indiana
    ["Des Moines", "Cedar Rapids", "Davenport"],  # Iowa
    ["Wichita", "Overland Park", "Kansas City"],  # Kansas
    ["Louisville", "Lexington", "Bowling Green"],  # Kentucky
    ["New Orleans", "Baton Rouge", "Shreveport"],  # Louisiana
    ["Portland", "Lewiston", "Bangor"],  # Maine
    ["Baltimore", "Frederick", "Rockville"],  # Maryland
    ["Boston", "Worcester", "Springfield"],  # Massachusetts
    ["Detroit", "Grand Rapids", "Warren"],  # Michigan
    ["Minneapolis", "St. Paul", "Rochester"],  # Minnesota
    ["Jackson", "Gulfport", "Southaven"],  # Mississippi
    ["Kansas City", "St. Louis", "Springfield"],  # Missouri
    ["Billings", "Missoula", "Great Falls"],  # Montana
    ["Omaha", "Lincoln", "Bellevue"],  # Nebraska
    ["Las Vegas", "Henderson", "Reno"],  # Nevada
    ["Manchester", "Nashua", "Concord"],  # New Hampshire
    ["Newark", "Jersey City", "Paterson"],  # New Jersey
    ["Albuquerque", "Las Cruces", "Rio Rancho"],  # New Mexico
    ["New York City", "Buffalo", "Rochester"],  # New York
    ["Charlotte", "Raleigh", "Greensboro"],  # North Carolina
    ["Fargo", "Bismarck", "Grand Forks"],  # North Dakota
    ["Columbus", "Cleveland", "Cincinnati"],  # Ohio
    ["Oklahoma City", "Tulsa", "Norman"],  # Oklahoma
    ["Portland", "Eugene", "Salem"],  # Oregon
    ["Philadelphia", "Pittsburgh", "Allentown"],  # Pennsylvania
    ["Providence", "Warwick", "Cranston"],  # Rhode Island
    ["Charleston", "Columbia", "North Charleston"],  # South Carolina
    ["Sioux Falls", "Rapid City", "Aberdeen"],  # South Dakota
    ["Nashville", "Memphis", "Knoxville"],  # Tennessee
    ["Houston", "San Antonio", "Dallas"],  # Texas
    ["Salt Lake City", "West Valley City", "Provo"],  # Utah
    ["Burlington", "South Burlington", "Rutland"],  # Vermont
    ["Virginia Beach", "Norfolk", "Chesapeake"],  # Virginia
    ["Seattle", "Spokane", "Tacoma"],  # Washington
    ["Charleston", "Huntington", "Morgantown"],  # West Virginia
    ["Milwaukee", "Madison", "Green Bay"],  # Wisconsin
    ["Cheyenne", "Casper", "Laramie"],  # Wyoming
]

restaurants_dictionary = {}

hasAccepted = False
for i in range(len(states)):
    state = states[i]
    print(i)
    for j in range(len(cities[i])):
        print(j)
        city = cities[i][j]
        citystate = f'{city}, {state}'
        restaurants_dictionary[citystate] = []
        driver.get(f"https://www.google.com/search?q=best+restaurants+{city}+{state}")
        if hasAccepted is False:
            time.sleep(5)
            accept = driver.find_element(By.ID, "L2AGLb")
            accept.click()
            hasAccepted = True
        restaurant = RestaurantScraper(city, state)
        time.sleep(5)
        more_places = driver.find_element(By.CLASS_NAME, "jRKCUd")
        more_places.click()
        restaurant.scrape_details(restaurant.city, restaurant.state, restaurants_dictionary)
        try:
            restaurant.next_page(1, restaurant.city, restaurant.state, restaurants_dictionary)
        except:
            print("Completed")
            print(len(restaurants_dictionary[citystate]))
            print(restaurants_dictionary[citystate])

with open("restaurantsbycity.json", "w") as outfile:
    json.dump(restaurants_dictionary, outfile)



