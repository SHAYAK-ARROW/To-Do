import json
import sqlite3 as db
import datetime as dt
import time
import os 
import gui
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    while True:

        conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE status = 'Pending' ORDER BY date_time ASC")
        pending_tasks = cursor.fetchall()
        conn.close()
        
        now = dt.datetime.now()
        five_mins_later = now + dt.timedelta(minutes=10)
        
        upcoming_tasks = []
        
        for task in pending_tasks:
            task_time_str = task[3] 
            task_dt = dt.datetime.strptime(task_time_str, "%Y-%m-%d %H:%M")
            
            # ekhon overdue (ageker somoy) task-o dhora porbe, notun ba shudhu
            # future-er task na
            if task_dt <= five_mins_later:
                upcoming_tasks.append(task)
                
        if upcoming_tasks:
            while True:
                task_1st=upcoming_tasks[0][3]
                task_time= dt.datetime.strptime(task_1st, "%Y-%m-%d %H:%M")
                now=dt.datetime.now()
                left=task_time-now
                # overdue task hole 'left' negative hote pare, tai 0-er niche
                # jete debo na, nahole time.sleep() error dey
                seconds = max(0, left.total_seconds())
                time.sleep(seconds)
                dic={"id":upcoming_tasks[0][0],"task":upcoming_tasks[0][1],"descreption":upcoming_tasks[0][2],"date":upcoming_tasks[0][3]}
                with open(os.path.join(BASE_DIR, "alert.json"), "w") as f:
                    json.dump(dic, f, indent=4)
                os.system('start python "' + os.path.join(BASE_DIR, "show.py") + '"')
                upcoming_tasks.pop(0)
                if upcoming_tasks:
                    pass
                else:
                    break
                                
        else:
        
            time.sleep(600)

if __name__ == "__main__":
    main()