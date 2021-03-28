"""
Machine Learning Knowledge Base
 by James Butcher
 version 1.0
 finished 3/26/21

 - A web app designed to easily manage and access a knowledge base
 - The knowledge base is intended for my collection of machine learning knowledge,
    but can be used for any other domain as well.

4 pages:
    - Home page: Introduction and instructions on how to use
    - Knowledge base: Add and remove RDF triples
    - Recommender: Select an application and get info on ML methods that can do it
    - Custom Query: Make simple queries on the knowledge base

 This was my first web app. The whole basic structure was built by following
 this YouTube video:

    Python Website Full Tutorial - Flask, Authentication, Databases & More
     by Tech With Tim - Feb 1, 2021
     https://www.youtube.com/watch?v=dam0GPOAvVI&list=PLwGZ7X2gMChQbGLrYP57YW2S_lrknkw1_&index=57

 My introduction to the subject of ontology, knowledge graphs, and RDF came from the online course I took
 for my MCS - Masters of Computer Science degree from ASU on Coursera, taken in Spring A 2021:
     CSE 579 - Knowledge Representation and Reasoning, created by Dr. Joohyung Lee

"""

from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
