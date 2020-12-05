from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
    
driver = webdriver.Chrome()
driver.get('https://fplreview.com/team-planner/#forecast_table')

team_id = driver.find_element_by_name('TeamID')
team_id.send_keys(123)
team_id.submit()

# wait for the ad to load
WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'orderModal_popop')))

# hide the ad
driver.execute_script("jQuery('#orderModal_popop').modal('hide');")

# export csv
WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div/div/div/div[1]/div/article/div[2]/div/button[6]')))
export_button = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/div/div[1]/div/article/div[2]/div/button[6]')
export_button.click()

# wait for download
time.sleep(3)

driver.quit()