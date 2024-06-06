from django.core.management.base import BaseCommand
import pandas as pd
from users.models import Transaction

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        df = pd.read_csv('/home/oem/Downloads/data.csv')
        for ind in df.index:
            print(f'populating data of row: {ind}')
            models = Transaction(user_id=df['user'][ind], date=df['date'][ind], transaction_type=df['transaction_type'][ind], ammount=df['amount'][ind])
            models.save()
