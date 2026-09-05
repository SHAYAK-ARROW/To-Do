import os
import sqlite3 as db
import datetime as dt
import calendar
import arrowgui as gui
# A pogram as a gift to NC Sir on teachers day from Shayak.

COLOR_NORMAL = "#c9d1d9"
COLOR_SUCCESS = "#3fb950"
COLOR_ERROR = "#f85149"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def make_db():
    assets_dir = os.path.join(BASE_DIR, "assets")
    os.makedirs(assets_dir, exist_ok=True)


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
    
    
    conn.commit()
    conn.close()
    gui.printf("Database and table created successfully!", color=COLOR_SUCCESS)





def get_valid_datetime():
    now = dt.datetime.now()
    
    # year validation
    while True:
        try:
            task_year = int(gui.scanf("Enter the task year: ", color=COLOR_NORMAL))
            if task_year < now.year:
                gui.printf("Error: Year cannot be from the past. Try again.", color=COLOR_ERROR)
            else:
                break
        except ValueError:
            gui.printf("Invalid input! Please enter a valid year number.", color=COLOR_ERROR)

    # month validation
    while True:
        try:
            task_month = int(gui.scanf("Enter the task month (1-12): ", color=COLOR_NORMAL))
            if task_month < 1 or task_month > 12:
                gui.printf("Invalid month! Must be between 1 and 12.", color=COLOR_ERROR)
            elif task_year == now.year and task_month < now.month:
                gui.printf("Error: Month cannot be from the past for this year. Try again.", color=COLOR_ERROR)
            else:
                break
        except ValueError:
            gui.printf("Invalid input! Please enter a valid month number.", color=COLOR_ERROR)

    # date validetion
    days_in_month = calendar.monthrange(task_year, task_month)[1]
    while True:
        try:
            task_date = int(gui.scanf(f"Enter the task date (1-{days_in_month}): ", color=COLOR_NORMAL))
            if task_date < 1 or task_date > days_in_month:
                gui.printf(f"Invalid date! {task_month}/{task_year} has only {days_in_month} days.", color=COLOR_ERROR)
            elif task_year == now.year and task_month == now.month and task_date < now.day:
                gui.printf("Error: Date cannot be from the past. Try again.", color=COLOR_ERROR)
            else:
                break
        except ValueError:
            gui.printf("Invalid input! Please enter a valid date number.", color=COLOR_ERROR)

    # hour validetion
    while True:
        try:
            task_hour = int(gui.scanf("Enter the task hour (0-23): ", color=COLOR_NORMAL))
            if task_hour < 0 or task_hour > 23:
                gui.printf("Invalid hour! Must be between 0 and 23.", color=COLOR_ERROR)
            elif task_year == now.year and task_month == now.month and task_date == now.day and task_hour < now.hour:
                gui.printf("Error: Hour cannot be from the past. Try again.", color=COLOR_ERROR)
            else:
                break
        except ValueError:
            gui.printf("Invalid input! Please enter a valid hour number.", color=COLOR_ERROR)

    # minitue validetion
    while True:
        try:
            task_minute = int(gui.scanf("Enter the task minute (0-59): ", color=COLOR_NORMAL))
            if task_minute < 0 or task_minute > 59:
                gui.printf("Invalid minute! Must be between 0 and 59.", color=COLOR_ERROR)
            elif task_year == now.year and task_month == now.month and task_date == now.day and task_hour == now.hour and task_minute <= now.minute:
                gui.printf("Error: Deadline must be in the future! Try again.", color=COLOR_ERROR)
            else:
                break
        except ValueError:
            gui.printf("Invalid input! Please enter a valid minute number.", color=COLOR_ERROR)
            
    # 
    return f"{task_year:04d}-{task_month:02d}-{task_date:02d} {task_hour:02d}:{task_minute:02d}"

def insert_task(task):
    t_name = task[0]
    t_desc = task[1]
    t_time = task[2]
    t_status = task[3]
    
    
    conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
    cursor = conn.cursor()
    
    
    cursor.execute("""
        INSERT INTO tasks (task_name, task_description, date_time, status)
        VALUES (?, ?, ?, ?)
    """, (t_name, t_desc, t_time, t_status))
    
    conn.commit()
    conn.close()
    gui.printf("Task list theke successfully database-e entry hoye geche!", color=COLOR_SUCCESS)
    pass

