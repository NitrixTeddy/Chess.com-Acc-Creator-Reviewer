from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from string import ascii_letters
from random import randint
import sqlite3

game = input("Game ID: ")

conn = sqlite3.connect('accounts.db')
cur = conn.cursor()

cur.execute("""
    SELECT id, username, password, used
    FROM accounts
    WHERE used = 0
    ORDER BY RANDOM()
    LIMIT 1
""")

row = cur.fetchone()

account_id = row[0]
cur.execute(
    "UPDATE accounts SET used = 1 WHERE id = ?",
    (account_id,)
)
conn.commit()

opts = Options()
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument("--no-first-run")
opts.add_argument("--no-default-browser-check")

driver = webdriver.Chrome(options=opts)

driver.get("https://www.chess.com/login")

if driver.current_url != "https://www.chess.com/login":
    print("Solve captcha then press enter in here...")
    input()

wait = WebDriverWait(driver, 10)

# username
username_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input#login-username")
    )
)
username_input.clear()
username_input.send_keys(row[1])

#password
password_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "input#login-password")
    )
)
password_input.clear()
password_input.send_keys(row[2])

#login button
password_input = wait.until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button#login")
    )
)
password_input.click()

sleep(1)

if driver.current_url == "https://www.chess.com/login_check":
    print("Solve captcha then press enter in here...")
    input()

driver.get(f"https://www.chess.com/analysis/game/live/{game}/review")

print("Press enter in here to exit...")
input()