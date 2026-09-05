import json
import sqlite3 as db
import datetime as dt
import time
import os 
def kill_other_bg_instances():
    my_pid = os.getpid()  
    ps_command = (
        f'Get-CimInstance Win32_Process | '
        f'Where-Object {{ $_.CommandLine -like \'*bg.pyw*\' -and $_.ProcessId -ne {my_pid} }} | '
        f'ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}'
    )
    os.system(f'powershell -Command "{ps_command}" >nul 2>&1')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    # eta ekbaroi cholbe, main() shuru howar shomoy -- loop-er bhitore rakhle
    # protibar cycle-e (protita 10 minit-e, ba overdue thakle aro ghono ghono)
    # bar bar cholto, jeta onaboshok, tai loop-er baire ana holo
    kill_other_bg_instances()

    while True:
        try:
            conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_name TEXT NOT NULL,
                    task_description TEXT,
                    date_time TEXT NOT NULL,
                    status TEXT NOT NULL
                )
            """)
            cursor.execute("SELECT * FROM tasks WHERE status = 'Pending' ORDER BY date_time ASC")
            pending_tasks = cursor.fetchall()
            conn.close()
        except db.Error as e:
            print(f"Database error: {e}")
            time.sleep(600)
            continue

        now = dt.datetime.now()
        five_mins_later = now + dt.timedelta(minutes=10)

        upcoming_tasks = []

        for task in pending_tasks:
            task_time_str = task[3]
            try:
                task_dt = dt.datetime.strptime(task_time_str, "%Y-%m-%d %H:%M")
            except ValueError:
                print(f"Skipping task ID {task[0]}: invalid date format '{task_time_str}'")
                continue

            # ekhon overdue (ageker somoy) task-o dhora porbe, notun ba shudhu
            # future-er task na
            if task_dt <= five_mins_later:
                upcoming_tasks.append(task)

        if upcoming_tasks:
            while True:
                task_1st = upcoming_tasks[0][3]
                try:
                    task_time = dt.datetime.strptime(task_1st, "%Y-%m-%d %H:%M")
                except ValueError:
                    print(f"Skipping task ID {upcoming_tasks[0][0]}: invalid date format '{task_1st}'")
                    upcoming_tasks.pop(0)
                    if upcoming_tasks:
                        continue
                    else:
                        break

                now = dt.datetime.now()
                left = task_time - now
                # overdue task hole 'left' negative hote pare, tai 0-er niche
                # jete debo na, nahole time.sleep() error dey
                seconds = max(0, left.total_seconds())
                time.sleep(seconds)
                dic = {
                    "id": upcoming_tasks[0][0],
                    "task": upcoming_tasks[0][1],
                    "descreption": upcoming_tasks[0][2],
                    "date": upcoming_tasks[0][3],
                }
                with open(os.path.join(BASE_DIR, "alert.json"), "w") as f:
                    json.dump(dic, f, indent=4)
                os.system('start pythonw "' + os.path.join(BASE_DIR, "show.pyw") + '"')
                upcoming_tasks.pop(0)
                if upcoming_tasks:
                    pass
                else:
                    break

            # inner loop shesh hoyeche -- kintu popup-e thaka task-er status
            # ekhono DB-te "Pending"-i (user "OK" na dile), tai outer loop
            # ekhoni abar DB porle sei same task-ke abar dhorbe, notun popup
            # khub tarataribi khule jabe. Tai eta ekta cooldown, jate ekoi
            # task-er jonno bar bar (flooding-er moto) notun window na khole
            time.sleep(30)
        else:

            time.sleep(600)

if __name__ == "__main__":
    main()