class Machine:
    """Class to represent a virtual or local machine to contain the drives and the information"""

    def __init__(self):
        """Initializes the machine with space to add as much drives as we want"""
        self.drives = []

    def drive_error(self):
        """Prints common error when dealing with drives in a local or virtual machine"""
        print("Error. Drive name already in local or virtual machine")

    def not_drive(self):
        """Prints common error for drive not found in the local or virtual machine"""
        print("Error. Drive not found in local or virtual machine.")

    def activedrive_error(self):
        """Prints common error when dealing with drives in a local or virtual machine"""
        print("Error. Cannot remove the drive you are currently at.")
        print("Please, change your active drive using d - command and then delete it")

    def duplicate_drives(self, name):
        """
        Checks for duplicated drives in the local or virtual machine

        Input: STRING - Drive name
        Output: BOOL - Whether the drive with drive in input already exists in the machine
        """
        for e in self.drives:
            if e.name == name:
                self.drive_error()
                return True
        return False

    def add_drive(self, name):
        """
        Instantiates a Drive inside the machine

        Input: STRING - New drive name
        """
        if self.duplicate_drives(name) == False:
            self.drives.append(Drive(name, name))

    def search_drive(self, name):
        """
        Searches for a specifi drive in the machine

        Input: STRING - The name of the drive to be searched
        Output: BOOL
                Drive Object - The drive in the machine we were looking for. The machine itself otherwise."""
        for i in self.drives:
            if i.name == name:
                self = i
                return True, self
        return False, self

    def remove_drive(self, name):
        """
        Searches and removes a selected drive in place

        Input: STRING - The name of the drive to be deleted
        """
        if self.search_drive(name)[0] == True:
            self.drives.remove(self.search_drive(name)[1])
        else:
            self.not_drive()

    def display_drives(self):
        """Displays the drives currently active in the machine"""
        print("")
        print("Available Drives in Local Machine")
        print("")
        for d in self.drives:
            print(d.name, d.size, 'KB')
        print("")


class Drive(Machine):
    """
    Class to represent a memory drive of any type.
    Inherits from Class Machine
    The __init__ method states the attributes of the objects from this class
    """

    #
    def __init__(self, name, path, parent=None, size=0):
        self.name = name
        self.child = []
        self.path = path
        self.parent = parent
        self.size = size

    """
    The following error methods should be pretty self explanatory.
    Depending on the implementation raise excemptions can also be used.
    """

    def file_error(self):
        print("Error. File not found in directory.")

    def duplicate_error(self):
        print("Error. File already in directory.")

    def path_error(self):
        print("Error. Path not found.")

    def command_error(self, command):
        print("{} is not recognized as an internal command or text file.".format(command))

    """
    The following methods create text files, folders and zip files respectively.

    All of them follow a similar logic:
    1. Check for duplicates in the destination directory
    2. Instantiate the object and add to the destination directory
    3. Modify paths and sizes of the directories in the network of the new instance accordingly
    """

    def create_text(self, name, content):
        if self.duplicate(name) == False:
            file = Text(name, self.path + name, content, self)
            self.child.append(file)
            self.resize()

    def create_folder(self, name):
        if self.duplicate(name) == False:
            folder = Folder(name, self.path + name + '/', self)
            self.child.append(folder)
            self = folder
            return self
        else:
            return self

    def create_zip(self, name):
        if self.duplicate(name) == False:
            if self.existance(name[:-4])[0] == True:
                self.child.append(Zip(name, self.path + name, self, self.existance(name[:-4])[1]))
                self.resize()
            else:
                self.file_error()

    """
    Since they all of them were very recurent,
    the following methods were abstracted from other methods of the class to facilitate the design

    """

    def repath(self, path):
        """
        Given a path, changes the path of the calling object in place and all the objects contained in it.

        Input: STRING - New path to be modified for
        """
        if type(self) != Text and self.child == []:
            self.path = path + self.name + '/'
        elif type(self) == Text:
            self.path = path + self.name
        elif len(self.child) >= 1:
            self.path = path + self.name + '/'
            for e in self.child:
                # Recursively modifies the path of the children
                e.repath(self.path)

    def duplicate(self, name):
        """
        Revises whether a file already exists in a specific directory

        Input: STRING - Name of the file to check whether it is already in a specific directory
        """
        for e in self.child:
            if e.name == name:
                self.duplicate_error()
                return True
        return False

    def existance(self, name):
        """
        Revises whether a file actually exists in a specific directory

        Input: STRING - Name of the file to check whether it exists in a specific directory
        """
        for i in self.child:
            if i.name == name:
                self = i
                return True, self
        return False, self

    def resize(self):
        """
        Given an object in the file system, resizes in place the other in its netwrok after an action.
        First, sets the size of the object calling the method as zero.
        Then, adds the size of all the children of the object, if any and sets it as its new size.
        Proceeds similarly with the parent of the object and so on until the root.
        """
        # Modifies the size of all the directories after an action
        while self.parent != None:
            self.size = 0
            for e in self.child:
                self.size += e.size
            self = self.parent

        # Fetches the size of the drive after an action
        self.size = 0
        for e in self.child:
            self.size += e.size

    def delete(self, file_name):
        """
        Given the name of an object, this method deletes the file in place if it exists as a child of directory

        Input: STRING - The name of the file to be deleted
        """
        if self.existance(file_name)[0] == True:
            self.child.remove(self.existance(file_name)[1])
            self.resize()
        else:
            self.file_error()

    def openfile(self, file_name):
        """
        When a Text or Zip object is selected, returns the object selected.

        Input: STRING, the name of the file to open

        Output: TEXT or ZIP object, the object selected
        """
        exist, obj = self.existance(file_name)
        if exist == True and type(obj) == Text:
            print(obj.content)
            return obj
        elif exist == True and type(obj) == Zip:
            return obj
        else:
            return self.file_error()

    def unzip(self, file_name):
        """
        Method to return the content of a Zip file
        """
        if self.existance(file_name)[0] == True and type(self.existance(file_name)[1]) == Zip:
            self.delete(file_name)
            self.child.append(self.existance(file_name)[1])
            self.resize()
        else:
            self.file_error()

    def root(self):
        """
        Method to go from a directory to the root drive
        """
        while self.parent != None:
            self = self.parent
        return self

    def move(self, command, machine):
        """
        Method to move in place any file object to any drive and directory in the machine

        Input: STRING - The name of the file to move followed by a space and the destination path
                Machine object - The machine where all the drives and files are working
        """

        # Splits the command to obtain the name of the file to be moved and the destination path
        items = command.split()

        # Stores the drive and directories of the destination path as elements of a list
        new_path = items[2].split('/')[:-1]

        # Revises whether the file to be moved exists in the source path. Returns error otherwise
        if self.existance(items[1])[0] == True:
            moving_file = self.existance(items[1])[1]

            # Checks whether the destination path contains the same drive as in the source path
            # Changes the drive accordingly when required
            # The variable self_temp branches to the destination path starting by the destination drive
            # Try except block to handle the case when the drive does not exist
            # It aims to provide higher level justification in the errors made
            try:
                if self.root().name != new_path[0] + '/':
                    if machine.search_drive(new_path[0] + '/')[0] == True:
                        self_temp = machine.search_drive(new_path[0] + '/')[1]
                        exist_bool = True
                    else:
                        self.path_error()
                else:
                    self_temp = self.root()
                    exist_bool = True
            except:
                machine.not_drive()

            # Walks through the branched destination path checking the path is correct.
            # Returns path error otherwise
            for name in new_path[1:]:
                exist_bool, child_obj = self_temp.existance(name)
                if exist_bool == True and type(child_obj) == Folder or type(child_obj) == Drive:
                    self_temp = child_obj
                else:
                    self.path_error()
                    break

            # Revises whether the move would generate a duplicate in the destination directory
            # Assumes the path was correct from previous revisions
            # Adds a copy of the object to be moved to the new directory, deletes the original
            # Modifies attributes of the network
            # Try except block for the case when the drive was not found
            try:
                if self_temp.duplicate(moving_file.name) == False:
                    if exist_bool == True:
                        moving_file.repath(items[2])
                        moving_file.parent = self_temp
                        self_temp.child.append(moving_file)
                        self_temp.resize()
                        self.delete(moving_file.name)
                        self.resize()
                else:
                    self_temp.duplicate_error()
            except:
                pass

        else:
            self.file_error()


