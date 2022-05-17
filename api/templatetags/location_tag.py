from django import template
import logging, json
from datetime import date, timedelta, timezone, time, datetime

register= template.Library()


@register.filter(name='timeToDate')
def timeToDate(value):
    #val = datetime.fromtimestamp(int(value), timezone.utc).strftime('%d %b %H:%M')
    val = datetime.fromtimestamp(int(value)).strftime('%d %b %H:%M')
    return str(val)
