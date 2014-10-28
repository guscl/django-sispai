from django.template import Context, loader
from core.models import Adult, Pool
from django.http import HttpResponse
import httplib

status_ativacao = False

def index(request):
    global status_ativacao
    t = loader.get_template('core/base.html')
    c = Context({'ativado': status_ativacao})
    return HttpResponse(t.render(c))

def alterStatus(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	
	httpServ = httplib.HTTPConnection("http://192.168.0.168", 8080)
	httpServ.connect()
	httpServ.request('POST', '/23/on', '')
	httpServ.close()
	
	t = loader.get_template('core/base.html')
	c = Context({'ativado': status_ativacao})
	return HttpResponse(t.render(c))

