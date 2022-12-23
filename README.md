# Big Project for 2022 DATA REPRESENTATION Course

To Run this project:
1. Create a 'config.py' file in the main folder with 2 dictionary objects in the following format:
musicMatch = {
    "apiKey" : "XXXXXXXXXXXXXXXXXXXXXXXX"
}

mysqlConfig={
    "database": "project",
    "host":"XXXX", 
    "user":"XXXXX", 
    "password":"XXXXX"    
}

2. Run 'prepareDB.py' script to create a 'project' database and required tables ('user' and 'favorites') on your MySQL server.
3. Signup on 'https://developer.musixmatch.com/' to get a free apiKey
4. Add the apiKey to musicMatch Distonary object in 'config.py'
5. Project hosted on Project hosted on http://pbil.pythonanywhere.com