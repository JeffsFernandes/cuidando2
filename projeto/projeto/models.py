from persistent.mapping import PersistentMapping
from persistent import Persistent


class MyModel(PersistentMapping):
    __parent__ = __name__ = None


class Cidadao(Persistent):

    def __init__(
        self,
        nome,
        senha,
        nome_completo="",
        genero="",
        nascimento="",
        email="",
        rua="",
        bairro="",
        cidade="",
        estado="",
        foto="",
        informacoes="",
        login_twitter="",
        login_facebook="",
    ):

        self.nome = nome
        self.senha = senha

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
        self.login_facebook = login_facebook

        self.notificacoes_site = []
        self.notificacoes_email = []
        self.atualizacoes_pontos = []
        self.atualizacoes_eventos = []


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MyModel()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
