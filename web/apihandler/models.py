from django.db import models


class Events(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    purposed_datetime = models.DateTimeField(blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f'Event {self.title} {self.purposed_datetime}:\n'
                f'{self.description}\n'
                f'created at: {self.created_datetime}\n')

    class Meta:
        ordering = ['-created_datetime']
