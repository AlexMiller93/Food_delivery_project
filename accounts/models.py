from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Card(models.Model):
    bank = models.CharField(max_length=40, default='Bank New America')
    number = models.CharField(max_length=16)
    deadline = models.DateTimeField()
    cvv = models.CharField(max_length=3)
    user = models.ForeignKey(User,
                             blank=True,
                             null=True,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} card's with number {self.number}"


class Account(models.Model):
    USER_TYPES = (
        ('Customer', 'Customer'),
        ('Manager', 'Manager'),
        ('Courier', 'Courier'),
        ('Cook', 'Cook')
    )
    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    user = models.OneToOneField(User,
                                related_name='accounts',
                                on_delete=models.CASCADE)

    user_type = models.CharField(max_length=8,
                                 choices=USER_TYPES,
                                 default='Customer')

    points = models.SmallIntegerField(default=0, blank=True, null=True)
    gender = models.CharField(max_length=6,
                              choices=GENDERS,
                              default='Male')

    address = models.CharField(max_length=100)
    card = models.ForeignKey(Card,
                             null=True,
                             blank=True,
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.user_type}'

    class Meta:
        ordering = ['-user_type']
