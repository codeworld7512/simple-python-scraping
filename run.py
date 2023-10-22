import requests
from bs4 import BeautifulSoup
from lxml import etree
import csv

header = ['Title', 'Share Type', 'Location', 'Postcode', 'Room Price', 'Available', 'Minimum Term', 'Maximum Term', 'Security deposit', 'Bills included', 'Furnishings', 'Parking',
    'Disabled access', 'Balcony', 'Living_room', 'Broadband', 'Included', 'Garden', 'Garage', 'Housemates', 'Total_rooms', 'Age', 'Smoker', 'Any_pets', 'Language', 'Interests', 'Gender',
    'Smoking ok', 'Pets ok', 'Occupation', 'New flatmate preferences gender', 'References', 'Advertiser Name', 'Who is Advertiser', 'Last Active', 'Description' ]
data = [header]

# URL = "https://www.spareroom.co.uk/flatshare/?offset=0&search_id=1231712550&"
# URL = "https://www.spareroom.co.uk/flatshare/angus/dundee"
# URL = 'https://www.spareroom.co.uk/flatshare/angus/dundee?sort_by=price_low_to_high'

while(1):
    print("Enter 'Q' or 'Ctrl + C' to finish this program!")
    URL = input("Enter a URL to scrap: ")

    while(1):
        try:
            if(URL=='q' or URL=='Q'):
                break
            page = requests.get(URL)
            break
        except:
            print("Enter Valid URL")
            URL = input("Enter a URL to scrap: ")
            
    if(URL=='q' or URL=='Q'):
        break
    soup = BeautifulSoup(page.content, "html.parser")
    next_url = URL

    result_number = soup.find(id="maincontent").find_all('strong')[1].text
    location_keyword = soup.find('input', {'name': 'search'})['value'].strip()

    i = 1 
    while(i<int(result_number)):

        current_page = requests.get(next_url)
        current_soup = BeautifulSoup(current_page.content, "html.parser")
        url_chips = current_soup.find_all("li", {"class":"listing-result"})

        for url_chip in url_chips:
            data_page = requests.get("https://www.spareroom.co.uk/" + url_chip.find('a').get('data-detail-url'))
            data_soup = BeautifulSoup(data_page.content, "html.parser")
            # data_dom = etree.HTML(str(data_soup))

            title = data_soup.find(id="mainheader").find('h1').text.strip()
            
            #-------------------------------details--------------------------------
            details = data_soup.find("section", {"class": "feature feature--details"})
            share_type = details.find_all('li')[0].text.strip()
            location = details.find_all('li')[1].text.strip()
            postcode = details.find_all('li')[2].text.strip()

            #------------------------------price-----------------------------------
            try:
                room_price = data_soup.find("strong", {"class": "room-list__price"}).text.strip()
                # Do something with the price value
            except AttributeError as e:
                # Handle the exception
                room_price = data_soup.find("section", {"class": "feature feature--price-whole-property"}).find('h3').text.strip()

            #-------------------------Availability----------------------------
            availability = data_soup.find("section", {"class": "feature feature--availability"})
            available = availability.find_all('dd')[0].text.strip()
            minimum_term = availability.find_all('dd')[1].text.strip()
            maximum_term = availability.find_all('dd')[2].text.strip()

            #-------------------------Extra Cost------------------------------
            extra_cost = data_soup.find("section", {"class": "feature feature--extra-cost"})
            security_deposit = extra_cost.find_all('dd')[0].text.strip()
            try:
                bills_included = extra_cost.find_all('dd')[1].text.strip()
            except:
                bills_included = ""

            #-------------------------Amentities------------------------
            amenities = data_soup.find("section", {"class": "feature feature--amenities"})
            try:
                furnishings = list(filter(lambda x: x.text == "Furnishings", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                furnishings = ''

            try:
                parking = list(filter(lambda x: x.text == "Parking", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                parking = ""

            try:
                disabled_access = list(filter(lambda x: x.text == "Disabled access", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                disabled_access = ""

            try:
                balcony = list(filter(lambda x: x.text == "Balcony/patio", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                balcony = ""

            try:
                living_room = list(filter(lambda x: x.text == "Living room", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                living_room = ""
                
            try:
                broadband = list(filter(lambda x: x.text == "Broadband", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                broadband = ""
                
            try:
                included = list(filter(lambda x: x.text == "included", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                included = ""
                
            try:
                garden = list(filter(lambda x: x.text == "Garden/terrace", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                garden = ""

            try:
                garage = list(filter(lambda x: x.text == "Garage", amenities.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                garage = ""
            
            #-------------------------------------Current household----------------------------------
            try:
                current_household = data_soup.find("section", {"class": "feature feature--current-household"})
                try:
                    housemates = list(filter(lambda x: x.text.find("housemates") != -1 or x.text.find('flatmates') != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    housemates = ""

                try:
                    total_rooms = list(filter(lambda x: x.text.find("Total") != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    total_rooms = ""
                    
                try:
                    age = list(filter(lambda x: x.text.find("Age") != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    age = ""
                    
                try:
                    smoker = list(filter(lambda x: x.text.find("Smoker") != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    smoker = ""
                    
                try:
                    any_pets = list(filter(lambda x: x.text.find("pets") != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    any_pets = ""
                    
                try:
                    language = list(filter(lambda x: x.text.find("Language") != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    language = ""
                    
                try:
                    interests = list(filter(lambda x: x.text == "Interests", current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    interests = ""
                    
                try:
                    gender = list(filter(lambda x: x.text.find("Gender") != -1, current_household.find_all('dt')))[0].find_next('dd').text.strip()
                except:
                    gender = ""
            except:
                housemates=""
                total_rooms = ""
                age = ""
                smoker = ""
                any_pets = ""
                language = ""
                interests = ""
                gender = ""

            #------------------------------------New flatmate preferences----------------------------------
            new_flatmate_preferences = data_soup.find("section", {"class": "feature feature--household-preferences"})
            try:
                couples_ok = list(filter(lambda x: x.text.find("Couples") != -1, new_flatmate_preferences.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                couples_ok = ""

            try:
                smoking_ok = list(filter(lambda x: x.text.find("Smoking") != -1, new_flatmate_preferences.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                smoking_ok = ""
            
            try:
                pets_ok = list(filter(lambda x: x.text.find("Pets") != -1, new_flatmate_preferences.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                pets_ok = ""
                
            try:
                occupation = list(filter(lambda x: x.text.find("Occupation") != -1, new_flatmate_preferences.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                occupation = ""
                
            try:
                new_gender = list(filter(lambda x: x.text.find("Gender") != -1, new_flatmate_preferences.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                new_gender = ""

            try:
                references = list(filter(lambda x: x.text.find("References") != -1, new_flatmate_preferences.find_all('dt')))[0].find_next('dd').text.strip()
            except:
                references = ""

            try:
                description = data_soup.find("p", {"class": "detaildesc"}).text.strip()
            except:
                description = ""
            
            #--------------------------------------advertiser---------------------------------
            advertiser_name = data_soup.find("strong", {"class": "profile-photo__name"}).text
            advertiser_who = data_soup.find("strong", {"class": "profile-photo__name"}).find_next('em').text
            advertiser_last_active = data_soup.find("span", {"class": "last-online light-grey"}).text

            row = [title, share_type, location, postcode, room_price, available, minimum_term, maximum_term, security_deposit, bills_included, furnishings, parking,
            disabled_access, balcony, living_room, broadband, included, garden, garage, housemates, total_rooms, age, smoker, any_pets, language, interests, gender,
            smoking_ok, pets_ok, occupation, new_gender, references, advertiser_name, advertiser_who, advertiser_last_active, description]
            
            data.append(row)
            print(title)

            i += 1

        next_dom = etree.HTML(str(current_soup))
        try:
            sub_next_url = next_dom.xpath('//*[@id="paginationNextPageLink"]')[0].get("href")
            if(sub_next_url.find('flatshare/') != -1):
                next_url = 'https://www.spareroom.co.uk' + sub_next_url
            else:
                next_url = 'https://www.spareroom.co.uk/flatshare/' + sub_next_url
        except:
            next_url = ''

    with open(location_keyword+'.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    print(result_number+"results was extracted successfully!/n")
