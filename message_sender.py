import pandas as pd
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def connect_db():
    return sqlite3.connect('contactos.db')

def get_contacts_from_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT telefono FROM contactos")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def send_messages(message, confirm_whatsapp_linked):
    if not message:
        return "Error: Por favor, escribe un mensaje."

    # Obtener los números de teléfono desde la base de datos
    contactos = get_contacts_from_db()
    if not contactos:
        return "Error: No se encontraron contactos en la base de datos."

    # Configuración de Selenium
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://web.whatsapp.com')
    confirm_whatsapp_linked()

    for numero in contactos:
        url = f"https://web.whatsapp.com/send?phone={numero}&text={message}"
        
        driver.get(url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
        )
        
        send_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        
        send_button.click()
        
        time.sleep(2)

    driver.quit()
    return "Éxito: Los mensajes han sido enviados."