from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC




def launch_browser(login_link,chromedriver_path):

    chrome_options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")
   # chrome_path = r'C:\Users\97258\Desktop\chromedriver-win64\chromedriver.exe'
    service = Service(chromedriver_path)
    wb = wd.Chrome(service=service, options=chrome_options)
    wb.implicitly_wait(2)
    wb.get(login_link)
    return wb

def login(wb, username, password):  # make a login
    wb.implicitly_wait(15)
    username_field = wb.find_element(By.NAME,'Ecom_User_ID')
    username_field.send_keys(username)
    password_field = wb.find_element(By.NAME,'Ecom_Password')
    password_field.send_keys(password)
    login_btn = wb.find_element(By.NAME,'loginButton2')
    login_btn.click()



def navigate_to_register_form(wb):  # click on the edit button

    home_reg_btn = wb.find_element(By.ID, "tabIndex4")
    home_reg_btn.click()
    sec_reg_btn = wb.find_element(By.ID, "L1N1")
    sec_reg_btn.click()
    wb.implicitly_wait(2)


def nevigate_to_courses_list(wb,semester):
    div_element = wb.find_element(By.ID, semester)
    div_element.click()


def choose_to_course_by_id(wb, courses):
    for course_id in courses:
        course_id_input = WebDriverWait(wb, 5).until(
            EC.presence_of_element_located((By.ID, "aaaa.ModuleBasketView.short_smInp")))
        course_id_input.clear()
        course_id_input.send_keys(course_id)
        course_id_input.send_keys(Keys.ENTER)
        time.sleep(0.2)
        checkbox = WebDriverWait(wb, 5).until(EC.element_to_be_clickable((By.ID, "aaaa.ModuleBasketView.Choose.0")))
        checkbox.click()
        time.sleep(0.2)

    register_course_btn = WebDriverWait(wb, 5).until(EC.element_to_be_clickable((By.ID, "aaaa.ModuleBasketView._46:1")))
    register_course_btn.click()

def get_available_places(wb):
    groups = []

    try:
        # Locate the table body containing the rows for each group
        tbody = wb.find_element(By.ID, "aaaa.EventPackageSelectionView.packageTable-contentTBody")

        # Loop through each row in the tbody
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:
            try:
                # Get the group name from the first <td> column
                group_name_element = row.find_element(By.XPATH,
                                                      ".//td[2]//span[contains(@id, 'aaaa.EventPackageSelectionView.se_stext_0_editor')]")
                group_name = group_name_element.text

                # Get the available places from the second <td> column
                places_left_element = row.find_element(By.XPATH,
                                                       ".//td[3]//span[contains(@id, 'aaaa.EventPackageSelectionView.se_freeCap_0_editor')]")
                places_left = places_left_element.text

                # Store the group information
                groups.append({
                    "group_name": group_name,
                    "places_left": places_left
                })

                print(f"Group: {group_name}, Places Left: {places_left}")

            except Exception as e:
                print(f"Error processing row: {e}")

    except Exception as e:
        print(f"Error locating table body: {e}")

    return groups


def click_max_places(wb, attempt):
    max_places = 0
    max_places_element = None

    try:
        # Locate the table body containing the rows for each group
        tbody = wb.find_element(By.ID, "aaaa.EventPackageSelectionView.packageTable-contentTBody")

        # Loop through each row in the tbody
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows[1:]:  # Start from the second row
            try:
                # Locate the available places element in the row
                places_left_element = row.find_element(By.XPATH,".//td[3]//span[contains(@id, 'aaaa.EventPackageSelectionView.se_freeCap_0_editor')]")
                places_left = int(places_left_element.text)  # Convert text to integer

                # Check if this row has the most places available
                if places_left > max_places:
                    max_places = places_left
                    max_places_element = places_left_element

            except Exception as e:
                print(f"Error processing row: {e}")

        # Click on the <span> with the most places available
        if max_places > 0:
            if max_places_element:
                max_places_element.click()
                print(f"Clicked on the group with the most places: {max_places}")
                return max_places
        else:
            if attempt == 0:
                print("Trying scrolling down to find other groups")
                scrollbar_nxt = wb.find_element(By.ID, "aaaa.EventPackageSelectionView.packageTable-scrollV-Nxt")
                for i in range(3):
                    scrollbar_nxt.click()
                click_max_places(wb, 1)
                return max_places
            else:
                print("Course is full, please try again later")
                return 0


    except Exception as e:
        print(f"Error locating table body: {e}")



def register_courses(wb,courses):
    value1 = 1
    value2 = 0
    for course in courses:
        get_available_places(wb)
        places_left = click_max_places(wb, 0)
        time.sleep(0.1)
        if (places_left > 0):
            #wb.find_element(By.ID, "aaaa.EventPackageSelectionView.bookingButton").click()
            print(f"register to course: {course} succeed")
        value1 += 1
        value2 += 1
        wb.find_element(By.ID, f"aaaa.EventsView.ModuleTable:{value1}.{value2}").click()


