#!/usr/bin/env python
# -*- coding: utf-8 -*-

from deform import widget
from pyramid_deform import CSRFSchema
import colander
from colander import (
    MappingSchema,
    SchemaNode,
    Schema,
    String,
    Integer,
    Length,
    Regex,
    Function,
    OneOf,
    Email,
    Mapping,
    All,
    Invalid,
    Boolean,
    Date,
    #FileData,
)

from .models import Cidadao

def record_to_appstruct(self):
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__)
                 if '_sa_' != k[:4]])

def merge_session_with_post(session, post):
    for key, value in post:
        setattr(session, key, value)
    return session
#Define os gêneros possíveis na configuração do perfil do usuário	
generos = (
    ('', '-Selecionar-'),
    ('fem', 'Feminino'),
    ('mas', 'Masculino')
)
#Define os tipos de pontos que o usuário pode inserir no mapa
tipoLocal = (
    ('coment', 'Comentário'),
    ('denun', 'Denúncia'),
    ('perg', 'Pergunta')
)		
#Define os estados que o usuário pode inserir no seu endereço - configuração do usuário
estados = (
    ('', '-Selecionar-'),
    ('AC','Acre'),
    ('AL','Alagoas'),
    ('AP','Amapá'),
    ('AM','Amazonas'),
    ('BA','Bahia'),
    ('CE','Ceará'),
    ('DF','Distrito Federal'),
    ('ES','Espírito Santo'),
    ('GO','Goiás'),
    ('MA','Maranhão'),
    ('MT','Mato Grosso'),
    ('MS','Mato Grosso do Sul'),
    ('MG','Minas Gerais'),
    ('PA','Pará'),
    ('PB','Paraíba'),
    ('PR','Paraná'),
    ('PE','Pernambuco'),
    ('PI','Piauí'),
    ('RJ','Rio de Janeiro'),
    ('RN','Rio Grande do Norte'),
    ('RS','Rio Grande do Sul'),
    ('RO','Rondônia'),
    ('RR','Roraima'),
    ('SC','Santa Catarina'),
    ('SP','São Paulo'),
    ('SE','Sergipe'),
    ('TO','Tocantins')
)
#Define a lista de meios de notificações para o usuário	
notificacoes = (
    ('email', 'E-mail'),
    ('site', 'Site'))
#Define quais tipos de notificação o usuário receberá
tipoNot = (
    ('ponto', 'Atualizações de pontos próximos ao endereço cadastrado'),
    ('evento', 'Eventos próximos ao endereço cadastrado'))

@colander.deferred
def deferred_verif_email_unico(node, kw):
    request = kw.get('request')
    emails = request.db["usrTree"].keys()
    return All(
        Email('E-mail inválido'),
        Function(lambda x: not (x in emails), u"Email já cadastrado")
    )

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
		validator=deferred_verif_email_unico,
        description='Digite seu e-mail',
        widget=widget.CheckedInputWidget(
            subject='Email',
            confirm_subject='Confirmar e-mail',
            size=40)
	)	
    senha = SchemaNode(
        String(),
        validator=Length(min=5, max=32),
        widget=widget.CheckedPasswordWidget(size=20),
        description='Digite sua senha (no mínimo 5 caracteres) e a confirme'
    )
    confirmar = SchemaNode(
        Boolean(),	
        #description='Aceitar termos e condições',
        label='Aceitar termos e condições',
        widget=widget.CheckboxWidget(),
        title='Confirmar',
        validator=Function(lambda x: x, u'É necessário aceitar as condições'),
    )			

