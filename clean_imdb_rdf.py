from rdflib import Graph, URIRef, Literal, Namespace

g = Graph()
g.parse('rdf_movies.ttl', format='turtle')

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

# Separamos los generos de las peliculas
for nodo_pelicula , _ , _ in peliculas:
    movie_node = URIRef(nodo_pelicula)

    # Obtenemos los géneros de la película
    generos = list(g.objects(movie_node, EX["genre"]))
    if generos:
        # Los géneros están separados por coma
        genero_str = generos[0]
        generos_list = genero_str.split(',')

        # Eliminar el género actual del TTL
        g.remove((movie_node, EX.genre, Literal(genero_str)))

        # Añadir los géneros individualmente
        for genero in generos_list:
            g.add((movie_node, EX.genre, URIRef(EX[genero.strip()])))

# Separamos los actores de las peliculas
for nodo_pelicula , _ , _ in peliculas:
    movie_node = URIRef(nodo_pelicula)

    # Obtenemos los géneros de la película
    stars = list(g.objects(movie_node, EX["stars"]))
    if stars:
        # Las estrellas estarán separadas por coma
        star_str = stars[0]
        stars_list = star_str.split(',')

        # Eliminar el género actual del TTL
        g.remove((movie_node, EX.stars, Literal(star_str)))

        # Añadir los géneros individualmente
        for star in stars_list:
            g.add((movie_node, EX.star, Literal(star.strip())))

# Guardar el archivo actualizado
g.serialize('cleaned_imdb.ttl', format='turtle')