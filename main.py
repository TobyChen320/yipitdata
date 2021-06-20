import requests
import re
import numpy as np
import pandas as pd

class Oscars():
    '''
    Hits data file url that I downloaded and pushed to git - https://raw.githubusercontent.com/TobyChen320/yipitdata/main/data/movies -
    And returns every Oscar winning movie and its budget along with the average budget.
    '''
    def __init__(self):
        self.base_url = 'https://raw.githubusercontent.com/TobyChen320/yipitdata/main/data/movies'
        # create a list of dictionaries that stores film title, year, url, and budget
        self.winning_films = []
  
    def search(self):
        '''
        Searches the data to return winning movies.
        This will also add the movies that fit the criteria into winning_films.
        '''
        main = requests.get(self.base_url).json()
        yearly_list = main['results']
        # loop through the results from main to get each year's nominations
        for year in yearly_list:
            yearly_films = year['films']
        # loop through each film every year to find the winners
            for films in yearly_films:
                # if the film is a winner add to winning_films list
                if films['Winner'] == True:
                    winner = {}
                    winner['film'] = films['Film']
                    winner['year'] = year['year']
                    winner['url'] = films['Detail URL']
                    self.winning_films.append(winner)
    
    def get_budget(self):
        '''
        Returns budget of each winning film from its Detail URL page.
        '''
        for film in self.winning_films:
            movie = requests.get(film['url']).json()
            # if there is no budget data; I just set it to None (You can change this to fill the missing value with whatever you desire depending on what you are looking for)
            film['budget'] = movie.get('Budget', None)
    
    def clean(self):
        '''
        Cleans the data by removing irrelevant characters such as currency symbol.
        It will perform foreign exchange calculation if needed and it gives numeric value for 'million'.
        If given a budget range; it will use the high value of that range.
        '''
        # loop through winning films
        for film in self.winning_films:
            # clean title value
            title = film['film']
            film['title'] = re.sub("\[[^\]][\]]", '', title)
            # clean year value
            year = film['year']
            film['year'] = re.sub("\[[^\]][\]]", '', year)
            # if the film budget is not None it will clean the budget value
            if film['budget'] != None:
                budget = film['budget']
                # if the first character is not $, clean the value
                if budget[0] != '$':
                    # if the value is '£', clean and multiply by current exchange rate (As of 6/19/21 £1 = $1.38) to USD
                    if budget[0] == '£':
                        clean_currency = re.sub('£', '', budget)
                        remove_footnotes = re.sub('[\(\[].*?[\)\]]', '', clean_currency)
                        currency = re.sub('million.*', ' 1380000', remove_footnotes)
                        try:
                            first = [float(x.replace(',', '')) for x in currency.split( )]
                            second = int(np.prod(np.array(first)))
                            film['budget'] = second
                        except ValueError:
                            range_value = currency[0].split('-')
                            high_value = int(range_value[1]) * int(range_value[2])
                            film['budget'] = high_value
                    # if the starting character is U as opposed to '$'
                    elif budget[0] == 'U':
                        remove_currency = re.sub('[US$ ]', '', budget)
                        remove_footnotes = re.sub("[\(\[].*?[\)\]]", '', remove_currency)
                        currency = re.sub('million.*', ' 1000000', remove_footnotes)
                        try:
                            first = [float(x.replace(',', '')) for x in currency.split( )]
                            second = int(np.prod(np.array(first)))
                            film['budget'] = second
                        except ValueError:
                            range_value = currency[0].split('-')
                            high_value = int(range_value[1]) * int(range_value[2])
                            film['budget'] = high_value
                # if first character is $; this will clean the values
                elif budget[0] == '$':
                    remove_currency = re.sub('[$]', '', budget)
                    remove_footnotes = re.sub("[\(\[].*?[\)\]]", '', remove_currency)
                    currency = re.sub('million.*', ' 1000000', remove_footnotes)
                    try:
                        first = [float(x.replace(',', '')) for x in currency.split( )]
                        second = int(np.prod(np.array(first)))
                        film['budget'] = second
                    except ValueError:
                        range_value = re.split('\-|\–|  ',currency)
                        high_value = int(range_value[1]) * int(range_value[2])
                        film['budget'] = high_value

    # if for some reason you wish to find out the average budget for all the winning movies together (only works for the movies that have a budget value)
    # def average_budget(self):
    #     '''
    #     Calculates the average budget of the winning movies that have budget data
    #     '''
    #     total_movies = 0
    #     total_dollars = 0
    #     for film in self.winning_films:
    #         if film['budget'] != None:
    #             total_movies += 1
    #             total_dollars += film['budget']
    #             average = int(total_dollars/total_movies)
    #             return average

    # this just makes it easier on the eyes
    # def movies_reformat(self):
    #     '''
    #     Converts the url into a pandas dataframe and into a csv file
    #     '''
    #     movies = requests.get(self.base_url).json()
    #     df = pd.concat([pd.DataFrame(pd.json_normalize(x)) for x in movies['results']], ignore_index=True)
    #     df["Detail URL"] = [x[0]["Detail URL"] for x in df["films"]]
    #     df["Producer(s)"] = [x[0]["Producer(s)"] for x in df["films"]]
    #     df["Production Company(s)"] = [x[0]["Production Company(s)"] for x in df["films"]]
    #     df["Wiki URL"] = [x[0]["Wiki URL"] for x in df["films"]]
    #     df["Winner"] = [x[0]["Winner"] for x in df["films"]]
    #     df["films"] = [x[0]["Film"] for x in df["films"]]
    #     df.to_csv('movies.csv', index=False)

    def print_all(self):
        '''
        Prints results
        '''
        for film in self.winning_films:
            print(film['title'], film['year'], film['budget'])
            # Uncomment this if you want to see the average budget.
            # print("Average budget: $", self.average_budget())
    
    def run(self):
        '''
        Run function
        '''
        self.search()
        self.get_budget()
        self.clean()
        self.print_all()
        # uncomment if you wish to reformat data
        # self.movies_reformat()

start = Oscars()
start.run()
