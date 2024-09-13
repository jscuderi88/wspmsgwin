import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def send_messages(excel_file, message, confirm_whatsapp_linked):
    if not excel_file or not message:
        return "Error: Por favor, selecciona un archivo y escribe un mensaje."
    
    df = pd.read_excel(excel_file)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    driver.get('https://web.whatsapp.com')
    confirm_whatsapp_linked()

    for index, row in df.iterrows():
        numero = row['Número de Teléfono']
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
