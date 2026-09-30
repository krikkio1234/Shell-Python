import sys
import os
import subprocess

#handler -> è un boss di una classe che richiama tutte le funzioni 

class Parse:
#echo hello world
    def parse(self, commandUser):
        flag = ""
        saveCommandShell = []
        for char in commandUser:
            if char != " ":
                flag += char
            elif char == " ":
                saveCommandShell.append(flag) 
                flag = ""
        if flag != "": saveCommandShell.append(flag)
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
        print(f"{self.commandUser}: command not found", end="")

    def exitCommand(self) -> bool:
        if self.commandUser == "exit": return False
        else: return True

    #print(f"{commandUser}: not found", end="")
    def typeCommand(self, commandUser):
        if commandUser in self.commandShell.keys(): 
            print(f"{commandUser} is a shell builtin", end="")
            return 
        executableFile = self.searchExecuteFiles(commandUser)
        if executableFile == None:
            print(f"{commandUser}: not found", end="")
            return

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
        print(os.getcwd(), end="")

    def cdCommand(self, commandUser):
        if os.path.isdir(commandUser): os.chdir(commandUser)
        else: print(f"cd: {commandUser}: No such file or directory")

def main(baseCommand : BaseCommands):
    loop = True
    while loop:
        sys.stdout.write("$ ")  
        parsed = baseCommand.parse.parse(baseCommand.userInput())
        loop = baseCommand.exitCommand()
        if parsed[0] in baseCommand.commandShell:
            #print("prova")
            if (len(parsed)) == 1:
                recovery = baseCommand.commandShell.get(parsed[0])
                recovery()
            else:    
                recovery = baseCommand.commandShell.get(parsed[0])
                for i in range (1, len(parsed)):
                    recovery(parsed[i])
        else:
            if baseCommand.searchExecuteFiles(parsed[0]) == None: baseCommand.cannotFoundCommand()
            else: 
                subprocess.run([baseCommand.searchExecuteFiles(parsed[0]), *parsed[1:]])
        print()

if __name__ == "__main__":
    baseCommands = BaseCommands(Parse())
    main(baseCommands)