from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

options = uc.ChromeOptions()
options.add_argument('--headless')

driver = uc.Chrome(options=options)

driver.get("https://www.eventbrite.com/d/italy--bari/all-events/?page=1")

print('Downloading page 1...')
pages = int(str(driver.find_element(By.CSS_SELECTOR, 'li.Pagination-module__search-pagination__navigation-minimal___1eHd9').text).split('of ')[1])

print('There are '+str(pages)+' pages.')

f = open('eventbrite_bari_ids.txt', 'w', encoding="utf-8")

for idx_page in range(pages):
    if idx_page > 0:
        print('Downloading page '+str(idx_page+1)+'/'+str(pages))
        driver.get("https://www.eventbrite.com/d/italy--bari/all-events/?page="+str(idx_page+1))

    events = driver.find_elements(By.CSS_SELECTOR, 'div.SearchResultPanelContentEventCardList-module__map_experiment_event_card___vyRC3') 
    
    for event in events:
        event_id = str(event.find_element(By.CSS_SELECTOR, 'a.event-card-link').get_attribute('data-event-id'))
        f.write(event_id+'\n')

f.close()

driver.quit()
