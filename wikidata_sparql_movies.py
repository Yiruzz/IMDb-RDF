import requests

url = "https://query.wikidata.org/sparql"

def search_movie_on_wikidata(title, year):
    # Consulta SPARQL para buscar una película en Wikidata
    query = """
    SELECT DISTINCT ?movie ?imdb_id ?capital_cost ?narrative_location_label ?production_company_label WHERE {
    ?movie wdt:P31 wd:Q11424 ;
            wdt:P1476 ?title ;
            wdt:P577 ?release_date ;
            rdfs:label ?label ;
            wdt:P345 ?imdb_id .

    OPTIONAL { ?movie wdt:P2130 ?capital_cost .}
    OPTIONAL { ?movie wdt:P840 ?narrative_location .
               ?narrative_location rdfs:label ?narrative_location_label . 
               FILTER(lang(?narrative_location_label) = "en") }
    OPTIONAL { ?movie wdt:P272? ?production_company .
               ?production_company rdfs:label ?production_company_label . 
               FILTER(lang(?production_company_label) = "en") }

    FILTER((lang(?label) = "en") && (lcase(str(?title)) = "%s"))
    FILTER(YEAR(?release_date) = %d)
    }
    """ % (title.lower(), year)

    response = requests.get(url, params={'query': query, 'format': 'json'})

    # Verifica si la respuesta fue exitosa
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

# Ejemplo de uso:
# search_movie_on_wikidata("The Shawshank Redemption", 1994)