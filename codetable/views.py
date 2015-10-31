from django.shortcuts import render,get_object_or_404,redirect#render_to_response,
from django.template import RequestContext
from .models import Code
from django.core.exceptions import ObjectDoesNotExist
from .forms import CodeForm

import requests
import cgi

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
            obj.hash = str(r1['code_id'])
            hash = str(r1['code_id'])
            obj.publish()
            #output="debug"
            form2 = CodeForm()
            data_pass = {}
            data_pass['i']=stdin
            data_pass['s']=str(r1['run_status']['status'])
            data_pass['sd']=r1['run_status']['status_detail']
            if data_pass['s']=="CE":
                data_pass['o']=r1['compile_status']
                data_pass['t']="0.0"
                data_pass['m']="0"
            else:
                data_pass['o']=r1['run_status']['output_html']
                data_pass['t']=r1['run_status']['time_used']
                data_pass['m']=r1['run_status']['memory_used']
            request.session['data'] = data_pass
            return redirect('codetable.views.display',hash)
    else:
        form = CodeForm()
    return render(request,'codetable/home.html',{'form':form})

def display(request,hash):
    obj = get_object_or_404(Code,hash=hash)
    source = obj.code
    lang = obj.lang
    RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
    secret = "2a14a05d9c4e68f793ed8749117cb63b28dcb016"    
    code_data = {}
    if 'data' in request.session:
        data_pass = request.session['data']
        code_data['output'] = data_pass['o']
        code_data['time']= data_pass['t']
        code_data['memory']= data_pass['m']
        code_data['status_detail'] = data_pass['sd']
        code_data['status']=data_pass['s']
        dict_data = {}
        dict_data['inp']=request.session['i']
        dict_data['text']=source
        dict_data['langs']=lang
        form = CodeForm(initial = dict_data)
        method = 1
        request.session.pop('data')
        data_pass = {}
    elif request.method == "POST":
        form = CodeForm(data = request.POST)
        if form.is_valid():
            try:
                stdin = form.data['inp']
            except:
                stdin = ""
            source = form.data['text']
            lang = form.cleaned_data['langs']
            json_src = {
               'client_secret': secret,
                'async': 0,
                'source': source,
                'lang': lang,
                'input':stdin,
            }            
            r = requests.post(RUN_URL,data=json_src)
            r1 = r.json()
            #r1 = {u'run_status': {u'status': u'AC', u'time_limit': 5, u'output_html': u'Hello&nbsp;World!<br>', u'memory_limit': 262144, u'time_used': u'0.1482', u'signal': u'OTHER', u'status_detail': u'N/A', u'async': 0, u'output': u'Hello World!\n', u'memory_used': u'1540020'}, u'code_id': u'63cfe2T', u'web_link': u'https://code.hackerearth.com/63cfe2T', u'compile_status': u'OK'}
            #output = r1['run_status']['output_html']
            #print(type(output))
            obj.code = source
            obj.lang = lang
            obj.publish()
            code_data = {}
            code_data['status']= r1['run_status']['status']
            if code_data['status'] == "CE":
                code_data['output'] = (r1['compile_status'])
                code_data['time']= "0.0"
                code_data['memory']= "0"
            else:
                code_data['output'] = (r1['run_status']['output_html'])
                code_data['time']= r1['run_status']['time_used']
                code_data['memory']= r1['run_status']['memory_used']
            code_data['status_detail'] = r1['run_status']['status_detail']

            dict_data = {}
            dict_data['text'] = source
            dict_data['inp'] = stdin
            dict_data['langs'] = lang
            form = CodeForm(initial = dict_data)
            method = 1
    else:
        method = 0
        code_data['output'] = ""
        code_data['time']= ""
        code_data['memory']= ""
        code_data['status_detail'] = ""
        dict_data = {}
        dict_data['text'] = source
        dict_data['langs'] = lang
        form = CodeForm(initial=dict_data)
    return render(request,'codetable/display.html',{'form':form,'out':code_data,'method':method })
