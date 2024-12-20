from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.by import By


def switch_iframes(wb, iframes):
    # switch iframes to aloow bot click on required button.
    try:
        # Switch to each iframe in the order specified
        for iframe in iframes:
            wb.switch_to.frame(iframe)
            print(f"Successfully switched to iframe: {iframe}")
        return True
    except NoSuchFrameException:
        print(f"Error: iframe '{iframe}' not found.")
        wb.switch_to.default_content()  # Switch back to main content if any iframe is not found
        return False
