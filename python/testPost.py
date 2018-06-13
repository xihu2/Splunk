#!/usr/bin/python
import pytest
import requests

"""
Post movie with required payload
"""
def postMovie(movie_name, desc):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Content-Type': 'application/json',}
	payload = '{"name": ' + movie_name + ', "description": ' + desc + '}'
	r = requests.post(url, headers=headers, data=payload)

	return r.status_code

"""
Post movie with required payload, Get API return the posted movie
"""
def validatePostMovie(movie_name, desc):
		
	if postMovie(movie_name, desc) == 200:
	
		url = 'https://splunk.mocklab.io/movies'	
		headers = {'Accept': 'application/json',}
		params = (('q', movie_name),)
		r = requests.get(url, headers=headers, params=params)
		
		if (r.status_code == 200):
			data = r.json()
			if (len(data['results']) > 0):
				for i in range(len(data['results'])):
					if data['results'][i]['title'] == movie_name:
						return True
						
			return False
			
		else:	
			return "Get API failed!"
	else:	
		return "Post API failed!"
		
	
"""
Post movie without Description in payload
"""
def postMoviewithoutDesc(movie_name):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Content-Type': 'application/json',}
	payload = '{"name": ' + movie_name + '}'
	r = requests.post(url, headers=headers, data=payload)

	return r.status_code

"""
Post movie without Name in payload
"""	
def postMoviewithoutName(desc):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Content-Type': 'application/json',}
	payload = '{"description": ' + desc + '}'
	r = requests.post(url, headers=headers, data=payload)

	return r.status_code

"""
Post movie without payload
"""
def postMoviewithoutPayload():
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Content-Type': 'application/json',}
	r = requests.post(url, headers=headers)

	return r.status_code

"""
Post movie without Header
"""
def postMoviewithoutHeader(movie_name, desc):
	
	url = 'https://splunk.mocklab.io/movies'	
	payload = '{"name": ' + movie_name + ', "description": ' + desc + '}'
	r = requests.post(url, data=payload)

	return r.status_code
	
"""
Post movie with not existing payload
"""
def postMoviewithTitleName(movie_name, desc):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Content-Type': 'application/json',}
	payload = '{"titleName": ' + movie_name + ', "description": ' + desc + '}'
	r = requests.post(url, headers=headers, data=payload)

	return r.status_code
			
"""
Test curl -d '{"name":"superman", "description":"the best movie ever made"}' 
	-H "Content-Type: application/json" -X POST https://splunk.mocklab.io/movies
"""

#Post movie with name & description
@pytest.mark.parametrize('name, desc, expected', [('Super Batman', 'Best Movie', 200), ('', 'Love it', 404), ('True Batman', '', 404), ('', '', 404)])
def testPostMovie(name, desc, expected):
	assert postMovie(name, desc) == expected
	
#Post movie with required payload, Get API return the posted movie
def testvalidatePostMovie():
	assert validatePostMovie('Superbatman', 'Best movie') == True


#Post movie without Description in payload	
def testpostMoviewithoutDesc():
	assert postMoviewithoutDesc('SuperBatman') == 404
	
#Post movie without Name in payload	
def testpostMoviewithoutName():
	assert postMoviewithoutName('Love it!') == 404

#Post movie without Header	
def testpostMoviewithoutHeader():
	assert postMoviewithoutHeader('Superman', 'Good!') == 404

	
#Post movie without payload	
def testpostMoviewithoutPayload():
	assert postMoviewithoutPayload() == 404

#Post movie with not existing payload
def testpostMoviewithTitleName():
	assert postMoviewithTitleName('CoCo', 'Super!') == 404

