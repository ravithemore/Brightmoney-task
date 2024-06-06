from celery import shared_task

from users.helpers.constants import  MAXIMUM_THRESHOLD_AMMOUNT, \
    MAXIMUM_CREDIT_VALUE, MINIMUM_THRESHOLD_AMMOUNT, MINIMUM_CREDIT_VALUE, UNIT_NET_TRANSACTION, \
    UNIT_CREDIT_POINT
from users.helpers.credit_calculation import UserTransactionProfile
from users.models import User

@shared_task
def get_credit_score(user_id):
    ut_obj = UserTransactionProfile(user_id)
    user = User.objects.get(user_id=user_id)
    if ut_obj.is_user_transaction_exist():
        total_debit = ut_obj.get_total_debited_ammount()
        total_credit = ut_obj.get_total_credited_ammount()
        net = total_credit - total_debit
        if net >= MAXIMUM_THRESHOLD_AMMOUNT:
            credit_score = MAXIMUM_CREDIT_VALUE

        elif net <= MINIMUM_THRESHOLD_AMMOUNT:
            credit_score = MINIMUM_CREDIT_VALUE

        else:
            credit_score = MINIMUM_CREDIT_VALUE + ((net - MINIMUM_THRESHOLD_AMMOUNT) // UNIT_NET_TRANSACTION) * UNIT_CREDIT_POINT

        user.credit_score = credit_score
        user.is_credit_score_genrated = True
        user.save()
    else:
        user.is_credit_score_genrated = True
        user.save()
        print(f'no transaction exist for user:{user_id}')