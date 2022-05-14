from sched import scheduler
from django.apps import AppConfig


class LocationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'location'

    def ready(self) -> None:
        return super().ready()
        from jobs import scheduler
        scheduler.start()
