from projectDAO import userDAO, favoritesDAO

latestid = userDAO.create('Derek')

result = userDAO.findByID(latestid)

print("Test create and find by id")
print(result)

#update
userDAO.update('Fred', latestid)
result = userDAO.findByID(latestid)
print("Test update and find by id")
print(result)

#getall
print("Test of GetAll()")
allStudents = userDAO.getAll()
for student in allStudents:
    print(student)

#delete
userDAO.delete(latestid)


latestid = favoritesDAO.create(1, 3456)
latestid = favoritesDAO.create(1, 3156)
latestid = favoritesDAO.create(1, 39056)
latestid = favoritesDAO.create(1, 598)

latestid = favoritesDAO.create(10, 3456)
latestid = favoritesDAO.create(10, 3156)
latestid = favoritesDAO.create(10, 39056)
latestid = favoritesDAO.create(10, 598)

# Find user favorites
result = favoritesDAO.getFavoritesByUserID(10)
print("Test create and find favorites by iuser_d")
print(result)


#delete
userDAO.delete(latestid)