def add():
    task_name = gui.scanf("Enter the task: ", color=COLOR_NORMAL).strip()
    while not task_name:
        gui.printf("Error: Task name cannot be empty. Try again.", color=COLOR_ERROR)
        task_name = gui.scanf("Enter the task: ", color=COLOR_NORMAL).strip()
    task_description = gui.scanf("Enter the task description: ", color=COLOR_NORMAL).strip()
    
    task_deadline = get_valid_datetime()
    task = [task_name, task_description, task_deadline, "Pending"]
    
    
    insert_task(task)
    
    gui.printf(f"\nTask Added Successfully with Deadline: {task_deadline}", color=COLOR_SUCCESS)
    run()
 

def delete():
    gui.printf("\n--- DELETE TASK ---", color=COLOR_NORMAL)
    

    try:
        t_id = int(gui.scanf("Enter the Task ID you want to delete: ", color=COLOR_NORMAL))
    except ValueError:
        gui.printf("Error: Invalid input! Please enter a valid number for Task ID.", color=COLOR_ERROR)
        return

    conn = None
    try:
        conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (t_id,))
        task_exists = cursor.fetchone()
        
        if not task_exists:
            gui.printf(f"\nError: No task found with ID {t_id}.", color=COLOR_ERROR)
        else:
            
            cursor.execute("DELETE FROM tasks WHERE id = ?", (t_id,))
            conn.commit()
            gui.printf(f"\nSuccess: Task ID {t_id} has been deleted successfully!", color=COLOR_SUCCESS)
            
    except db.Error as e:
        gui.printf(f"\nDatabase Error: {e}", color=COLOR_ERROR)
    finally:
        if conn:
            conn.close()
    run()
def eddite():
    gui.printf("\n--- EDIT TASK ---", color=COLOR_NORMAL)
    
    show_all()
    try:
        t_id = int(gui.scanf("Enter the Task ID you want to edit: ", color=COLOR_NORMAL))
    except ValueError:
        gui.printf("Invalid ID! Please enter a valid number.", color=COLOR_ERROR)
        return


    conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
    cursor = conn.cursor()
    
    cursor.execute("SELECT task_name, task_description, date_time, status FROM tasks WHERE id = ?", (t_id,))
    old_task = cursor.fetchone()
    
    
    if not old_task:
        gui.printf(f"\nError: No task found with ID {t_id}.", color=COLOR_ERROR)
        conn.close()
        return
    
    old_name, old_desc, old_time, old_status = old_task

    gui.printf(f"\n[Current Details] Name: {old_name} | Desc: {old_desc} | Time: {old_time}", color=COLOR_NORMAL)
    gui.printf("If you want to keep the old value, just press ENTER without typing anything.\n", color=COLOR_NORMAL)


    t_name_input = gui.scanf(f"Enter new task name [{old_name}]: ", color=COLOR_NORMAL).strip()
    t_name = t_name_input if t_name_input else old_name

    t_desc_input = gui.scanf(f"Enter new task description [{old_desc}]: ", color=COLOR_NORMAL).strip()
    t_desc = t_desc_input if t_desc_input else old_desc

    choice_time = gui.scanf("Do you want to change the deadline? (y/n): ", color=COLOR_NORMAL).strip().lower()
    if choice_time == 'y':
        gui.printf("Enter new deadline details:", color=COLOR_NORMAL)
        t_time = get_valid_datetime()
    else:
        t_time = old_time  

    
    cursor.execute("""
        UPDATE tasks
        SET task_name = ?, task_description = ?, date_time = ?, status = ?
        WHERE id = ?
    """, (t_name, t_desc, t_time, old_status, t_id))
    
    conn.commit()
    conn.close()
    gui.printf(f"\nTask ID {t_id} successfully updated!", color=COLOR_SUCCESS)
    run()
    
def show_all():
    conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    
    if tasks:
        gui.printf("\nAll Tasks:", color=COLOR_NORMAL)
        for task in tasks:
            gui.printf(f"ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Deadline: {task[3]}, Status: {task[4]}", color=COLOR_NORMAL)
    else:
        gui.printf("No tasks found.", color=COLOR_NORMAL)
    
    conn.close()



