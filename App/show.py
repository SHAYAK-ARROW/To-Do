import json
import os
import datetime as dt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    with open(os.path.join(BASE_DIR, "alert.json"), "r") as f:
        data = json.load(f)
        
    task_id = data.get("id")
    task_name = data.get("task")
    task_description = data.get("descreption")
    date_time_str = data.get("date")
    
    task_dt = dt.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
    
    sms = f"""
    ====================================
        ARROW TO DO MANNEGER
    ====================================
    Alert: You have a task due soon!
    TASK ID: {task_id}
    TASK NAME: {task_name}
    DESCRIPTION: {task_description}
    TIME: {date_time_str}
    =====================================
                THANK YOU
    _______________________________________
    """
    
    
    if task_dt < dt.datetime.now():
        sms = f"""
    ====================================
        ARROW TO DO MANNEGER
    ====================================
    Alert: You have a task due soon!
    TASK ID: {task_id}
    TASK NAME: {task_name}
    DESCRIPTION: {task_description}
    TIME: {date_time_str}
    =====================================
        ALERT: The task is overdue!          
        Please take immediate action.
    =====================================
                THANK YOU
    ______________________________________
    """
    
    print(sms)

if __name__ == "__main__":
    main()