import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "detector.settings")

app = Celery("detector")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.timezone = "Europe/Minsk"


# таски в очередь
app.conf.beat_schedule = {
    "every-1-hours": {
        "task": "erc20.tasks.check_and_update_erc20_contracts",
        "schedule": 3600,
    },
}
