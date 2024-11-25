# IMDb-RDF
This repository contains the files used for the project of the Web de Datos (CC7220-1) course of the Department of Computer Science of the University of Chile. The authors of the project are Arturo Kullmer, Camila Salas, and Javiera Labrín.

## Description
The project consists of the transformation of the IMDb top 1000 movies dataset into RDF format. The dataset was obtained from [Kaggle](https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows) page. The dataset contains information about movies, actors, directors, etc. The goal of the project is to transform this data into RDF format, using the [RDF 1.1 Turtle](https://www.w3.org/TR/turtle/) syntax to then enrich de data with [WikiData](https://query.wikidata.org/sparql) and finally be able to query the data using [SPARQL](https://www.w3.org/TR/sparql11-query/).

## Code Execution

If you want to execute the code, you must have the libraries specified in the `requirements.txt` file. 

Then, to execute the queries you must run the following command:

```bash
python queries.py
```

This will execute the queries specified in the `queries.py` file and print the results in the console.  The user will be prompted to enter the number of the query they want to execute. The queries available are the following:

```bash
1. Find the 5 locations with the most movies
2. The 5 directors with the most movies
3. Rating by genre
4. The pair of actors that appear together in the most movies
5. Top number of movies that have the same director and actor
6. The count of movies by release year
7. Top 5 actors who appear in more movies
8. Top 5 directors who appear in more movies
9. The actor and director who have worked together the most
10. The 5 producers with the most movies
```

## Files

### Data
- `imdb_top_1000.csv`: CSV file containing the IMDb top 1000 movies dataset.
- `rdf_movies.ttl`: RDF file containing the IMDb top 1000 movies dataset in RDF format after cleaning the csv in python and converting the csv to ttl.
- `cleaned_imdb.ttl`: RDF file containing the IMDb top 1000 movies dataset in RDF format after cleaning the `rdf_movies.ttl` file in python.
- `enricheced_imdb_rdf.ttl`: RDF file containing the IMDb top 1000 movies dataset in RDF format after enriching the `cleaned_imdb.ttl` file with [Wikidata](https://query.wikidata.org/sparql) movies data using **SparQL**.

### Code
- `csv_to_rdf.ipynb`: Jupyter notebook containing the code used to convert the `imdb_top_1000.csv` file to RDF format and also used to clean some of the csv data.
- `clean_imdb_rdf.py`: Python script used to clean the `rdf_movies.ttl` file, specifaclly the `rdf_movies.ttl` file was cleaned to parse the genres and stars in a format more suitable to a graph database.
- `imdb_rdf.py`: Python script used to enrich the `cleaned_imdb.ttl` file with [Wikidata](https://query.wikidata.org/sparql) movies data using **SPARQL**. The query used is defined in the `wikidata_sparql_movies.py` file.
- `queries.py`: Python script containing the queries executed to `enriched_imdb_rdf.ttl` file.

Also you should note that the comments on the code are written in *spanish*.

## Methodology

The methodology used to transform the IMDb top 1000 movies dataset into RDF format is the following:

The `imdb_top_1000.csv` file was cleaned using the `csv_to_rdf.ipynb` Jupyter notebook. The cleaning process consisted of removing unnecessary columns and transforming the data into a more usable format. The cleaned data was then saved into the `rdf_movies.ttl` file. Then, with the `clean_imdb_rdf.py` script, the `rdf_movies.ttl` file was cleaned to parse the genres and stars in a format more suitable to a graph database. The data was then saved into the `cleaned_imdb.ttl` file. 

After that, the `cleaned_imdb.ttl` file was enriched with [Wikidata](https://query.wikidata.org/sparql) movies data using **SPARQL**. In this process we noticed that the Wikidata API blocked our requests if they were too frequent, so we had to wait 2 seconds between every query. The query used to enrich the data is defined in the `wikidata_sparql_movies.py` file. The `imdb_rdf.py` script was used to execute the query and enrich the data. The data was then saved into the `enriched_imdb_rdf.ttl` file.

Finally, the `queries.py` script was used to execute the queries to the `enriched_imdb_rdf.ttl` file. A presentation in **Spanish** with the results of the queries can be found in the `presentation.pdf` file.

## Future Work
- Add more queries to the `queries.py` file.
- Add more data to the RDF file using [Wikidata](https://query.wikidata.org/sparql) or other sources.
- Transform the `grossing` and `capitalCost` value datatype to a more usable format.
