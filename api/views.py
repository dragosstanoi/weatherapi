from functools import partial
from pickle import FALSE
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from location.models import Location, Parameter
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from location.serializers import LocationSerializer, DetailLocationSerializer, LocationParameterSerializer, LocationParameterDetailSerializer
import logging
from pprint import pformat, pprint

#from account.models import Account
#from rest_framework.authtoken.models import Token


# Create your views here.


def api_login(request):

    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            user=authenticate(request, username=request.POST.get('username'), password= request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username or password is incorrect')

        return render(request, 'login.html')


def api_logout(request):
    logout(request)
    return redirect('login')



@login_required(login_url='/login/')
def api_home(request):

    #run once
    #for user in Account.objects.all():
    #    Token.objects.get_or_create(user=user)

    context = {}
    return render(request, "index.html", context)
    

@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_locations(request, *args, **kwargs):

    try:
        locations = Location.objects.filter(user=request.user)
    except Location.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data=LocationSerializer(locations, many=True).data
        return Response(data)

    elif request.method == 'POST':
        location = Location(user=request.user)
        status_data={}
        serializer = LocationSerializer(location, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_data['status'] = 'Location added !'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_location_detail(request, *args, **kwargs):
    
    #logger=logging.getLogger('django')
    #logger.info('Args :' +pformat(kwargs))
    
    user=request.user

    try:
        location = Location.objects.get(pk = kwargs['pk'])   
        if location.user != user:
            return Response({'response' : "You do not have permissions for this."})

    except Location.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data=DetailLocationSerializer(location).data
        return Response(data)
    
    elif request.method == 'PATCH':
        status_data={}
        serializer = DetailLocationSerializer(location, data = request.data, partial=True)
        if serializer.is_valid(raise_exception=True):

            logger=logging.getLogger('django')
            logger.info('Validated data :' + pformat(dir(serializer)))
            #
            # Just user information
            if(request.data.get('location_name') or request.data.get('location_lat') or request.data.get('location_lon') or request.data.get('user')):
               status_data['error'] = 'You can\'t modify location name/latitude/longitude or user. !'
               return Response(data=status_data)

            serializer.save()
            
            status_data['status'] = 'Location updated !'
            status_data['data'] = request.data
            return Response(data=status_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        action = location.delete()
        status_data={}
        if action:
            status_data['status'] = 'Location, ' + location.location_name + ' deleted !'
        else: 
            status_data['status'] = 'We have an error deleting this location :' + location.location_name
        return Response(data=status_data)


@api_view(["GET", "POST"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_location_parameters(request, *args, **kwargs):

    user=request.user

    try:
        location = Location.objects.get(pk = kwargs['lk'])
        location_para = location.parameter_set.all()
        if location.user != user:
            return Response({'response' : "You do not have permissions for this."})
    except Location.DoesNotExist or Parameter.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data=LocationParameterSerializer(location_para, many=True).data
        return Response(data)

    elif request.method == 'POST':
        status_data={}
        serializer = LocationParameterSerializer(data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_data['status'] = 'Location Parameter added !'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def api_location_parameters_detail(request, *args, **kwargs):

    user = request.user

    try:
        location = Location.objects.get(pk = kwargs['lk'])
        location_para = Parameter.objects.get(pk = kwargs['pk'])
        if location.user != user:
            return Response({'response' : "You do not have permissions for this."})
    except Location.DoesNotExist or Parameter.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data=LocationParameterDetailSerializer(location_para).data
        return Response(data)

    elif request.method == 'POST':
        status_data={}
        serializer = LocationParameterDetailSerializer(data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_data['status'] = 'Location Parameter modified !'
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        action = location_para.delete()
        status_data={}
        if action:
            status_data['status'] = 'Location paramenter, ' + location_para.name + ' deleted !'
        else: 
            status_data['status'] = 'We have an error deleting this location :' + location_para.name
        return Response(data=status_data)
