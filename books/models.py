from django.db import models

# Create your models here.


class BooksStatus(models.IntegerChoices):
    AVAILABLE = 1
    RETURNED = 2
    RESERVED = 3
    ASSIGNED = 4
    DELETED = 5
    OVERDUE = 6

class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(null=True, blank=True, max_length=100)
    published_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=BooksStatus.AVAILABLE, choices=BooksStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)



class StudentBooks(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    student_id = models.IntegerField()
    assign_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=BooksStatus.choices, default=BooksStatus.ASSIGNED)

    def __str__(self):
        return f"Book: {self.book.title}, Student ID: {self.student_id}"
