from django.db import models
from adaptor.model import CsvModel
from reviews.models import CustomUser


class MyCsvModel(CsvModel):
    id = models.AutoField(match="id")
    username = models.CharField(match="username")
    email = models.EmailField(match="email")
    role = models.CharField(match="role")
    bio = models.TextField(match="bio")
    first_name = models.CharField(match="first_name")
    last_name = models.CharField(match="last_name")

    class Meta:
        delimiter = ","
        dbModel = CustomUser
