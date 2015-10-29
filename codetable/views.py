from django.shortcuts import render,get_object_or_404,redirect#render_to_response,
from django.template import RequestContext
from .models import Code
from django.core.exceptions import ObjectDoesNotExist
from .forms import CodeForm

import requests

def home(request):
    #form = CodeForm()
    if request.method=="POST":
        print("invalid")
        form = CodeForm(data = request.POST)
        print(form.errors)
        if form.is_valid():
            print("Valid")
            data = form.data['text']
            RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
            secret = "2a14a05d9c4e68f793ed8749117cb63b28dcb016"
            stdin = form.data['inp']
            lang = form.cleaned_data['langs']
            #lang = dict(form.fields['langs'].choices)[ll]
            source = data
            json_src = {
               'client_secret': secret,
                'async': 0,
                'source': source,
                'lang': lang,
                'input':stdin,
            }
            r = requests.post(RUN_URL,data=json_src)
            r1 = r.json() 
            obj = Code()
            obj.code = data
            obj.lang = lang
            output = str(r1['run_status']['output'])
            obj.hash = str(r1['code_id'])
            hash = str(r1['code_id'])
            obj.publish()
            output="debug"
            form2 = CodeForm()
            request.session['i']=stdin
            return redirect('codetable.views.display',hash)
    else:
        form = CodeForm()
    return render(request,'codetable/home.html',{'form':form})

def display(request,hash):
    obj = get_object_or_404(Code,hash=hash)
    source = obj.code
    lang = obj.lang
    ip = request.session['i']
    output = ""
    form = CodeForm(initial = {'text':source,'inp':ip,'langs':lang})
    RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
    secret = "2a14a05d9c4e68f793ed8749117cb63b28dcb016"
    if request.method == "POST":
        form = CodeForm(data = request.POST)
        if form.is_valid():
            stdin = form.data['inp']
            source = form.data['text']
            lang = form.cleaned_data['langs']
            #lang = dict(form.fields['langs'].choices)[ll]
            
            json_src = {
               'client_secret': secret,
                'async': 0,
                'source': source,
                'lang': lang,
                'input':stdin,
            }            
            r = requests.post(RUN_URL,data=json_src)
            r1 = r.json()
            #output = r1
            output = str(r1['run_status']['output'])
            obj.code = source
            obj.lang = lang
            obj.publish()

            dict_data = {}
            dict_data['text'] = source
            dict_data['inp'] = stdin
            dict_data['langs'] = lang
            form = CodeForm(initial = dict_data)

    return render(request,'codetable/display.html',{'form':form,'out':output})