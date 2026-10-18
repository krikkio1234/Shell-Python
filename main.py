import sys
import os
import subprocess

#handler -> è un boss di una classe che richiama tutte le funzioni 

class Parse:
    def parse(self, commandUser):
        insideQuotes = None
        flag = ""
        saveCommandShell = []
        for i, char in enumerate(commandUser):
            #echo "example\"insidequotes"shell\"
            #Expected: example"insidequotesshell"
            #Received: example"insidequotesshell
            if i + 1 > len(commandUser):
                continue
            if char == "\\" and commandUser[i - 1] != "\\":
                continue
            if commandUser[i - 1] == "\\" and insideQuotes:
                flag += char
                continue
            if commandUser[i - 1] == "\\" and not insideQuotes:
                flag += char
                continue
            if char == "'" and insideQuotes == '"':        
                flag += char
                continue
            if char == '"' and insideQuotes  == "'":
                flag += char
                continue
            if char == "'" or char == '"':
                if char == insideQuotes:
                    insideQuotes = None
                    continue
                insideQuotes = char
                continue
            if char != " ": 
                flag += char
                continue
            if char == " " and insideQuotes:
                flag += char
                continue          
            if flag and char == " ":
                saveCommandShell.append(flag) 
                flag = ""
        if flag != "": saveCommandShell.append(flag)
        #print(saveCommandShell)
        return saveCommandShell

class BaseCommands:
    def __init__(self, parse : Parse):
        self.parse = parse
        self.commandShell = {
            "echo" : self.echoCommand,
            "exit" : self.exitCommand,
            "type" : self.typeCommand,
            "pwd" : self.pwdCommand,
            "cd" : self.cdCommand
        }

    def userInput(self):
        self.commandUser = input()
        return self.commandUser

    def echoCommand(self, commandUser):
        print(commandUser, end=" ")

    def cannotFoundCommand(self):
        print(f"{self.commandUser}: command not found")

    def exitCommand(self) -> bool:
        if self.commandUser == "exit": return False
        else: return True

    def typeCommand(self, commandUser):
        if commandUser in self.commandShell.keys(): 
            print(f"{commandUser} is a shell builtin")
            return 
        executableFile = self.searchExecuteFiles(commandUser)
        if executableFile == None:
            print(f"{commandUser}: not found")
            return
        print(f"{commandUser} is {executableFile}")

    def searchExecuteFiles(self, commandUser):
        fullPath = os.getenv("PATH")
        pathWindows = list(fullPath.split(os.pathsep))
        executableFile = False
        for i in pathWindows:
            compleatePath = os.path.join(i, commandUser)
            if os.path.exists(compleatePath):
                if os.access(compleatePath, os.X_OK):
                    namePath = compleatePath
                    executableFile = True
                    break
        if executableFile: return namePath
        return None

    def pwdCommand(self):
        print(os.getcwd())

    def cdCommand(self, commandUser):
        if commandUser != "~":
            if os.path.isdir(commandUser): os.chdir(commandUser)
            else: print(f"cd: {commandUser}: No such file or directory")
        else:
            os.chdir(os.path.expanduser("~"))

def main(baseCommand : BaseCommands):
    loop = True
    while loop:
        sys.stdout.write("$ ")  
        sys.stdout.flush()
        parsed = baseCommand.parse.parse(baseCommand.userInput())
        loop = baseCommand.exitCommand()
        cmd = parsed[0]
        if cmd in baseCommand.commandShell:
            if parsed[0] == "echo":
                separator = " "
                base = separator.join(parsed[1:])
                print(base)
                continue
            if (len(parsed)) == 1:
                recovery = baseCommand.commandShell.get(cmd)
                recovery()
            else:    
                recovery = baseCommand.commandShell.get(cmd)
                for i in range (1, len(parsed)):
                    recovery(parsed[i])
        else:
            if baseCommand.searchExecuteFiles(cmd) is None: 
                baseCommand.cannotFoundCommand()
            else: 
                executablePath = baseCommand.searchExecuteFiles(cmd) 
                subprocess.run([cmd, *parsed[1:]], executable=executablePath)
                continue

if __name__ == "__main__":
    baseCommands = BaseCommands(Parse())
    main(baseCommands)