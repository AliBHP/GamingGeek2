from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from . import DatabaseControler as dbClass
from .ErrorReporting import ausError as ERR
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage

############################################################################################
#####     Navigation Methods
############################################################################################

def MainPage(request):

    ##### Show the Store Items

    # Session Check
    if 'username' in request.session:
        # Session is there

        r = GetFullStoreInfo()

        if type(r) is ERR:
            return render(request, 'Error.html', context={"Error_Message": r.func_PrintError()})
        else:
            # Data are OK
            if len(r):
                return render(request, 'mainPage.html', context={"ItemsList": r})
            else:
                # Store is Empty
                return render(request, 'mainPage.html',  context={"ItemsList": ['NO ITEMS']})

    else:
        # NO SESSION go login page
        return redirect(to='/')


def home(request):

    #####  Show the login Page

    # Logout of the system
    #request.session.clear()

    # Loign Page Open
    return render(request, 'index.html')

def addItems(request):

    #### Show Add Item Page

    # Session Check
    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):
        return render(request, 'addItems.html')
    else:
        # NO SESSION go login page
        return redirect(to='/')

def editUsers(request):

    #### Show users list

    # Session Check
    if 'username' in request.session and request.session['Privlage'] == 1:

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})

        # Preper the SQL
        TheSQL = "SELECT * FROM users WHERE ID != " + str(request.session['ID'])
        print(TheSQL)

        # Send the SQL
        r = dbClass.func_SendSQL(db, TheSQL)
        dbClass.func_CloseConnection(db)

        # Check results
        if type(r) is ERR:
            return render(request, 'EditUsers.html', context={"lblResult": r.func_PrintError()})
        else:
            print(r)
            return render(request, 'EditUsers.html', context={"ItemsList": r})

    else:
        # NO SESSION go login page
        return redirect(to='/')

def about(request):

    #### Show About Page

    return render(request, 'About.html')

def editStore(request):

    #### Show Edit Items Page

    # Session Check

    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):
        # get the store info
        r = GetFullStoreInfo()

        if type(r) is ERR:
            return render(request, 'Error.html', context={"Error_Message": r.func_PrintError()})
        elif len(r):
            return render(request, 'EditStore.html', context={"ItemsList": r})
        else:
            # Store is Empty
            return render(request, 'EditStore.html')
    else:
        # NO SESSION go login page
        return redirect(to='/')

############################################################################################
#####     WORKING FUNCIONT for POST requests
############################################################################################

def InsertNewItems(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: InsertNewItems/
    # HTML FILE: addItems.html

    # JOB: Insert a NEW item with picture to the database
    ###########################

    # Session Check
    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2):

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})

        # Preper the SQL
        parameters = {"itemId": request.POST['itemId'], "itemname": request.POST['itemname'],
                      "shortname": request.POST['shortname'], "description": request.POST['description'],
                      "Quantity": request.POST['Quantity'], "orginalprice": request.POST['orginalprice'],
                      "sellingprice": request.POST['sellingprice'], "category": request.POST['category'],
                      "hight": request.POST['hight'], "width": request.POST['width'],
                      "length": request.POST['length'], "weight": request.POST['weight'],
                      "minplayer": request.POST['minplayer'], "maxplayer": request.POST['maxplayer'],
                      "playtime": request.POST['playtime'], "imagePath":request.POST['imagePath']}

        TheSQL = "INSERT INTO `items`(`itemId`, `itemname`, `shortname`, `description`, `Quantity`, `orginalprice`, " \
                 "`sellingprice`, `category`, `hight`, `width`, `length`, `weight`, `minplayer`, `maxplayer`, " \
                 "`playtime`, `image1`) VALUES (%(itemId)s, %(itemname)s, %(shortname)s, %(description)s, %(Quantity)s," \
                 " %(orginalprice)s, %(sellingprice)s, %(category)s," \
                 " %(hight)s, %(width)s, %(length)s, %(weight)s, %(minplayer)s, %(maxplayer)s, %(playtime)s, %(imagePath)s)"


        # Send the SQL
        r = dbClass.func_InsertSQL(db, TheSQL, parameters)
        dbClass.func_CloseConnection(db)

        # Check results
        if type(r) is ERR:
            return render(request, 'addItems.html', context={"lblResult": r.func_PrintError()})
        else:
            return render(request, 'addItems.html', context={"lblResult":"Item was added successfully! "})
    else:
        # NO SESSION go login page
        return redirect(to='/')

