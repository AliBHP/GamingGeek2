
from django.shortcuts import render

from . import DatabaseControler as dbClass
from .ErrorReporting import ausError as ERR

from django.shortcuts import redirect

import hashlib, math, random

def login(request):

    # Logout of the system
    #if request.session:
    #    request.session.clear()

    db = dbClass.func_ConnectToDB()

    if type(db) is ERR:
        return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})

    # Prepere the SQL
    theSQL = "select * from users where username = %(inUsername)s and password = %(inPassword)s "

    # Hashing the password
    HashedPassword = hashlib.sha512(request.POST['psw'].encode("utf-8")).hexdigest()
    parameters = {"inUsername": request.POST['uname'], "inPassword": HashedPassword}

    # Send the SQL
    r = dbClass.func_SendSQL(myDBin=db, SQLStatment=theSQL, parameters=parameters)
    dbClass.func_CloseConnection(db)

    # print(request.POST['uname'] + " " + request.POST['psw'])

    if type(r) is ERR:
        return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})
    else:
        if len(r):

            ########################
            #   Success Access
            #######################

            # Session Establishments
            request.session['ID'] = r[0][0]
            request.session['username'] = r[0][1]
            request.session['RealName'] = r[0][3]
            request.session['Privlage'] = r[0][9]

            # REDIRECT to the stores Pages
            return redirect(to='/storehome', paramters={"flan":request.session['RealName']})

        else:
            # print("Wrong password or username")
            return render(request, 'index.html',context={"msg":"Wrong password or username"})

def register(request):

    # Logout of the system
    request.session.clear()

    return render(request, 'NewUser.html')

def addNewUser(request):

    # Connect to database
    db = dbClass.func_ConnectToDB()
    if type(db) is ERR:
        return render(request, 'Error.html', context={"Error_Message": db.func_PrintError()})

    # Check for password
    if request.POST['password'] != request.POST['password']:
        return render(request, 'NewUser.html', context={'lblResult':"password and password confirmation are not the same, please make sure you entered your password in the correct way"})
    else:
        # Hashing the password
        HashedPassword = hashlib.sha512(request.POST['password'].encode("utf-8")).hexdigest()

    # Check for email entry
    if request.POST['email'] != request.POST['email_c']:
        return render(request, 'NewUser.html', context={'lblResult':"Email and email confirmation are not the same, please make sure you entered your mail address in the correct way"})
    else:
        # Produce email verification
        emailCode = generateOTP()

    # Input to the database
    parameters = {"username": request.POST['username'], "password": HashedPassword, "Name": request.POST['Name'],
                  "email": request.POST['email'], "emailVerficationcode": emailCode, "phone": request.POST['phone']}

    TheSQL = "INSERT INTO `users` (`ID`, `username`, `password`, `Name`, `email`, `emailVerficationcode`, `phone`) " \
             "VALUES (NULL, %(username)s, %(password)s, %(Name)s, %(email)s, %(emailVerficationcode)s, %(phone)s )"

    # Send the SQL
    r = dbClass.func_InsertSQL(db, TheSQL, parameters)
    dbClass.func_CloseConnection(db)

    # Check results
    if type(r) is ERR:
        return render(request, 'NewUser.html', context={"lblResult": r.func_PrintError()})
    else:
        MsgBody = "Item was added successfully! "

        # Send The verificion code to email
        #send_mail(
        #    'GamingGeek Verification Code',
        #    'Dear Mr. ' + request.POST["Name"] + "\n\n You have register to GamingGeek website, Please use this code to verify your email address: \n\n " \
        #        + emailCode + "\n\n + Thank you for selecting Gaming Geek. ",
        #    'support@gaminggeek.co',
        #    [request.POST['email']],
        #    fail_silently=False,)

        return render(request, 'NewUser.html', context={"lblResult":MsgBody})

def generateOTP():
    # Declare a string variable
    # which stores all string
    string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(string)
    for i in range(6):
        OTP += string[math.floor(random.random() * length)]

    return OTP
