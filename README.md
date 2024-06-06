# assesment_brightmoney_

to populate data :
	python3 manage.py populate transaction
	
	
make sure django server running
	python3 manage.py runserver
	

make sure your redis server running
> ping
pong


to start celery worker 
	celery -A loan_api worker -l info
	

endpoints:
	http://127.0.0.1:8000/api/register
method:
	post
payload:
	{
    "user_id": "01995856-968e-4b41-8893-a0535d2c3a33",
    "name": "kusum jha",
    "email_id": "kusum@gmail.com",
    "annual_income": 100000
}


endpoints:
	http://127.0.0.1:8000/api/apply-loan
method:
	post
payload:
	{
"loan_type":"Car",
"user_id":"01995856-968e-4b41-8893-a0535d2c3a33",
"ammount":500000,
"term_period":84,
"intrest_rate":15,
"disbursement_date":"2023-09-13"
}


endpoints:
	http://127.0.0.1:8000/api/make-payment
method:
	post
payload:
	{
    "loan_id":"car-10092023011753-9817",
    "paid_ammount":9000
}


endpoints:
	http://127.0.0.1:8000/api/get-statement
method:
	get
payload:
	{
    "loan_id": "car-10092023011753-9817"
}
