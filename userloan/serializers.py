from rest_framework import serializers
from .models import Loan, Emi, Payment
from users.models import User

from .helpers.constants import MINIMUM_INTEREST_RATE, \
    MINIMUM_CREDIT_SCORE_TO_AVAIL_LONE, MINIMUM_ANNUAL_SALARY_TO_AVAIL_LONE, \
        CAR_LOAN_MAXIMUM_AMOUNT, HOME_LOAN_MAXIMUM_AMMOUNT, EDUCATIONAL_LOAN_MAXIMUM_AMOUNT, \
            PERSONAL_LOAN_MAXIMUM_AMMOUNT

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
      model = Loan
      fields = ['loan_id','loan_type','user_id','ammount','term_period','intrest_rate','disbursement_date']
    
    def validate(self, data):
        try:
            user = User.objects.get(user_id=data.get('user_id'))
        except Exception as e:
            raise serializers.ValidationError('user does not exist')
        
        intrest_rate = data.get('intrest_rate')
        user_annual_income = user.annual_income
        user_credit_score = user.credit_score
        loan_type = data.get('loan_type')
        ammount = data.get('ammount')

        if intrest_rate < MINIMUM_INTEREST_RATE:
            raise serializers.ValidationError(f'intrest rate provided is lower than {MINIMUM_INTEREST_RATE} percent')

        if user_credit_score < MINIMUM_CREDIT_SCORE_TO_AVAIL_LONE:
            raise serializers.ValidationError(f'user credit score is lower than {MINIMUM_CREDIT_SCORE_TO_AVAIL_LONE}')

        if user_annual_income < MINIMUM_ANNUAL_SALARY_TO_AVAIL_LONE:
            raise serializers.ValidationError(f'user annual salary  is lower than {MINIMUM_ANNUAL_SALARY_TO_AVAIL_LONE}')

        if loan_type == 'Car' and ammount > CAR_LOAN_MAXIMUM_AMOUNT:
            raise serializers.ValidationError(f'maximum ammount to be availed for car loan is {CAR_LOAN_MAXIMUM_AMOUNT}')

        if loan_type == 'Home' and ammount > HOME_LOAN_MAXIMUM_AMMOUNT:
            raise serializers.ValidationError(f'maximum ammount to be availed for home loan is {HOME_LOAN_MAXIMUM_AMMOUNT}')

        if loan_type == 'Educational' and ammount > EDUCATIONAL_LOAN_MAXIMUM_AMOUNT:
            raise serializers.ValidationError(f'maximum ammount to be availed for education loan is {EDUCATIONAL_LOAN_MAXIMUM_AMOUNT}')

        if loan_type == 'Personal' and ammount > PERSONAL_LOAN_MAXIMUM_AMMOUNT:
            raise serializers.ValidationError(f'maximum ammount to be availed for personal loan is {PERSONAL_LOAN_MAXIMUM_AMMOUNT}')
        
        return data

class EmiSerializer(serializers.ModelSerializer):
    class Meta:
      model = Emi
      fields = ["id","loan_id","emi_amount","emi_principle","emi_intrest","user","deu_date","is_payment_made"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
      model = Payment
      fields = ["loan_id","paid_ammount","payment_date","emi_id","loan_id","user"]