import time
from typing import Any
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException

from selenium import webdriver

def select_star_rating(driver, rating: int):
    """
    Clicks on the star with data-rating = rating.
    Example: rating=5 means 'Leave a 5 star review'.
    """
    # wait until at least one star is present in DOM
    star = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f"a.WriteReviewStars__star[data-rating='{rating}']"
        ))
    )
    star.click()
    print(f"[RPA] Clicked {rating}-star rating")

def fill_comment(driver, text: str):
    try:
        comment_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "textarea#comments"))
        )

        try:
            comment_box.clear()
        except Exception:
            pass

        comment_box.send_keys(text)
        print("[RPA] Wrote comment into textarea")

    except TimeoutException:
        print("[RPA] Could not find / click the comment textarea in time")

def fill_name(driver, full_name: str):
    try:
        name_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#name"))
        )

        try:
            name_input.clear()
        except Exception:
            pass

        name_input.send_keys(full_name)
        print(f"[RPA] Filled name: {full_name}")

    except TimeoutException:
        print("[RPA] Name input not found / not interactable in time")

def fill_email(driver, email: str):
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#email"))
        )

        try:
            email_input.clear()
        except Exception:
            pass

        email_input.send_keys(email)
        print(f"[RPA] Filled email: {email}")

    except TimeoutException:
        print("[RPA] Email input not found / not interactable in time")

def submit_review(driver):
    try:
        # wait until the button is present AND clickable
        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button#submitReview"))
        )

        btn.click()
        print("[RPA] Clicked Submit Review")

    except TimeoutException:
        print("[RPA] Couldn't find clickable Submit Review button in time")

    except ElementClickInterceptedException as e:
        # Sometimes there's a sticky overlay; you can force click with JS as fallback
        print(f"[RPA] Normal click blocked, trying JS click: {e}")
        driver.execute_script("document.querySelector('button#submitReview').click();")
        print("[RPA] Clicked Submit Review via JS fallback")

def run_task(driver: webdriver.Chrome, task: dict[str, Any]) -> None:
    """
    Example RPA step:
    - open site_url
    - maybe log in with login/password
    - perform specific 'action'

    This is where you customize.
    We'll show a simple pattern you can extend.
    """

    site_url = task.get("url", "").strip()
    username = task.get("login", "").strip()
    password = task.get("password", "").strip()
    stars = len(task.get("stars", "").strip())
    name = task.get("name", "").strip()
    comment = task.get("comment", "").strip()
    email = task.get("email", "").strip()

    if not site_url:
        print("Task skipped: no site_url")
        return

    print(f"\n[Task] Navigating to {site_url}")
    driver.get(site_url)
    time.sleep(2)

    select_star_rating(driver, stars)
    fill_comment(driver, comment)
    fill_name(driver, name)
    fill_email(driver, email)

    submit_review(driver)
