import sqlite3

def reset_used_flags(db_path="accounts.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE accounts
        SET used = 0
        WHERE used = 1
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    reset_used_flags()
