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
    ):        
        self.senha = senha
        self.email = email
		
        self.apelido = ""
        self.nome_completo = ""
        self.genero = ""
        self.nascimento = ""
        self.nome = ""
        self.rua = ""
        self.bairro = ""
        self.cidade = ""
        self.estado = ""
        self.foto = ""
        self.informacoes = ""
        self.login_twitter = ""
        self.twitter_key = ""
        self.twitter_secret = ""		
        self.login_facebook = ""
        self.facebook_url = ""
        self.facebook_token = ""		
        self.notificacoes_site = False
        self.notificacoes_email = False
        self.atualizacoes_pontos = False
        self.atualizacoes_eventos = False
        	
        self.pontos_inseridos = []		
        self.pontos_a_seguir = []
		#denúncias das mídias que este usuário inseriu
        self.denuncias = []	
		
    def addSeguir(self, Atividade, inserir):
		#atividade que o usuário quer seguir
		#aqui é verificado se o usuário está seguindo a atividade senão não adiciona

        i = 0
        if inserir:
		    #segundo if necessário para não adicionar novamente a mesma atividade na lista
            if Atividade.atividade not in self.pontos_a_seguir:	
                self.pontos_a_seguir.append(Atividade.atividade)		
				# inserir só o nome da atividade?.....
        else:		
            for x in self.pontos_a_seguir:
                if Atividade.atividade == x:
                    inserir = False			
                    del self.pontos_a_seguir[i]			
                i = i +1			
			
        self._p_changed = 1	

    def addInseridos(self, Atividade):
        self.addSeguir(self, Atividade, true)
        self.pontos_inseridos.append(Atividade.atividade)
		# inserir só o nome da atividade?.....
        self._p_changed = 1			

    def addDenuncia(self,Denuncia):
		#adiciona comentario   
        self.denuncias.append(Denuncia)	
        self._p_changed = 1		

class Cidadao_twitter(Cidadao):
    """
    Classe de cidadãos (usuários) cadastrados
    """	
    def __init__(
        self,
    ):   
        Cidadao.__init__(self, "", "")	
        self.nomeUsr = ""

	
        		   		
#é necessário?? os usuários já teem as listas: pontos_inseridos e pontos_a_seguir
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
    ):
		#usar algum número aleatório como id? Acho melhor do que usar o nome da atividade....
        self.atividade = ""
        self.descricao = ""
        self.id = 0		
		
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

    def addFoto(self,Foto):
		#adiciona videos   
        self.midia_foto.append(Foto)
        self._p_changed = 1		
		
    #método que irá varrer as mídias à procura de alguma marcada para exclusão		
    def delMidiaDen(self):
        i = 0	
        for x in self.midia_video:
            if x.excluir == True:	
                del self.midia_video[i]			
            i = i +1	
			
        i = 0	
        for x in self.midia_foto:
            if x.excluir == True:	
                del self.midia_foto[i]			
            i = i +1
			
        i = 0	
        for x in self.midia_coment:
            if x.excluir == True:	
                del self.midia_coment[i]			
            i = i +1
		
#persistent ou persistent mapping??

class Atividade_cidadao(Atividade):
    """
    Deve herdar de Atividade
    Classe atividades inseridas pelos usuários
    """	
    def __init__(
        self,
    ):
        Atividade.__init__(self)
        self.cidadao = ""	
        self.data = ""
        self.tipo = ""
		
        self.denuncias = []	
		#auxiliar para saber indice do comentário pai....
        self.aux =0
			

class Atividade_orcamento(Atividade):
    """
    Deve herdar de Atividade
    Classe atividades orçamentárias vindas do cuidando 1.0
    """	
    def __init__(
        self,
    ):
        Atividade.__init__(self)
        self.atividade = ""
        self.orcado = 0
        self.atualizado = 0    
        self.ano = 0
        self.empenhado = 0
        self.liquidado = 0    
        self.orgao = ""
		

