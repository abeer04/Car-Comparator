from django.db import models
from datetime import datetime, timedelta

# Create your models here.
"""
Fields are added to the class to specify the columns of
the model's table in the database.
"""

def setExpiryTime():
    return datetime.now() + timedelta(hours = 6) # set it 6 hours from now

class Keyword(models.Model):
    keyword_id = models.AutoField(primary_key=True)
    unique_id = models.CharField(max_length=100, default=None, blank=True, null=True)
    keyword = models.TextField()
    expiryTime = models.DateTimeField(default=setExpiryTime)

    # This is for basic and custom serialization to return it to client as a JSON.
    # @property
    # def to_dict(self):
    #     data = {
    #         'data': json.loads(self.data),
    #         'date': self.date
    #     }
    #     return data

    # def __str__(self):
    #     return self.keyword_id

class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    url = models.TextField()
    title = models.TextField()
    price = models.IntegerField()
    location = models.CharField(max_length=100)
    model = models.TextField()
    mileage = models.IntegerField()
    fuel = models.CharField(max_length=20)
    engine = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)

    # This is for basic and custom serialization to return it to client as a JSON.
    # @property
    # def to_dict(self):
    #     data = {
    #         'data': json.loads(self.data),
    #         'date': self.date
    #     }
    #     return data

    # def __str__(self):
    #     return self.car_id

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    url = models.TextField()
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)

    # This is for basic and custom serialization to return it to client as a JSON.
    # @property
    # def to_dict(self):
    #     data = {
    #         'data': json.loads(self.data),
    #         'date': self.date
    #     }
    #     return data

    # def __str__(self):
    #     return self.image_id

class KeywordCar(models.Model):
    keywordCar_id = models.AutoField(primary_key=True)
    keyword_id = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)

    # This is for basic and custom serialization to return it to client as a JSON.
    # @property
    # def to_dict(self):
    #     data = {
    #         'data': json.loads(self.data),
    #         'date': self.date
    #     }
    #     return data

    # def __str__(self):
    #     return self.unique_id