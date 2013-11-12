#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyramid.view import view_config
from .models import Cidadao, Atividade_cidadao, Atividade_orcamento
#from .models import Cidadao, UsrTree, Atividade_cidadao
#from .models import Cidadao, MyModel, UsrTree
#por que MyModel?
from beaker.middleware import SessionMiddleware
from datetime import datetime
import warnings
import itertools

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    #HTTPForbidden,
)
from pyramid.security import (
    remember,
    forget,
    authenticated_userid,
)
from forms import (
    merge_session_with_post,
    record_to_appstruct,
    FormCadastrar,
    FormConfigurar,
    FormContato,
    FormLogin,	
    FormMapa,
    FormInserirP,
    FormOrcamento,
    FormRecadSenha,	
    FormRSenha,
    FormPesqMapa,
    FormOrcFoto,
    FormOrcVideo,
)
import deform
import transaction

@view_config(route_name='inicial', renderer='inicial.slim')
def my_view(request):
    return {'project': 'projeto'}

@view_config(
    route_name='lista',
    renderer='lista.slim',
    permission='comum'
)
def lista(request):
    cidadaos = request.db['usrTree'].values()
    atividades = request.db['atvTree'].values()
    return {
        'cidadaos': cidadaos,
        'atividades': atividades,
    }
	
@view_config(route_name='cadastro', renderer='cadastro.slim')
def cadastro(request):
    """Cadastro de usuário"""
	# soh eh rodado 1 vez... tem que colocar na configurcao ou coisa assim?...
    # Ensure that a ’userdb’ key is present
    # in the root
    if not request.db.has_key("usrTree"):
        from BTrees.OOBTree import OOBTree
        request.db["usrTree"] = OOBTree()
		
    esquema = FormCadastrar().bind(request=request)
    esquema.title = "Cadastrar novo usuário"
    form = deform.Form(esquema, buttons=('Cadastrar',))
    if 'Cadastrar' in request.POST:
        # Validação do formulário
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}
			
		# Criação e inserção	
        cidadao = Cidadao("","")
        cidadao = merge_session_with_post(cidadao, request.POST.items())
		#tchau lista
        #request.db['cidadaos'][cidadao.email] = cidadao
        request.db['usrTree'][cidadao.email] = cidadao
        transaction.commit()
        request.session.flash(u"Usuário registrado com sucesso.")
        request.session.flash(u"Agora você já pode logar com ele.")
        return HTTPFound(location=request.route_url('lista'))
    else:
        # Apresentação do formulário
        return {'form': form.render()}

@view_config(
    route_name='configuracao',
    renderer='configuracao.slim',
    permission='basica'
)
def configuracao(request):
    """Configuração de usuário"""

    esquema = FormConfigurar().bind(request=request)
    esquema.title = "Configuração de usuário"
    cidadao = Cidadao("","")
    cidadao = request.db["usrTree"][authenticated_userid(request)]	

    form = deform.Form(esquema, buttons=('Salvar', 'Excluir'))
    if 'Salvar' in request.POST:
        # Validação do formulário
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}
        
        cidadao = merge_session_with_post(cidadao, request.POST.items())
        transaction.commit()		
        return HTTPFound(location=request.route_url('usuario'))
    elif 'Excluir' in request.POST:
        del request.db["usrTree"][authenticated_userid(request)]
        transaction.commit()
        headers = forget(request)
        return HTTPFound(location=request.route_url('inicial'))		
    else:
        # Apresentação do formulário
        appstruct = record_to_appstruct(cidadao)
        return{'form':form.render(appstruct=appstruct)}	
		
@view_config(route_name='contato', renderer='contato.slim')
def contato(request):
    """Contato"""
    # Import smtplib for the actual sending function
    import smtplib
	
    esquema = FormContato().bind(request=request)
    esquema.title = "Entre em contato com o Cuidando"
    form = deform.Form(esquema, buttons=('Enviar',))
    if 'Enviar' in request.POST:
        # Validação do formulário
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        sender = request.POST.get("email")
        receivers = ['silvailziane@yahoo.com.br']	
        message = request.POST.get("assunto")		
        						
        try:
            #s = smtplib.SMTP( [host [, port [, local_hostname]]] )
            s = smtplib.SMTP('pop.mail.yahoo.com.br',587)
            smtpObj.sendmail(sender, receivers, message)	
            s.quit()	        
            print "Successfully sent email"
		#except SMTPException:
        except:
            print "Error: unable to send email"		
      
		
        return HTTPFound(location=request.route_url('inicial'))
    else:
        # Apresentação do formulário
        return {'form': form.render()}

@view_config(route_name='logout', permission='basica')
def logout(request):
    """Página para logout"""
    headers = forget(request)
    request.session.flash(u"Você foi deslogado.")
    #request.session.pop_flash()
    return HTTPFound(location=request.route_url('inicial'), headers=headers)

@view_config(route_name='login', renderer='login.slim')
def login(request):

    esquema = FormLogin().bind(request=request)
    esquema.title = "Login"
	#botoes nao aceitam frases como label = "esqueci a senha"
    #form = deform.Form(esquema, buttons=('Entrar', 'Esqueci a senha'))
    form = deform.Form(esquema, buttons=('Entrar', 'Esqueci'))

    if 'Entrar' in request.POST:
        try:
            form.validate(request.POST.items())		
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        email = request.POST.get("email")
        senha = request.POST.get("senha")
        if email in request.db["usrTree"]:
            cidadao = Cidadao("","")
            cidadao = request.db["usrTree"][email]
            if cidadao.senha == senha:
                headers = remember(request, email)
                next = request.route_url('usuario')
                return HTTPFound(location=next, headers=headers)				
            else:
                warnings.warn("Email ou senha inválidos", DeprecationWarning)
        else:
            warnings.warn("Email ou senha inválidos", DeprecationWarning)
        return {'form': form.render()}
    #não entra nesse elif
	#elif 'Esqueci a senha' in request.POST:  
    elif 'Esqueci' in request.POST:  
        return HTTPFound(location=request.route_url('r_senha'))
    else:
        return {'form': form.render()}
    
