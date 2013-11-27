#!/usr/bin/env python
# -*- coding: utf-8 -*-

from persistent.mapping import PersistentMapping
from persistent import Persistent
from BTrees.OOBTree import OOBTree
from deform.interfaces import FileUploadTempStore 
from ZODB.blob import Blob


import transaction
from pyramid.security import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
    )
from pyramid_zodbconn import get_connection

class RootFactory(object):
    """
    Inicia conexão do banco
    Grupos de permissões para acesso ao banco 
    """	
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
        (Allow, 'g:cidadao', 'basica'),
        (Allow, Everyone, 'comum'),
    ]

    def __init__(self, request):
        conn = get_connection(request)
        request.db = conn.root()
        appmaker(conn.root())
        #return None
        #return conn.root()

#ainda não entendi o que é esse myModel		
class MyModel(PersistentMapping):
    __parent__ = __name__ = None

class UsrTree(OOBTree):
    __usr__ = __name__ = "usrTree"	

class Cidadao(PersistentMapping):
    """
    Classe de cidadãos (usuários) cadastrados
    """	
    def __init__(
        self,
        email,		
        senha,
        id="",
        nome_completo="",
        genero="",
        nascimento="",
        nome="",
        rua="",
        bairro="",
        cidade="",
        estado="",
		#como guardar a imagem?
        foto="",#Blob(),
        informacoes="",
        login_twitter="",
        twitter_key="",		
        twitter_secret="",			
        login_facebook="",
        notificacoes_site= False,
        notificacoes_email= False,
        atualizacoes_pontos= False,
        atualizacoes_eventos= False,
    ):

        self.nome = nome
        self.senha = senha
		
        self.id = id
        self.nome_completo = nome_completo
        self.genero = genero
        self.nascimento = nascimento
        self.email = email
        self.rua = rua
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.foto = foto
        self.informacoes = informacoes
        self.login_twitter = login_twitter
        self.twitter_key = twitter_key
        self.twitter_secret = twitter_secret		
        self.login_facebook = login_facebook
        self.notificacoes_site = notificacoes_site
        self.notificacoes_email = notificacoes_email
        self.atualizacoes_pontos = atualizacoes_pontos
        self.atualizacoes_eventos = atualizacoes_eventos
        	
        self.pontos_inseridos = []		
        self.pontos_a_seguir = []
		#denúncias de outros usuários para este
        self.denuncias = []	
		
    def addSeguir(self, Atividade, inserir):
		#atividade que o usuário quer seguir
		#aqui é verificado se o usuário está seguindo a atividade senão não adiciona

        i = 0
        if inserir:
		    #segundo if necessário para não adicionar novamente a mesma atividade na lista
            if Atividade.atividade not in self.pontos_a_seguir:	
                self.pontos_a_seguir.append(Atividade.atividade)				
        else:		
            for x in self.pontos_a_seguir:
                if Atividade.atividade == x:
                    inserir = False			
                    del self.pontos_a_seguir[i]			
                i = i +1			
			
        self._p_changed = 1	

    		

class Notificacao(Persistent):
    """
    Classe para armazenar as atividades a serem notificadas para o usuário quando há atualizações
    """	
    def __init__(
        self,
        atividade,        
    ):

        self.atividade = atividade

class Atividade(Persistent):
    """
    Classe mãe das atividades orçamentárias e atividades inseridas pelos usuários
    """	
    def __init__(
        self,
        atividade ="",
        descricao ="",

    ):

        self.atividade = atividade
        self.descricao = descricao
		
        self.midia_video = []	   
        self.midia_foto = []	
        self.midia_coment = []	

    def addComent(self,Coment):
		#adiciona comentario   
        self.midia_coment.append(Coment)
        self._p_changed = 1		
		
    def addVideo(self,Video):
		#adiciona videos   
        self.midia_video.append(Video)
        self._p_changed = 1			
		
#persistent ou persistent mapping??

class Atividade_cidadao(Atividade):
    """
    Deve herdar de Atividade
    Classe atividades inseridas pelos usuários
    """	
    def __init__(
        self,
        cidadao ="",
		#nao lembro o que era essa atividade... sao so titulo??
		#atividade_cidadao deveria herdar de atividade
        atividade ="",
        descricao ="",
        data ="",
        tipo ="",

    ):
        self.cidadao = cidadao
        self.atividade = atividade
        self.descricao = descricao		
        self.data = data
        self.tipo = tipo

		#auxiliar para saber indice do comentário pai....
        self.aux =0

			

class Atividade_orcamento(Atividade):
    """
    Deve herdar de Atividade
    Classe atividades orçamentárias vindas do cuidando 1.0
    """	
    def __init__(
        self,
        atividade = "",
        orcado ="",
        atualizado = "",
        ano="",
        empenhado="",
        liquidado="",
        orgao="",

    ):

        self.atividade = atividade
        self.orcado = orcado
        self.atualizado = atualizado    
        self.ano = ano
        self.empenhado = empenhado
        self.liquidado = liquidado    
        self.orgao = orgao
		

