# Big Project for 2022 DATA REPRESENTATION Course

## Decrription

This is a submission for the final project for Data Representation Course ran at Atlantic TU in Autumn 2022. 

## To Run this project:

1. Create a `config.py` file in the main folder with 2 dictionary objects in the following format:

```
musicMatch = {
    "apiKey" : "XXXXXXXXXXXXXXXXXXXXXXXX"
}

mysqlConfig={
    "database": "project",
    "host":"XXXX", 
    "user":"XXXXX", 
    "password":"XXXXX"    
}
```

2. To get the ApiKEy for MusixMatch service: signup on https://developer.musixmatch.com/ to get a free apiKey.
3. Run 'prepareDB.py' script to create a 'project' database and required tables ('user' and 'favorites') on your MySQL server.
4. Project hosted on Project hosted on http://pbil.pythonanywhere.com