def upload(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: upload/
    # HTML FILE: uploadImage.html

    # JOB: Upload an image from the user desktop to the media folder of the serever
        # and return the file name connected to the media folder. This method is used as
        # part of other html file using {% include %}
    # NOW it works with edit store and add item to upload the user picture for the game

    ###########################

    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        if request.POST['TheSender'].__eq__("EDIT"):
            return render(request, 'EditStore.html', {'file_url': file_url})
        else:
            return render(request, 'addItems.html', {'file_url': file_url})

    return render(request, 'Error.html', context={"Error_Message": "Error loading the image. Please try again!"})

def GetFullStoreInfo():

    ###########################
    ## A FUNCION ###

    # Connected: show store / show store for edit

    # JOB: Get all store item from the database and return in a normal dict
    ###########################

    # Connect to database
    db = dbClass.func_ConnectToDB()
    if type(db) is ERR:
        return ERR

    r = dbClass.func_SendSQL(db, "SELECT * FROM items")
    dbClass.func_CloseConnection(db)

    if type(r) is ERR:
        return ERR
    else:
        # SQL was OK
        return r


def updateAnItem(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: updateItem/
    # HTML FILE: editStore.html

    # JOB: Update the changes to an item when user click 'save' or 'delete' buttons  by
        # the user in the editStore.html file
    ###########################

    if 'username' in request.session \
            and (request.session['Privlage'] == 1 or request.session['Privlage'] == 2) :

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return ERR
        else:
            if request.POST['action'].__eq__("Save"):

                # Preper the SQL
                parameters = {"itemId": request.POST['itemId'], "itemname": request.POST['itemname'],
                              "shortname": request.POST['shortname'], "description": request.POST['description'],
                              "Quantity": request.POST['Quantity'], "orginalprice": request.POST['orginalprice'],
                              "sellingprice": request.POST['sellingprice'], "category": request.POST['category'],
                              "hight": request.POST['hight'], "width": request.POST['width'],
                              "length": request.POST['length'], "weight": request.POST['weight'],
                              "minplayer": request.POST['minplayer'], "maxplayer": request.POST['maxplayer'],
                              "playtime": request.POST['playtime'], "imagePath": request.POST['imagePath']}

                TheSQL = "UPDATE `items` SET `itemname`=%(itemname)s,`shortname`=%(shortname)s,`description`=%(description)s," \
                         "`Quantity`=%(Quantity)s,`orginalprice`=%(orginalprice)s, " \
                         "`sellingprice`=%(sellingprice)s,`hight`=%(hight)s,`width`=%(width)s,`length`=%(length)s, " \
                         "`weight`= %(weight)s,`minplayer`=%(minplayer)s,`maxplayer`=%(maxplayer)s," \
                         "`playtime`=%(playtime)s,`image1`=%(imagePath)s WHERE `itemId`=%(itemId)s "


            elif request.POST['action'].__eq__('Delete'):

                parameters = {"itemId": request.POST['itemId']}

                TheSQL = "DELETE FROM `items` WHERE `itemId`=%(itemId)s"


            r = dbClass.func_SendSQL(myDBin=db, SQLStatment=TheSQL, parameters=parameters, returnDate=False)

        dbClass.func_CloseConnection(db)

        if type(r) is ERR:
            print(r.func_PrintError())
            request.session['FeedBackMsg'] = 'There was an error procssing the request. Please try again and make usre you enter the correct data.'
            return redirect(to='/editStore/')
        else:
            # SQL was OK
            request.session['FeedBackMsg'] = 'Update done succssfully!'
            return redirect(to='/editStore/')
    else:
        return render(request, 'Error.html', context={"Error_Message": "You do NOT have the Right to access this page. Please make sure you have the correct right or contact the website admin to grandt you the right."})

def updateUser(request):

    ###########################
    ## POST ACCPT ###

    # CALLING LINK: updateUser/
    # HTML FILE: editUsers.html

    # JOB: Update the status of the user by the admin when clicking 'Accept' or 'Promote'
        # buttons  by in the editUsers.html file
    ###########################

    if 'username' in request.session and request.session['Privlage'] == 1:

        # Connect to database
        db = dbClass.func_ConnectToDB()
        if type(db) is ERR:
            return ERR
        else:
            print(request.POST['action'])
            if request.POST['action'].__eq__("Accept"):
                TheSQL = "UPDATE `users` SET `mainverification`=1 WHERE %(userID)s"
                paratmer = {'userID': request.POST['userID']}
                dbClass.func_SendSQL(myDBin=db,SQLStatment=TheSQL, parameters=paratmer,returnDate=False)

            elif request.POST['action'].__eq__("Promote"):
                if request.POST['Privlage'] < 2:
                    TheSQL = "UPDATE `users` SET `PrivlageLevel`=`PrivlageLevel`+ 1 WHERE %(userID)s"
                    paratmer = {'userID': request.POST['userID']}
                    dbClass.func_SendSQL(myDBin=db,SQLStatment=TheSQL, parameters=paratmer,returnDate=False)

            dbClass.func_CloseConnection(db)
            return redirect(to='/editUsers')
    else:
        # NO SESSION go login page
        return redirect(to='/')