class FormConfigurar(CSRFSchema):

    nome = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_email_unico, u"Nome já cadastrado"),
            Regex("^(\w)*$", "Usar apenas letras, números ou _"),
        ),
        missing=unicode(''),		
        description='Digite seu nome de usuário'
    )
    sobrenome = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_nome_unico, u"Nome já cadastrado"),
        ),
        missing=unicode(''),		
        description='Digite seu sobrenome'
    )	
    genero = SchemaNode(
        String(),
        missing=unicode(''),
        widget=widget.SelectWidget(values=generos),
        title = "Gênero",		
    )	
    nascimento = SchemaNode(
        Date(),
        missing=unicode(''),
        description='Digite a data de nascimento'
    )        

    foto = SchemaNode(
        String(),
	    #FileData(),
        #widget=.widget.FileUploadWidget(tmpstore, item_css_class='mapped_widget_custom_class')		
        missing=unicode(''),		
        description='Carregar foto'	
    )   
		
    rua = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite sua rua')
    bairro = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite seu bairro')
    cidade = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite sua cidade')
    estado = SchemaNode(
        String(),
        missing=unicode(''),
        widget=widget.SelectWidget(values=estados))		
    informacoes = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite informações sobre você',
        title='Informações',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=10, cols=60)
    )		

    senha = SchemaNode(
        String(),
        missing=unicode(''),		
        validator=Length(min=5, max=32),
        widget=widget.CheckedPasswordWidget(size=20),
        description='Alterar sua senha (no mínimo 5 caracteres) e a confirme'
    )	
    notificacoes = SchemaNode(
        String(),
        missing=unicode(''),
        validator=Length(min=1),
        widget=widget.CheckboxChoiceWidget(values=notificacoes),	
        title='Mostrar notificações')	
		
    tipoNot = SchemaNode(
        String(),
        missing=unicode(''),
        validator=Length(min=1),
        widget=widget.CheckboxChoiceWidget(values=tipoNot),	
        title='Tipos de notificações')	
	
class FormContato(CSRFSchema):
    nome = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_nome_unico, u"Nome já cadastrado"),
            Regex("^(\w)*$", "Usar apenas letras, números ou _"),
        ),
        description='Digite seu nome de usuário'
    )
    assunto = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            #Function(verif_nome_unico, u"Nome já cadastrado"),
        )
    )	
    email = SchemaNode(
        String(),
		validator=Email('E-mail inválido'),
        description='Digite seu e-mail'
	)	
    mensagem = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite sua mensagem',
        title='Mensagem',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=10, cols=60)
    )								
	
class FormMapa(CSRFSchema):
    mensagem = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite sua mensagem',
        title='Mensagem',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=10, cols=60, css_class='form-control')
    )

class FormOrcamento(CSRFSchema):
    comentario = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Comente sobre o orçamento',
        title='Comentário',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=10, cols=60)
    )	
	
class FormLogin(CSRFSchema):
    email = SchemaNode(
        String(),
        validator=Email('E-mail inválido'),
        description='Digite seu e-mail'
    )	
    senha = SchemaNode(
        String(),
        validator=Length(min=5, max=32),
        widget=widget.PasswordWidget(),
        description='Digite sua senha'
    )

class FormInserirP(CSRFSchema):
    atividade = SchemaNode(
        String(),
        validator=All(
            Length(max=32),
            Regex("^(\w)*$", "Usar apenas letras, números ou _"),
        ),
        title='Título',		
        description='Nome do local')
    endereco = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Endereço do local',
        title='Endereço',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=1, cols=60)
    )		
    tipo = SchemaNode(
        String(),
        missing=unicode(''),
        widget=widget.SelectWidget(values=tipoLocal),
        title = "Gênero",		
    )
    foto = SchemaNode(
        String(),
	    #FileData(),
        #widget=widget.FileUploadWidget(tmpstore),
        missing=unicode(''),		
        description='Carregar foto'
    )  
    video = SchemaNode(
        String(),
	    #FileData(),
        #widget=widget.FileUploadWidget(tmpstore),
        missing=unicode(''),		
        description='Carregar vídeo'
    )    	
    descricao = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Comente sobre o orçamento',
        title='Descrição',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=10, cols=60)		
    )		

class FormRecadSenha(CSRFSchema):

    token = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite o código enviado pelo email'
    )

    senha = SchemaNode(
        String(),
        missing=unicode(''),		
        validator=Length(min=5, max=32),
        widget=widget.CheckedPasswordWidget(size=20),
        description='Alterar sua senha (no mínimo 5 caracteres) e a confirme'
    )	
	
class FormRSenha(CSRFSchema):

    email = SchemaNode(
        String(),
        validator=Email('E-mail inválido'),
        description='Digite seu e-mail'
    )	