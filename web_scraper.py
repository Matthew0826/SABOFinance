from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

class WebScraper():
    def __init__(self):
        # Path to the ChromeDriver executable
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)

    def submit_reimbursement(self, user, request, cost, id ):
        
        files_to_submit = []
        # Send the path of the file to upload
        for root, dirs, files in os.walk(r"/root/SABOFinance/temp_" + str(id)):
                for name in files:
                    files_to_submit.append( root + "/" + name )

        if( len( files_to_submit ) == 0 ):
            return

        self.driver.get("https://sabo.studentlife.northeastern.edu/sabo-expense-reimbursement-voucher/")

        for i in range( 1, 8 ):
            self.driver.find_element(By.NAME, f'input_155.{i}').click()
            time.sleep(.1)

        name = user["Name"].split(' ')

        self.driver.find_element(By.NAME, f'input_2.3').send_keys(name[0])
        self.driver.find_element(By.NAME, f'input_2.6').send_keys(name[1])

        self.driver.find_element(By.NAME, f'input_76').send_keys(user["NUId"])
        self.driver.find_element(By.NAME, f'input_97').send_keys(user["Street/PO Box"])
        self.driver.find_element(By.NAME, f'input_94').send_keys(user["City"])
        self.driver.find_element(By.NAME, f'input_95').send_keys( Keys.BACKSPACE + Keys.BACKSPACE + user["State"] )
        self.driver.find_element(By.NAME, f'input_96').send_keys(user["Zip Code"])

        self.driver.find_element(By.NAME, f'input_13').click()

        purpose = request["Project"] + ("" if request["Subteam"] == "" else " (" + request["Subteam"] + ")")
        self.driver.find_element(By.NAME, f'input_141').send_keys(purpose)

        self.driver.find_element(By.NAME, f'input_142').send_keys(request["Description"])

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'input_11'))
        )
        element.send_keys(datetime.now().strftime(str("%m/%d/%Y")))

        index_number = "800376" if request["Budget Index"] == "Budget Account" else "830561"
        self.driver.find_element(By.NAME, f'input_16').send_keys(index_number)
        self.driver.find_element(By.NAME, f'input_17').send_keys(request["Account"][0:5])
        self.driver.find_element(By.NAME, f'input_18').send_keys(cost)

        # Locate the checkbox using its ID
        checkbox = self.driver.find_element(By.ID, 'choice_2_156_1')

        # Click the checkbox
        self.driver.execute_script("arguments[0].click();", checkbox)

        # Find the hidden file input element
        file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')

        for file in files_to_submit:
            file_input.send_keys(file)  


        self.driver.find_element(By.NAME, f'input_81.3').send_keys(name[0])
        self.driver.find_element(By.NAME, f'input_81.6').send_keys(name[1])
        self.driver.find_element(By.NAME, f'input_98').send_keys(user["Email"])
        self.driver.find_element(By.NAME, f'input_153').send_keys(user["Phone Number"])

        self.driver.find_element(By.NAME, f'input_165.3').send_keys("Matthew")
        self.driver.find_element(By.NAME, f'input_165.6').send_keys("Geisel")
        self.driver.find_element(By.NAME, f'input_166').send_keys("geisel.m@northeastern.edu")

        self.driver.find_element(By.NAME, f'input_64.3').send_keys("Peter")
        self.driver.find_element(By.NAME, f'input_64.6').send_keys("Whitney")
        self.driver.find_element(By.NAME, f'input_65').send_keys(Keys.BACKSPACE*20 + "j.whitney@northeastern.edu")

        checkbox = self.driver.find_element(By.NAME, f'input_99.1')
        self.driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(10)

        #This is the final submit button
        final_button = self.driver.find_element(By.ID, f'gform_submit_button_2')
        self.driver.execute_script("arguments[0].click();", final_button)  

if __name__ == '__main__':
    w = WebScraper()
    w.submit_reimbursement( {"Name": "Matthew Geisel"})
