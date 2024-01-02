#!/usr/bin/env python
# coding: utf-8

# 
# Lien du site : 
# https://www.leparking.be/?utm_content=cmp-true#!/voiture-occasion/%3Fid_pays%3D18%26tri%3Ddate

# # Scrappe Le parking

# ## Import

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import urllib
import re
import requests
import csv
import time
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.service import Service
from fake_useragent import UserAgent
from urllib3.exceptions import NewConnectionError
import logging
from datetime import datetime, timedelta
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
import pandas as pd 
import numpy as np 

import random
from selenium.webdriver.common.action_chains import ActionChains
from itertools import combinations
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from fake_useragent import UserAgent


# ## Annex fonc

# In[2]:


def get_info_elements(info_elements, element_name):
    max_retries = 3
    retry_count = 0
    values_list = []  # Initialize an empty list to store the values
    
    while retry_count < max_retries:
        try:
            # Wait for the elements to be present
            elements_list = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, info_elements))
            )
            
            for element in elements_list:
                try:
                    info = element.get_attribute('textContent')
                    values_list.append(info)  # Add the value to the list
                except StaleElementReferenceException:
                    # Handle StaleElementReferenceException by re-finding the element
                    pass

            break  # If successful, exit the loop
            
        except NoSuchElementException as e:
            print(f"Une erreur s'est produite lors de la récupération des informations ({element_name}) : {e}")
            retry_count += 1
            time.sleep(1)  # Wait for a short time before retrying
        except TimeoutException:
            print(f"Timeout waiting for {element_name} elements to be present.")
            return []
    if retry_count == max_retries:
        print(f"Échec après {max_retries} tentatives. Veuillez vérifier votre code.")
    
    return values_list  # Return the list of values


# In[3]:




def get_carac(info_elements, element_name):
    max_retries = 3
    retry_count = 0
    values_list = []  # Initialize an empty list to store the values
    
    while retry_count < max_retries:
        try:
            # Wait for the elements to be present
            elements_list = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, info_elements))
            )
            
            for info_p in elements_list:
                try:
                    info = info_p.text

                    # Diviser les informations en parties
                    info_parts = info.split('\n')

                    # Assigner les parties aux variables appropriées
                    carburant = info_parts[0].strip() if len(info_parts) > 0 else ""
                    kilometrage = info_parts[1].strip().replace(' Km', '') if len(info_parts) > 1 and info_parts[1].strip() != "" else 0
                    annee = info_parts[2].strip() if len(info_parts) > 2 else 0
                    boite_vitesse = info_parts[3].strip() if len(info_parts) > 3 else ""
                    departements = info_parts[4].strip() if len(info_parts) > 4 else ""

                    # Utilisez ces variables comme bon vous semble
                    values_list.append({
                        "Carburant": carburant,
                        "Kilométrage": kilometrage,
                        "Année": annee,
                        "Boîte de vitesse": boite_vitesse,
                        "Departements": departements
                    })
                
                except StaleElementReferenceException:
                    # Handle StaleElementReferenceException by re-finding the elements
                    pass
                except TimeoutException:
                    print(f"Timeout waiting for {element_name} elements to be present.")
                    return []
            break  # If successful, exit the loop
            
        except NoSuchElementException as e:
            print(f"Une erreur s'est produite lors de la récupération des informations ({element_name}) : {e}")
            retry_count += 1
            time.sleep(3)  # Wait for a short time before retrying

    if retry_count == max_retries:
        print(f"Échec après {max_retries} tentatives. Veuillez vérifier votre code.")
    
    return values_list  # Return the list of values


# In[4]:


import csv
import os

def write_to_csv(csv_file_path, modele_list, marque_list, date_list, loc_list, modified_prix_list, carac_list):
    # Check if the CSV file is empty
    file_exists = os.path.isfile(csv_file_path) and os.path.getsize(csv_file_path) > 0

    # Open the CSV file in append mode
    with open(csv_file_path, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # If the file is empty, write column names
        if not file_exists:
            column_names = [
                'Modele',
                'Marque',
                'Date',
                'Location',
                'Prix',
                'Carburant',
                'Kilométrage',
                'Année',
                'Boîte de vitesse',
                'Departements'
            ]
            csv_writer.writerow(column_names)

        # Check if the lengths of all lists are the same
        if all(len(lst) == len(modele_list) for lst in [marque_list, date_list, loc_list, modified_prix_list, carac_list]):
            # Iterate over the lists and write data for each entry
            for i in range(len(modele_list)):
                data = [
                    modele_list[i],
                    marque_list[i],
                    date_list[i],
                    loc_list[i],
                    modified_prix_list[i],
                    carac_list[i]["Carburant"],
                    carac_list[i]["Kilométrage"],
                    carac_list[i]["Année"],
                    carac_list[i]["Boîte de vitesse"],
                    carac_list[i]["Departements"]
                ]
                csv_writer.writerow(data)
            print("+1")
        else:
            print("Error: Length mismatch in lists. Data not written to CSV.")


# In[5]:


def action_aleatoire(driver):
    actions_possibles = ["scroll_full", "scroll_half", "move_to_element"]
    action_choisie = random.choice(actions_possibles)

    # Enregistrer la position actuelle de la page
    current_scroll_position = driver.execute_script("return window.pageYOffset;")

    if action_choisie == "scroll_full":
        # Action aléatoire : Faites défiler la page vers le bas
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    elif action_choisie == "scroll_half":
        # Action aléatoire : Faites défiler la moitié de la page vers le bas
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    elif action_choisie == "move_to_element":
        # Action aléatoire : Bougez la souris vers un élément aléatoire (par exemple, div de class PriceInformation_classifiedPrice__b-Jae)
        wait = WebDriverWait(driver, 10)
        element_to_move = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'center')))
        driver.execute_script("arguments[0].scrollIntoView();", element_to_move)

    # Revenir à la position enregistrée
    driver.execute_script(f"window.scrollTo(0, {current_scroll_position});")


