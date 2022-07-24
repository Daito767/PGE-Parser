import time

from ColoredText import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import json


class ParserJumpPGE:
    def __init__(self):
        self.URL1 = 'https://geomartx.cloud.pge.com/arcgis/rest/services/JUMP/JumpViewer/MapServer/1/query?f=json&resultRecordCount=5&where=SAPEQUIPID=%27{sap_id}%27&outFields=BARCODE,CLASS,HEIGHT,INSTALLATIONDATE,JPNUMBER,JPSEQUENCE,SPECIES,GPSLATITUDE,GPSLONGITUDE,LOCDESC1&returnGeometry=false'
        self.URL2 = "https://api.cloud.pge.com/Electric/Poles/v1/PTTJump/ZIPTT_INPUTSet?$filter=Equnr eq '{sap_id}'&$expand=NAVINPUTINSPECTION&$format=json"

        options = FirefoxOptions()
        options.set_preference('devtools.jsonview.enabled', False)

        self.driver = webdriver.Firefox(executable_path=r'C:\\Users\\ghimc\\Downloads\\Mozilla Driver\\geckodriver.exe', options=options)
        self.email = ''
        self.password = ''

    def user_login(self, email: str, password: str, login_url: str = 'https://www3.pge.com/jump') -> bool:
        print_yellow('[INFO]')
        print(' User login started')

        self.email = email
        self.password = password

        try:
            self.driver.get(login_url)

            self.driver.implicitly_wait(10)

            email = self.driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/section/div/div/div/div/form/div[1]/input')
            email.clear()
            email.send_keys(self.email)

            password = self.driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/section/div/div/div/div/form/div[2]/input')
            password.clear()
            password.send_keys(self.password)

            login_btn = self.driver.find_element(By.XPATH, '/html/body/div/div/div[3]/div/div/div/section/div/div/div/div/form/button')
            login_btn.click()

            try:
                self.driver.implicitly_wait(5)
                element = self.driver.find_element(By.XPATH, 'errorLoginServer')
                if element.is_displayed():
                    print_red('[ERROR]')
                    print(f' Please enter a valid Username and/or Password')
                else:
                    print_green('[INFO]')
                    print(f' User authentication was successful')

                return False

            except Exception as e:
                print_green('[INFO]')
                print(f' User authentication was successful')

                return True

        except Exception as e:
            print_red('[ERROR]')
            print(f' User login failed. {e}')

            return False

    def collect_general_pole_data(self, sap_id: str) -> dict:
        try:
            url = self.URL1.format(sap_id=sap_id)
            self.driver.get(url)

            result = json.loads(self.driver.find_element(By.XPATH, '/html/body/pre').text)['features'][0]['attributes']

            return result

        except Exception as e:
            print_yellow('[ERROR]')
            print(f' Error collecting general data. Sap ID: {sap_id}. {e}')

    def collect_inspection_pole_data(self, sap_id: str) -> dict:
        try:
            url = self.URL2.format(sap_id=sap_id)
            self.driver.get(url)
            result = json.loads(self.driver.find_element(By.XPATH, '/html/body/pre').text)['d']['results'][0]['NAVINPUTINSPECTION']['results']

            return result

        except Exception as e:
            print_yellow('[ERROR]')
            print(f' Error collecting inspection data. Sap ID: {sap_id}. {e}')

