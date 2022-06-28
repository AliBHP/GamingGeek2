# Name: Error reporting class ( err )
# Main Job: This claass should be called whenever you want to read or write to the database
#
# Author: Ali Albahrani
# Craated Date: 30 March 2021
# Version: 1.0.0
# Class ID: 0000

# Class Usage
#   Use for reporting errors in the applicion.

# Error code number, each class in the project should have a unique number that will be used to locate the error.
    # This number should be a 4 digit number, make sure each class has that number
class ausError:

    err_ErrorCode:int = ""
    # Short error name the idntify it.
    err_ErrorName:str = ""
    # The error description and user help
    err_ErrorHelp:str = ""

    # Extra Infor
    err_ExtraInfo = ""

    # Initit an error object
    def __init__(self, ErrorCode:int, ErrorName:str, ErrorHelp:str):
        self.err_ErrorCode = ErrorCode
        self.err_ErrorName = ErrorName
        self.err_ErrorHelp = ErrorHelp

    def func_PrintError(self):
        print("Error #" + str(self.err_ErrorCode) + ":", \
              self.err_ErrorName, "\n" , self.err_ErrorHelp )

    def func_WebPageErrorShow(self):
        print("HTML")