# In[6]:


def initialize_driver() -> webdriver.Firefox:
    ua = UserAgent()
    user_agent = ua.random

    options = Options()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Firefox(options=options)
    return driver


# In[13]:


def scrape_page(driver, base_url, csv_file_path):
    try:
        driver.get(base_url)

        while True:
            time.sleep(random.uniform(15, 20))

            modele_list = get_info_elements(".//div[contains(@class, 'block-title-list')]//span[contains(@class, 'sub-title title-block three-dots')][1]", "modèle_list")
            marque_list = get_info_elements(".//div[contains(@class, 'block-title-list')]//span[contains(@class, 'title-block brand three-dots')]", "marque_list")
            date_list = get_info_elements(".//div[contains(@class, 'loc-date')]//p[contains(@class, 'btn-publication show-before')]", "date_elements")
            loc_list = get_info_elements(".//div[contains(@class, 'loc-date')]//div[contains(@class, 'location three-dots')]//span[contains(@class, 'upper')]", "loc_elements")
            prix_list = get_info_elements(".//div[contains(@class, 'title-n-price')]//div[contains(@class, 'price-block ')]//p[contains(@class, 'prix')]", "prix_list")
            modified_prix_list = [price.strip() for price in prix_list if 'prix initial' not in price]
            carac_list = get_carac(".//div[contains(@class, 'bc-info clearfix bigScreen')]", "info_elements")

            if len(modele_list) == len(marque_list) == len(date_list) == len(loc_list) == len(modified_prix_list):
                write_to_csv(csv_file_path, modele_list, marque_list, date_list, loc_list, modified_prix_list, carac_list)

            btn_next = driver.find_element(By.CLASS_NAME, 'btn-next') if driver.find_elements(By.CLASS_NAME, 'btn-next') else None

            if btn_next:
                btn_next.click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                print("\n---\n")
            else:
                break

    except TimeoutException as te:
        print(f"TimeoutException: {te}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


# # Scrappe

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.firefox.options import Options
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# from fake_useragent import UserAgent
# import time
# import random
# import csv
# import os
# ua = UserAgent()
# 
# user_agent = ua.random
# 
# options = Options()
# options.add_argument('--headless')
# options.add_argument(f'user-agent={user_agent}')
# 
# driver = webdriver.Firefox(options=options)
# base_url = "https://www.leparking.be/voiture-occasion/#!/voiture-occasion/%3Fid_pays%3D1%7C6%7C18%7C32"
# 
# 
# 
# driver.get(base_url)
# csv_file_path = "parking.csv"
# 
# while True:
#     time.sleep(random.uniform(5, 10))
#     
#     # Scrape
#     modele_list = get_info_elements(".//div[contains(@class, 'block-title-list')]//span[contains(@class, 'sub-title title-block three-dots')][1]", "modèle_list")
#     marque_list = get_info_elements(".//div[contains(@class, 'block-title-list')]//span[contains(@class, 'title-block brand three-dots')]", "marque_list")
#     date_list = get_info_elements(".//div[contains(@class, 'loc-date')]//p[contains(@class, 'btn-publication show-before')]", "date_elements")
#     loc_list = get_info_elements(".//div[contains(@class, 'loc-date')]//div[contains(@class, 'location three-dots')]//span[contains(@class, 'upper')]", "loc_elements")
#     prix_list = get_info_elements(".//div[contains(@class, 'title-n-price')]//div[contains(@class, 'price-block ')]//p[contains(@class, 'prix')]", "prix_list")
#     modified_prix_list = [price.strip() for price in prix_list if 'prix initial' not in price]
#     carac_list = get_carac(".//div[contains(@class, 'bc-info clearfix bigScreen')]", "info_elements")
#     #CSV appending
#     if len(modele_list) == len(marque_list)  == len(date_list) == len(loc_list) == len(modified_prix_list):
#         # Open the CSV file for appending
#         write_to_csv(csv_file_path, modele_list, marque_list, date_list, loc_list, modified_prix_list, carac_list)
#     # Pagination
#     try:
#         btn_next = driver.find_element(By.CLASS_NAME, 'btn-next') if driver.find_elements(By.CLASS_NAME, 'btn-next') else None
# 
#         if btn_next:
#             btn_next.click()
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.TAG_NAME, 'body'))
#             )
#             
#             
#             print("\n---\n")
#         else:
#             break
# 
#     except TimeoutException as e:
#         print(f"TimeoutException: {e}")
#         break
#     except Exception as e:
#         print(f"Une erreur s'est produite : {e}")
# 
# # Fermez le navigateur à la fin
# driver.quit()
# 

# # Scrappe 

# In[8]:


base_url = "https://www.leparking.be/voiture-occasion/#!/voiture-occasion/%3Fid_pays%3D84"

csv_file_path = "parking_ind.csv"



# In[9]:


driver = initialize_driver()
scrape_page(driver, base_url, csv_file_path)




