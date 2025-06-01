from threading import Event
from datetime import datetime
from django.db import connection
from django.core.management.base import BaseCommand
from books.models import StudentBooks, BooksStatus
from apscheduler.schedulers.blocking import BackgroundScheduler



def mark_overdue_books():
    now = datetime.now()
    books_data = StudentBooks.objects.filter(return_date__lt=now, 
                                            status=BooksStatus.ASSIGNED)
    overdue_book = books_data.update(status=BooksStatus.OVERDUE)
    
    # Close the database connection to avoid issues with long-running processes
    connection.close_if_unusable_or_obsolete()
    
    if overdue_book == 0:
        print(f"""[{now.strftime('%Y-%m-%d %H:%M:%S')}]
                                        No overdue books found.""")
    else:
        print(f"""[{now.strftime('%Y-%m-%d %H:%M:%S')}] 
                        Marked {overdue_book} books as OVERDUE.""")
    

class Command(BaseCommand):
    help = 'Run APScheduler to mark overdue books'

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        # scheduler.add_job(mark_overdue_books, 'cron', hour=0, minute=0)  # Run daily at midnight
        scheduler.add_job(mark_overdue_books, 'cron', minute='*/1')  # Run every minute
        scheduler.start()
        print("Scheduler started. Checking for overdue books...")
        try:
            Event().wait()  # Keep the script running
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            print("Scheduler stopped.")