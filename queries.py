from rdflib import Graph, URIRef, Literal, Namespace
from wikidata_sparql_movies import search_movie_on_wikidata

g = Graph()
g.parse('enriched_imdb.ttl', format='turtle')

# Define namespaces
EX = Namespace("http://example.org/movies#")
g.bind("ex", EX)

query_1 = """
SELECT ?location (COUNT(?movie) as ?moviecount)
WHERE {
  ?movie a ex:Movie ;
         ex:narrativeLocation ?location .
}
GROUP BY ?location
HAVING (COUNT(?movie) > 1)
ORDER BY DESC(?moviecount)
LIMIT 5
"""
q1 = ("Encontrar las 5 localizacion que tienen más peliculas", query_1)

query_2 = """
SELECT ?director (COUNT(?movie) as ?moviecount)
WHERE {
  ?movie a ex:Movie ;
         ex:director ?director .
}
GROUP BY ?director
HAVING (COUNT(?movie) > 1)
ORDER BY DESC(?moviecount)
LIMIT 5
"""
q2 = ("Los 5 director que tienen más peliculas", query_2)

query_3 = """
SELECT ?genre (AVG(xsd:float(?imdbRating)) AS ?averageRating)
WHERE {
  ?movie a ex:Movie ;
         ex:genre ?genre ;
         ex:imdbRating ?imdbRating .
}
GROUP BY ?genre
"""
q3 = ("Rating por genero", query_3)

query_4 = """
SELECT ?actor1 ?actor2 (COUNT(?movie) AS ?sharedMovies)
WHERE {
  ?movie a ex:Movie ;
         ex:star ?actor1 ;
         ex:star ?actor2 .
  FILTER (?actor1 != ?actor2)
}
GROUP BY ?actor1 ?actor2
HAVING (COUNT(?movie) > 1)
ORDER BY DESC(?sharedMovies)
LIMIT 1
"""
q4 = ("El par de actores que aparecen juntos en la mayor cantidad de películas", query_4)

query_5 = """
SELECT ?movie ?director ?actor (COUNT(?movie) AS ?movieCount)
WHERE {
  ?movie a ex:Movie ;
         ex:director ?director ;
         ex:star ?actor .
    FILTER (?director = ?actor)
}
    GROUP BY ?director ?actor
    HAVING (COUNT(?movie) > 1)
    ORDER BY DESC(?movieCount)
    LIMIT 5
"""
q5 = ("Top cantidad de películas que tienen el mismo director y actor ", query_5)

query_6 = """
SELECT ?releaseYear (COUNT(?movie) AS ?movieCount)
WHERE {
  ?movie a ex:Movie ;
         ex:releaseYear ?releaseYear .
}
GROUP BY ?releaseYear
ORDER BY DESC(?movieCount)
"""
q6 = ("El conteo de películas por año de estreno", query_6)


query_7 = """
SELECT ?actor (COUNT(?movie) AS ?movieCount)
WHERE {
  ?movie a ex:Movie ;
         ex:star ?actor .
}
GROUP BY ?actor
ORDER BY DESC(?movieCount)
LIMIT 5
"""
q7 = ("Top 5 actores que aparecen en más películas", query_7)

query_8 = """
SELECT ?director (COUNT(?movie) AS ?movieCount)
WHERE {
  ?movie a ex:Movie ;
         ex:director ?director .
}
GROUP BY ?director
ORDER BY DESC(?movieCount)
LIMIT 5
"""
q8 = ("Top 5 directores que aparecen en más películas", query_8)

query_9 = """
SELECT ?actor ?director (COUNT(?movie) AS ?movieCount)
WHERE {
  ?movie a ex:Movie ;
         ex:star ?actor ;
         ex:director ?director .
}
GROUP BY ?actor ?director
ORDER BY DESC(?movieCount)
LIMIT 1
"""
q9 = ("El actor y director que más han trabajado juntos", query_9)

query_10 = """
SELECT ?productionCompany (COUNT(?movie) AS ?movieCount)
WHERE {
    ?movie a ex:Movie ;
              ex:productionCompany ?productionCompany .
}
GROUP BY ?productionCompany
ORDER BY DESC(?movieCount)
LIMIT 5
"""
q10 = ("Las 5 productoras que tienen más peliculas", query_10)


label_query = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

enumarte_query = [f"\t{i+1}. {label}" for i, (label, _) in enumerate(label_query)]
enumarte_query_print = "Consultas disponibles:\n" + "\n".join(enumarte_query)

try:
    print(enumarte_query_print)
    query_a_consultar = int(input(f"Ingrese el número de la query que desea consultar (1-{len(label_query)}):\n"))

    while query_a_consultar >= 1 and query_a_consultar <= len(label_query):

        label, query = label_query[query_a_consultar-1]
        print(f"Resultados para query_{query_a_consultar}:")
        print(label + ":")
        results = g.query(query)
        for row in results:
            print(row)

        print(enumarte_query_print)
        query_a_consultar = int(input(f"Ingrese el número de la query que desea consultar (1-{len(label_query)}):\n"))
except KeyboardInterrupt:
    print("\nSaliendo...")