class Folder(Drive):
    """
    Class to represent a Folder file of any type
    Inherits from Class Drive
    The __init__ function uses polyphormism to override the method from the superclass Drive
    """

    def __init__(self, name, path, parent):
        super().__init__(name, path, parent)


class Zip(Drive):
    """
    Class to represent a Zip file of any type
    Inherits from Class Drive
    The __init__ function uses polyphormism to override the method from the superclass Drive
    """

    def __init__(self, name, path, parent, obj):
        super().__init__(name, path, parent)
        # The content of the Zip file is another folder or text file
        self.child.append(obj)
        # The size of a Zip file is half of its content, as required
        self.size = obj.size // 2


class Text(Folder, Zip):
    """
    Class to represent a Text file of any type
    In theory, inherits from Class Folder and Class Zip
    """

    def __init__(self, name, path, content, parent=None):
        self.name = name
        self.path = path
        self.content = content
        self.size = len(content)
        self.parent = parent

    def overwrite(self, new_content):
        """
        Replaces the content of the text file with the input of the function
        """
        self.content = new_content
        self.size = len(self.content)
        print(self.content)

    def add_text(self, more_content):
        """
        Given a string as an input, adds the input string to the text file
        """
        self.content += ' ' + more_content
        self.size = len(self.content)
        print(self.content)

    def text_error(self, command):
        print("{} is not recognized as an internal command in this text editor environment.".format(command))

    def text_editor(self):
        """
        Starts a text editor to use the functions previously stated and modify the content of the file
        """

        while True:

            command_txt = input()

            if command_txt[0:6] == 'write:':
                self.add_text(command_txt[6:])
            elif command_txt[0:10] == 'overwrite:':
                self.overwrite(command_txt[10:])
            elif command_txt[0:4] == 'help:':
                print('write: *text* --> Adds *text* to the current file')
                print('overwrite: *text* --> Erases the content of the file and adds *text*')
                print('exit --> Exits the text editor environment back to the file system interface')
            elif command_txt[0:4] == 'exit':
                # Modifies the size of the parent directories
                self.parent.resize()
                break
            else:
                self.text_error(command_txt)