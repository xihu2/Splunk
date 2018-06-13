#!/usr/bin/python
import pytest
import requests

"""
Get movie with parameter q
"""
def getMovie(movie_name):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Accept': 'application/json',}
	params = (('q', movie_name),)
	r = requests.get(url, headers=headers, params=params)

	return r.status_code

"""
Get movie with parameter q return all the expected records with the values passed in q
"""
def validateGetMovie(movie_name):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Accept': 'application/json',}
	params = (('q', movie_name),)
	r = requests.get(url, headers=headers, params=params)
	
	if (r.status_code == 200):
		data = r.json()
		total = len(data['results'])
		
		for i in range(total):
			if movie_name not in data['results'][i]['title']:
				return False
		
		return True
		
	else:
		return "Get API failed!"		
				
"""
Get movie without parameter q
"""
def getMoviewithoutq():
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Accept': 'application/json',}

	r = requests.get(url, headers=headers)

	return r.status_code


"""
Get movie with parameter count
"""
def getMoviewithcount(movie_name, count):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Accept': 'application/json',}
	params = (('q', movie_name),('count', count))
	r = requests.get(url, headers=headers, params=params)
	
	data = r.json()
	
	return len(data['results'])

"""
Get movie without Header
"""
def getMoviewithoutHeader(movie_name):
	
	url = 'https://splunk.mocklab.io/movies'	
	params = (('q', movie_name),)
	r = requests.get(url, params=params)

	return r.status_code
	
"""
Get movie with parameter not existing
"""
def getMoviewithdirector(director):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Accept': 'application/json',}
	params = (('d', director),)
	r = requests.get(url, headers=headers, params=params)

	return r.status_code	



"""
Test curl -X GET https://splunk.mocklab.io/movies?q=batman -H "Accept: application/json"
"""
total_movie = 16
movieName = 'batman'

#Get movie with parameter q
def testGetMoviewithq():
	assert getMovie(movieName) == 200

#Get movie with parameter q return all the expected records with the values passed in q
def testvalidateGetMovie():
	assert validateGetMovie(movieName)

#Get movie without parameter q
def testGetMoviewithoutq():	
	assert getMoviewithoutq() == 404 
	
#Get movie with parameter count = 0, 2 & total batman movie plus 10	
@pytest.mark.parametrize('count, expected', [(0, total_movie), (2, 2), (total_movie+10, total_movie)])
def testGetMovieWithCount(count, expected):
	assert getMoviewithcount(movieName, count) == expected

#Get movie without Header
def testgetMoviewithoutHeader():
	assert getMoviewithoutHeader(movieName) == 404


#Get movie with parameter not existing
def testgetMoviewithdirector():
	assert getMoviewithdirector('James') == 404
	


