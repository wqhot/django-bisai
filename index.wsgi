import sae
from GameServer import wsgi

application = sae.create_wsgi_app(wsgi.application)