import requests
from location.models import Location, Parameter
from datetime import date, timedelta, timezone, time, datetime
from dateutil import tz, parser
import logging
from pprint import pformat, pprint
from statistics import mean
import json

##
#
def getUpdateLocData():
    
    myloc = Location.objects.all()

    #logger=logging.getLogger('django')

    for i in myloc:
        
        locAgg =[]
        params=i.parameter_set.all()
        
        #logger.info("Location :" + i.location_name )
        returnData = apiCallHistory(i.location_lat, i.location_lon)

        if params:

            for y in params:               
                #logger.info(pformat(returnData))
                y.latest_value=json.dumps({returnData['current']['dt'] : returnData['current'][y.parameter_key_name]})

                myparaHist={}
                for z in returnData['hist_hourly']:
                    myparaHist[z['dt']] = z[y.parameter_key_name]
                y.values=json.dumps(myparaHist)

                myparaAgg = {
                    'min': min(myparaHist.values()),
                    'mean': round(mean(myparaHist.values()), 2),
                    'max' : max(myparaHist.values())
                }
                y.aggregation = json.dumps(myparaAgg)

                y.save()

                #location aggregation
                locAgg.append( {
                    "id" :y.id,
                    "name" : y.name,
                    "avg" : round(mean(myparaHist.values()), 2),
                    "min" : min(myparaHist.values()),
                    "max" : max(myparaHist.values()),
                    "units" : y.unitsofmeasurment
                    })
        
            i.aggregation=json.dumps(locAgg)
            
        i.location_latest_data = json.dumps(returnData.get('current'))
        i.save()

#get location by name
#
def apiCallSingle(location):

    #apidata = get_object_or_404(WeatherAPI)
    url = "https://api.openweathermap.org/data/2.5/weather?"
    appid = "8efa6f661e49adaa27af6d9d7cd38d69"

    apicall = url + "q=" + location + "&lang=ro&units=metric&mode=json&appid=" + appid

    return requests.get(apicall).json()

# get history data by lon/lat
#
def apiCallHistory(lat, lon) :

    url = "https://api.openweathermap.org/data/2.5/onecall/timemachine?"
    appid = "8efa6f661e49adaa27af6d9d7cd38d69"

    #get history data
    #dt_now=datetime.now(tz=tz.tzlocal())
    dt_now=datetime.now(tz=tz.UTC)
    dt_now_timestamp = int(round(dt_now.timestamp()))

    # Yesterday date
    yesterday = dt_now - timedelta(days = 1)
    yeasterday_timestamp = int(round(yesterday.timestamp()))

    # day before yesterday
    #dby = dt_now - timedelta(days = 2)
    #dby_timestamp = int(round(dby.timestamp()))

    
    apicall_today = url + "lat=" + str(lat) + "&lon=" + str(lon) + "&dt=" + str(dt_now_timestamp) + "&appid=" + appid + "&units=metric"
    apicall_y = url + "lat=" + str(lat) + "&lon=" + str(lon) + "&dt=" + str(yeasterday_timestamp) + "&appid=" + appid + "&units=metric"
    #apicall_dby = url + "lat=" + str(lat) + "&lon=" + str(lon) + "&dt=" + str(dby_timestamp) + "&appid=" + appid + "&units=metric"
    
    res_apicall_today = requests.get(apicall_today).json()
    res_apicall_y = requests.get(apicall_y).json()
    #res_apicall_dby = requests.get(apicall_dby).json()
    #compute final list of data
    #tmp = res_apicall_dby['hourly'] + [ i for i in res_apicall_y['hourly'] if i not in res_apicall_dby['hourly']]
    #final_list = tmp + [i for i in res_apicall_today['hourly'] if i not in tmp]

    final_list = res_apicall_y['hourly'] + [i for i in res_apicall_today['hourly'] if i not in res_apicall_y['hourly']]
    
    #normalize key/parameters returned from api
    #scope : if dict don't have key/parameter set it to 0
    params = getDictKeys(final_list)
    for x in final_list:
        for y in params:
            if y not in x:
                x[y] = 0
    
    #return latest 24h results
    returnData = {}
    returnData['current'] = res_apicall_today['current']
    returnData['hist_hourly'] = final_list[-24:]
    returnData['params'] = params

    return returnData


#get largest dict/key's from a list of dict
#scope : if dict don't have key set it to 0
#
def getDictKeys(val):
    length = 0
    headers = []
    for i in val:
        if isinstance(i, dict):
            if length < len(i.keys()):
                headers=list(i.keys())
                length = len(i.keys())
    return headers


