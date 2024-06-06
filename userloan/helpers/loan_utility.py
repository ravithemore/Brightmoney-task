import random
import calendar
import datetime
from users.models import User
from .constants import MINIMUM_TOTAL_INTREST, \
    MAXIMUM_EMI_VALUE_TO_INCOME, DATE_FORMAT

def add_months(sourcedate, months):
    '''
    add months
    handling if adding month crosses year
    '''
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])

    return datetime.date(year, month, day)

def gen_loan_id(loan_type):
    if loan_type is None:
        loan_type = ''
    now = datetime.datetime.now()
    id = loan_type.lower() + '-' + now.strftime("%m%d%Y%H%M%S")+ \
             '-' + str(random.randint(0,10000))
    return id

class UserLoan():
    def __init__(self, data):
        self.loan = data.get('loan_id')
        self.user = data.get('user_id')
        self.interest_rate = data.get('intrest_rate')
        self.term_period = data.get('term_period')
        self.ammount = data.get('ammount')
        self.disbursement_date = datetime.datetime.strptime(data.get('disbursement_date'), DATE_FORMAT)
        #total intrest
        self.total_intrest = None 
        #intrest and principle and aggregate in each EMI
        self.emi_principle = None
        self.emi_intrest = None
        self.emi_value = None
        #Emi obj
        self.emi_obj_list = []

    def validate_loan_request_on_emi(self):
        '''
        EMI amount must be at-most 60% of the monthly income of the User
        Total interest earned should be >10000
        '''
        error_msg = []
        user_annual_income = User.objects.get(user_id = self.user).annual_income
        user_monthly_income = round((user_annual_income/12), 2)
        user_monthly_income_60_percent = round((user_monthly_income * MAXIMUM_EMI_VALUE_TO_INCOME/100), 2)

        if self.emi_value > user_monthly_income_60_percent:
            error = "EMI amount exceeded 60% of user monthly income"
            error_msg.append(error)

        if self.total_intrest < MINIMUM_TOTAL_INTREST:
            error = f"total intrest less than {MINIMUM_TOTAL_INTREST}"
            error_msg.append(error)

        return error_msg

        
    def calculate_intrest(self):
        '''
        not clear from docs which method to choose either compound or
        simple , not givn compounding period(daily,monthly,yearly)
        ---- goint with simple intresting

        each time intrest will be calculated on 
        remaining principle value
        '''

        unit_principle = round((self.ammount / self.term_period), 2)

        principle = unit_principle
        intrest = 0
        for i in range(self.term_period):
            intrest_ = round(((principle * self.interest_rate) / (12 * 100)), 2)
            intrest = round((intrest + intrest_), 2)
            principle = round((principle + unit_principle), 2)

        self.emi_principle = unit_principle
        self.total_intrest = intrest


    def calculate_emi(self):
        self.calculate_intrest()
        self.emi_intrest = round((self.total_intrest/self.term_period), 2)
        self.emi_value = round((self.emi_principle + self.emi_intrest), 2)


    def generate_emi(self):
        self.calculate_emi()
        #first deu date will be 1st date of upcomming month
        emi_obj_list = []
        dew_date = datetime.date(self.disbursement_date.year, self.disbursement_date.month, 1) 
        for i in range(self.term_period):
            emi_obj = {}
            emi_obj["loan_id"] = self.loan
            emi_obj["emi_amount"] = self.emi_value
            emi_obj["emi_principle"] = self.emi_principle
            emi_obj["emi_intrest"] = self.emi_intrest
            emi_obj["user"] = self.user
            emi_obj["deu_date"] = dew_date.strftime("%Y-%m-%d")
            emi_obj["is_payment_made"] = False

            emi_obj_list.append(emi_obj)
            dew_date = add_months(dew_date,1)

        self.emi_obj_list = emi_obj_list


        





        

