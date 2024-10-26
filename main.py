import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class Flight:
    def __init__(self, idx, departure_time, arrival_time, courier, length, stop, price):
        self.idx = idx
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.courier = courier
        self.length = length
        self.stop = stop
        self.price = price

    def print_all(self):
        print(self.departure_time + " - " + self.arrival_time + " : " + self.courier + " - " + self.length + " - " + self.stop + " - " + self.price)

class Trip:
    def __init__(self, departure_flight, possible_return_flights):
        self.departure_flight = departure_flight
        self.possible_return_flights = possible_return_flights

def get_flight_prices(origin, destination, departure_date, return_date=None):
    # Set up Chrome options to try and bypass GPU and rendering issues
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU to avoid rendering issues
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
    chrome_options.add_argument("--use-gl=swiftshader")  # Use SwiftShader for software-based rendering
    chrome_options.add_argument("--headless")  # Headless mode
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})  # Disable cookies

    # Initialize the Chrome driver with the specified options
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Load Google Flights page
    driver.get('https://www.google.com/flights')

    # Wait until the flight form loads
    try:
        flight_form = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Where from?']"))
        )
    except TimeoutException as e:
        print(f"Failed to load flight form: {e}")
        driver.quit()
        return

    # Input the origin airport
    try:
        origin_input = driver.find_element(By.XPATH, "//input[@aria-label='Where from?']")
        origin_input.clear()
        origin_input.send_keys(origin)

        # Wait for the suggestion to appear and click the first suggestion
        suggestion_xpath = "//li[@role='option' and @data-code='{}']".format(origin)
        suggestion = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, suggestion_xpath))
        )
        driver.execute_script("arguments[0].click();", suggestion)
        time.sleep(1)

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Failed to select origin airport: {e}")
        driver.quit()
        return

    # Input the destination airport
    try:
        destination_input = driver.find_element(By.XPATH, "//input[@aria-label='Where to? ']")
        destination_input.clear()
        destination_input.send_keys(destination)

        # Wait for the suggestion to appear and click the first suggestion
        suggestion_xpath = "//li[@role='option' and @data-code='{}']".format(destination)
        suggestion = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, suggestion_xpath))
        )
        driver.execute_script("arguments[0].click();", suggestion)
        time.sleep(1)

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Failed to select destination airport: {e}")
        driver.quit()
        return

    # Set the departure date using JavaScript
    try:
        # Click the departure input field to open the calendar
        departure_input = driver.find_element(By.XPATH, "//input[@aria-label='Departure']")
        driver.execute_script("arguments[0].click();", departure_input)
        time.sleep(1)

        # Locate the departure date element by its data-iso attribute and click it
        departure_date_xpath = f"//div[@data-iso='{departure_date}']"
        departure_date_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, departure_date_xpath))
        )
        driver.execute_script("arguments[0].click();", departure_date_element)
        time.sleep(1)

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException) as e:
        print(f"Failed to set departure date: {e}")
        driver.quit()
        return

    # If there's a return date, set it
    if return_date:
        try:
            # Click the departure input field to open the calendar
            return_input = driver.find_element(By.XPATH, "//input[@aria-label='Return']")
            driver.execute_script("arguments[0].click();", return_input)
            time.sleep(1)

            # Locate the return date element by its data-iso attribute and click it
            return_date_xpath = f"//div[@data-iso='{return_date}']"
            return_date_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, return_date_xpath))
            )
            driver.execute_script("arguments[0].click();", return_date_element)

        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException) as e:
            print(f"Failed to set return date: {e}")
            driver.quit()
            return
    
    # Click the "Done" button
    try:
        done_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe') and contains(@class, 'nCP5yc')]"))
        )
        driver.execute_script("arguments[0].click();", done_button)
        time.sleep(1)

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Failed to click 'Done' button: {e}")
        driver.quit()
        return
    
    # Click the "Search" button
    try:
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Search']"))
        )
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(1)

    except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
        print(f"Failed to click 'Search' button: {e}")
        driver.quit()
        return
    
    # Refresh the page to ensure everything loads correctly
    driver.refresh()

    # Wait for the results to load properly after refresh
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'HeMQ4')]"))
        )
    except TimeoutException as e:
        print(f"Failed to load results after refresh: {e}")
        driver.quit()
        return
    
    try:
        # Locate the <h3> element
        heading_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'zBTtmb') and contains(@class, 'ZSxxwc')]"))
        )
    
        # Locate the following <ul> element relative to the <h3> element
        ul_element = heading_element.find_element(By.XPATH, "following-sibling::ul")

        # Get all <li> elements within the <ul>
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")

        # Create a list to store the text of each <li> element
        li_texts = [li.text for li in li_elements]

        # Print out the text from each <li> element
        departing_flights_list = []
        for idx, text in enumerate(li_texts):
            temp = ""
            temp_list = []
            idx = 0
            for i in text:
                temp = temp + i
                if i == '\n':
                    temp_list.append(temp)
                    temp = ""
            departing_flights_list.append(Flight(idx, temp_list[0].strip(), temp_list[2].strip(), temp_list[3].strip(), temp_list[4].strip(), temp_list[6].strip(), temp_list[9].strip()))
            idx = idx + 1
            
        try:
            # Locate the specific flight element to click on (using the given class name and attributes)
            flight_to_click = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'JMc5Xc') and @role='link']"))
            )

            # Scroll to the element to make sure it is in view
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", flight_to_click)
            time.sleep(1)  # Allow some time for the page to adjust

            # Use JavaScript to click the element to avoid interception issues
            driver.execute_script("arguments[0].click();", flight_to_click)
            time.sleep(2)  # Allow time for the return flight section to load

        except (NoSuchElementException, TimeoutException, ElementClickInterceptedException, WebDriverException) as e:
            print(f"Failed to click on the departing flight element: {e}")
            driver.quit()
            return

        # Wait for the best returning flights section to load
        try:
            # Locate the <h3> element
            return_heading_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//h3[contains(@class, 'zBTtmb') and contains(@class, 'ZSxxwc')]"))
            )
    
            # Locate the following <ul> element relative to the <h3> element
            ul_element = return_heading_element.find_element(By.XPATH, "following-sibling::ul")

            # Get all <li> elements within the <ul>
            li_elements = ul_element.find_elements(By.TAG_NAME, "li")

            # Create a list to store the text of each <li> element
            return_li_texts = [li.text for li in li_elements]

            # Print out the text from each return flight option
            returning_flights_list = []
            for idx, text in enumerate(return_li_texts):
                temp = ""
                temp_list = []
                idx = 0
                for i in text:
                    temp = temp + i
                    if i == '\n':
                        temp_list.append(temp)
                        temp = ""
                if temp_list[6].strip() == "Nonstop":
                    returning_flights_list.append(Flight(idx, temp_list[0].strip(), temp_list[2].strip(), temp_list[3].strip(), temp_list[4].strip(), temp_list[6].strip(), temp_list[9].strip()))
                else:
                    returning_flights_list.append(Flight(idx, temp_list[0].strip(), temp_list[2].strip(), temp_list[3].strip(), temp_list[4].strip(), temp_list[6].strip(), temp_list[10].strip()))
                idx = idx + 1

            for item in returning_flights_list:
                item.print_all()

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to locate the return flight elements: {e}")
            driver.quit()
            return

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Failed to locate the <h3> or the <ul> elements: {e}")
        driver.quit()
        return

    # Close the browser after a delay for visual confirmation
    time.sleep(20)
    driver.quit()

# Example usage
get_flight_prices('JFK', 'LAX', '2024-12-20', '2024-12-30')
