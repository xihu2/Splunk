#!/usr/bin/python
import pytest
import requests
import urllib2

"""
get all movie with movie name
"""
def getMovie(movie_name, count):
	
	url = 'https://splunk.mocklab.io/movies'	
	headers = {'Accept': 'application/json',}
	params = (('q', movie_name),('count', count))
	r = requests.get(url, headers=headers, params=params)
	
	if r.status_code == 200:
		return r.json()
	else:
		return "Get API failed!"
		

"""
SPL-001 no 2 movie has same poster_path image
"""	
def checkPosterPathDup(movie_name, count):
	
	data = getMovie(movie_name, count)
	
	total = len(data['results'])
	
	posterPath = []
	
	for i in range(total):
		if 'poster_path' in data['results'][i]:
			if data['results'][i]['poster_path'] is not None:
				posterPath.append(data['results'][i]['poster_path'])
				
	posterPath.sort()
	for i in range(len(posterPath)-1):
		if posterPath[i+1] == posterPath[i]:
			# found duplicate
			return False
			
	return True
	
"""
check url valid

"""
def valid_url(url):
    try:
        urllib2.urlopen(url)
        return True
    except Exception, e:
        return False


"""
SPL-002 all poster_path link must be valid and null is acceptable 
"""
def checkPosterPathValid(movie_name, count):
	
	data = getMovie(movie_name, count)
	total = len(data['results'])
	
	posterPath = []
	
	for i in range(total):
		if 'poster_path' in data['results'][i]:
			if data['results'][i]['poster_path'] is not None:
				posterPath.append(data['results'][i]['poster_path'])
				
	for i in range(len(posterPath)):
		if valid_url(posterPath[i]):
			r = requests.get(posterPath[i])
			if r.status_code != 200:
				#found invalid poster_path link
				return False
		else:
			return False
				
	return True

"""
SPL-003 sorting rules 1 - genre_ids null movies are returned first
"""
def checkSortingRule1(movie_name, count):

	data = getMovie(movie_name, count)
	total = len(data['results'])
	
	i = 0
	
	while i<total and len(data['results'][i]['genre_ids']) == 0:
		i = i+1
		
	if 	i >= total:
		return True
		
	else:
		while i<total and len(data['results'][i]['genre_ids']) != 0:
			i = i+1
			
	if i>= total:
		return True
		
	else:
		return False	
			

"""
SPL-003 sorting rules 2 part 1 - multiple genre_ids null movies are sorted by id
"""	
def checkSortingRule2_part1(movie_name, count):
	
	if checkSortingRule1(movie_name, count):
		data = getMovie(movie_name, count)
		total = len(data['results'])
	
		i = 0
		id = []
	
		while i<total and len(data['results'][i]['genre_ids']) == 0:
			id.append(data['results'][i]['id'])
			i = i+1

		if len(id) > 1:
			for j in range(len(id)-1):
				if id[j+1] < id[j]:
					return False
					
		return True
		
	else:
		return "Please fix SPL-003 Rule #1"


"""
SPL-003 sorting rules 2 part 2 - for genre_ids non-null, movies are sorted by id
"""	
def checkSortingRule2_part2(movie_name, count):
	
	if checkSortingRule1(movie_name, count):
		data = getMovie(movie_name, count)
		total = len(data['results'])
	
		i = 0
		id = []
	
		while i<total:
			if len(data['results'][i]['genre_ids']) != 0:
				id.append(data['results'][i]['id'])
				
			i = i+1
			
		if len(id) > 1:
			for j in range(len(id)-1):
				if id[j+1] < id[j]:
					return False
					
		return True
		
	else:
		return "Please fix SPL-003 Rule #1"
		
		
"""
SPL-004: The number of movies whose sum of "genre_ids" > 400 should be no more than 7
"""		
def checkmovieGenreIDSum(movie_name, count):

	data = getMovie(movie_name, count)
	total = len(data['results'])
	
	i = 0
	movie_num = 0
	
	while i<total:
		if len(data['results'][i]['genre_ids']) != 0:
			genreID_sum = 0
			for j in range(len(data['results'][i]['genre_ids'])):
				genreID_sum = genreID_sum + data['results'][i]['genre_ids'][j]
			
			if 	genreID_sum > 400:
				movie_num = movie_num + 1
				
		i = i+1
		
	if movie_num > 7 :
		return False
		
	else:
		return True	

"""
check palindrome
"""
def checkPalindrome(title):
	if (len(title) > 2):
		for i in range(len(title)/2):
			if title[i].upper() != title[len(title)-1-i].upper():
				return False
	
		return True
	
	else:
		return False

"""
SPL-005: There is at least one movie whose title has a palindrome in it
"""		
def checkMovieNamePalindrome(movie_name, count):
	
	data = getMovie(movie_name, count)
	total = len(data['results'])
	
	i = 0
	
	while i<total:
		
		titleWords = data['results'][i]['title'].split(" ")
		print titleWords
		for j in range(len(titleWords)):
			if checkPalindrome(titleWords[j]):
				return True
		
		i = i+1		
				
	return False
			
"""
SPL-006: There are at least two movies whose title contain the title of another movie
"""	
def checkMovieTitle(movie_name, count):

	data = getMovie(movie_name, count)
	total = len(data['results'])
	
	title = []
	num = 0
	
	for i in range(total):
		title.append(data['results'][i]['title'])
		
	title.sort(key=len)
	
	for i in range(total-1):
		for j in range(i+1, total):
			if num > 2:
				return True
			
			if title[i] in title[j]:
				num = num + 1
		
	return False


"""
Test SPL
"""
MovieName = 'batman'

#SPL-001 no 2 movie has same poster_path image
def testcheckPosterPathDup():	
	assert checkPosterPathDup(MovieName, 0) == True
	
	
#SPL-002 all poster_path link must be valid and null is acceptable 
def testcheckPosterPathValid():
	assert checkPosterPathValid(MovieName, 0) == True
	
#SPL-003 sorting rules 1 - genre_ids null movies are returned first
def testcheckSortingRule1():
	assert checkSortingRule1(MovieName, 0) == True
	
#SPL-003 sorting rules 2 part 1 - multiple genre_ids null movies are sorted by id
def testcheckSortingRule2_part1():
	assert checkSortingRule2_part1(MovieName, 0) == True

#SPL-003 sorting rules 2 part 2 - for genre_ids non-null, movies are sorted by id
def testcheckSortingRule2_part2():
	assert checkSortingRule2_part2(MovieName, 0) == True

#SPL-004: The number of movies whose sum of "genre_ids" > 400 should be no more than 7
def testcheckmovieGenreIDSum():
	assert checkmovieGenreIDSum(MovieName, 0) == True
	
#SPL-005: There is at least one movie in the database whose title has a palindrome in it
def testcheckMovieNamePalindrome():	
	assert checkMovieNamePalindrome(MovieName, 0) == True
	
#SPL-006: There are at least two movies whose title contain the title of another movie
def testcheckMovieTitle():	
	assert checkMovieTitle(MovieName, 0) == True
	
	
	
	
	
	