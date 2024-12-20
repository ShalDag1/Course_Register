from selenium.webdriver.common.by import By

from defs import (launch_browser,
                  login,
                  navigate_to_register_form,
                  nevigate_to_courses_list,
                  get_available_places,
                  choose_to_course_by_id,
                  click_max_places,
                  register_courses)

from frames import switch_iframes
import time
from dotenv import load_dotenv
import os


choose_semester_btn = {     #dict repesents specific btn IDs According to semester
    "semA" : "aaaa.ProgramView.BookingButton.0",
    "semB" : "aaaa.ProgramView.BookingButton.1",
    "semc" : "aaaa.ProgramView.BookingButton.2",
}

choose_sem_btn_eng_student = {   #dict repesents specific btn IDs According to semester for who are need to register for english courses
    "english_semA" : "aaaa.ProgramView.BookingButton.0",
    "english_semB" : "aaaa.ProgramView.BookingButton.1",
    "english_semC" : "aaaa.ProgramView.BookingButton.2",
    "semA": "aaaa.ProgramView.BookingButton.3",
    "semB": "aaaa.ProgramView.BookingButton.4",
    "semc": "aaaa.ProgramView.BookingButton.5",
}

if __name__ == "__main__":
    try:
        # Load credentials
        username = os.getenv("USERNAME")
        password = os.getenv("PASSWORD")
        login_link = "https://stud.haifa.ac.il/irj"
        chrome_path = './chromedriver-win64/chromedriver.exe'
        wb = launch_browser(login_link,chrome_path)
        login(wb, username, password)
        iframes = ["contentAreaFrame", "isolatedWorkArea"]
        courses = ["203.1820", "203.3770", "203.3730", "203.3140"]
        navigate_to_register_form(wb)
        switch_iframes(wb, iframes)
        nevigate_to_courses_list(wb, choose_sem_btn_eng_student["semA"])
        choose_to_course_by_id(wb, courses)
        register_courses(wb,courses) #uncomment in register function to really register
        # Keep the browser open after finishing
        input("Process completed. Press Enter to close...")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Keep the browser open to inspect the error
        input("Press Enter to close the browser after reviewing the error.")