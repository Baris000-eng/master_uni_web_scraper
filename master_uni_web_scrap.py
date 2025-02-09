import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
options = Options()
options.add_argument("--headless")  # Run browser in headless mode (without opening a window)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = "https://www.topuniversities.com/world-university-rankings?page="

all_universities = []

driver.get(f"{base_url}1")

# Find the last page number 
pagination = driver.find_elements(By.CSS_SELECTOR, ".pagination a")
if not pagination:
    print("Pagination not found!")
    driver.quit()
    exit()

last_page_number = int(pagination[-2].text)  


for page_num in range(1, last_page_number + 1):
    print(f"Scraping page {page_num}...")  
    
    # Open the current page
    driver.get(f"{base_url}{page_num}")
    
    # Wait until university names are present on the page 
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".uni-link")))
    except Exception as e:
        print(f"Error on page {page_num}: {str(e)}")
        continue  
    
    # Find all universities on the current page 
    university_names = driver.find_elements(By.CSS_SELECTOR, ".uni-link")
    university_locations = driver.find_elements(By.CSS_SELECTOR, ".location")
    university_ranks = driver.find_elements(By.CSS_SELECTOR, ".rank-no")
    university_scores = driver.find_elements(By.CSS_SELECTOR, ".rank-score.di-inline")  
    
    print(f"Found {len(university_names)} universities on page {page_num}")
    
    # Continue to next page if no universities are found
    if not university_names:
        print(f"No universities found on page {page_num}, skipping.")
        continue

    for name, rank, location, score in zip(university_names, university_ranks, university_locations, university_scores):
        all_universities.append({
            "name": name.text,
            "rank": rank.text,
            "location": location.text,
            "overall_score": score.text,  
        })


df = pd.DataFrame(all_universities)
total_uni_num = len(all_universities)
print(f"Total universities scraped: {total_uni_num}")
excel_filename = f"top_" + str(total_uni_num) + "_universities.xlsx"
df.to_excel(excel_filename, index=False)
print(f"All universities have been saved to {excel_filename}")


# Close the browser
driver.quit()










