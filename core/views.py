from django.template import Context, loader
from core.models import Adult, Pool
from django.http import HttpResponse

def index(request):
    adult_list = Adult.objects.all().order_by('name')
    t = loader.get_template('core/base.html')
    c = Context({
        'adult_list': adult_list,
    })
    return HttpResponse(t.render(c))