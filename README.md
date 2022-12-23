# Big Project for 2022 DATA REPRESENTATION Course

## Description

This is the final project for the Data Representation Course offered at Atlantic Technical University during the Winter 22/23 Semester. 

The project entailed the development of a web application that allows users to create and manage their own profiles, categorizing their favorite music albums in the process. 

Through the use of the Musixmatch service, users are able to search for and add new albums to their profiles, as well as edit and remove both their profiles and favorite albums as desired. Overall, the goal of this project was to create a user-friendly platform for organizing and accessing music collections, and I hope that it will prove to be a useful and enjoyable tool for the users.

## To Run this project.

Please follow the following steps:

1. Create a config.py file in the main folder and include the following dictionary objects:

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

2. Obtain an API key for the MusixMatch service by signing up at https://developer.musixmatch.com/ to get a free apiKey.
3. Run the prepareDB.py script to create the necessary project database and tables (user and favorites) on your MySQL server.
4. The project can be accessed at http://pbil.pythonanywhere.com