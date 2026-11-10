from django.db import models

class Task(models.Model):
    task = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task

    def complete(self):
        self.is_completed = True
        self.save()
        return self

    def reopen(self):
        self.is_completed = False
        self.save()
        return self

    def toggle_complete(self):
        self.is_completed = not self.is_completed
        self.save()
        return self
    
    