def show():
    gui.printf('''
_____________________________
Enter 1 for SHOW ALL TASKS
Enter 2 for SHOW PENDING TASKS
Enter 3 for SHOW COMPLETED TASKS
Enter 4 for SHOW TASKS BY DEADLINE
''', color=COLOR_NORMAL)
    while True:
        try:
            chiose=int(gui.scanf("Enter your chiose: ", color=COLOR_NORMAL))
            if 1<=chiose<=4:
                break
            else:
                raise ValueError
        except ValueError:
            gui.printf("Opps! wrong input. Try again!", color=COLOR_ERROR)
    if chiose==1:
        show_all()
    elif chiose==2:
        conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE status = 'Pending'")
        pending_tasks = cursor.fetchall()
        gui.printf("\nPending Tasks:", color=COLOR_NORMAL)
        conn.close()
        for task in pending_tasks:
            gui.printf(f"ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Deadline: {task[3]}, Status: {task[4]}", color=COLOR_NORMAL)
        
    
        
    elif chiose==3:
        conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE status = 'Completed'")
        completed_tasks = cursor.fetchall()
        conn.close()
        gui.printf("\nCompleted Tasks:", color=COLOR_NORMAL)
        for task in completed_tasks:   
            gui.printf(f"ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Deadline: {task[3]}, Status: {task[4]}", color=COLOR_NORMAL)
    elif chiose==4:
        while True:
            try:
                task_year = int(gui.scanf("Enter the task year: ", color=COLOR_NORMAL))
                if task_year < 2000 or task_year > 2100:
                    gui.printf("Invalid year! Must be between 2000 and 2100.", color=COLOR_ERROR)
                else:
                    break
            except ValueError:
                gui.printf("Invalid input! Please enter a valid year number.", color=COLOR_ERROR)

     # month
        while True:
            try:
                task_month = int(gui.scanf("Enter the task month (1-12): ", color=COLOR_NORMAL))
                if task_month < 1 or task_month > 12:
                    gui.printf("Invalid month! Must be between 1 and 12.", color=COLOR_ERROR)
                else:
                    break
            except ValueError:
                gui.printf("Invalid input! Please enter a valid month number.", color=COLOR_ERROR)

        # date
        while True:
            try:
                task_date = int(gui.scanf("Enter the task date (1-31): ", color=COLOR_NORMAL))
                if task_date < 1 or task_date > 31:
                    gui.printf("Invalid date! Must be between 1 and 31.", color=COLOR_ERROR)
                else:
                    break
            except ValueError:
                gui.printf("Invalid input! Please enter a valid date number.", color=COLOR_ERROR)

        # hour
        while True:
            try:
                task_hour = int(gui.scanf("Enter the task hour (0-23): ", color=COLOR_NORMAL))
                if task_hour < 0 or task_hour > 23:
                    gui.printf("Invalid hour! Must be between 0 and 23.", color=COLOR_ERROR)
                else:
                    break
            except ValueError:
                gui.printf("Invalid input! Please enter a valid hour number.", color=COLOR_ERROR)

        # minitues
        while True:
            try:
                task_minute = int(gui.scanf("Enter the task minute (0-59): ", color=COLOR_NORMAL))
                if task_minute < 0 or task_minute > 59:
                    gui.printf("Invalid minute! Must be between 0 and 59.", color=COLOR_ERROR)
                else:
                    break
            except ValueError:
                gui.printf("Invalid input! Please enter a valid minute number.", color=COLOR_ERROR)
                
        
        deadline1=f"{task_year:04d}-{task_month:02d}-{task_date:02d} {task_hour:02d}:{task_minute:02d}"
        gui.printf(f"Do you want to show a range ? (y/n): ", color=COLOR_NORMAL)
        while True:
            chiose1=gui.scanf(color=COLOR_NORMAL).strip().lower()
            if chiose1 in ['y', 'n']:
                break
            else:
                gui.printf("Invalid input! Please enter 'y' or 'n'.", color=COLOR_ERROR)
        conn = db.connect(os.path.join(BASE_DIR, "assets", "todo.db"))
        cursor = conn.cursor()
                    
        if chiose1=='y':

            while True:
                try:
                    task_year = int(gui.scanf("Enter the task year: ", color=COLOR_NORMAL))
                    if task_year < 2000 or task_year > 2100:
                        gui.printf("Invalid year! Must be between 2000 and 2100.", color=COLOR_ERROR)
                    else:
                        break
                except ValueError:
                    gui.printf("Invalid input! Please enter a valid year number.", color=COLOR_ERROR)


            while True:
                try:
                    task_month = int(gui.scanf("Enter the task month (1-12): ", color=COLOR_NORMAL))
                    if task_month < 1 or task_month > 12:
                        gui.printf("Invalid month! Must be between 1 and 12.", color=COLOR_ERROR)
                    else:
                        break
                except ValueError:
                    gui.printf("Invalid input! Please enter a valid month number.", color=COLOR_ERROR)

            while True:
                try:
                    task_date = int(gui.scanf("Enter the task date (1-31): ", color=COLOR_NORMAL))
                    if task_date < 1 or task_date > 31:
                        gui.printf("Invalid date! Must be between 1 and 31.", color=COLOR_ERROR)
                    else:
                        break
                except ValueError:
                    gui.printf("Invalid input! Please enter a valid date number.", color=COLOR_ERROR)

            
            while True:
                try:
                    task_hour = int(gui.scanf("Enter the task hour (0-23): ", color=COLOR_NORMAL))
                    if task_hour < 0 or task_hour > 23:
                        gui.printf("Invalid hour! Must be between 0 and 23.", color=COLOR_ERROR)
                    else:
                        break
                except ValueError:
                    gui.printf("Invalid input! Please enter a valid hour number.", color=COLOR_ERROR)

            
            while True:
                try:
                    task_minute = int(gui.scanf("Enter the task minute (0-59): ", color=COLOR_NORMAL))
                    if task_minute < 0 or task_minute > 59:
                        gui.printf("Invalid minute! Must be between 0 and 59.", color=COLOR_ERROR)
                    else:
                        break
                except ValueError:
                    gui.printf("Invalid input! Please enter a valid minute number.", color=COLOR_ERROR)
                    

            deadline2=f"{task_year:04d}-{task_month:02d}-{task_date:02d} {task_hour:02d}:{task_minute:02d}"

            # deadline2 ke deadline1-er theke por hote hobe, nahole BETWEEN
            # query khali/vul result debe. Jodi ulto kore dey (end age, start
            # pore), amra nije theke sathe sathe swap kore nicchi
            if deadline2 < deadline1:
                gui.printf("Note: end date was before start date, swapping them.", color=COLOR_NORMAL)
                deadline1, deadline2 = deadline2, deadline1

            # dedeline 
            cursor.execute("""
                SELECT * FROM tasks 
                WHERE date_time BETWEEN ? AND ?
            """, (deadline1, deadline2))
            
            #
            tasks_list = cursor.fetchall()
        else:
            cursor.execute("""
                SELECT * FROM tasks 
                WHERE date_time = ?
            """, (deadline1,))
            tasks_list=cursor.fetchall()
        conn.close()
        for task in tasks_list:
            gui.printf(f"ID: {task[0]}, Name: {task[1]}, Description: {task[2]}, Deadline: {task[3]}, Status: {task[4]}", color=COLOR_NORMAL)
        
