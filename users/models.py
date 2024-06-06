from django.db import models
from loan_api.common_utils.model_utils import Basemodel

class User(Basemodel):
    user_id = models.CharField(max_length=36, primary_key=True)
    name=models.CharField(max_length=30)
    email_id=models.CharField(max_length=30000)
    annual_income=models.IntegerField()
    credit_score=models.IntegerField(blank=True, default=0)
    is_credit_score_genrated=models.BooleanField(blank=True, default=False)
    
    def __str__(self):
        return self.user_id

class Transaction(Basemodel):
    user_id = models.CharField(max_length=36)
    date = models.DateField()
    transaction_type = models.CharField(max_length=8)
    ammount = models.IntegerField()
