from django.db import models

class sub(models.Model):
    content = models.TextField()
    label = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    
