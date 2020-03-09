from setup import *

# Instantiates
machine = Machine()
machine.add_drive('C:/')
machine.add_drive('F:/')
pointer = machine.drives[0]

################################################################
"""
SEE HELP COMMAND TO UNDERSTAND THE REST OF THE CODE
"""
################################################################


while True:

    command = input(str(pointer.path) + '>')

    if command[0:5] == 'mkdir':
        pointer = pointer.create_folder(command[6:])


    elif command[0:5] == 'mktxt':
        content = input()
        pointer.create_text(command[6:] + '.txt', content)


    elif command[0:3] == 'zip':
        pointer.create_zip(command[4:] + '.zip')


    elif command[0:5] == 'unzip':
        pointer.unzip(command[6:])


    elif command[0:3] == 'del':
        pointer.delete(command[4:])


    elif command[0:4] == 'move':
        pointer.move(command, machine)


    elif command == 'cd -':
        if pointer.parent != None:
            pointer = pointer.parent
        else:
            pointer.path_error


    # Shows the file chidlren of a specific directory
    elif command[0:3] == 'dir':
        for e in pointer.child:
            print("")
            print(e.name, type(e), e.size, 'KB')


    elif command == 'cd /':
        pointer = pointer.root()


    elif command[0:2] == 'cd':
        if pointer.existance(command[3:])[0] == True:
            pointer = pointer.existance(command[3:])[1]
        else:
            pointer.file_error()


    elif command[0:3] == 'd -':
        dri = command[4:]
        if machine.search_drive(command[4:])[0] == True:
            pointer = machine.search_drive(command[4:])[1]
        else:
            machine.not_drive()


    elif command[0:6] == 'drives':
        machine.display_drives()


    elif command[0:7] == 'mkdrive':
        machine.add_drive(command[8:])


    elif command[0:11] == 'removedrive':
        if pointer.root().name == command[12:]:
            pointer.activedrive_error()
        else:
            machine.remove_drive(command[12:])

    # Exits the File System CMD
    elif command == 'quit':
        break


    # Provides the list of available commands
    elif command[0:6] == "help":
        print("")
        print("Available Commands")
        print("")
        print("mkdir *name* : ", "Creates new folder/directory with name *name*")
        print("mktxt *name* : ", "Creates new text file with name *name*")
        print("del *name* : ", "Deletes file in current directory with name *name*")
        print("move *name* *path* :", "Moves file in current directory with name *name* to path *path*")
        print("cd - : ", "Go back one directory. Limited to the current drive")
        print("cd *name* : ", "Changes the current directory to a directory named *name* inside the current directory")
        print("cd / : ", "Goes back to current directory")
        print("quit : Finishes Kernel Session")
        print("d - *name* : ", "Changes drive among available drives in the local or virtual machine")
        print("drives : ", "Displays available drives in the local machine")
        print("mkdrive *name*: ", "Creates a drive in the local or virtual machine with name *name*")
        print("zip *name* : ", "Creates a zip file with name *name* out of the directory named *name*")
        print("unzip *name* : ", "Unzip the file *name*")


    # Enters the file text editor
    elif command[-4:] == '.txt':
        if pointer.existance(command)[0] == True:
            text = pointer.openfile(command)
            text.text_editor()
        else:
            pointer.command_error(command)

    # Triggers access to a Zip File
    elif command[-4:] == '.zip':
        if pointer.existance(command)[0] == True:
            pointer = pointer.openfile(command)
        else:
            pointer.command_error(command)


    else:
        # Returns error when no command is recognized
        pointer.command_error(command)