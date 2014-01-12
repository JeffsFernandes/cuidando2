#!/usr/bin/env python
# -*- coding: utf-8 -*-
import deform
from deform import widget
from deform.interfaces import FileUploadTempStore 
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
)

from .models import Cidadao, Atividade_orcamento

def record_to_appstruct(self):
    """
    Insere os valores vindos do objeto do banco para o formulário
    """
    return dict([(k, self.__dict__[k]) for k in sorted(self.__dict__)
                 if '_sa_' != k[:4]])

def merge_session_with_post(session, post):
    """
    Insere os valores vindos do formulário para o banco 
    """
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

#Define a lista de anos mapeados (seria interessante se fosse dinâmica de alguma forma..)
anoMapa = (
    ('2013', '2013'),
    ('2012', '2012'),
    ('2011', '2011'),
    ('2010', '2010'),
    ('2009', '2009'),
    ('2008', '2008'),
)

@colander.deferred
def deferred_verif_email_unico(node, kw):
    """
	Verifica se o email inserido para cadastro já existe no banco
	"""
    request = kw.get('request')
    emails = request.db["usrTree"].keys()
    return All(
        Email('E-mail inválido'),
        Function(lambda x: not (x in emails), u"Email já cadastrado")
    )

class MemoryTmpStore(dict):
    """ 
    Para upload da imagem
    Instances of this class implement the
    :class:`deform.interfaces.FileUploadTempStore` interface
    """
    def preview_url(self, uid):
        return None

tmpstore = MemoryTmpStore()
#tmpstore = FileUploadTempStore()

class FormCadastrar(CSRFSchema):
    """ 
    Formulário para cadastro de novo usuário
    falta acesso para termos e condições de uso
    """
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
    """
    Formulário para configuração de perfil do usuário
    """
    
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
        String(),	
        #máscara não funciona....
		#Date(),
        missing=unicode(''),
        description='Digite a data de nascimento',
		#DateInputWidget não dá erro pelo menos..
        widget= widget.TextInputWidget(mask='99/99/9999')
    )        
    """
    erro	
    foto = SchemaNode(
        deform.FileData(),
        widget=widget.FileUploadWidget(tmpstore),
        missing=unicode(''),		
        description='Carregar foto'
    ) 
    """		
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

    notificacoes_site = SchemaNode(
        Boolean(),	
        label='Receber notificações pelo site',
        widget=widget.CheckboxWidget(),
        title='Notificações',
        missing=unicode(''),		
    )	
    notificacoes_email = SchemaNode(
        Boolean(),	
        label='Receber notificações pelo email',
        widget=widget.CheckboxWidget(),
        title='Notificações',
        missing=unicode(''),		
    )	
    atualizacoes_pontos = SchemaNode(
        Boolean(),	
        label='Atualizações de pontos próximos ao endereço cadastrado',
        widget=widget.CheckboxWidget(),
        title='Atualização',
        missing=unicode(''),		
    )	
    atualizacoes_eventos = SchemaNode(
        Boolean(),	
        label='Eventos próximos ao endereço cadastrado',
        widget=widget.CheckboxWidget(),
        title='Atualização',
        missing=unicode(''),		
    )	

class FormSeguirAtv(CSRFSchema):
    """ 
    Formulário para seguir atividade orçamentária/usuário
    """	
    seguir = SchemaNode(
        Boolean(),	
        label='Receber atualizações desta atividade',
        widget=widget.CheckboxWidget(),
        title='Seguir',
        missing=unicode(''),		
    )		

class FormContato(CSRFSchema):
    """ 
    Formulário para contato com equipe do site
    """
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
    """ 
    Formulário para o mapa (se necessário)
    """
    mensagem = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Digite sua mensagem',
        title='Mensagem',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=10, cols=60, css_class='form-control')
    )
		
class FormPesqMapa(CSRFSchema):
    """
    Formulário de pesquisa no mapa
    """	
    ano = SchemaNode(
        String(),
        missing=unicode(''),
        widget=widget.SelectWidget(values=anoMapa),
        title = "Ano",		
    )
    endereco = SchemaNode(
        String(),
        missing=unicode(''),		
        title='Ir para endereço',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=1, cols=60)
    )
	
class FormOrcamento(CSRFSchema):
    """
    Formulário para inserção de comentários no orçamento
    """
    comentario = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Comente sobre o orçamento',
        title='Comentário',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=3, cols=60),
    )	
	
class FormOrcamentoResp(CSRFSchema):
    """
    Formulário para inserção de comentários no orçamento
    """
    resposta = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Responda a este comentáro',
        title='Responda',
        validator=Length(max=100),
        widget=widget.TextAreaWidget(rows=3, cols=60),
    )		
	
class FormOrcFoto(CSRFSchema):
    """
    Formulário para upload de fotos para o orçamento
    """

    foto = SchemaNode(
        String(),
        missing=unicode(''),
        description='Carregar foto'
    )  	

class FormOrcVideo(CSRFSchema):
    """
    Formulário para upload de vídeos para o orçamento
    """
    video = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Carregar url de vídeo'
    )    	
	
class FormLogin(CSRFSchema):
    """ 
    Formulário para login
    """
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
    """ 
    Formulário para inserção de novo ponto/atividade no mapa
    """
    atividade = SchemaNode(
        String(),
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
    """	
    foto = SchemaNode(
        deform.FileData(),
        widget=widget.FileUploadWidget(tmpstore),
        missing=unicode(''),		
        description='Carregar foto'
    )  
    """	
    foto = SchemaNode(
        String(),
        missing=unicode(''),
        description='Carregar foto'
    )  	
    video = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Carregar url de vídeo'
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
    """ 
    Formulário para cadastrar uma nova senha, só será possível se o token estiver correto
    """
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
    """ 
    Formulário para enviar token de senha para o usuário, de acordo com o email inserido
    """
    email = SchemaNode(
        String(),
        validator=Email('E-mail inválido'),
        description='Digite seu e-mail'
    )	

class FormDenuncia(CSRFSchema):
    """ 
    Formulário para enviar denúncia de mídias
    """
    motivo = SchemaNode(
        String(),
        missing=unicode(''),		
        description='Qual o motivo da denúncia?',
        title='Motivo',
        validator=Length(max=200),
        widget=widget.TextAreaWidget(rows=10, cols=60)	
    )	