from django.db import models
from django.core.validators import MinLengthValidator

class County(models.Model):
    fip = models.IntegerField()
    countyName = models.CharField(max_length=100)
    stateName = models.CharField(max_length=100)

class CountyCase(models.Model):
    county  = models.ForeignKey('County', null=False, 
                                on_delete=models.CASCADE)

    cases  = models.IntegerField()
    deaths = models.IntegerField()

    date = models.DateField()
    
    def __radd__(self, other):
        if other:
            cases_other, deaths_other = other
        else:
            cases_other, deaths_other = 0, 0

        return (self.cases+cases_other, self.deaths+deaths_other)

    def __str__(self):
        return self.county.countyName

class Order(models.Model):
    stateName = models.CharField(max_length=100, null=False)
    title     = models.CharField(max_length=1000, null=False)
    url       = models.CharField(max_length=1000, null=False)
    date      = models.DateField(null=True)

