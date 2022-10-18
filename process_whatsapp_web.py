import time
from manage_images import is_id_in_db
from selenium.webdriver.common.by import By

def process_message( message, driver, db_path ):
    img_id = message.get_attribute("data-id")
    
    if is_id_in_db( img_id, db_path ) == False:
        try:
            imgs = message.find_elements(
                by=By.XPATH, 
                value='//div[@data-testid="image-thumb"]'
            )
        except:
            imgs = []

        for img in imgs:
            img.click()
            time.sleep(0.5)

            try:
                download_button = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='div[title="Download"]'
                )
                download_button.click()
            except:
                menu_button = driver.find_element(
                    by=By.CSS_SELECTOR,
                    value='div[title="Download"]'
                )

            time.sleep(0.5)

            close_button = driver.find_element(
                by=By.CSS_SELECTOR,
                value='div[title="Schließen"]'
            )

            close_button.click()
            time.sleep(1.5)
            
        return img_id
    else:
        raise Exception("img already in db")