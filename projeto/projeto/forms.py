#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deform import widget
from pyramid_deform import CSRFSchema
from colander import (
    MappingSchema,
    SchemaNode,
    String,
    Integer,
    Length,
    Regex,
    Function,
    Email,
    Mapping,
    All,
    Invalid,
)

from .models import Cidadao

def record_to_appstruct(self):
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__)
                 if '_sa_' != k[:4]])


def merge_session_with_post(session, post):
    for key, value in post:
        setattr(session, key, value)
    return session

class FormRegistrar(CSRFSchema):
    nome = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_nome_unico, u"Nome já cadastrado"),
            Regex("^(\w)*$", "Usar apenas letras, números ou _"),
        ),
        description='Digite seu nome de usuário'
    )	
    senha = SchemaNode(
        String(),
        validator=Length(min=5, max=32),
        widget=widget.CheckedPasswordWidget(size=20),
        description='Digite sua senha (no mínimo 5 caracteres) e a confirme')	
	
class FormCadastrar(CSRFSchema):
    nome = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_nome_unico, u"Nome já cadastrado"),
            Regex("^(\w)*$", "Usar apenas letras, números ou _"),
        ),
        description='Digite seu nome de usuário'
    )
    email = SchemaNode(
        String(),
		validator=Email('Email inválido'),
        description='Digite seu e-mail'
	)	
    senha = SchemaNode(
        String(),
        validator=Length(min=5, max=32),
        widget=widget.CheckedPasswordWidget(size=20),
        description='Digite sua senha (no mínimo 5 caracteres) e a confirme')
		
class FormConfigurar(CSRFSchema):
    nome = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_nome_unico, u"Nome já cadastrado"),
            Regex("^(\w)*$", "Usar apenas letras, números ou _"),
        ),
        description='Digite seu nome de usuário'
    )
    email = SchemaNode(
        String(),
		validator=Email('Email inválido'),
        description='Digite seu e-mail'
	)	
    senha = SchemaNode(
        String(),
        validator=Length(min=5, max=32),
        widget=widget.CheckedPasswordWidget(size=20),
        description='Digite sua senha (no mínimo 5 caracteres) e a confirme')	
	
