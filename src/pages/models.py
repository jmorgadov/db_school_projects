from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.TextField()
    raze = models.TextField()
    damage = models.IntegerField()
    weakness = models.TextField()

class Beast(models.Model):
    name = models.TextField()
    raze = models.TextField()