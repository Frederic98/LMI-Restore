
#-----CreateTable.py-----#
#Function is used to create a Table within the database
def db_CreateTable(db):
	#db, connection to the database
	db.cursor().execute('CREATE TABLE storage (box INT, row INT, column INT)')
	print 'Table Created.'
	#Usually this function is only used ones for each database


#-----GenDB.py-----#
#Function used to fill the database with zeros
def GenDB(db, row, column):
	#db, connection to the database
	#row, defines the amount of rows in the database
	#column, defines the amount of columns in the database	
	for x in range(1, row+1):	#for loop through the amount of rows
		for i in range(1, column+1):	#for each row, for loop through the amount of columns
			db_Insert(db, 0, x, i)		#for each column in each row add zero on position (row, column)


#-----GetAll.py-----#
#Function used to print all data in database
def db_GetAll(db):
	#db, connection to the database
	c = db.cursor()		#c is used because the for loop wouldnt work otherwise
	c.execute('SELECT * FROM storage')
	for row in c:		#for loop through the results of the database function
		print(row)		#print each returned value
	#print ""


#-----Insert.py-----#
#Function used to add line in database
def db_Insert(db, data, row, column):
	#db, connection to the database
	#data, the box number which will be added
	#row, row location of the box
	#column, column location of the box
	print "Insert"
	db.cursor().execute('INSERT INTO storage VALUES('+str(data)+','+str(row)+','+str(column)+')')
	db.commit() #Saves the changes in the database


#-----SearchBox.py-----#
#Search in the data base for a specific box
def db_SearchBox(db, data):
	#db, connection to the database
	#data, number of the box that needs to be found
	c = db.cursor()	
	c.execute("SELECT row, column FROM storage WHERE box = '" + str(data) + "'")
	for x in c: #for loop through the results of the database function
		return x #Returns the first found location


#-----Update.py-----#
#Update a position in the database, searching by a box name
#After finding the box by its name change the name in 0
def db_UpdateByBox(db, box):
	#db, connection to the database
	#box, name of the box that needs to be changed to 0
	db.cursor().execute("UPDATE storage SET box = 0 WHERE box = '" + str(box) + "'")
	db.commit()


#Update a position in the database, searching the row and colomn values
#After finding the position matching the row and column value change the box name to the given box
def db_UpdateByCoor(db, data, row, column):
	#db, connection to the database
	#data, new name of the box at position [row,column]
	#row, used to search for matching positions
	#column, used to search for matching positions	
	db.cursor().execute("UPDATE storage SET box = '" + str(data) + "' WHERE row = '" + str(row) + "' AND column = '" + str(column) + "'")
	db.commit()	


#Function used to add a box to the database
def AddBox(db, data):
	#db, connection to the database
	#data, name of the box to add to the database

	val = {'row': 0, 'column': 0, 'message': "", 'error': 0}	#define val to return
	
	check = db_SearchBox(db, data)	#check if the box is already in the storage
	if(str(check) != 'None'):	#if box is already in storage return error message
		val["message"] = "Box "+str(data)+" is already in storage"
		val["error"] = 1
		return val
	
	coor = db_SearchBox(db, 0)	#search for first empty position
	db_UpdateByCoor(db, data, coor[0], coor[1])	#call the "UpdateByCoor" function to add the box to the storage
	
	#return val to confirm the box is added to database
	val["message"] = "Box "+str(data)+" has been added to the storage at row "+str(coor[0])+" column "+str(coor[1])
	val["row"] = coor[0]
	val["column"] = coor[1]
	return val
	

#Function used to delete box from the database
def DeleteBox(db, data):
	#db, connection to the database
	#data, name of the box to delete from the database

	val = {'row': 0, 'column': 0, 'message': "", 'error': 0}	#define val to return
	
	check = db_SearchBox(db, data)	#check if the box is already in the storage
	if(str(check) == 'None'):	#if box is not in storage return error message
		val["message"] = "Box "+str(data)+" is not in storage"
		val["error"] = 1
		return val

	db_UpdateByBox(db, data)	#call the "UpdateByBox" function to delete the box from the storage
	
	#return val to confirm the box is delteted from the database
	val["message"] = "Box "+str(data)+" is removed from the storage"
	val["row"] = check[0]
	val["column"] = check[1]
	return val



















