import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from fake_useragent import UserAgent

# Configurations du navigateur
ua = UserAgent()
user_agent = ua.random
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
options.add_argument(f'user-agent={user_agent}')

# Initialisation du navigateur
driver = webdriver.Firefox(options=options)
base_url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page="
xpath_expression = "//a[contains(@class, 'Vehiculecard_Vehiculecard_vehiculeCard Containers_Containers_containers Containers_Containers_borderRadius Containers_Containers_darkShadowWide')]"

# Numéro de la première page à visiter
current_page = 0
data = []
# Boucle pour parcourir les pages
while True:
    # Construire l'URL de la page actuelle
    all_links = []
    url = base_url + str(current_page)
    time.sleep(random.uniform(2, 5))

    # Charger la page web
    driver.get(url)

    try:
        # Insérer ici le code pour extraire les liens ou effectuer d'autres opérations sur la page
        links = driver.find_elements(By.XPATH, xpath_expression)

        # Ajouter les liens à la liste
        all_links.extend(link.get_attribute("href") for link in links)

        # Parcourir chaque lien pour effectuer des opérations
        for link in all_links:
            try:
                # Afficher le lien trouvé
                print("Lien trouvé :", link)

                # Accéder à la page du lien
                driver.get(link)
                time.sleep(random.uniform(2, 5))

                # Insérer ici le code pour effectuer des opérations sur la page du lien

                try:
                    nom_xpath = "//div[contains(@class, 'Text_Text_text SummaryInformation_title__5CYhW Text_Text_headline3')]"
                    
                    nom = driver.find_element(By.XPATH, nom_xpath).text
                    print("Nom du véhicule:", nom)
                    time.sleep(random.uniform(2, 5))
                except NoSuchElementException:
                    # Si la div n'est pas trouvée sur la page du lien, afficher un message
                    nom = " "
                    print("aucun nom trouvé")
                
                data.append(nom)
                
                try:
                    carac_xpath = "//div[contains(@class, 'Text_Text_text SummaryInformation_subtitle__M7MAb Text_Text_body2')]"
                    carac = driver.find_element(By.XPATH, carac_xpath).text
                    print("Carac:", carac)

                    # Diviser le texte en éléments
                    elements = carac.split()

                    # Variables pour stocker les informations
                    cylindree_moteur = ""
                    type_moteur = ""
                    puissance = ""
                    finition = ""

                    # Utiliser un indicateur pour savoir quel type d'information on traite actuellement
                    current_type = None

                    # Parcourir les éléments et attribuer aux variables appropriées
                    for element in elements:
                        # Vérifier s'il s'agit de la cylindrée du moteur (exprimée en centimètres cubes)
                        if element.replace(".", "").isdigit() and not cylindree_moteur:
                            cylindree_moteur = element
                        # Vérifier s'il s'agit du type de moteur (contient des lettres)
                        elif any(char.isalpha() for char in element) and not type_moteur:
                            type_moteur = element
                        # Vérifier s'il s'agit de la puissance (contient des chiffres)
                        elif element.isdigit() and not puissance:
                            puissance = element
                        # Si ce n'est ni la cylindrée, ni le type, ni la puissance, c'est probablement la finition
                        elif not finition:
                            finition += element + " "
                    cylindree_moteur = cylindree_moteur.strip()
                    type_moteur = type_moteur.strip()
                    puissance = puissance.strip()
                    finition = finition.strip()
                    # Afficher les résultats
                    print("Cylindrée du moteur:", cylindree_moteur.strip())
                    print("Type de moteur:", type_moteur.strip())
                    print("Puissance:", puissance.strip())
                    print("Finition:", finition.strip())
        
                except NoSuchElementException:
                    # Si la div n'est pas trouvée sur la page du lien, afficher un message
                    carac = " "
                    print("Carac non trouvé")
                data.append(cylindree_moteur,type_moteur,puissance,finition)
                try:
                    prix_xpath = "//span[contains(@class, 'PriceInformation_classifiedPrice__b-Jae')]"
                    
                    prix = driver.find_element(By.XPATH, prix_xpath).text
                    print("prix:", prix)
                    time.sleep(random.uniform(2, 5))
                except NoSuchElementException:
                    # Si la div n'est pas trouvée sur la page du lien, afficher un message
                    prix = " "
                    print("aucun nom trouvé")
                data.append(prix)
                try:
                    duree_publi_xpath = "//div[contains(@class, 'Text_Text_text Text_Text_body2')]"
                    
                    duree_publi = driver.find_element(By.XPATH, duree_publi_xpath).text
                    print("publié depuis:",  duree_publi)
                    time.sleep(random.uniform(2, 5))
                except NoSuchElementException:
                    # Si la div n'est pas trouvée sur la page du lien, afficher un message
                    durée_publi = " "
                    print("no durée publi renseigné")
                data.append(duree_publi)
                try:
                    volume_coffre_xpath = "//div[contains(@class, 'Gauge_Gauge_gaugeWrapper')]//button[contains(@class, 'Gauge_Gauge_value Button_Button_button Button_Button_shaded Button_Button_small Button_Button_square')]//span[contains(@class, 'Text_Text_text Text_Text_label2')]"
                    volume_coffre_element = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located((By.XPATH, volume_coffre_xpath))
                    )

                    volume_coffre = volume_coffre_element.get_attribute('textContent')
                    print("volume_coffre", volume_coffre)
                    time.sleep(random.uniform(2, 5))
                except NoSuchElementException:
                    # Si la div n'est pas trouvée sur la page du lien, afficher un message
                    volume_coffre = " "
                    print("no volume_coffrerenseigné")
                except TimeoutException:
                    # Gérer la TimeoutException ici
                    print("Élément non trouvé après 15 secondes. Continuer avec le reste du code.")
                    volume_coffre = " "
                    
                data.append(volume_coffre)
                
                try:
                    spans_xpath = "//span[contains(@class, 'Text_Text_text Icon-button_IconButton_label Text_Text_label2')]"

                    spans = driver.find_elements(By.XPATH, spans_xpath)
                    
    # Nombre de spans
                    num_spans = len(spans)

    # Créer des variables dynamiquement
                    point_forts_values = []

                    for index, span in enumerate(spans, start=1):
                        try:
                            # Utilisation de JavaScript pour extraire le texte
                            span_text = driver.execute_script("return arguments[0].textContent;", span)
                            variable_name = f"point_fort{index}"
                            locals()[variable_name] = span_text.strip()
                            print(f"{variable_name}:", locals()[variable_name])

                            # Ajouter la valeur du point fort à la liste
                            point_forts_values.append(locals()[variable_name])

                            time.sleep(random.uniform(2, 5))
                        except NoSuchElementException:
                            # Si la div n'est pas trouvée sur la page du lien, afficher un message
                            variable_name = f"point_fort{index}"
                            locals()[variable_name] = " "
                            print(f"{variable_name}: not found")
                            # Ajouter la valeur du point fort à la liste
                            point_forts_values.append(locals()[variable_name])

                    # Ajouter le tuple de valeurs des points forts à la liste data
                        data.append(tuple(point_forts_values))
                
                 
                
                        h3_values = []
                        

                        try:
                            h3_xpath = "//h3[contains(@class, 'Text_Text_text Text_Text_subtitle1')]"
                            h3_elements = driver.find_elements(By.XPATH, h3_xpath)

                            time.sleep(random.uniform(2, 5))

                            for h3_element in h3_elements:
                                try:
                                    ul_element = h3_element.find_element(By.XPATH, "following-sibling::ul")
                                    li_elements = ul_element.find_elements(By.XPATH, "li")

                                        # Initialiser une liste pour stocker les valeurs des éléments LI
                                    li_values = []

                                    for index, li_element in enumerate(li_elements, start=0):
                                        time.sleep(random.uniform(2, 5))

                                        try:
                                                # Essayer de trouver le texte du span directement
                                            first_span_xpath = ".//span[contains(@class, 'Text_Text_text Text_Text_subtitle2')]"
                                            first_span_element = find_element_with_retry(li_element, By.XPATH, first_span_xpath)
                                            variable_name = first_span_element.get_attribute('textContent')

                                            span_xpath = ".//span[@class='Item_content__Xyd3d']"
                                            span_element = find_element_with_retry(li_element, By.XPATH, span_xpath)
                                            variable_value = span_element.get_attribute('textContent')

                                        except NoSuchElementException:
                                                # Si le premier essai échoue, essayer de trouver le texte du span à l'intérieur
                                            span_xpath = ".//span[@class='Item_content__Xyd3d']//span"
                                            span_element = find_element_with_retry(li_element, By.XPATH, span_xpath)
                                            variable_value = span_element.get_attribute('textContent')

                                            # Ajouter le tuple de valeurs des éléments LI à la liste
                                        li_values.append((variable_name, variable_value))

                                        # Ajouter le tuple de valeurs des éléments H3 à la liste
                                    h3_values.append(tuple(li_values))

                                except NoSuchElementException:
                                    print("UL ou LI non trouvé pour cet élément H3")

                        except NoSuchElementException:
                            print("H3 non trouvé")

                            # Ajouter le tuple de valeurs des éléments H3 à la liste data
                        data.append(tuple(h3_values))
                
                ########################EN COURS######################  
                        try:
                            # Attendre que le bouton soit cliquable
                            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_button_options)))

                            # Utiliser ActionChains pour survoler et cliquer sur le bouton
                            action = ActionChains(driver)
                            action.move_to_element(button).click().perform()

                            print("Button clicked successfully")

                        except NoSuchElementException:
                            print(f"Button with XPath '{xpath_button_options}' not found")
                        except Exception as e:
                            print(f"An error occurred: {e}")

                        ####Scrappe equipement####
                        # Dictionnaire pour stocker les résultats
                        results = {}

                        

                        # XPath pour sélectionner les uls
                        ul_xpaths = "//ul[contains(@class, 'EquipmentOptionsInformation_column__rQp-a')]"

                        # Parcourir les uls
                        uls = driver.find_elements(By.XPATH, ul_xpaths)

                        # Parcourir chaque ul
                        for ul_index, ul_element in enumerate(uls, start=1):
                            try:
                                # Trouver tous les li dans l'ul actuel
                                li_elements = ul_element.find_elements(By.XPATH, "./li")

                                # Parcourir chaque li
                                for li_index, li_element in enumerate(li_elements, start=1):
                                    # Obtenir tous les éléments h3 et div à l'intérieur du li
                                    h3_elements = li_element.find_elements(By.XPATH, "./h3")
                                    div_elements = li_element.find_elements(By.XPATH, "./div")

                                    # Concaténer les textcontents de tous les h3 et div
                                    li_textcontent = " ".join(element.get_attribute('textContent') for element in h3_elements + div_elements)
                                    
                                    # Ajouter le résultat au dictionnaire
                                    results[f"ul{ul_index}_li{li_index}"] = f",{li_textcontent}"

                            except NoSuchElementException:
                                print("UL non trouvé")

                        # Afficher les résultats
                        #for key, value in results.items():
                            #print(f"{key}: {value}")
                        
                        # Ajouter le tuple de valeurs des résultats à la liste data
                        data.append(tuple(results.values()))

                        
                        print(data)


        except StaleElementReferenceException:
                # Si l'élément de lien est obsolète, afficher un message
            print("StaleElementReferenceException pour le lien :", link)

    except NoSuchElementException:
        # Si l'élément n'est pas trouvé, cela signifie probablement que la page n'existe pas
        print("Fin de la boucle : La page", current_page, "n'existe pas.")
        break

    # Passer à la page suivante
    current_page += 1

# Fermer le navigateur à la fin
driver.quit()
