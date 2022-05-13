from django.db import models


# Create your models here.

# register user
'''
class user(models.Model):
    admin = 'admin'
    player = 'player'
    coach = 'coach'
    userTypeChoices = [
        (admin, 'Admin'),
        (player, 'Player'),
        (coach, 'Coach'),
    ]
    userId = models.AutoField(primary_key=True)  # automatically generated
    account = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=20, blank=False)
    type = models.CharField(
        max_length=20,
        choices=userTypeChoices,
        default=player,
        blank=False,
    )

    def __str__(self):
        return self.userId


class team(models.Model):
    teamId =models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=20, blank=False)
    '''