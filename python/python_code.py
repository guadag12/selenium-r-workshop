import random
from bs4 import BeautifulSoup
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import re

## Páginas a descargar info:
paginas = [
           "https://www.sothebys.com/en/auctions/2012/latin-american-art-n08862.html",
           "https://www.sothebys.com/en/auctions/2012/latin-american-art-n08907.html",
           "https://www.sothebys.com/en/auctions/2013/latin-american-art-n08998.html",
           "https://www.sothebys.com/en/auctions/2013/latin-american-art-n09044.html",
           "https://www.sothebys.com/en/auctions/2014/latin-american-art-n09152.html",
           "https://www.sothebys.com/en/auctions/2014/latin-american-art-n09223.html",
           "https://www.sothebys.com/en/auctions/2014/mexico-contemporary-n09228.html",
           "https://www.sothebys.com/en/auctions/2015/latin-america-legacy-of-abstraction-n09353.html",
           "https://www.sothebys.com/en/auctions/2015/latin-american-art-modern-contemporary-n09355.html",
           "https://www.sothebys.com/en/auctions/2015/latin-america-modern-art-n09428.html",
           "https://www.sothebys.com/en/auctions/2015/latin-america-modern-contemporary-art-n09508.html",
           "https://www.sothebys.com/en/auctions/2016/latin-america-modern-contemporary-art-n09579.html",
           "https://www.sothebys.com/en/auctions/2017/latin-american-modern-art-evening-sale-n09682.html",
           "https://www.sothebys.com/en/auctions/2017/latin-american-contemporary-art-n09769.html",
           "https://www.sothebys.com/en/auctions/2017/contemporary-art-day-auction-n09714.html",
           "https://www.sothebys.com/en/auctions/2017/latin-america-modern-art-n09683.html",
           "https://www.sothebys.com/en/auctions/2018/impressionist-modern-art-evening-sale-n09860.html",
           "https://www.sothebys.com/en/auctions/2018/impressionist-modern-art-day-sale-n09861.html",
           "https://www.sothebys.com/en/auctions/2018/contemporary-art-evening-auction-n09858.html",
           "https://www.sothebys.com/en/auctions/2018/contemporary-art-day-auction-n09859.html",
           "https://www.sothebys.com/en/auctions/2018/latin-online-chappard-n09863.html",
           "https://www.sothebys.com/en/auctions/2018/18028-contemporary-art-online.html",
           "https://www.sothebys.com/en/auctions/2018/contemporary-curated-n09909.html",
           "https://www.sothebys.com/en/auctions/2018/contemporary-art-online-september-n09910.html",
           "https://www.sothebys.com/en/auctions/2018/impressionist-modern-art-evening-sale-n09930.html",
           "https://www.sothebys.com/en/auctions/2018/impressionist-modern-art-evening-sale-n09930.html",
           "https://www.sothebys.com/en/auctions/2018/contemporary-art-evening-sale-n09932.html",
           "https://www.sothebys.com/en/auctions/2018/contemporary-art-day-sale-n09933.html",
           "https://www.sothebys.com/en/auctions/2019/contemporary-curated-n10027.html",
           "https://www.sothebys.com/en/auctions/2019/impressionist-modern-art-evening-n10067.html",
           "https://www.sothebys.com/en/auctions/2019/impressionist-modern-art-day-n10068.html",
           "https://www.sothebys.com/en/auctions/2019/contemporary-art-evening-auction-n10069.html",
           "https://www.sothebys.com/en/auctions/2019/contemporary-art-day-n10070.html",
           "https://www.sothebys.com/en/auctions/2019/contemporary-curated-n10116.html",
           "https://www.sothebys.com/en/auctions/2019/impressionist-modern-art-evening-n10147.html",
           "https://www.sothebys.com/en/auctions/2019/impressionist-modern-art-day-n10148.html",
           "https://www.sothebys.com/en/auctions/2019/contemporary-art-evening-n10149.html",
           "https://www.sothebys.com/en/auctions/2019/contemporary-art-day-n10150.html",           
           "https://www.sothebys.com/en/auctions/2020/contemporary-curated-n10321.html" 
]

### Inicializa el navegador y entrar al LOG IN
driver = webdriver.Chrome()

# Abre la página de Sotheby's
driver.get("https://www.sothebys.com/en/auctions/2012/latin-american-art-n08862.html")

# Espera a que la página se cargue completamente
time.sleep(5)  # Ajusta el tiempo según sea necesario

# Encuentra el botón 'LOG IN' usando el XPath y haz clic en él
log_in_button = driver.find_element(By.XPATH, '//a[@data-text-content="Log In"]')
log_in_button.click()

# Espera a que la página de inicio de sesión se cargue
time.sleep(5)  # Ajusta el tiempo según sea necesario

# Encuentra el campo de email y contraseña, luego ingresa las credenciales
email_field = driver.find_element(By.XPATH, '//input[@placeholder="Email address"]')
password_field = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')

email_field.send_keys("xxxxxxxxx@xxxxxx.xxx")
password_field.send_keys("xxxxxxxxxxxxxxxxxx")

time.sleep(5)  # Ajusta el tiempo según sea necesario

# Encuentra y haz clic en el botón de 'Log in' por ID
login_button = driver.find_element(By.ID, 'login-button-id')
login_button.click()

