
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


from fluidhubcommon.WaresOperations import WaresOperations


################################################################################
################################################################################


class GitMailManager :

  def __init__(self,WareType,WareID) :
    self.Type = WareType
    self.ID = WareID

    WaresOps = WaresOperations()
    self.MailingList = WaresOps.getMailingList(WareType,WareID)


################################################################################


  def sendMail(self,Objects) :
  # TODO implement mail sender
    print "send mail to", self.MailingList

    for obj in Objects.read_objects():
      if obj.obj_type_num == 1: # Commit
        for c in obj.obj_chunks :
          print c
        #print obj
    pass
