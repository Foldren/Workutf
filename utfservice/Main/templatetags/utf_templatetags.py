from django import template
from os import listdir

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def appjsfilesurls(app_name):
    listUrls = list()

    for element in listdir(path="/home/workutf/utfservice/static/js/"+app_name):
        listUrls.append("/static/js/"+app_name+"/"+element)

    return listUrls


@register.filter
def appcssfileurl(app_name):
    return "/static/css/"+app_name.lower()+".css"


@register.filter()
def to_int(value):
    return int(value)