## Se inicializan las tablas:
columns_ = ["Author",
                    "Title",
                    "Min Estimate",
                    "Max Estimate",
                    "Sold Price",
                    "Auction Title",
                    "Auction Date",
                    "Sale Total",
                    "Sale Number",
                    "Lots Count", 
                    "Web",
                    "Web Number",
                    'Code',
                    'Year']
df_empty_total=pd.DataFrame(columns= columns_)
df_empty_data=pd.DataFrame(columns= columns_)

numero = 0

###### Loop para todas las páginas
for web in paginas: 
    print(web, ",", numero)
    year = re.search(r'/(\d{4})/', web).group(1)
    code = re.search(r'/([^/]+)\.html', web).group(1)
    # Encuentra y haz clic en el botón de 'Log in'
    time.sleep(5)  # Ajusta el tiempo según sea necesario
    columns_ = ["Author", "Title","Min Estimate","Max Estimate","Sold Price","Auction Title","Auction Date","Sale Total",
                "Sale Number", "Lots Count", "Web","Web Number",'Code', 'Year']
    df_empty_data=pd.DataFrame(columns= columns_)
    numero = 0

    try: 
        driver.get(web)
        
        # Encuentra el último número de página en la paginación
        try:
            last_page_number = int(driver.find_element(By.XPATH, '//a[@class="with-border "][last()]').text)
        except Exception as e:
            print(f"Error al obtener el número de páginas: {e}")
            last_page_number = 1
        
        for i in range(1, last_page_number + 1): 
            pagina_numero = i 
            time.sleep(2)  # Ajusta el tiempo según sea necesario
            
            # Refresca la página con el nuevo número de página
            driver.get(f"{web}?p={i}")
            time.sleep(2)
            
            try:
                # Verificar si aparece el mensaje "Log in to view sale total"
                sale_total_message = driver.find_element(By.XPATH, '//div[@class="AuctionsModule-auction-info-total"]//div[contains(text(), "Log in to view sale total")]')
                if sale_total_message.is_displayed():
                    # Si aparece, refrescar la página una vez
                    print("Mensaje 'Log in to view sale total' encontrado, refrescando la página...")
                    driver.refresh()
                    time.sleep(5)
                    
            except Exception as e:
                print(f"No se encontró el mensaje 'Log in to view sale total'")
            
            # Extraer la información de las obras de arte
            artworks = driver.find_elements(By.XPATH, '//li[@class="AuctionsModule-results-item"]')    
            artworks_info = []
            
            for artwork in artworks:
                try:
                    author = artwork.find_element(By.XPATH, './/div[@class="title "]/a').text.split(". ")[1].strip()
                except:
                    author = "N/A"
                
                try:
                    title = artwork.find_element(By.XPATH, './/div[@class="description"]').text.strip()
                except:
                    title = "N/A"

                try:
                    estimate_text = artwork.find_element(By.XPATH, './/div[@class="estimate"]').text.replace("Estimate: ", "").strip()
                    min_estimate, max_estimate = estimate_text.replace("USD", "").strip().split(" – ")
                except:
                    min_estimate, max_estimate = "N/A", "N/A"
                
                try:
                    sold_price = artwork.find_element(By.XPATH, './/div[@class="sold"]').text.replace("Lot Sold: ", "").strip()
                except:
                    sold_price = "N/A"
                try: 
                    auction_title = driver.find_element(By.XPATH, '//div[@class="AuctionsModule-auction-title"]').text
                except:
                    auction_title = "N/A"
                try: 
                    auction_date = driver.find_element(By.XPATH, '//div[@class="AuctionsModule-auction-info"]').text
                except:
                    auction_date = "N/A"
                try: 
                    sale_total = driver.find_element(By.XPATH, '//div[@class="AuctionsModule-auction-info-totalPrice"]').text
                except:
                    sale_total = "N/A"
                try: 
                    sale_number = driver.find_element(By.XPATH, '//div[@class="AuctionsModule-auction-info-saleNumber"]').text
                except:
                    sale_number = "N/A"
                try: 
                    lots_count = driver.find_element(By.XPATH, '//div[@class="AuctionsModule-lotsCount"]').text
                except:
                    lots_count = "N/A"
                
                # Añade la información de la obra de arte a la lista
                artworks_info.append({
                    "Author": author,
                    "Title": title,
                    "Min Estimate": min_estimate,
                    "Max Estimate": max_estimate,
                    "Sold Price": sold_price,
                    "Auction Title":auction_title,
                    "Auction Date":auction_date,
                    "Sale Total":sale_total,
                    "Sale Number":sale_number,
                    "Lots Count":lots_count, 
                    "Web":web,
                    "Web Number":pagina_numero,
                    'Code':code,
                    'Year':year
                })
            df=pd.DataFrame(artworks_info)
            df["Auction Date"] = df["Auction Date"].str.replace('•', ';').str.strip()
            df["Auction Date"] = df["Auction Date"].str.replace('\n', ';').str.strip()            

            df_empty_total = pd.concat([df_empty_total, df], ignore_index=True)
            df_empty_data = pd.concat([df_empty_data, df], ignore_index=True)

            print(f"Datos extraídos de la página {i} de {web}")
            df_empty_total.to_excel("C:/Users/Usuario/Documents/GitHub/mora-descarga/df_old_empty.xlsx", index=False)
        df_empty_data.to_excel(f"C:/Users/Usuario/Documents/GitHub/mora-descarga/old_lots/{year}_{code}.xlsx", index=False)
    except Exception as e:
        print(f"Error procesando la web {web}: {e}")

    numero += 1