def run():
    os.system('powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*bg.pyw*\' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }" >nul 2>&1')
    os.system('start /b pythonw "' + os.path.join(BASE_DIR, "bg.pyw") + '"')
    pass
def main():
    gui.start_terminal()
    make_db()
    while True:
        welcome_sms='''
    ####################################
            ARROW TO DO MANNEGER
    ____________________________________

    ----------------MENU---------------
    Enter 1 for ADD TASK
    Enter 2 for EDITE TASK
    Enter 3 for DELETE TASK
    Enter 4 for SHOW  TASK
    Enter 5 for START BG_COUNT
    ENTER 0 for EXIT
    _____________________________________

    '''
        gui.printf(welcome_sms, color=COLOR_NORMAL)

        while True:
            try:
                chiose=int(gui.scanf("Enter your chiose: ", color=COLOR_NORMAL))
                if 0<=chiose<=5:
                    break
                else:
                    raise ValueError
            except ValueError:
                gui.printf("Opps! wrong input. Try again!", color=COLOR_ERROR)
        if chiose==0:
            exit()
        elif chiose==1:
            add()
        elif chiose==2:
            eddite()
        elif chiose==3:
            delete()
        elif chiose==4:
            show()
        elif chiose==5:
            run()
        clear=gui.scanf("YOUR PROSESS COMPLETED SUCCESSFULLY", color=COLOR_SUCCESS)
        gui.clear()


if __name__=="__main__":
    main()