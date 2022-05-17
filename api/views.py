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
from location.serializers import *
import logging
from pprint import pformat, pprint

from jobs.getData import apiCallSingle, apiCallHistory

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
        data=LocationViewSerializer(locations, many=True).data
        return Response(data)

    elif request.method == 'POST':
        
        response = apiCallSingle(request.data['location_name'])
        
        #logger=logging.getLogger('django')
        #logger.info('Args :' +pformat(response))
        #logger.info('Object :' +pformat(type(response)))
        
        status_data={}
        
        if (response['cod'] == 200):
            hyst_data = apiCallHistory(response['coord']['lat'], response['coord']['lon'])
            #logger.info('Hyst Data :' + pformat(hyst_data))
            
            
            # delete parametres thar are constant or not/aggregation
            hyst_data['params'].remove('dt')
            hyst_data['params'].remove('weather')

            build_data = {
                'description' : request.data['location_name'],
                'location_name' : request.data['location_name'],
                'location_lat' : response['coord']['lat'],
                'location_lon' : response['coord']['lon'],
                'location_country' : response['sys']['country'],
                'location_timezone' : response['timezone'],
                'location_id' : response['id'],
                'location_avail_params' : str(hyst_data['params'])        
            }
            location = Location(user=request.user)
            serializer = LocationAddSerializer(location, data = build_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                status_data['status'] = 'Location added !'
                status_data['response'] = response
                return Response(status_data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            status_data['status'] = 'We have an errror !'
            status_data['data'] = response
            return Response(status_data, status=status.HTTP_404_NOT_FOUND)


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

        location_id = Parameter(location_id = kwargs['lk'])
        
        status_data={}

        #logger=logging.getLogger('django')
        #logger.info('Args :' +pformat(location.location_avail_params))
        #logger.info('Args :' +pformat(type(list(location.location_avail_params))))
        location_para = list(location.location_avail_params)
        if request.data['parameter_key_name'] not in location_para:
            status_data['error'] = 'We have an error : parameter not in list !'
            status_data['data'] = request.data
            return Response(status_data, status=status.HTTP_400_BAD_REQUEST)

        
        serializer = LocationAddParameterSerializer(location_id, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            status_data['status'] = 'Location Parameter added !'
            status_data['data'] = serializer.data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "DELETE"])
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

    #elif request.method == 'POST':
    #    status_data={}
    #    serializer = LocationParameterDetailSerializer(data = request.data, partial=True)
    #    if serializer.is_valid():
    #        serializer.save()
    #        status_data['status'] = 'Location Parameter modified !'
    #        return Response(serializer.data, status=status.HTTP_201_CREATED)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        action = location_para.delete()
        status_data={}
        if action:
            status_data['status'] = 'Location paramenter, ' + location_para.name + ' deleted !'
        else: 
            status_data['status'] = 'We have an error deleting this location :' + location_para.name
        return Response(data=status_data)
