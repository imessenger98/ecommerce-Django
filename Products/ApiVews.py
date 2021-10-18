from rest_framework import serializers
from rest_framework.response import Response, responses
from rest_framework.decorators import api_view, permission_classes
from Vendor import models
from .models import User, order
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
# for importing token model
from rest_framework.authtoken.models import Token


@api_view()
@permission_classes([IsAuthenticated])
def showallusers(request):
    ad=User.objects.all()
    serializers=UserSerializer(ad,many=True)
    return Response(serializers.data)

@api_view()
def showallorders(request):
    ad=order.objects.all()
    serializers=UserSerializer(ad,many=True)
    return Response(serializers.data)

@api_view(['POST'])
def addcustomer(request):
    if request.method=="POST":
        email=request.data.get('email')
        password=request.data.get('password')
        address=request.data.get('address')
        postcode=request.data.get('postcode')
        city=request.data.get('city')
        phone=request.data.get('phone')
        k=User.objects.create_user(email=email,password=password,address=address,postcode=postcode,city=city,phone=phone)
        ad=User.objects.filter(email=k)
        serializer=UserSerializer(ad, many=True)
    return Response(serializers.data)

@api_view(['DELETE'])
def deletecustomer(request,param):
        # email=request.data.get('email')
        ad=User.objects.get(email=param)
        ad.delete()
        return Response("data removed successfully")
    
@api_view(['PUT'])
def updatecustomer(request,param):
        print(param)
        if request.method=="PUT":
            print("i am here")
            kmn=User.objects.filter(email=param).values()
            print("kmn:",kmn)
            email=request.data.get('email')
            password=request.data.get('password')
            address=request.data.get('address')
            postcode=request.data.get('postcode')
            city=request.data.get('city')
            phone=request.data.get('phone')
            kmn.update(email=email,password=password,address=address,postcode=postcode,city=city,phone=phone)
            print("data updated successfully")            
            return Response("data update successfully")


#token signup
@api_view(["POST"])
def sugnup(request):
    if request.method =="POST":
        email=request.data.get('email')
        password=request.data.get('password')
        u=User.objects.create_user(email=email,password=password)
        Token.objects.create(user=u)
        t=Token.objects.get(user=u).key
        return Response(data={"email":u.email,"response":"Successfully Registered a user","token":t})