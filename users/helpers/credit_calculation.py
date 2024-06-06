from users.models import Transaction,User
from django.db.models import Sum
from .constants import TRANSACTION_DEBIT, TRANSACTION_CREDIT

class UserTransactionProfile():
    def __init__(self, user_id):
        self.user_id = user_id

    def is_user_transaction_exist(self):
        is_exist = Transaction.objects.filter(user_id=self.user_id).exists()
        return is_exist

    def get_total_debited_ammount(self):
        total_debit = Transaction.objects.filter(user_id=self.user_id, transaction_type=TRANSACTION_DEBIT) \
                        .values('user_id').annotate(total_debit = Sum('ammount'))[0]['total_debit']

        return total_debit
        
    def get_total_credited_ammount(self):
        total_credit = Transaction.objects.filter(user_id=self.user_id, transaction_type=TRANSACTION_CREDIT) \
                        .values('user_id').annotate(total_credit = Sum('ammount'))[0]['total_credit']

        return total_credit

