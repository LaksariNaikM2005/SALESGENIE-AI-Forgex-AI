import time
from apscheduler.schedulers.background import BackgroundScheduler

def run_daily_followup_scan():
    print("[APScheduler Worker] Running daily follow-up scan for inactive leads...")

def run_crm_sync_job():
    print("[APScheduler Worker] Executing scheduled CRM background sync...")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_daily_followup_scan, 'interval', hours=24, id='daily_followups')
    scheduler.add_job(run_crm_sync_job, 'interval', hours=1, id='hourly_crm_sync')
    scheduler.start()
    print("SalesGenie AI Background Automation Scheduler initialized.")
    return scheduler

if __name__ == "__main__":
    s = start_scheduler()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        s.shutdown()
