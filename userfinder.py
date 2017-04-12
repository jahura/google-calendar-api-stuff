import subprocess as sp

#Get jsons file collected from the output on the command line
def analyzeOutput(output):
    start,end=-1,-1
    for i in range(len(output)):
        if output[i]=='\'':
            if start==-1:
                start=i
            else:
                end=i
                break
    return output[start+1:end].split("\\n")[:-1]

#Get user ID based on the selected json file name
def getSelectedUserId(jsonFile):
    for i in range(len(jsonFile)-1,-1,-1):
        if jsonFile[i]=='.':
            return jsonFile[:i]

#Get user ID from the path directory
def getUserID(path):

    #if path is empty string then get current directory
    if path=="":
        path="."

    #Create shell command to get all the json files at specified directory
    #choose variable holds which json file to choose
    commandLine,choose="cd "+path+" ;ls *.json",1

    #Get output of the command and analyze it to get a list of json files' name
    output=sp.check_output([commandLine],shell=True)
    jsonFiles=analyzeOutput(str(output))

    if jsonFiles==[]: #Return empty string if no json files found
        print("No json files found")
        return ""
    elif len(jsonFiles)>1: #Selected one json file if there are many of them
        print("Multiple json files found:")
        count=1
        for i in jsonFiles:
            print(count,".",i)
            count+=1
        while True:
            try:
                choose=int(input("Enter the number of the json file you want to run: "))
                if choose>len(jsonFiles) or choose<0:
                    print("Invalid input")
                else:
                    break
            except Exception:
                print("Invalid input")
    #Return the user ID get from selected json file
    return getSelectedUserId(jsonFiles[choose-1])

print("User selected: ",getUserID("json")) #debug-only
