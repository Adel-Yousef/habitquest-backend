from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Challenge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Participation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='participations')
    join_date = models.DateField('Join date', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.challenge.title}'
    
    class Meta:
        ordering = ['-join_date']
        
        unique_together = ['user', 'challenge']

PROGRESS_STATUS = (
    ('D', 'Done'),
    ('S', 'Skipped'),
    ('P', 'Partial')
)

class Progress(models.Model):
    date = models.DateField('Progress date')
    status = models.CharField(max_length=1, choices=PROGRESS_STATUS)
    participation = models.ForeignKey(Participation, on_delete=models.CASCADE, related_name='progress')

    def __str__(self):
        return f'{self.get_status_display()} - {self.date}'
    
    class Meta:
        ordering = ['-date']