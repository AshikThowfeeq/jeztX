from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler




class YourAppConfig1(AppConfig):
    name = 'myapp'

    def ready(self):
        from .tasks import loop
        # Create a scheduler instance
        scheduler = BackgroundScheduler()

        # Schedule the 'loop' function
        scheduler.add_job(loop, 'interval', seconds=3, args=['uploads/From-Local', 'uploads/Spider-Man'])


        # Start the scheduler
        scheduler.start()
