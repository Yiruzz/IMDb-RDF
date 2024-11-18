from rdflib import Graph, URIRef, Literal, Namespace
from wikidata_sparql_movies import search_movie_on_wikidata
import time

g = Graph()
g.parse('cleaned_imdb.ttl', format='turtle')

# Define namespaces
EX = Namespace("http://example.org/movies#")
g.bind("ex", EX)

query = """
SELECT ?pelicula ?titulo ?anio WHERE {
    ?pelicula rdf:type ex:Movie ;
            ex:title ?titulo ;
            ex:releaseYear ?anio .
}
"""

peliculas = [(str(row.pelicula), str(row.titulo), str(row.anio)) for row in g.query(query)] # List comprehension para obtener las peliculas del ttl

for nodo_pelicula, titulo, anio in peliculas:
    json_response = search_movie_on_wikidata(titulo, int(anio)) # Busca la pelicula en Wikidata

    # Itera sobre las entradas de la respuesta JSON
    for response_entry in json_response['results']['bindings']:
        movie_node = URIRef(nodo_pelicula) # URI de la pelicula en el TTL

        # IMDb ID
        if 'imdb_id' in response_entry:
            imdb_id = Literal(response_entry['imdb_id']['value'])
            g.add((movie_node, EX["imdbID"], imdb_id))

        # Capital cost
        if 'capital_cost' in response_entry:
            capital_cost = Literal(response_entry['capital_cost']['value'])
            g.add((movie_node, EX["capitalCost"], capital_cost))

        # Narrative location
        if 'narrative_location_label' in response_entry:
            narrative_location = Literal(response_entry['narrative_location_label']['value'])
            #narrative_location = search_URI_value(narrative_location_URI.split('/')[-1])
            g.add((movie_node, EX["narrativeLocation"], narrative_location))

        # Production company
        if 'production_company_label' in response_entry:
            production_company = Literal(response_entry['production_company_label']['value'])
            #production_company = search_URI_value(production_company_URI.split('/')[-1])
            g.add((movie_node, EX["productionCompany"], production_company))

        time.sleep(1) # Espera 1 segundo para no saturar el servidor y que (ojalá) no nos bloqueen

g.serialize('enriched_imdb.ttl', format="turtle")