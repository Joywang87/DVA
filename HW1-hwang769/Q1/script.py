import http.client
import json
import time
import sys
import collections
import csv



def get_url(domain, path):
    """ 
    args:
        domain (string) : the website
        path (string) : url to download
        e.g. https://api.themoviedb.org/3/movie/551?api_key=91c001153ba31e1892bf968d8ebb736b
    return:
        body (string) : body of the response
        e.g. {"adult":false, "backdrop_path" ...
    use 
    1. Create an connection object http.client.HTTPConnection
    2. Request the page  HTTPConnection.request()
    3. Get the response HTTPConnection.getresponse()
    https://docs.python.org/3/library/http.client.html#http.client.HTTPResponse
    4. Get the text from the response and return it (None if it fails)
    """
    connection = http.client.HTTPSConnection(domain)
    connection.request("GET", path)
    response = connection.getresponse()
    #headers = response.getheaders()
    data = response.read()
    connection.close()
    return data


def get_popular_movies(api_key, genre, counts, min_year):
    """ 
    https://developers.themoviedb.org/3/discover/movie-discover
    args:
        genre (string) : which genre to get, drama_id ='18'
        count (int) : the number to get
        min_year (int) : this year and later
    return: 
        list[(id, name)]

    use the get_url function
    for loop through the dictionary to extract out the keys and names
    """
    
    results = []
    count = 0
    page = 1
    while count < counts:
        path = "/3/discover/movie?api_key={}&sort_by={}&primary_release_date.gte={}-01-01&page={}&with_genres={}".format(api_key, "popularity.desc", min_year, page, genre)
        output = get_url('api.themoviedb.org', path)
        if output is None:
            print("Something is wrong")
            return results
        data = json.loads(output)
        for result in data['results']:
            if count >= counts:
                return results
            id = str(result['id'])
            name = str(result['original_title'])
            results.append((id,name))
            count += 1
        page += 1
    return results
 
def find_movies(api_key):
    """ tutorial: https://www.google.com/url?q=https://www.tutorialspoint.com/python3/python_command_line_arguments.htm&sa=D&ust=1548539598612000 
        command line:  python3 script.py <API_KEY>

    """
    #start = time.time()
    movies = get_popular_movies(api_key, "18", 350, 2014)
    
    with open('movie_ID_name.csv', 'w') as outfile:
        for movie in movies:
            outfile.write(movie[0])
            outfile.write(',')
            outfile.write(movie[1])
            outfile.write('\n')
    #end = time.time()
    # print(1.0*(end-start)/60)

def similar_movies(api_key):
    """
    tutorial: 
    https://developers.themoviedb.org/3/movies/get-similar-movies
    """
    start = time.time()
    with open('movie_ID_name.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        ids = []
        for row in csv_reader:
            movie_id = int(row[0])
            ids.append(movie_id)
    print('the length of the ids is : {}'.format(len(ids)))
    output_list = []
    unique = set()
    i = 1
    for movie_id in ids:
        print(i)
        count = 0
        page = 1
        while count < 5:
            path = "/3/movie/{}/similar?api_key={}&page={}".format(movie_id, api_key, page)
            output = get_url('api.themoviedb.org', path)
            data = json.loads(output)
            if not data.get('results', None):
                #print("No more results")
                break
            for result in data['results']:
                if count >= 5:
                    break
                similar_id = str(result['id'])
                temp = (str(movie_id), similar_id)
                if temp not in unique:
                    #print(temp)
                    output_list.append(temp)
                    unique.add(temp)
                count += 1
            page += 1
        i += 1

    with open('movie_ID_sim_movie_ID.csv', 'w') as outfile:
        for movie in output_list:
            outfile.write(movie[0])
            outfile.write(',')
            outfile.write(movie[1])
            outfile.write('\n')

    end = time.time()
    print('the total length of time is: {} minutes'.format(1.0*(end-start)/60))

if __name__== "__main__":
    if len(sys.argv) == 2:
        api_key = str(sys.argv[1]) #Write code to get key from command line arguments
        #find_movies(api_key)
        similar_movies(api_key)
    else:
        print("Please provide an api key.")