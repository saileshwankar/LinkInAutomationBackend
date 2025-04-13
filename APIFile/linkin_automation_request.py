from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import threading
import logging


logging.basicConfig(level=logging.INFO)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service("/usr/local/bin/chromedriver")  # use installed driver path
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
    })
    return driver

def login(driver, li_at=None, email=None, password=None):
    driver.get("https://www.linkedin.com/")
    if li_at:
        driver.delete_all_cookies()
        driver.get("https://www.linkedin.com")
        driver.add_cookie({
            "name": "li_at",
            "value": li_at,
            "domain": ".linkedin.com",
            "path": "/",
            "secure": True,
            "httpOnly": True
        })
        driver.get("https://www.linkedin.com/feed/")
        time.sleep(3)
        if "feed" in driver.current_url:
            logging.info("Login successful via cookie.")
            return True

    if email and password:
        try:
            driver.get("https://www.linkedin.com/login")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)
            driver.find_element(By.ID, "password").send_keys(password)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "global-nav-search")))
            logging.info("Login successful via email/password.")
            return True
        except Exception as e:
            logging.error(f"Login with credentials failed: {e}")
            return False
    return False

def send_requests(driver, keyword, connection_degree, location, total_to_send, include_note, letter):
    network_mapping = {
        "1st": "%5B%22F%22%5D",
        "2nd": "%5B%22S%22%5D",
        "3rd": "%5B%22O%22%5D"
    }
    net_param = network_mapping.get(connection_degree, "")
    base_url = f"https://www.linkedin.com/search/results/people/?keywords={keyword}&network={net_param}&origin=GLOBAL_SEARCH_HEADER"

    actions = ActionChains(driver)
    total_sent = 0
    current_page = 1

    while total_sent < total_to_send:
        paged_url = f"{base_url}&page={current_page}"
        logging.info(f"Navigating to page {current_page} URL: {paged_url}")
        driver.get(paged_url)
        time.sleep(4)

        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            connect_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[text()='Connect']/.."))
            )
            logging.info(f"Found {len(connect_buttons)} Connect buttons on page {current_page}.")
        except:
            logging.warning("No connect buttons found.")
            current_page += 1
            continue

        for connect_button in connect_buttons:
            if total_sent >= total_to_send:
                break

            try:
                actions.move_to_element(connect_button).perform()
                time.sleep(1)
                connect_button.click()
                time.sleep(1)

                try:
                    driver.find_element(By.XPATH, "//h2[text()='No free personalized invitations left']")
                    logging.error("No free personalized invitations left.")
                    return total_sent
                except:
                    pass

                try:
                    driver.find_element(By.XPATH, "//button[@aria-label='Got it']").click()
                except:
                    pass

                send_now_btn = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send without a note"]'))
                )
                send_now_btn.click()

                total_sent += 1
                logging.info(f"[SENT] {total_sent} connection(s) sent.")
                time.sleep(4)
            except Exception as e:
                logging.warning(f"Error during sending: {e}")
                try:
                    dismiss = driver.find_element(By.XPATH, '//button[@aria-label="Dismiss"]')
                    dismiss.click()
                    time.sleep(1)
                except:
                    pass
                continue

        current_page += 1

    return total_sent


def run_connection_cycle(data):
    driver = setup_driver()
    try:
        if not login(driver, li_at=data.get("li_at"), email=data.get("email"), password=data.get("password")):
            return {"status": "error", "message": "Login failed"}

        sent = send_requests(
            driver=driver,
            keyword=data.get("keyword", ""),
            connection_degree=data.get("connection_degree", "2nd"),
            location=data.get("location", ""),
            total_to_send=int(data.get("sendconnectionrequest", 5)),
            include_note=str(data.get("include_note", "false")).lower() == "true",
            letter=data.get("letter", "Hi {name}, let’s connect on LinkedIn.")
        )
        return {"status": "success", "sent": sent}
    except Exception as e:
        logging.error(f"run_connection_cycle error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        driver.quit()





def connect_on_linkin():
    data = request.json
    if not data.get("li_at") and (not data.get("email") or not data.get("password")):
        return jsonify({"status": "error", "message": "Missing login credentials"}), 400
    result = run_connection_cycle(data)
    return jsonify(result)


def auto_connect():
    data = request.json
    if not data.get("li_at") and (not data.get("email") or not data.get("password")):
        return jsonify({"status": "error", "message": "Missing login credentials"}), 400

    def background_task():
        total_sent = 0
        pages_per_batch = int(data.get("batch_limit", 2))
        interval = int(data.get("interval_minutes", 2))
        while total_sent < 1000:
            data["limit"] = pages_per_batch
            result = run_connection_cycle(data)
            total_sent += result.get("sent", 0)
            logging.info(f"Batch done. Total sent so far: {total_sent}")
            if total_sent >= 1000:
                break
            time.sleep(interval * 60)

    threading.Thread(target=background_task).start()
    return jsonify({"status": "started", "message": "Auto-connect thread started."})

