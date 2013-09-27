#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyramid.view import view_config
from .models import Cidadao, MyModel
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    #HTTPForbidden,
)
from forms import (
    merge_session_with_post,
    FormRegistrar,
    FormCadastrar,
    FormConfigurar,
    FormContato,	
)
import deform
import transaction


@view_config(route_name='inicial', renderer='inicial.slim')
def my_view(request):
    return {'project': 'projeto'}

@view_config(route_name='lista', renderer='lista.slim')
def lista(request):
    cidadaos = request.db.values()
    return {
        'cidadaos': cidadaos,
    }
	
@view_config(route_name='cadastro', renderer='cadastro.slim')
def cadastro(request):
    """Cadastro de usuário"""

    esquema = FormCadastrar().bind(request=request)
    esquema.title = "Cadastrar novo usuário"
    form = deform.Form(esquema, buttons=('Cadastrar',))
    if 'Cadastrar' in request.POST:
        # Validação do formulário
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        # Atualizar registro - usuário logado
        #cidadao = Cidadao("","")
        #cidadao = merge_session_with_post(cidadao, request.POST.items())
        #request.db[cidadao.nome] = cidadao
        #request.db.commit()
        #transaction.commit()
        #request.session.flash(u"Usuário registrado com sucesso.")
        #request.session.flash(u"Agora você já pode logar com ele.")
        return HTTPFound(location=request.route_url('lista'))
    else:
        # Apresentação do formulário
        return {'form': form.render()}

@view_config(route_name='configuracao', renderer='configuracao.slim')
def configuracao(request):
    """Configuração de usuário"""

    esquema = FormConfigurar().bind(request=request)

    esquema.title = "Configuração de usuário"
    form = deform.Form(esquema, buttons=('Salvar', 'Excluir conta'))
    if 'Configurar' in request.POST:
        # Validação do formulário
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        # Criação e inserção
        cidadao = Cidadao("","")
        cidadao = merge_session_with_post(cidadao, request.POST.items())
        request.db[cidadao.nome] = cidadao
        #request.db.commit()
        transaction.commit()
        #request.session.flash(u"Usuário registrado com sucesso.")
        #request.session.flash(u"Agora você já pode logar com ele.")
        return HTTPFound(location=request.route_url('lista'))
    else:
        # Apresentação do formulário
        return {'form': form.render()}		
		
@view_config(route_name='contato', renderer='contato.slim')
def contato(request):
    """Contato"""

    esquema = FormContato().bind(request=request)
    esquema.title = "Entre em contato com o Cuidando"
    form = deform.Form(esquema, buttons=('Enviar',))
    if 'Contato' in request.POST:
        # Validação do formulário
        try:
            form.validate(request.POST.items())
        except deform.ValidationFailure as e:
            return {'form': e.render()}

        return HTTPFound(location=request.route_url('lista'))
    else:
        # Apresentação do formulário
        return {'form': form.render()}

