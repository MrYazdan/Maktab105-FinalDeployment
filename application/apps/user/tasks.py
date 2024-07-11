from time import sleep

from celery import shared_task


@shared_task
def print_after_3s():
    sleep(3)
    print("Salam Refigh !")

    return "in adad mne"
