from django.db import models
from django.utils import timezone

import datetime

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Building(models.Model):
    name = models.CharField(max_length=200)
    start_use = models.DateTimeField('date started using', blank=True)
    end_use = models.DateTimeField('date ended using', blank=True)
    zipcode = models.IntegerField('zip code')
    latitude = models.FloatField('latitude', default=180)
    longitude = models.FloatField('longitude', default=180)
    def __str__(self):
        return self.name

class Breaker_Position(models.Model):
    name = models.CharField(max_length=24)
    def __str__(self):
        return self.name

class Breaker_Orientation(models.Model):
    name = models.CharField(max_length=24)
    def __str__(self):
        return self.name

class Breaker_Capacity(models.Model):
    name = models.IntegerField('amps', unique=True)
    def __str__(self):
        return self.name

class Breaker_Poles(models.Model):
    poles = models.IntegerField('single or double', unique=True)
    def __str__(self):
        return str(self.poles)

class Panel(models.Model):
    code = models.CharField(max_length=10)
    building = models.ForeignKey(Building, null=True, on_delete=models.SET_NULL)
    start_use = models.DateTimeField('date started using', blank=True)
    end_use = models.DateTimeField('date ended using', blank=True)
    main_amps = models.IntegerField('main breaker amps')
    brand_model = models.CharField('brand and model', max_length=36, blank=True)
#    parent = models.ForeignKey(Breaker, 'if sub-panel', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.code

class Breaker(models.Model):
    number = models.IntegerField(default=0)
    orientation = models.ForeignKey(Breaker_Orientation, null=True, on_delete=models.SET_NULL)
    position = models.ForeignKey(Breaker_Position, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=24)
    panel = models.ForeignKey(Panel, null=True, on_delete=models.SET_NULL)
    start_use = models.DateTimeField('date started using', blank=True)
    end_use = models.DateTimeField('date ended using', blank=True)
    capacity = models.ForeignKey(Breaker_Capacity, null=True, on_delete=models.SET_NULL)
    poles = models.ForeignKey(Breaker_Poles, null=True, on_delete=models.SET_NULL)
    paired_breaker = models.CharField(max_length=10, blank=True)
    gfci = models.BooleanField('is GFCI?', default=False)
    afci = models.BooleanField('is AFCI?', default=False)
#    feeds_sub = models.ForeignKey(Panel, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return str(self.number)

class Room(models.Model):
    name = models.CharField(max_length=40, blank=True)
    building = models.ForeignKey(Building, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name

class Device_Type(models.Model):
    name = models.CharField(max_length=24, unique=True)
    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=40, blank=True)
    type = models.ForeignKey(Device_Type, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    breaker = models.ForeignKey(Breaker, null=True, on_delete=models.SET_NULL)
    start_use = models.DateTimeField('date started using', blank=True)
    end_use = models.DateTimeField('date ended using', blank=True)
    gfci = models.BooleanField('is GFCI?', default=False)
    afci = models.BooleanField('is AFCI?', default=False)
#    feeds_sub = models.ForeignKey(Panel, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name

