from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from string import ascii_letters
from random import randint
import sqlite3
from sys import exit

while True:

    conn = sqlite3.connect('accounts.db')
    cursor = conn.cursor()

    opts = Options()
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--no-first-run")
    opts.add_argument("--no-default-browser-check")

    driver = webdriver.Chrome(options=opts)

    letters = []
    randname = ""
    randpass = ""

    for i in ascii_letters: letters.append(i)
    for i in range(randint(13, 16)):  randname += letters[randint(1, len(letters) - 1)]
    for i in range(randint(10, 15)): randpass += letters[randint(1, len(letters) - 1)]
    for i in range(randint(1, 2)): randpass += str(randint(1, 9))

    driver = webdriver.Chrome()
    driver.get("https://www.chess.com/register?returnUrl=https%3A%2F%2Fwww.chess.com%2F&step=login-info")

    if driver.current_url != "https://www.chess.com/register?returnUrl=https%3A%2F%2Fwww.chess.com%2F&step=login-info":
        print("IP blacklisted, exit script and switch VPN server...")
        sleep(1)
        exit()

    wait = WebDriverWait(driver, 10)

    email_element = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.main-screen-button-new-onboarding-designs")
        )
    )
    email_element.click()

    email_input = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
            "div.index-form-group.index-email.index-form-group-new-onboarding-designs input")
        )
    )
    email_input.clear()
    email_input.send_keys(randname + "@gmasl.com")


    password_input = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR,
            "div.index-form-group.index-form-group-password.index-form-group-new-onboarding-designs input")
        )
    )
    password_input.clear()
    password_input.send_keys(randpass)


    reg_element = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.index-button-new-onboarding-designs")
        )
    )
    reg_element.click()

    username_element = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.username-form-group.username-form-group-new-onboarding-design input")
        )
    )
    username_element.clear()
    username_element.send_keys(randname)

    sleep(4)

    usercont_element = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "div.username-wrap-new-onboarding-design button")
        )
    )
    usercont_element.click()

    sleep(2)

    if driver.current_url == "https://www.chess.com/register":
        print("IP blacklisted, exit script and switch VPN server...")
        sleep(1)
        exit()

    randname += "@gmasl.com"
    cursor.execute("INSERT INTO accounts (username, password, used) VALUES (?, ?, ?)", (randname, randpass, 0))
    conn.commit()
    cursor.close()
    conn.close()

    print("Done")
    print(f"Account created: {randname} | {randpass}")

    driver.quit()