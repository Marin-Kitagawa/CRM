from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Models resemble database tables see References directory

class Patient(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  #  Whenever a user is deleted we delete the relationship to the customer
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='default.jpg', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)



    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)


class Game(models.Model):
    CATEGORY = (
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('Puzzle','Puzzle'),
        ('RPG','RPG'),
        ('Racing','Racing'),
    )
    name = models.CharField(max_length=200, null=True)
    score = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return str(self.name)


class Activity(models.Model):
    STATUS = (
        ('UPF', 'UPF'),
        ('ELP', 'ELP'),
        ('OPF', 'OPF'),
    )
    patient = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)
    # Customers to be a reference to a parent i.e. One-to-many relationship
    # On deleting the customer we don't delete the order because it is a bad design. So, we SET_NULL to have an order without customer.
    game = models.ForeignKey(Game, null=True, on_delete=models.SET_NULL)
    # 1tomany relationship because we don't want to set the string value to be set every single time a product is ordered.
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)


    def __str__(self):
        return str(self.game.name)
