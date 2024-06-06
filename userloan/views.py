from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from rest_framework import status
from .serializers import LoanSerializer, EmiSerializer, PaymentSerializer
from .models import Payment, Emi, Loan
import datetime
import calendar
today = datetime.datetime.today()

from .helpers.loan_utility import UserLoan, gen_loan_id, add_months

class LoanApplicationView(APIView):
  def post(self,request):
    data = request.data
    loan_id = gen_loan_id(data.get('loan_type'))
    data.update({'loan_id':loan_id})
    serializer = LoanSerializer(data=data)

    if serializer.is_valid():
        UserLoan_obj = UserLoan(data)
        UserLoan_obj.generate_emi()
        
        errors = UserLoan_obj.validate_loan_request_on_emi()
        if len(errors) == 0:
            data.update({"intrest":UserLoan_obj.total_intrest})
            serializer_emi = EmiSerializer(data=UserLoan_obj.emi_obj_list, many=True)
            serializer.save()
            if serializer_emi.is_valid():
                serializer_emi.save()
                emi_date_amount_list = [{"Emi_date":item['deu_date'],"Amount_due":item['emi_amount']} \
                                            for item in UserLoan_obj.emi_obj_list]
                resp = {
                    "loan_id":data['loan_id'],
                    "Due_dates":emi_date_amount_list
                }
                return Response(resp,status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_emi.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PaymentView(APIView):
    def post(self,request):
        data = request.data
        loan_id = data.get('loan_id')
        month = today.month
        year = today.year

        deu_date = add_months(datetime.date(year, month, 1),1)
        if loan_id:
            loan_obj_qs = Loan.objects.filter(loan_id=loan_id)
            emi_obj_qs = Emi.objects.filter(loan_id=loan_id, deu_date=deu_date)
            loan_obj = loan_obj_qs[0] if len(loan_obj_qs) > 0 else {}
            emi_obj = emi_obj_qs[0] if len(emi_obj_qs) > 0 else {}
        

            if loan_obj:
                data['user'] = loan_obj.user_id
            else:
                return Response(f"loan_id {loan_id} does not exist",status=status.HTTP_400_BAD_REQUEST)

            if emi_obj:
                if emi_obj.is_payment_made:
                    return Response(f"payment already made for this due date: {deu_date}",status=status.HTTP_400_BAD_REQUEST)
                else:
                    data['emi_id'] = emi_obj.id
            else:
                return Response(f"no emi-deu exist for this loan_id:{loan_id}",status=status.HTTP_400_BAD_REQUEST)
        
        import pdb;pdb.set_trace()
        data['payment_date'] = today.strftime("%Y-%m-%d")
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            emi_obj.is_payment_made = True
            emi_obj.save()

            #EMI Ammount recalculation is user paid less or more
            if data['paid_ammount'] != emi_obj.emi_amount:
                param = {}
                param['loan_id'] = loan_obj.loan_id
                param['disbursement_date'] = loan_obj.disbursement_date.strftime("%Y-%m-%d")
                param['user'] = loan_obj.user_id
                param['intrest_rate'] = loan_obj.intrest_rate

                diffrence = emi_obj.emi_amount - data['paid_ammount']
                remaining_principle = Emi.objects.filter(loan_id=loan_id, is_payment_made=False) \
                    .values('loan_id').annotate(remaining_principle = Sum('emi_principle'))[0]['remaining_principle']

                remaining_period = Emi.objects.filter(loan_id=loan_id, is_payment_made=False) \
                    .values('loan_id').annotate(remaining_period = Count('deu_date'))[0]['remaining_period']

                revised_principle = remaining_principle + diffrence
                param['ammount'] = revised_principle
                param['term_period'] = remaining_period

                UserLoan_obj = UserLoan(param)
                UserLoan_obj.calculate_emi()
                emi_obj_qs = Emi.objects.filter(loan_id=loan_id, is_payment_made=False)

                for obj in emi_obj_qs:
                    obj.emi_intrest = UserLoan_obj.emi_intrest
                    obj.emi_principle = UserLoan_obj.emi_principle
                    obj.emi_amount = UserLoan_obj.emi_value
                    obj.save()
            
            return Response({"msg":"sucessfull"},status=status.HTTP_201_CREATED)
        else:
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
            

class TransactionView(APIView):
    def get(self,request):
        data = request.data
        loan_id = data.get('loan_id')
        if loan_id:
            loan_obj_qs = Loan.objects.filter(loan_id=loan_id)
            emi_obj_qs = Emi.objects.filter(loan_id=loan_id)

        else:
            return Response(f"loan_id is required",status=status.HTTP_400_BAD_REQUEST)

        if len(loan_obj_qs) == 0:
            return Response(f"loan_id is not valid",status=status.HTTP_400_BAD_REQUEST)

        past_transaction = []
        upcoming_transaction = []
        for obj in emi_obj_qs:
            resp = {}
            payment_obj_qs = Payment.objects.filter(emi_id=obj.id)
            if len(payment_obj_qs) > 0:
                resp['date'] = obj.deu_date
                resp['principle'] = obj.emi_principle
                resp['intrest'] = obj.emi_intrest 
                resp['Amount_paid'] = payment_obj_qs[0].paid_ammount

                past_transaction.append(resp)
            else:
                resp['date'] = obj.deu_date
                resp['Amount_deu'] = obj.emi_amount
                #not clear what to do with past emi for which no transaction exist so adding it in upcoming
                upcoming_transaction.append(resp)

        final_resp = {
            "past transaction": past_transaction,
            "upcoming transaction": upcoming_transaction
        }

        return Response(final_resp,status=status.HTTP_201_CREATED)



        


        







