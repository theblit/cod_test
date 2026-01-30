from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configuration du navigateur
driver = webdriver.Chrome()  # Assure-toi que chromedriver est installé

# 001 - Accès à la page d'accueil
driver.get("http://127.0.0.1")
assert "Page d'accueil" in driver.page_source

# 002 - Inscription avec email existant
driver.find_element(By.ID, "email").send_keys("Kaloushkaorelie@gmail.com")
driver.find_element(By.ID, "submit").click()
assert "Connexion" in driver.page_source

# 003 - Inscription avec email inexistant
driver.find_element(By.ID, "email").clear()
driver.find_element(By.ID, "email").send_keys("Kaloushka@gmail.com")
driver.find_element(By.ID, "submit").click()
assert "erreur sur adresse gmail inexistante" in driver.page_source

# 004 - Identification sans identifiants
driver.find_element(By.ID, "submit").click()
assert "Erreur d'identification" in driver.page_source

# 007 - Connexion avec identifiants corrects
driver.find_element(By.ID, "email").clear()
driver.find_element(By.ID, "email").send_keys("Kaloushkaorelie@gmail.com")
driver.find_element(By.ID, "password").send_keys("Kaloushka05")
driver.find_element(By.ID, "submit").click()
assert "Connexion" in driver.page_source

# 008 - Paiement sans connexion
driver.get("http://127.0.0.1/paiement")
assert "page de connexion" in driver.page_source

# 012 à 015 - Navigation onglets
driver.find_element(By.LINK_TEXT, "Accueil").click()
assert "Page d'accueil" in driver.page_source

driver.find_element(By.LINK_TEXT, "Deals").click()
assert "Deals" in driver.page_source

driver.find_element(By.LINK_TEXT, "A propos").click()
assert "A propos" in driver.page_source

driver.find_element(By.LINK_TEXT, "Contact").click()
assert "Contact" in driver.page_source

# Fermeture du navigateur
driver.quit()


# test_selenium.py
def test_dummy():
    assert True
