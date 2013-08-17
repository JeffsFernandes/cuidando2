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
)
import deform
import transaction


@view_config(route_name='inicial', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'projeto'}

@view_config(route_name='registro', renderer='registro.slim')
def registro(request):
    """Registro de usuário"""

    esquema = FormRegistrar().bind(request=request)
    esquema.title = "Registrar"
    form = deform.Form(esquema, buttons=('Registrar',))
    if 'Registrar' in request.POST:
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


@view_config(route_name='lista', renderer='lista.slim')
def lista(request):
    cidadaos = request.db.values()
    return {
        'cidadaos': cidadaos,
    }
