import pickle
import os

class Database:
    # DB is an array of dictionaries
    db = []
    
    def __init__(self):
        if os.path.exists('db.pickle'):
            with open('db.pickle', 'rb') as database:
                self.db = pickle.load(database)
        else:
            with open('db.pickle', 'wb') as database:
                pickle.dump(self.db, database)

    def saveToDB(self):
        with open('db.pickle', 'wb') as database:
            pickle.dump(self.db, database)
    
    def updateDB(self, name, email):
        isPresent, index = self.checkSameDB(name)
        if isPresent:
            self.db[index]['email'] = email
        else:
            row = {
                'name' : name,
                'email' : email
            }
            self.db.append(row)
        self.saveToDB()
    
    def printRowsDB(self):
        for row in self.db:
            print(row)

    def checkSameDB(self, name):
        count = 0
        for row in self.db:
            if row.get('name') == name:
                return True, count
            count = 0
        return False, None

    def deleteRowDB(self, name):
        isPresent, index = self.checkSameDB(name)
        if isPresent:
            del self.db[index]
            self.saveToDB()
            return True
        return False

    def dropDB(self):
        os.remove('db.pickle')
        self.db = []
        with open('db.pickle', 'wb') as database:
            pickle.dump(self.db, database)
    
    def getEmail(self, name):
        isPresent, index = self.checkSameDB(name)
        if isPresent:
            return self.db[index].get('name'),isPresent
        return None,False
    
    def getEmailfromPartialName(self, word):
        for row in self.db:
            name = row.get('name')
            if word in name:
                return row.get('email'), True
        return None, False
    
    def getNameFromEmail(self, email):
        for row in self.db:
            em = row.get('email')
            if email == em:
                return row.get('name'),True
        return None,False