class Midia(Persistent):
    """
    Classe mãe dos tipos de mídias que serão associados às atividades
    """	
    def __init__(
        self,
        data,
        cidadao,
        atividade="",		

    ):

        self.atividade = atividade
        self.data = data
        self.cidadao = cidadao 
		
        self.denuncias = []		

class Midia_foto(Midia):
    """
    Herda de Mídia
    Classe que receberá as imagens
    """	
    def __init__(
        self,
        imagem,

    ):

        self.imagem = imagem 
		
        self.denuncias = []			

class Midia_video(Midia):
    """
    Herda de Mídia
    Classe que receberá os links para os vídeos
    """	
    def __init__(
        self,
        link= "",

    ):

        self.linkOrig = link 
        self.link = ""		

        self.denuncias = []	        

#comentamos sobre lista de comentarios....
class Midia_comentario(Midia):
    """
    Herda de Mídia
    Classe que receberá os comentários
    """	
    def __init__(
        self,
        comentario,
        data,
        comentarioPai="",	

    ):

        self.comentario = comentario
        self.data = data    
        self.comentarioPai = comentarioPai  
		
        self.respostas = []		
		
        self.denuncias = []	#pensando bem.. nao sei se eh necessario no comentario
	
#ira se transformar em uma hash
#deixa ai por enquanto	

class Denuncia(Persistent):
    """
    Classe que irá armazenar as denúncias relacionadas ás mídias inseridas
    """	
    def __init__(
        self,
        midia,
        descricao,
        atividade,

    ):
        self.midia = midia
        self.descricao = descricao
        self.atividade = atividade
		
        self.video = []       
        self.foto = [] 	
        self.coment = [] 		

class Dados_site(PersistentMapping):
    """
    Objeto único no bd para inserir os dados estatísticos do site
    """
    def __init__(
        self,
		# na atividade a lista não ficou no init.... qual  diferença?
        atualiz_atv = [],
        destaque_atv = [],		
        qtde_usr = 0,
        qtde_atv_orc = 0,
        qtde_atv_usr = 0,
        qtde_fotos = 0,
        qtde_videos = 0,
        qtde_coment = 0,
    ):
        self.atualiz_atv = atualiz_atv
        self.destaque_atv = destaque_atv
        self.qtde_usr = qtde_usr
        self.qtde_atv_orc = qtde_atv_orc
        self.qtde_atv_usr = qtde_atv_usr
        self.qtde_fotos = qtde_fotos
        self.qtde_videos = qtde_videos
        self.qtde_coment = qtde_coment

	#está inserindo o objeto todo da atividade, não sei se é melhor só guardar o nome...
	# mas aí o interessante é redirecionar o objeto para o link a ser aberto....
    def addAtual(self, atualiz_atv):
		#insere só 5 novas atualizações, se lista copleta, deleta o mais antigo
        if(	len(self.atualiz_atv) > 5):	
            del self.atualiz_atv[0]	
        for atual in self.atualiz_atv:
            if atual.atividade == atualiz_atv.atividade:
                return			
        self.atualiz_atv.append(atualiz_atv)	
        self._p_changed = 1
		
    def addAtvUsr(self):
		#adiciona contador de atividades inseridas pelo usuario
        #não tem uma forma mais bonita de adicionar 1?...
        self.qtde_atv_usr = self.qtde_atv_usr +1

    def addAtvOrc(self):
		#adiciona contador de atividades de orçamento
		#provavelmente só chamada da importação dos dados do 1.0
        self.qtde_atv_orc = self.qtde_atv_orc +1
		
    def addUsr(self):
		#adiciona contador de usuário cadastrados
        self.qtde_usr = self.qtde_usr +1
		
    def addFoto(self):
		#adiciona contador de usuário cadastrados
        self.qtde_fotos = self.qtde_fotos +1
		
    def addVideo(self):
		#adiciona contador de usuário cadastrados
        self.qtde_videos = self.qtde_videos +1
		
    def addComent(self):
		#adiciona contador de usuário cadastrados
        self.qtde_coment = self.qtde_coment +1
		
class Atualizacao_Usr(PersistentMapping):

    def __init__(
        self,
        usuario = []
    ):
        self.usuario = usuario

    def addAtual(self, usuario):
        self.usuario.append(usuario)
        self._p_changed = 1		
		
def appmaker(zodb_root):
    """
    Quando é rodado??
    """
	
    alterado = False
    if not 'usrTree' in zodb_root:
		#teste
        #zodb_root['usrTree'] = PersistentMapping()
        zodb_root['usrTree'] = OOBTree()
        alterado = True

    if not "atualUsr" in zodb_root:
        zodb_root["atualUsr"] = PersistentMapping()		
        alterado = True
		
    if not "dadosSite" in zodb_root:
        print("criou md")
        zodb_root["dadosSite"] = Dados_site()
        alterado = True
		
    if alterado:
        transaction.commit()

    #if not 'app_root' in zodb_root:
    #    app_root = MyModel()
    #    zodb_root['app_root'] = app_root
    #    import transaction
    #    transaction.commit()
    #return zodb_root['app_root']
