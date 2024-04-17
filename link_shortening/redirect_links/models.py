from django.db import models
import random

char = ['a','b','c','d','f','g','h','i','j',
        'k','l','m','n','o','p','q','r','s',
        't','u','v','w','x','y','z','1','2',
        '3','4','5','6','7','8','9','0']


# def generate_short_link() -> str:
#     not_unique = True
#     while not_unique:
#         unique_ref = ''.join(random.choices(char, k=10))
#         if not Links.objects.filter(short_link = unique_ref):
#             not_unique = False
#     return unique_ref

class Companies(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=500)
    short_link = models.CharField(max_length=64, unique=True)
    user_id = models.IntegerField(blank=True, null=True)


