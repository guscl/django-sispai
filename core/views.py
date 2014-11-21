from django.template import Context, loader
from core.models import Adult, Pool, PoolLog
from django.http import HttpResponse
from emailSender import sendMessage
import httplib
import sys

status_ativacao = False

def index(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	t = loader.get_template('core/base.html')
	ad1= Adult.objects.get(email="root")
	p1= Pool.objects.get(adult=ad1.email)

	c = Context({'ativado': status_ativacao, 'checado':p1.isChecked})
	return HttpResponse(t.render(c)) 
              
def alterStatus(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	
	httpServ = httplib.HTTPConnection("10.42.0.30", 5000)
	httpServ.connect()
	if(status_ativacao):
		httpServ.request('GET', '/4/on', '')
	else:
		httpServ.request('GET', '/4/off', '')
	httpServ.close()
	
	t = loader.get_template('core/base.html')
	c = Context({'ativado': status_ativacao})
	return HttpResponse(t.render(c))

def alterSensorStatus(request):
	ad1= Adult.objects.get(email="root")
	p1= Pool.objects.get(adult=ad1.email)
	p1.isChecked = True
	p1.save()
	log = PoolLog.create(p1,"Sensores com Problema")
	log.save()
	sendMessage()
	t = loader.get_template('core/base.html')
	c = Context({'checado': 1})
	return HttpResponse(t.render(c))
	


