from django.conf import settings
from django.db import models
from django.utils import timezone


class Task(models.Model):
    PRIORITY = [('L', 'Low'), ('M', 'Medium'), ('H', 'High')]
    STATUS = [('T', 'To Do'), ('P', 'In Progress'), ('D', 'Done')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY, default='M')
    status = models.CharField(max_length=1, choices=STATUS, default='T')
    due_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', 'due_date', '-created']

    def __str__(self):
        return self.title

    @property
    def overdue(self):
        return bool(self.due_date and self.status != 'D' and self.due_date < timezone.localdate())
