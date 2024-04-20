from django.db import models


class Companies(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    short_link = models.CharField(max_length=64, unique=True)
    data = models.DateField(auto_now_add=True, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

class Sesions(models.Model):
    id_company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    user_id = models.IntegerField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)
    ip_user = models.GenericIPAddressField()
    browser = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


