"""
Run this file on the command line ('python functions.py') to enter 
 command-line mode for easy diagnostics and debugging
"""

import rdflib
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.plugins.sparql import prepareQuery

# For debugging
g = Graph()
namespace_string = "http://JamesButcher_ML_KnowledgeBase.org/"
n = Namespace(namespace_string)
g.bind("mykb", n)

# For easy removal of poorly-entered triples - see remove_last_triple() method
last_added_triple = None

#-----------------------------------------------------------------------------------------------------
# Loading and Saving
#-----------------------------------------------------------------------------------------------------

def save_graph(save_format="n3"):
    """ Save graph file """
    g.serialize(destination="graph.{}".format(save_format), format=save_format)
    print("Saved graph as graph.{}".format(save_format))

def load_graph(load_format=None):
    """ Load saved graph file """
    # By default, try some common graph file extensions
    if load_format is None:
        load_formats = ["nt", "n3", "turtle", "xml", "pretty-xml"]
        for f in load_formats:
            try:
                g.load("graph.{}".format(f), format=f)
                print("Loaded file 'graph.{}'".format(f))
                return True
            except FileNotFoundError:
                pass
        print("No graph found.")
        return False
    # If a specific graph file extension is passed as an argument, try that one
    else:
        try:
            g.load("graph.{}".format(load_format), format=load_format)
            print("Loaded file 'graph.{}'".format(load_format))
            return True
        except FileNotFoundError:
            print("Graph file 'graph.{}' not found.".format(load_format))
            return False


#-----------------------------------------------------------------------------------------------------
# Conversion Functions
#-----------------------------------------------------------------------------------------------------

def isolate_last_part_of_URI(uri):
    """ Get the substring at the end of the URI after the last '/' """
    if isinstance(uri, Literal):
        return uri
    if uri is None:
        return ""
    return uri[uri.rfind('/')+1 : ]

def string_to_URI(s):
    """ Convert a string to a URIRef

     Example: "Machine Learning" -->  URIRef(http://JamesButcher_ML_KnowledgeBase.org/Machine_Learning)
    """
    if s is None:
        return None
    # If the string is enclosed in quotes, turn it into a Literal
    if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
        s = s.replace('"', '')
        s = s.replace("'", "")
        return Literal(s)
    else:
        uri_string = namespace_string + s.replace(' ', '_')
        return URIRef(uri_string)

def triple_to_text(triple):
    """ Convert a triple into three plain-language strings separated by dashes """
    # If the 3rd part of the triple (the object) is a Literal, enclose it in quotes
    obj = triple[2]
    if isinstance(obj, Literal):
        obj = '"' + obj + '"'
    else:
        obj = isolate_last_part_of_URI(obj).replace('_', ' ')

    return isolate_last_part_of_URI(triple[0]).replace('_', ' ') + ' ---- ' + \
           isolate_last_part_of_URI(triple[1]).replace('_', ' ') + ' ---- ' + \
           obj

def text_to_triple(triple_text):
    """ Convert a plain-text triple into a regular triple with URIs (or a Literal) """
    elements = triple_text.split(' ---- ')
    s = string_to_URI(elements[0])
    p = string_to_URI(elements[1])
    o = string_to_URI(elements[2])
    triple = (s, p, o)
    return triple


#-----------------------------------------------------------------------------------------------------
# Adding and Removing Triples
#-----------------------------------------------------------------------------------------------------

def input_new_triple(subject, predicate, obj):
    """ Process raw string triple input into RDF format and return """
    # Validate input
    if subject is None or predicate is None or obj is None or len(subject) == 0 or len(predicate) == 0 or len(obj) == 0:
        print("\nERROR - missing an input\n")

    # Process subject and convert to URI
    subject = subject.strip().lower().replace(' ', '_')
    subject = string_to_URI(subject)

    # Process predicate and convert to URI
    predicate = predicate.strip().lower().replace(' ', '_')
    predicate = string_to_URI(predicate)

    # Process object - Make the object a Literal if enclosed in quotes or is a link, otherwise make it a URI
    if (obj[0] == '"' and obj[-1] == '"') or (obj[0] == "'" and obj[-1] == "'") or "/" in obj:
        obj = obj.strip("\"'")
        obj = Literal(obj)
    else:
        obj = string_to_URI(obj)

    return subject, predicate, obj

