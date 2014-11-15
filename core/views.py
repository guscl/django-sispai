from django.template import Context, loader
from core.models import Adult, Pool
from django.http import HttpResponse
import httplib
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

status_ativacao = False

def index(request):

	global status_ativacao
	status_ativacao = not status_ativacao
	t = loader.get_template('core/base.html')
	tb = loader.get_template('core/top_bar_login.html')
	ad1= Adult.objects.get(email="root")
	p1= Pool.objects.get(adult=ad1.email)

	c = Context({'ativado': status_ativacao, 'checado':p1.isChecked})
	return HttpResponse(t.render(c)) 
              


def alterStatus(request):
	global status_ativacao
	status_ativacao = not status_ativacao
	
	httpServ = httplib.HTTPConnection("10.42.0.96", 5000)
	httpServ.connect()
	if(status_ativacao):
		httpServ.request('GET', '/4/on', '')
	else:
		httpServ.request('GET', '/4/off', '')
	httpServ.close()
	
	t = loader.get_template('core/base.html')
	c = Context({'ativado': status_ativacao})
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