@view_config(route_name='usuario', renderer='usuario.slim', permission='basica')
def usuario(request):
    """
	Página do perfil do usuário
	"""
    cidadao = Cidadao("","")
    cidadao = request.db["usrTree"][authenticated_userid(request)]	
    return {
        'cidadao': cidadao
    }

@view_config(route_name='sobre', renderer='sobre.slim')
def sobre(request):
    return {}

@view_config(route_name='mapa', renderer='mapa.slim')
def mapa(request):
    """
    Página dos orçamentos mapeados
    """
    esquemaPesq = FormPesqMapa().bind(request=request)
    esquemaPesq.title = "Pesquisa"
    formPesq = deform.Form(esquemaPesq, buttons=('Pesquisar',))	
    
    esquema = FormMapa().bind(request=request)
    esquema.title = "Mapa"
	#legenda do botão - inserir ponto
    form = deform.Form(esquema, buttons=('Inserir',))

	
    if 'Pesquisar' in request.POST:
        try:
            formPesq.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        return HTTPFound(location=request.route_url('lista'))
    elif 'Inserir' in request.POST:
        return HTTPFound(location=request.route_url('inserir_ponto'))	
    else:

        # values passed to template for rendering
        return {
            'form':form.render(),
            'formPesq':formPesq.render(),
            'showmenu':True,
            }

@view_config(route_name='orcamento', renderer='orcamento.slim')
def orcamento(request):
    """
    Página de um orçamento individual
    """
    esquemaFoto = FormOrcFoto().bind(request=request)
    esquemaFoto.title = "Foto"
    formFoto = deform.Form(esquemaFoto, buttons=('Upload',))	

    esquemaVideo = FormOrcVideo().bind(request=request)
    esquemaVideo.title = "Video"
    formVideo = deform.Form(esquemaVideo, buttons=('Upload',))		
	
    esquema = FormOrcamento().bind(request=request)
    esquema.title = "Comentários"
    form = deform.Form(esquema, buttons=('Enviar',))
	
    atv_orc = Atividade_orcamento("","")
	#atividade vinda do mapa
    #atv_orc = request.db["orctree"][authenticated_userid(request)]	
	
    if 'Orcamento' in request.POST:
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

    else:
        return {
            'form': form.render(),
            'formVideo': formVideo.render(),
            'formFoto': formFoto.render(),
        }
	
@view_config(route_name='inserir_ponto', renderer='inserir_ponto.slim')
def inserir_ponto(request):

    esquema = FormInserirP().bind(request=request)
    esquema.title = "Inserir ponto no mapa"
    form = deform.Form(esquema, buttons=('Inserir', 'Cancelar'))
	
    if not request.db.has_key("atvTree"):
        from BTrees.OOBTree import OOBTree
        request.db["atvTree"] = OOBTree()
		
    if 'Inserir' in request.POST:
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        if(authenticated_userid(request)):	
		    # Criação e inserção	
            atividade = Atividade_cidadao("","")
            atividade = merge_session_with_post(atividade, request.POST.items())
		    #inserir id para a atividade?
            atividade.data = datetime.now()
            atividade.cidadao = authenticated_userid(request)
            request.db['atvTree'][atividade.atividade] = atividade
            transaction.commit()
            request.session.flash(u"Atividade de usuário cadastrada com sucesso.")
		#teste	
        return HTTPFound(location=request.route_url('lista'))
    else:
        return {'form': form.render()}

@view_config(route_name='privacidade', renderer='privacidade.slim')
def privacidade(request):
    return {}
		
@view_config(route_name='termos', renderer='termos.slim')		
def termos(request):
    return {}

@view_config(
    route_name='rcad_senha',
    renderer='rcad_senha.slim',
    permission='basica'
)
def rcad_senha(request):
    """Redefinir senha de usuário"""

    esquema = FormRecadSenha().bind(request=request)
    esquema.title = "Redefinir senha"
    cidadao = Cidadao("","")
    
    form = deform.Form(esquema, buttons=('Salvar',))
    if 'Salvar' in request.POST:
        # Validação do formulário
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}
        #validar token, se ok, merge session
        cidadao = merge_session_with_post(cidadao, request.POST.items())
        transaction.commit()		
        return HTTPFound(location=request.route_url('usuario'))
    else:
        return{'form':form.render()}
		
@view_config(
    route_name='r_senha',
    renderer='r_senha.slim',
    permission='comum'
)
def r_senha(request):
    """Reenviar senha de usuário"""

    esquema = FormRSenha().bind(request=request)
    esquema.title = "Reenviar senha"
    
    form = deform.Form(esquema, buttons=('Enviar',))
    if 'Enviar' in request.POST:
        # Validação do formulário
        try:
            appstruct = form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}
			
        email = request.POST.get("email")

        if email in request.db["usrTree"]:
            #enviar email com token, armazenar esse token
            headers = remember(request, email)
            return HTTPFound(location=request.route_url('rcad_senha'), headers=headers)				
        else:
            warnings.warn("Email ou senha inválidos", DeprecationWarning)
		
        return HTTPFound(location=request.route_url('rcad_senha'))
    else:
        return {'form': form.render()}		