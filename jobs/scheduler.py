from apscheduler.schedulers.background import BackgroundScheduler
from jobs import getData

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(getData.getUpdateLocData, 'interval', minutes=30, id="locdata_01", replace_existing = True)
    #scheduler.print_jobs()
    scheduler.start()




