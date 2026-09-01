import json
import os
import time
import datetime as dt
import sqlite3 as db

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def build_message(task_id, task_name, task_description, date_time_str, is_overdue):
    sms = f"""
    ====================================
        ARROW TO DO MANNEGER
    ====================================
    Alert: You have a task due soon!
    TASK ID: {task_id}
    TASK NAME: {task_name}
    DESCRIPTION: {task_description}
    TIME: {date_time_str}
    ====================================="""
    if is_overdue:
        sms += """
        ALERT: The task is overdue!
        Please take immediate action."""
    sms += """
    =====================================
                THANK YOU
    _______________________________________
    """
    return sms


def get_new_datetime():
    now = dt.datetime.now()
    while True:
        try:
            year = int(input("Enter new year: "))
            month = int(input("Enter new month (1-12): "))
            date = int(input("Enter new date (1-31): "))
            hour = int(input("Enter new hour (0-23): "))
            minute = int(input("Enter new minute (0-59): "))
            new_dt = dt.datetime(year, month, date, hour, minute)
            if new_dt <= now:
                print("Error: New deadline must be in the future. Try again.")
                continue
            return new_dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            print("Invalid input! Please enter valid numbers for a real date/time.")


def mark_completed(task_id):
    conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


def reassign_task(task_id):
    new_time = get_new_datetime()
    conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET date_time = ? WHERE id = ?", (new_time, task_id))
    conn.commit()
    conn.close()
    print(f"\nTask ID {task_id} rescheduled to {new_time}.")


def main():
    # alert.json ekbaroi porchi, memory te rakhchi -- bg.pyw pore file
    # overwrite korle amader chalman popup-er upor kono probhab porbe na
    with open(os.path.join(BASE_DIR, "alert.json"), "r") as f:
        data = json.load(f)

    task_id = data.get("id")
    task_name = data.get("task")
    task_description = data.get("descreption")
    date_time_str = data.get("date")
    task_dt = dt.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

    while True:
        is_overdue = task_dt < dt.datetime.now()
        print(build_message(task_id, task_name, task_description, date_time_str, is_overdue))

        choice = input(
            "Enter OK if done, R to reassign a new time, "
            "or anything else to be reminded again in 10 minutes: "
        ).strip().lower()

        if choice == "ok":
            mark_completed(task_id)
            print("Task marked as completed. Bye!")
            break
        elif choice == "r":
            reassign_task(task_id)
            break
        else:
            print("Okay, I'll remind you again in 10 minutes...")
            time.sleep(600)


if __name__ == "__main__":
    main()