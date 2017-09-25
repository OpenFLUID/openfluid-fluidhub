
__license__ = "AGPLv3"
__author__ = "Jean-Christophe Fabre <jean-christophe.fabre@inra.fr>"


import os
import subprocess
import re
import json
import shutil

from FluidHub.GitInfosReader import GitInfosReader
from FluidHub import Tools


################################################################################
################################################################################


class GitInfosWriter(GitInfosReader) :

  def __init__(self,WareType,WareID,WareGitPath) :
    GitInfosReader.__init__(self,WareType,WareID,WareGitPath)


################################################################################


  def getBranchesList(self):

    P = subprocess.Popen(["git","for-each-ref","--format=%(refname:short)","refs/heads"],
                         stdout=subprocess.PIPE,cwd=self.WarePath)
    StdOut,StdErr = P.communicate()
    Branches = StdOut.splitlines()
    return Branches


################################################################################


  def generateCommitsHistoryFiles(self,BranchName):

    Tools.makedirs(self.getGitBranchPath(BranchName))

    P = subprocess.Popen(["git","log","--format=%H:::%an:::%ae:::%ad:::%s",BranchName],
                        stdout=subprocess.PIPE,cwd=self.WarePath)
    StdOut,StdErr = P.communicate()

    CommitsLines = StdOut.splitlines()

    CommitsFile = open(self.getGitBranchHistoryFile(BranchName),"w")
    FirstLine = True

    CommitsFile.write("{")

    for Line in CommitsLines:
      Infos = Line.split(":::")
      if len(Infos) == 5 :
        if not FirstLine :
          CommitsFile.write(",")
        CommitsFile.write("\n")
        CommitsFile.write("  \"%s\" : {\n" % Infos[0])
        CommitsFile.write("    \"authorname\" : \"%s\",\n" % Infos[1])
        CommitsFile.write("    \"authoremail\" : \"%s\",\n" % Infos[2])
        CommitsFile.write("    \"date\" : \"%s\",\n" % Infos[3])
        CommitsFile.write("    \"subject\" : \"%s\"\n" % Infos[4].replace("\"","\\\""))
        CommitsFile.write("  }")
        FirstLine = False

    CommitsFile.write("\n}\n")
    CommitsFile.close()


################################################################################


  def extractBranchFile(self,BranchName,FileName):

    Output = ""
    try :
      P = subprocess.Popen(["git","show",BranchName+":"+FileName],stdout=subprocess.PIPE,cwd=self.WarePath)
      StdOut,StdErr = P.communicate()
      ExtractedFile = open(os.path.join(self.WaresHubDataPath,BranchName,FileName),"w")
      ExtractedFile.write(StdOut)
      ExtractedFile.close()
    except :
      pass


################################################################################


  def findHigherBranch(self,BranchesList):

    ValidBranches = []

    for Branch in BranchesList:
      ValidFound = re.match("openfluid-(\d+\.\d+(\.\d+)*)$",Branch)
      if ValidFound:
        ValidBranches.append(Branch)

    if not ValidBranches :
      return ""

    return max(ValidBranches)


################################################################################


  def generateGitStatsFile(self,BranchesList):

    GitStatsFile = open(self.getGitStatsFile(),"w")

    # branches

    GitStatsFile.write("{\n  \"branches\" : [")

    FirstLine = True

    for Branch in BranchesList :
      if not FirstLine :
        GitStatsFile.write(",")
      GitStatsFile.write("\n")
      GitStatsFile.write("    \"%s\"" % Branch)
      FirstLine = False

    GitStatsFile.write("\n  ],\n")


    # commiters stats

    P = subprocess.Popen(["git","shortlog","-s","-n","-e","-w0","--all"],stdout=subprocess.PIPE,cwd=self.WarePath)
    StdOut,StdErr = P.communicate()
    CommitersLines = StdOut.splitlines()

    GitStatsFile.write("  \"committers\" : {")

    FirstLine = True

    for Line in CommitersLines :
      Commiter = Line.split("\t")

      if len(Commiter) == 2 :
        Count = Commiter[0].strip()

        NameEmail = Commiter[1].strip().split("<")
        Name = NameEmail[0].strip()
        Email = NameEmail[1].replace('>','')

        if not FirstLine :
          GitStatsFile.write(",")
        GitStatsFile.write("\n")

        GitStatsFile.write("    \"%s\" : {\n" % Name)
        GitStatsFile.write("      \"email\" : \"%s\",\n" % Email)
        GitStatsFile.write("      \"count\" : \"%s\"\n" % Count)
        GitStatsFile.write("    }")

        FirstLine = False

    GitStatsFile.write("\n  },\n")


    # open-issues stats

    OpenIssues = dict()
    OpenIssues["bug"] = 0;
    OpenIssues["feature"] = 0;
    OpenIssues["review"] = 0;

    DefaultBranch = self.findHigherBranch(BranchesList)
    WHFilePath = os.path.join(self.WarePath,DefaultBranch,"wareshub.json")

    if (os.path.isfile(WHFilePath)):
      try:
        WHFileContent=open(WHFilePath)
        WHFileJSON = json.load(WHFileContent)

        if "issues" in WHFileJSON.keys():
          for IssueID, IssueInfos in WHInfosManFileJSON["issues"].iteritems():
            IssueInfosList = IssueInfos.keys()
            if "state" not in IssueInfosList or IssueInfos["state"] != "closed":
              if "type" in IssueInfosList:
                OpenIssues[IssueInfos["type"]] += 1

      except ValueError:
        pass

    GitStatsFile.write("  \"open-issues\" : {\n")
    GitStatsFile.write("    \"bug\" : \"%s\",\n" % OpenIssues["bug"])
    GitStatsFile.write("    \"feature\" :\"%s\",\n" % OpenIssues["feature"])
    GitStatsFile.write("    \"review\" : \"%s\"\n" % OpenIssues["review"])
    GitStatsFile.write("  }\n")


    GitStatsFile.write("}\n")


################################################################################


  def setDefaultBranch(self,BranchesList):

    DefaultBranch = self.findHigherBranch(BranchesList)

    P = subprocess.Popen(["git","symbolic-ref","-q","HEAD","refs/heads/"+DefaultBranch],cwd=self.WarePath)
    P.wait()


################################################################################


  def rebuildInfos(self) :

    shutil.rmtree(self.WaresHubDataPath,ignore_errors=True)
    Tools.makedirs(self.WaresHubDataPath)

    Branches = self.getBranchesList()

    for Branch in Branches :
      self.generateCommitsHistoryFiles(Branch)
      self.extractBranchFile(Branch,"wareshub.json")
      self.extractBranchFile(Branch,"README")
      self.extractBranchFile(Branch,"README.md")
      self.extractBranchFile(Branch,"LICENSE")
      self.extractBranchFile(Branch,"COPYING")

      self.generateGitStatsFile(Branches)

      self.setDefaultBranch(Branches)
