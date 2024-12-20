from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.by import By


def check_frames(wb):
    print("\n=== Checking for Frames ===")

    # Find all iframes
    iframes = wb.find_elements(By.TAG_NAME, "iframe")
    frames = wb.find_elements(By.TAG_NAME, "frame")

    print(f"\nFound {len(iframes)} iframes and {len(frames)} frames")

    # Print details for iframes
    print("\n--- iFrames ---")
    for idx, iframe in enumerate(iframes):
        try:
            print(f"\niFrame #{idx + 1}:")
            print(f"ID: {iframe.get_attribute('id')}")
            print(f"Name: {iframe.get_attribute('name')}")
            print(f"Src: {iframe.get_attribute('src')}")

            # Try to switch to the frame and get content
            wb.switch_to.frame(iframe)
            print("Successfully switched to frame")

            # Print some basic content info
            elements = wb.find_elements(By.XPATH, "//*")
            print(f"Number of elements in frame: {len(elements)}")

            # Switch back to default content
            wb.switch_to.default_content()
            print("Switched back to main content")

        except Exception as e:
            print(f"Error inspecting iframe: {str(e)}")
            wb.switch_to.default_content()

    # Print details for frames
    print("\n--- Frames ---")
    for idx, frame in enumerate(frames):
        try:
            print(f"\nFrame #{idx + 1}:")
            print(f"ID: {frame.get_attribute('id')}")
            print(f"Name: {frame.get_attribute('name')}")
            print(f"Src: {frame.get_attribute('src')}")
        except Exception as e:
            print(f"Error inspecting frame: {str(e)}")

            # Switch to the second iframe, if it exists

    return iframes




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