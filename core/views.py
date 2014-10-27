from django.template import Context, loader
from core.models import Adult, Pool
from django.http import HttpResponse

status_ativacao = False

def index(request):
    adult_list = Adult.objects.all().order_by('name')
    t = loader.get_template('core/base.html')
    c = Context({
        'adult_list': adult_list,
    })
    return HttpResponse(t.render(c))

def alterStatus(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	print status_ativacao
	t = loader.get_template('core/base.html')
	c = Context({
		'ativado': status_ativacao,
	})
	return HttpResponse(t.render(c))

	



