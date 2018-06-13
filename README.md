# Splunk Movie API project
##**Environment setup:**

* need python 2.7 (run $ python --version)
* need requests, pytest packages
* to check if pytest, requests are installed
	* $ pip list 
* to install pytest, requests packages
	* $ pip install pytest
	* $ pip install requests




##**Test structures:**
* all test cases and scripts are located under Splunk/python directory
	* testGet.py is testing all the functionalities for Get API
	* testPost.py is testing all the functionalities for Post API
	* testSPL.py is testing all the requirements in Business requirements
	* movieAPITest_script.sh is the shell scripts to run all above tests together

* all documentations are under splunk/documents directory
	* get_rsp.txt is a sample Get API response
	* TestUseCases.docx contains the test plan and the details about test cases
	* BugList.xlsx contains the list of the bugs
	* test_run_Results.txt contains the Terminal run result for all the test cases

	


##**Test case run steps:**
* run python test by category under Splunk/python
	* $ pytest testGet.py -v
 	* $ pytest testPost.py -v
 	* $ pytest testSPL.py -v
 
* run shell script to run all the test cases under Splunk/python
 	* $ ./movieAPITest_script.sh
 
* setup daily test shell script run at 22:00pm in crontab under Splunk/python and stdout will be saved in run_results.log
	* $ crontab -e to edit crontab 
 	* add following line: 00 22 * * * movieAPITest_script.sh > run_results.log
 	*  save the file
	
* or setup daily test shell script CI run in Fusion or any related tools when there are any code chages checkin