def add_triple(subject, predicate, obj):
    """ Add a (subject, predicate, obj) triple to the graph """
    new_triple = (subject, predicate, obj)
    g.add(new_triple)

def remove_last_triple():
    """ Remove the most recently added triple during this session """
    if last_added_triple:
        g.remove(last_added_triple)
    print("\nRemoved last triple: ", triple_to_text(last_added_triple))


#-----------------------------------------------------------------------------------------------------
# Queries and Other Output Functions
#-----------------------------------------------------------------------------------------------------

def take_query():
    """ Take a non-SPARQL rdflib pattern matching "query" input and output the results """

    q = input("\nEnter a query as three words separated by spaces. Use keyword 'what' in place of the variables you want to query.\n" +
              " Example:   'what can_do classification'   -->   gets all the things that can do classification\n\n")
    if q == "e": return
    input_values = q.split(" ")
    # Reprompt user for correct input if not three strings separated by spaces
    while len(input_values) != 3:
        print("You must enter exactly three strings separated by spaces. Use underscores if necessary. Try again or enter 'e' to end query.")
        q = input(" -- : ")
        if q == "e": return
        input_values = q.split(" ")
        print()

    # Change any 'what' keywords to None. None acts as the wildcard for rdflib triple pattern matching
    s, p, o = input_values
    if s.lower() == "what": s = None
    if p.lower() == "what": p = None
    if o.lower() == "what": o = None

    # Run the pattern matching "query" and print the results
    results = g.triples((string_to_URI(s), string_to_URI(p), string_to_URI(o)))
    print("\nResults:\n")
    for r in results:
        print(triple_to_text(r))
    print()

def print_graph():
    """ Print the contents of the entire graph in both serialized format and plain-language format """
    print("\n--- Graph Contents: ---\n")
    print(" - In n3 format:\n")
    print(g.serialize(format="n3").decode("utf-8"))

    print(" - In plain text format:\n")
    triples = []
    # Sort the triples by subject
    for s, p, o in g:
        triples.append((s, p, o))
        triples.sort()
    for triple in triples:
        print(triple_to_text(triple))
    print()

def generator_to_list(generator, exclude_literals=False):
    """ Convert a graph generator object such as g.subjects() to a list with distinct text elements """
    item_list = []
    for i in generator:
        # If exclude_literals is set to True, skip over any Literals and add only URIs
        if exclude_literals and isinstance(i, Literal):
            continue
        if i not in item_list:
            item_list.append(i)
    item_text_list = [isolate_last_part_of_URI(i).replace('_', ' ') for i in item_list]
    item_text_list.sort()
    return item_text_list

def run_test():
    input_new_triple()
    print("\nLast added triple:\n", last_added_triple)
    t2x = triple_to_text(last_added_triple)
    print("\nTriple to text:\n", t2x)
    x2t =  text_to_triple(t2x)
    print("\nText back to triple:\n", x2t, "\n")
    print("Original equal to final output?: ", last_added_triple==x2t)


if __name__ == "__main__":

    print("\nWelcome to James's prototype Machine Learning Ontology Program - 3-13-21\n")

    # Load graph
    if not load_graph():
        print("Created new graph: 'graph.n3'.")

    print("\nEnter one of the following commands:\n" +
          " 'p' to print the contents of the graph,\n" +
          " 'q' to query the graph,\n" +
          " 'a' to add a new triple (enclose the object in quotes to make it a literal),\n" +
          " 'u' to remove the last added triple,\n" +
          " 's' to save the graph, or\n" +
          " 'e' to exit.\n")

    exit_command = False

    while not exit_command:

        input_command = input()

        if input_command == 'e':
            exit_command = True
            break
        elif input_command == 'q':
            take_query()
        elif input_command == 'p':
            print_graph()
        elif input_command == 'a':
            input_new_triple()
        elif input_command == 'u':
            remove_last_triple()
        elif input_command == 's':
            save_graph()
        elif input_command == 't':
            run_test()
        else:
            print("Not a recognized command. Try again.")

        print("\n Input new command [p, q, a, u, s, e] -- : ", end="")
