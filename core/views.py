from django.template import Context, loader
from core.models import Adult, Pool
from django.http import HttpResponse

status_ativacao = False

def index(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	t = loader.get_template('core/base.html')
	c = Context({'ativado': status_ativacao})
	return HttpResponse(t.render(c))