class Midia(Persistent):
    """
    Classe mãe dos tipos de mídias que serão associados às atividades
    """	
    def __init__(
        self,
        data,
        cidadao,
    ):

        self.data = data
        self.cidadao = cidadao 
		#é marcado no método addDenuncia, caso ultrapasse o número parametrizado
        self.excluir = False
		
        self.denuncias = []		

    def addDenuncia(self,Denuncia):
		#adiciona comentario   
        self.denuncias.append(Denuncia)
		#número fixo de denúncias = 10
        if(	len(self.denuncias) > 10):
            self.excluir = True
		
        self._p_changed = 1			

class Midia_foto(Midia):
    """
    Herda de Mídia
    Classe que receberá as imagens
    """	
    def __init__(
        self,
        imagem,
        data,
        cidadao,		
    ):
	    #data e cidadao?
        Midia.__init__(self, data, cidadao)
        self.imagem = imagem 
				

class Midia_video(Midia):
    """
    Herda de Mídia
    Classe que receberá os links para os vídeos
    """	
    def __init__(
        self,
        linkOrig,
        data,
        cidadao,
    ):
	    #data e cidadao?
        Midia.__init__(self, data, cidadao)
        self.linkOrig = linkOrig 
        self.link = ""		
     

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
        cidadao,		
    ):
	    #data e cidadao?
        Midia.__init__(self, data, cidadao)
        self.comentario = comentario
		
        self.respostas = []		
		
	
#ira se transformar em uma hash
#deixa ai por enquanto	
class Denuncia(Persistent):
    """
    Classe que irá armazenar as denúncias relacionadas ás mídias inseridas
    """	
    def __init__(
        self,
        descricao,
        denunciante		
    ):
        self.denunciante = denunciante
        self.descricao = descricao
		

class Dados_site(PersistentMapping):
    """
    Objeto único no bd para inserir os dados estatísticos do site
    """
    def __init__(
        self
    ):
        self.atualiz_atv = []
        self.destaque_atv = []
        self.qtde_usr = 0
        self.qtde_atv_orc = 0
        self.qtde_atv_usr = 0
        self.qtde_fotos = 0
        self.qtde_videos = 0
        self.qtde_coment = 0
        self.proxId = 0

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
		#adiciona ao contador de atividades inseridas pelo usuario
        #não tem uma forma mais bonita de adicionar 1?... Tipo um ++?...
        self.qtde_atv_usr = self.qtde_atv_usr +1

    def addAtvOrc(self):
		#adiciona ao contador de atividades de orçamento
		#provavelmente só chamada da importação dos dados do 1.0
        self.qtde_atv_orc = self.qtde_atv_orc +1
		
    def addUsr(self):
		#adiciona ao contador de usuário cadastrados
        self.qtde_usr = self.qtde_usr +1
		
    def addFoto(self):
		#adiciona ao contador de usuário cadastrados
        self.qtde_fotos = self.qtde_fotos +1
		
    def addVideo(self):
		#adiciona ao contador de usuário cadastrados
        self.qtde_videos = self.qtde_videos +1
		
    def addComent(self):
		#adiciona ao contador de usuário cadastrados
        self.qtde_coment = self.qtde_coment +1

#para mostrar na página do usuário as atualizações que ele segue	
#daí essa lista fica na atividade.. com os usuários que a seguem.. ainda não está sendo utilizado	
class Atualizacao_Usr(PersistentMapping):

    def __init__(
        self,
    ):
        self.usuario = []

    def addAtual(self, usuario):
        self.usuario.append(usuario)
        self._p_changed = 1		
		
def appmaker(zodb_root):
    """
    Quando é rodado??
    """
	
    alterado = False
    if not 'usrTree' in zodb_root:
        zodb_root['usrTree'] = OOBTree()
        alterado = True
		
    if not 'twtTree' in zodb_root:
        zodb_root['twtTree'] = OOBTree()
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
