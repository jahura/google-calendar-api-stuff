#This file find json file according to the giving path return the file name
import subprocess as sp

def analyzeOutput(output):
    print output
    start,end=-1,-1
    for i in range(len(output)):
        if output[i]=='\'':
            if start==-1:
                start=i
            else:
                end=i
                break
    return output[start+1:end].split("\\n")[:-1]

#Get the json file from directory
def getFile(path):
    if path=="":
        path="."
    length=len(path)
    if length>5 and path[length-5:length]==".json":
        return path
    commandLine="cd "+path+"; ls *.json"
    '''
    # python 3
    output=sp.getoutput(commandLine)
    fileList=str(output).split("\n")
    '''
    
    #python 2
    currentDir=sp.check_output(["pwd"],shell=True)
    output=sp.check_output([commandLine],shell=True)
    sp.call(["cd "+currentDir],shell=True)
    fileList=str(output).split("\n")

    if fileList==[]:
        raise Exception("No files found")
    print fileList[0]
    return path+"/"+fileList[0]

#print(getFiles("json/set")) #debug only
#print(getFiles("json/cancel")) #debug only
#print(getFiles("json/rescdule")) #debug only
