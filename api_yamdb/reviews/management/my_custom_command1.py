from adaptor.model import CsvModel
from reviews.models import CustomUser


class MyCsvModel(CsvModel):

    class Meta:
        delimiter = ";"
        dbModel = CustomUser
