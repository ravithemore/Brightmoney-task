from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

from users.helpers.celery_task import get_credit_score

class UserView(APIView):
  def post(self,request):
    import pdb;pdb.set_trace()
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      res = get_credit_score.delay(request.data.get('user_id'))
      return Response({'uuid':request.data.get('user_id')},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
  

