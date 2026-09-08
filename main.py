import sys
import os
import subprocess

def main():
    sys.stdout.write("$ ")
    pass

commandShell = {"exit", "type", "echo", "pwd", "cd"}
path = os.environ.get("PATH")
directory = path.split(os.pathsep)

exit = False
while not exit:
    if __name__ == "__main__":
        main()


    #echo 'hello    world'
    #echo 'hello world'

    command = input()
    commandPart = []
    current = ""
    insideQuotes = False

    for i in range(len(command)):
        if command[i] == "'":
            insideQuotes = not insideQuotes
        elif command[i] == " " and not insideQuotes:
            if current:
                commandPart.append(current)
                current = ""
        else:
            current += command[i]
    if current:
        commandPart.append(current)

    if commandPart[0] == "echo":
        for i in range(1, len(commandPart)):
            print(commandPart[i], end=" ")
        print()
    if command == "exit":
        exit = True
    if commandPart[0] == "type" and commandPart[1] in commandShell:
        print(f"{commandPart[1]} is a shell builtin")
    if commandPart[0] == "type" and commandPart[1] not in commandShell:
        find = False
        for i in directory:
            fullPath = os.path.join(i, commandPart[1]) #unione comandi
            if os.path.exists(fullPath): #controllo esistenza
                if os.access(fullPath, os.X_OK): #controllo execute
                    print(f"{commandPart[1]} is {fullPath}")
                    find = True
                    break
        if not find:
            print(f"{commandPart[1]}: not found")
    if commandPart[0] not in commandShell:
        find = False
        count = 0
        for i in directory:
            fullPath = os.path.join(i, commandPart[0])
            if os.path.exists(fullPath):
                if os.access(fullPath, os.EX_OK):                  
                    find = True
                    break
        if find:
            subprocess.run(commandPart, executable=fullPath)
    if commandPart[0] not in commandShell and not find:
        print(f"{command}: command not found")
    if commandPart[0] == "pwd":
        print(os.getcwd())
    if commandPart[0] == "cd":
        if commandPart[1] == "~":
            home = os.environ.get("HOME")
            os.chdir(home)
            continue
        if os.path.exists(commandPart[1]):
            os.chdir(commandPart[1])
        else:
            print(f"cd: {commandPart[1]}: No such file or directory")