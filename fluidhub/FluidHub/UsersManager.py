
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from sqlalchemy import create_engine, MetaData, Table
import bcrypt

from FluidHub import Tools


################################################################################
################################################################################


class UsersManager :

  def __init__(self,DBURI) :
    self.Engine = create_engine(DBURI, convert_unicode=True)
    self.Metadata = MetaData(bind=self.Engine)
    self.Users = Table('users', self.Metadata, autoload=True)


################################################################################


  def __comparePasswordToHash(self,Password,StoredHash):
    return bcrypt.checkpw(Password.encode('utf8'), StoredHash.encode('utf8'))


################################################################################


  def authenticateUser(self, Username, Password) :
    if not Username or not Password:
      return False

    Results = self.Users.select(self.Users.c.username == Username).execute().first()

    if Results is None:
      return False

    return self.__comparePasswordToHash(Password,Results['password'])


################################################################################


  def getUsers(self) :
    UsersList = []

    Results = self.Users.select().execute()

    for Row in Results:
      UsersList.append(Row['username'])

    return 200,UsersList


################################################################################


  def getUser(self,Username) :
    UserInfo = dict()

    Results = self.Users.select(self.Users.c.username == Username).execute().first()

    if Results is None:
      return 404,""
    else:
      UserInfo = {
                   "username" : Results['username'],
                   "fullname" : Results['fullname'],
                   "email" : Results['email']
                 }

    return 200,Tools.noneToEmptyString(UserInfo)


################################################################################


  def createUser(self, Username, Definition) :
    # check valid chars for username (A-Z,a-z,0-9,.,_, must start with an alphabetic char)
    if not Tools.isValidUsername(Username):
      return 400,"invalid username format"

    # check if provided json data is correct
    if not all(name in Definition for name in ("username","password")) :
      return 400,"invalid data provided"

    if Definition["username"] != Username :
      return 400,"username mismatch with provided data"

    if "email" not in Definition.keys() :
      Definition["email"] = ""
    elif not Tools.isValidEmail(Definition["email"]):
      return 400,"invalid email format"

    if "fullname" not in Definition.keys() :
      Definition["fullname"] = ""

    Code, Res = self.getUser(Username)
    if Code == 200 :
      return 409,"already exists"

    Salt = bcrypt.gensalt()
    HashedPassword = bcrypt.hashpw(Definition["password"].encode('utf8'), Salt)

    UserData = Definition
    UserData["password"] = HashedPassword

    Result = self.Users.insert(Definition).execute()

    if Result.rowcount == 1:
      return 201,""

    return 500,""


################################################################################


  def updateUser(self, Username, Definition) :

    if "fullname" in Definition:
      self.Users.update().where(self.Users.c.username == Username).values(fullname=Definition["fullname"]).execute()

    if "email" in Definition:
      self.Users.update().where(self.Users.c.username == Username).values(email=Definition["email"]).execute()

    return 200,""


################################################################################


  def deleteUser(self, Username) :

    Code, Res = self.getUser(Username)
    if Code != 200 :
      return 404,""

    Result =  self.Users.delete(self.Users.c.username == Username).execute()

    if Result.rowcount == 1:
      return 200,""

    return 500,""


################################################################################


  def changePassword(self, Username, NewPassword) :

    Salt = bcrypt.gensalt()
    HashedPassword = bcrypt.hashpw(NewPassword.encode('utf8'), Salt)

    self.Users.update().where(self.Users.c.username == Username).values(password=HashedPassword).execute()

    return 200,""


################################################################################


  @staticmethod
  def isAdmin(Username) :
    return Username == "admin"



################################################################################
################################################################################


UsersMan = UsersManager('sqlite:////data/common/users.db')
