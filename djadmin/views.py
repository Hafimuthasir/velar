from django.shortcuts import render
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from djapp.models import *
from djapp.serializer import *
from .serializers import *

# Create your views here.


@api_view(['POST'])
def logadmin(request):
    print('in logadmin')
    username = request.data['username']
    password = request.data['password']
    print(username, password)
    check = admins.objects.filter(
        user_name=username, password=password).first()
    if check:
        admincheck = 'True'
    else:
        admincheck = 'False'
    return Response(admincheck)


@api_view(['GET', 'POST'])
def userlist(request):
    print('in userlist', request.data)
    if request.data:
        if request.data['auth']:
            print("yes")
            allusers = User.objects.all()
            serializer = UserSerializers(allusers, many=True)
            print(allusers)
            print(serializer.data)
            return Response(serializer.data)
    else:
        print("no")
        return Response("Not authenticated")


@api_view(['PUT'])
def edituser(request, id):
    print('in edit', id)
    print('ddata', request.data)
    data = request.data

    try:
        user = User.objects.get(id=id)
        data['password'] = user.password
        print('ko', data)
    except:
        return Response('User not found in the data')
    editserializer = UserSerializers(user, data)
    if editserializer.is_valid():
        editserializer.save()
        check = User.objects.get(id=id)
        print('io', check)

        return Response(200)
    return Response(editserializer.errors)


@api_view(['POST'])
def deleteuser(request, id):
    try:
        user = User.objects.get(id=id)
        if user.is_blocked == True:
            user.is_blocked = False
        else:
            user.is_blocked = True
        user.save()
        return Response(200)
    except:
        return Response('User not found in the data')


@api_view(['GET', 'PUT'])
def BussinessReq(request, id):
    try:
        check = BussinessRequest.objects.get(user=id)
        return Response('User already in request list')
    except:
        add = BussinessRequest()
        use = User.objects.get(id=id)
        add.user = use
        add.save()
        return Response('added into bussiness requests')


@api_view(['GET'])
def getBussinessReqs(request):
    alldat = BussinessRequest.objects.all()
    serializer = BussinessSerializer(alldat, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def removeBussinessReq(request, id):
    try:
        bussreqdata = BussinessRequest.objects.get(id=id)
        bussreqdata.delete()
        return Response('removed successfully')
    except:
        return Response('Request not found')


@api_view(['GET'])
def acceptBussinessReq(request, id):
        print('kkkkkkk',id)
        busreq = BussinessRequest.objects.get(id = id)
        print('pppp',busreq.user)
        use = User.objects.get(email = busreq.user)
        use.is_bussiness = True
        use.save()
        busreq.delete()
        return Response(200)
   


@api_view(['GET'])
def allPost(request):
        print('kkkkkkk',id)
        busreq = BussinessRequest.objects.get(id = id)
        print('pppp',busreq.user)
        use = User.objects.get(email = busreq.user)
        use.is_bussiness = True
        use.save()
        busreq.delete()
        return Response(200)
