from django.db import models
from loan_api.common_utils.model_utils import Basemodel
from users.models import User

class Loan(Basemodel):
    LOAN_TYPE_CHOICES = [
        ("Car","car"),
        ("Home","home"),
        ("Educational",'educational'),
        ("Personal","personal")
    ]   

    loan_id = models.CharField(max_length=40, primary_key=True)
    loan_type = models.CharField(max_length=30, choices=LOAN_TYPE_CHOICES)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_user_rel')
    ammount =  models.FloatField()
    intrest = models.FloatField(blank=True, default=0)
    term_period = models.IntegerField()
    intrest_rate = models.FloatField()
    disbursement_date = models.DateField()

    def __str__(self):
        return self.loan_id


class Emi(Basemodel):
    id = models.AutoField(primary_key=True)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='emi_loan_rel') 
    emi_amount = models.FloatField()
    emi_principle = models.FloatField()
    emi_intrest = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emi_user_rel')
    deu_date = models.DateField()
    is_payment_made = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return str(self.id)
    

class Payment(Basemodel):
    id = models.AutoField(primary_key=True)
    emi_id = models.OneToOneField(Emi, on_delete=models.CASCADE, related_name='pmnt_emi_rel')
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='pmnt_loan_rel') 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pmnt_user_rel')
    paid_ammount = models.FloatField()
    payment_date = models.DateField(blank=True)




