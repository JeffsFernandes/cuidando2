from pyramid.config import Configurator
from pyramid_zodbconn import get_connection
import deform
from pkg_resources import resource_filename
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from .models import appmaker
from pyramid_beaker import session_factory_from_settings


def root_factory(request):
    conn = get_connection(request)
    request.db = conn.root()
    #return appmaker(conn.root())
    return conn.root()


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #ja esta no dev.ini
    #config.include('pyramid_beaker')
    session_factory = session_factory_from_settings(settings)  

    config = Configurator(
        root_factory=root_factory,
        settings=settings,
        session_factory=session_factory)
	
    config.add_translation_dirs(
        'colander:locale',
        'deform:locale',
    )
    #config.set_session_factory(session_factory)
	
    def translator(term):
        return get_localizer(get_current_request()).translate(term)
    deform_dir = resource_filename('deform', 'templates/')
    deform_dir2 = resource_filename('deform_bootstrap', 'templates/')
    deform_dir3 = resource_filename('projeto', 'templates/')
    zpt_renderer = deform.ZPTRendererFactory(
        [deform_dir3, deform_dir2, deform_dir],
        translator=translator)
    deform.Form.set_default_renderer(zpt_renderer)

    config.add_static_view('static', 'projeto:static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static')
    config.add_static_view('deform_bootstrap', 'deform_bootstrap:static')

    config.add_route('inicial', '/')
    config.add_route('lista', '/listar')
    config.add_route('cadastro', '/cadastrar')
    config.add_route('configuracao', '/configurar')
    config.add_route('contato', '/contato')
    config.add_route('login', '/login')
    config.add_route('sobre', '/sobre')
    config.add_route('usuario', '/usuario')
    config.add_route('mapa', '/mapa')
    config.add_route('orcamento', '/orcamento')	
    config.add_route('inserir_ponto', '/inserir_ponto')	
    config.add_route('privacidade', '/privacidade')	
    config.add_route('termos', '/termos')	
	
    config.scan()
    return config.make_wsgi_app()
