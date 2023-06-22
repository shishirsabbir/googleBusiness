# import modules including local

import re
import os
import csv
import json
import requests
from urllib import parse
from bs4 import BeautifulSoup
from locals.output_data import exportData
from locals.automate import By, Keys, EC, Action, wait_for, genBrowser, driverWait



# function to find phone and address
def get_info(info_txt):

    try:
        phone = re.search(r'\b\+[0-9]{2}\s[0-9]{1,5}\s[0-9]{1,5}\s[0-9]{1,5}\b', info_txt).group()
    except:
        phone = '--Not Provided--'

    try:
        address_text = re.search(r"(?:Sat|Sun|Mon|Tue|Wed|Thu|Fri|am|pm|ness)[A-Z][A-Za-z\s]+\s[A-Za-z]+\,\sAustralia\b", info_text).group()
        removal_chars = re.search(r"(?:Sat|Sun|Mon|Tue|Wed|Thu|Fri|am|pm|ness|hours)", address_text).group()
        address = address_text.replace(removal_chars, '')
    except:
        address = "--Not Provided--"
    
    return (phone, address)


# list to store the data in a list
data_list = []


# automation with selenium using context manager
with genBrowser() as chrome:
    input_url = input('Enter the URL: ')

    # custom url panel
    # input_url = "https://www.google.com/localservices/prolist?g2lbs=ADZRdks-47dflFkjPsWCi49kbkgSLeFepvG-cbbhbqqLwMJWy-JSYiOvdxj5T0cftqqeHueE-0MRgtVy0H0azD0ZqUz0VBATSPDP5SiUPuktGTuOVGF7irdROD8dJYVdBkRBKvm1xgiCRCRgJjSNfDGC8KhlmwHNPA%3D%3D&hl=en-BD&gl=bd&ssta=1&q=list%20of%20200%20dog%20trainers%20in%20adelaide&oq=list%20of%20200%20dog%20trainers%20in%20adelaide&slp=MgA6HENoTUlwdW44aHZyVV93SVZncFJtQWgwZVBRTzZSAggCYACSAawCCg0vZy8xMWh6OWh2MWdiCg0vZy8xMWhkNTVtY21wCgsvZy8xdGN5NGZmXwoML2cvMXloNXRyM3c0Cg0vZy8xMXJkXzAwcGhuCgsvZy8xdGdsbjBjNwoNL2cvMTFmNWJwdHNucgoNL2cvMTFnamo0N3c4YwoNL2cvMTFmcWtxbWR0aAoNL2cvMTFoYnN0NHg1bgoNL2cvMTFoMjA3dHE5NwoNL2cvMTFnaDAxX3MwegoNL2cvMTFycHAzbm0zYgoLL2cvMXR2cTQ3cjgKDS9nLzExczd3Y3piMjAKCy9nLzF0azYzN2s1CgsvZy8xdGRfeXF2XwoNL2cvMTFiel96OTQ1OQoML2cvMWhkXzluczcxCg0vZy8xMWYxMjFuM3k3EgQSAggBEgQKAggBmgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwjpn_WG-tT_AhWMbWwGHc7LDFoQjGp6BAgZEAE&scp=ChBnY2lkOmRvZ190cmFpbmVyElgSEgk_sybFxzW3ahFAxo5iVDYDBBoSCfPH6FueWKdqEdjQ-j2ZeX7bIhZBZGVsYWlkZSBTQSwgQXVzdHJhbGlhKhQN3Szu6hWzl4RSHThwWOslKi24UjAAGhhsaXN0IG9mIDIwMCBkb2cgdHJhaW5lcnMiJGxpc3Qgb2YgMjAwIGRvZyB0cmFpbmVycyBpbiBhZGVsYWlkZSoLRG9nIHRyYWluZXI%3D"
    chrome.get(input_url)

    while True:
        wait_for(4)
        card_list = chrome.find_elements(By.CSS_SELECTOR, 'div[role="list"] div[data-test-id="organic-list-card"]')

        print(len(card_list))

        for card in card_list:
            html = card.get_attribute('outerHTML')

            soup = BeautifulSoup(html, 'lxml')
            info_tags = soup.select('div.NwqBmc > div.I9iumb')
            info_text = soup.select_one('div.NwqBmc').text

            web_url_tag = soup.select_one('div.DyM7H div[jsname="K9a4Re"] a[aria-label="Website"]')

            if web_url_tag == None:
                continue
            else:
                web_url = web_url_tag['href']

                b_name = info_tags[0].text
                star_rating = info_tags[1].text

                try:
                    rating = re.search(r'\A\d\.\d', star_rating).group()
                except:
                    rating = 'No ratings'

                try:
                    review_count = re.search(r'\b\(\d+\)\b', star_rating).group().replace('(', '').replace(')', '')
                except:
                    review_count = 'No reviews'

                phone, address = get_info(info_text)


                data_dict = {
                    "title" : b_name,
                    "phone" : phone,
                    "rating" : rating,
                    "review" : review_count,
                    "address" : address,
                    "website" : web_url
                }

                data_list.append(data_dict)

        # card_body.send_keys(Keys.PAGE_DOWN)
        try:
            next_btn = chrome.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
            Action(chrome).move_to_element(next_btn).perform()
            wait_for(1)
            next_btn.click()
        except:
            print('List Complete')
            break

        # if len(trainer_list) > 100:
        #     break



# printing the length of the collected data list
print(len(data_list))


# demo a the last data
print(data_list[-1])


# export the data
exportData(input('Enter the name of the file: '), data_list)