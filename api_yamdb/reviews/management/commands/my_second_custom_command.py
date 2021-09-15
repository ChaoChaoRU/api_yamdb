from django.db import models
from adaptor.model import CsvModel
from reviews.models import CustomUser


class MyCsvModel(CsvModel):
    id = models.AutoField()
    username = models.CharField()
    email = models.EmailField()
    role = models.CharField()
    bio = models.TextField()
    first_name = models.CharField()
    last_name = models.CharField()

    class Meta:
        delimiter = ","
        dbModel = CustomUser
