from django.template import Context, loader
<<<<<<< HEAD
from core.models import Pool, PoolLog
=======
from core.models import Adult, Pool, PoolLog
>>>>>>> 45db55c... All communications done
from django.http import HttpResponse
#from emailSender import sendMessage
from django.contrib.auth.models import User
from django.shortcuts import redirect
import httplib
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
import sys

status_ativacao = False

def index(request):
	global status_ativacao
	t = loader.get_template('core/base.html')
	if not request.user.is_authenticated():
		return redirect(logar)
	ad1= request.user
	p1= Pool.objects.get(adult=ad1)
	status_ativacao = p1.isActivated
	checado = not(p1.infraRedFail or p1.zigbeeFail or p1.endCourseOpenFail or p1.endCourseCloseFail or p1.crushFail)
	c = Context({'ativado': status_ativacao, 'checado':checado, 'usuario':ad1.username})
	return HttpResponse(t.render(c)) 
    	          
def alterStatus(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	
	ad1= request.user
	p1= Pool.objects.get(adult=ad1)
	p1.isActivated = status_ativacao
	p1.save()
	
	httpServ = httplib.HTTPConnection("10.42.0.30", 5000)
	httpServ.connect()
	if(status_ativacao):
		httpServ.request('GET', '/4/on', '')
	else:
		httpServ.request('GET', '/4/off', '')
	httpServ.close()
	
	return index(request)

def poolOpen(request):
	username = request.POST.get('user')
	ad1 = User.objects.get(username=username)
	p1= Pool.objects.get(adult=ad1)
	p1.isActivated = True
	p1.endCourseOpen = True
	p1.endCourseOpenFail = False
	p1.endCourseClose = False
	p1.endCourseCloseFail = False
	p1.save()
	log = PoolLog.create(p1,"Piscina aberta")
	log.save()

def poolClose(request):
	username = request.POST.get('user')
	ad1 = User.objects.get(username=username)
	p1= Pool.objects.get(adult=ad1)
	p1.isActivated = True
	p1.endCourseOpen = False
	p1.endCourseOpenFail = False
	p1.endCourseClose = True
	p1.endCourseCloseFail = False
	p1.save()
	log = PoolLog.create(p1,"Piscina fechada")
	log.save()

def userGetOut(request):
	username = request.POST.get('user')
	ad1 = User.objects.get(username=username)
	p1= Pool.objects.get(adult=ad1)
	p1.isActivated = True
	p1.zigbee = False
	p1.zigbeeFail = False
	p1.save()
	log = PoolLog.create(p1,"Usuario saiu da area")
	log.save()

def userGetIn(request):
	username = request.POST.get('user')
	ad1 = User.objects.get(username=username)
	p1= Pool.objects.get(adult=ad1)
	p1.isActivated = True
	p1.zigbee = True
	p1.zigbeeFail = False
	p1.save()
	log = PoolLog.create(p1,"Usuario entrou na area")
	log.save()

def sensorFail(request):
	username = request.POST.get('user')
	ad1 = User.objects.get(username=username)
	p1= Pool.objects.get(adult=ad1)
	p1.infraRedFail = True if request.POST.get('infrared') == '1' else False
	p1.zigbeeFail = True if request.POST.get('zigbee') == '1' else False
	p1.endCourseOpenFail = True if request.POST.get('endCourseOpen') == '1' else False
	p1.endCourseCloseFail = True if request.POST.get('endCourseClose') == '1' else False
	p1.crushFail = True if request.POST.get('crush') == '1' else False
	p1.save()
	
	string_log = "falha no sensor "
	if (p1.infraRedFail):
		string_log = string_log + "infravermelho, "
	if (p1.zigbeeFail):
		string_log = string_log + "zigbee, "
	if (p1.endCourseOpenFail):
		string_log = string_log + "fim de curso de aberto, "
	if (p1.endCourseCloseFail):
		string_log = string_log + "fim de curso de fechado, "
	if (p1.crushFail):
		string_log = string_log + "de esmagamento."
	
	log = PoolLog.create(p1,string_log)
	log.save()

def alterSensorStatus(request):
	ad1= User.objects.get(email="root")
	p1= Pool.objects.get(adult=ad1.id)
	p1.isChecked = True
	p1.save()
	log = PoolLog.create(p1,"Sensores com Problema")
	log.save()
#	sendMessage()
	t = loader.get_template('core/base.html')
	c = Context({'checado': 1})
	return HttpResponse(t.render(c))
	


def registrar(request):
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            form.save()

            return HttpResponseRedirect("/core/")
        else:
            return render(request, "registrar.html", {"form": form})

    return render(request, "registrar.html", {"form": UserCreationForm() })

# pagina de login do jogador
def logar(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # Veja a documentacao desta funcao
        
        if form.is_valid():
            #se o formulario for valido significa que o Django conseguiu encontrar o usuario no banco de dados
            #agora, basta logar o usuario e ser feliz.
            login(request, form.get_user())
            return HttpResponseRedirect("/core/") # redireciona o usuario logado para a pagina inicial
        else:
            return render(request, "logar.html", {"form": form})
    
    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "logar.html", {"form": AuthenticationForm()})

def getParamsOfMenuBar(request):
	response_page = None
	if(request.GET.get('sensorInfo') is not None):
		response_page = sensorsReport(request)
	elif(request.GET.get('history') is not None):
		response_page = logPage(request)
	elif(request.GET.get('logout') is not None):
		response_page = close(request)
			
	return response_page	

def sensorsReport(request):
	if not request.user.is_authenticated():
		return redirect(logar)
	ad1= request.user
	p1= Pool.objects.get(adult=ad1)
	status_ativacao = p1.isActivated
	checado = not(p1.infraRedFail or p1.zigbeeFail or p1.endCourseOpenFail or p1.endCourseCloseFail or p1.crushFail)
	return render(request, "sensor_report.html", {'usuario':ad1.username, 'ativado': status_ativacao, 'checado':checado, "infrared": p1.infraRedFail, "zigbee": p1.zigbeeFail,"crush": p1.crushFail,"endCourseOpen": p1.endCourseOpenFail, "endCourseClose": p1.endCourseCloseFail})

def logPage(request):
	if not request.user.is_authenticated():
		return redirect(logar)
	ad1= request.user
	p1= Pool.objects.get(adult=ad1)
	status_ativacao = p1.isActivated
	checado = not(p1.infraRedFail or p1.zigbeeFail or p1.endCourseOpenFail or p1.endCourseCloseFail or p1.crushFail)
	logs = PoolLog.objects.filter(pool=p1)

	return render(request, "history.html", {'usuario':ad1.username, 'ativado': status_ativacao, 'checado':checado,"logList": logs})

def close(request):
	logout(request)
	return HttpResponseRedirect("/")

