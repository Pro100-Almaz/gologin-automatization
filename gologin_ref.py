from gologin import GoLogin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def init_go_login(access_token: str, profile_id: str) -> (GoLogin, webdriver.Chrome):
    """
    Start the specified GoLogin profile and return:
      - the GoLogin client (so we can stop it later)
      - the Selenium driver already attached to this profile
    """
    gl = GoLogin({
        "token": access_token,
        "profile_id": profile_id,
    })

    # Launch the GoLogin profile's browser and get its remote debugging address
    debugger_address = gl.start()

    # Get Orbita/Chromium version that profile is using
    chromium_version = gl.get_chromium_version()

    # Install matching chromedriver
    service = Service(ChromeDriverManager(driver_version=chromium_version).install())

    # Attach Selenium to that running browser
    opts = webdriver.ChromeOptions()
    opts.add_experimental_option("debuggerAddress", debugger_address)

    driver = webdriver.Chrome(service=service, options=opts)

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if "google.com" in driver.current_url or "accounts.google.com" in driver.current_url:
            driver.close()

    if len(driver.window_handles) > 0:
        driver.switch_to.window(driver.window_handles[0])
    else:
        driver.execute_script("window.open('about:blank', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])

    driver.get("about:blank")
    return gl, driver


def close_go_login(gl: GoLogin, driver: webdriver.Chrome):
    """
    Gracefully close the Selenium session and stop the GoLogin profile
    so cookies/fingerprint/etc are saved.
    """
    try:
        driver.quit()
    finally:
        gl.stop()