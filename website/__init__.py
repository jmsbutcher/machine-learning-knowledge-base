
from flask import Flask 
import rdflib
from rdflib import Graph, Namespace, Literal, URIRef

from functions import load_graph

# The "knowledge base"
g = Graph()

# This string acts as the prefix to all URIs in the knowledge base
namespace_string = "http://JamesButcher_ML_KnowledgeBase.org/"

# You can use n as a shorthand prefix when defining a URI in the code.
#  Instead of writing out "http://JamesButcher_ML_KnowledgeBase.org/regression",
#  you can write n.regression and it will create a URI identical to the above.
n = Namespace(namespace_string)

# When serializing the graph into a file format such as n3, use "mykb" as the prefix
g.bind("mykb", n)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'q,fso3,snfIme&3j0&jsm@euse,wieytosYEowjGTw27'
    
    load_graph()

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app

