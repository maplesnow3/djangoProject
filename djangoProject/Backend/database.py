import mariadb
import random
import re
import datetime
from iso3166 import countries
import views.user_views

'''
Connects to the database using the connection string
'''


def openConnection():
    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connection string
        conn = mariadb.connect(
            user="injury_surv_editor",
            password="3c697dbb262165796fbddb80c071fc",
            host="108.61.184.187",
            port=3306,
            database="injury_surv_db_test"
        )
    except mariadb.Error as e:
        print(e)

    # return the connection to use
    return conn


'''
Validate a user login request based on account and password
'''


def login(account, password):
    conn = openConnection()
    try:
        curs = conn.cursor()
        # execute the query  #/
        curs.execute(
            "SELECT * FROM User WHERE account=%r and password=%r"
            % (account, password))

        # loop through the resultset #/
        nr = 0
        row = curs.fetchone()
        if row is not None:
            nr += 1
        if nr == 0:
            return None

        userInfo = [str(row[0]), str(row[1]), str(row[2]), str(row[3])]
        curs.close()

    except mariadb.Error as e:
        print(e)

    # default:userInfo = ['1', 'test01@test.com', 'test01', 'player']
    return userInfo


'''
Change password for a given userId
'''


def changePw(userid, oldpw, newpw):
    conn = openConnection()
    try:

        curs = conn.cursor()
        # Check whether the given old password is correct
        curs.execute(
            "SELECT * FROM User WHERE userId=%r and password=%r"
            % (userid, oldpw))
        check = curs.fetchone()
        if check is None:
            # Not correct, return Fail
            return "Fail"
        else:
            # Correct, update the password with the new one and return Success
            curs.execute(
                "Update User Set password=%r Where userId=%r"
                % (newpw, userid))
            conn.commit()

        curs.close()
        return "Success"


    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Register a new user with given account, password and user type
'''


def register(account, password, type):
    conn = openConnection()
    try:
        curs = conn.cursor()
        # Insert the new user
        userid = key('userId', 'User')
        curs.execute(
            "Insert into User (userId, account, password, type) values (%r, %r, %r, %r)"
            % (userid, account, password, type)
        )
        conn.commit()
        curs.close()
        registerAth = addAth(userid)
        if registerAth == "Success":
            return userid
        else:
            return "Fail"
    except mariadb.Error as e:
        print(e)
        return "Fail"


def addAth(userid):
    conn = openConnection()
    try:
        curs = conn.cursor()
        # Insert a new athlete
        athleteid = key('athleteId', 'Athlete')
        code = random.sample("abcdefghijklmnopqrstuvwxyz", 10)
        newcode = ''
        for x in code:
            newcode = newcode + x
        curs.execute(
            "Insert into Athlete (athleteId, code, userId) values (%r, %r, %r)"
            % (athleteid, newcode, userid)
        )
        conn.commit()
        curs.close()
        return "Success"

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Insert the personal information for a new user
'''


def addPerInf(userid, surname, givenName, dateofbirth, ebackground, mobile, address, country):
    conn = openConnection()
    try:

        curs = conn.cursor()
        # Get the email which is the account
        curs.execute(
            "SELECT account FROM User WHERE userId=%r"
            % (userid))
        getemail = curs.fetchone()
        if getemail is None:
            # No such a user, return Fail
            return "Fail"
        else:
            email = str(getemail[0])
        perInfId = key('perInfoId', 'PerInfo')
        country_inf = countries.get(country)
        country_code = country_inf[3]
        curs.execute(
            "Insert into PerInfo (perInfoId, surname, givenName, dateOfBirth, address, email, mobile, country, ethicBackground) "
            "values (%r, %r, %r, %r, %r, %r, %r, %r)"
            % (perInfId, surname, givenName, dateofbirth, address, email, mobile, country_code, ebackground))
        conn.commit()
        curs.execute(
            "Update Athlete Set perInfoId=%r Where userId=%r"
            % (perInfId, userid))
        conn.commit()
        curs.close()
        return "Success"

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Insert the baseline information for a new user (Not Tested)
'''


def addBaseInf(userid, medHistory, medHisInput, medicine, takeMedicine, injHistory, injHisInput, surgery, surYear,
               concHis, concDes):
    conn = openConnection()
    try:
        curs = conn.cursor()
        baseInfoId = key('baseInfoId', 'BaseInfo')
        now = datetime.datetime.now()
        baseInfoTime = now.strftime('%Y-%m-%d %H:%M:%S')
        sufferFrom = list2str(medHistory)
        sufferLength = list2str(medHisInput)
        for x in takeMedicine:
            medicine.append(x)
        medicineTaken = list2str(medicine)
        injuryName = list2str(injHistory)
        injuryLocation = list2str(injHisInput)
        surgeryName = list2str(surgery)
        surgeryYear = list2str(surYear)
        concuHistory = list2str(concHis)
        curs.execute("Insert into BaseInfo (baseInfoId, baseInfoTime, sufferFrom, sufferLength, "
                     "medicineTaken, injuryName, injuryLocation, surgeryName, surgeryYear, concuHistory, concuSympDesc) "
                     "values (%r, %r, %r, %r, %r, %r, %r, %r, %r, %r)"
                     % (baseInfoId, baseInfoTime, sufferFrom, sufferLength, medicineTaken, injuryName, injuryLocation,
                        surgeryName, surgeryYear, concuHistory, concDes))
        conn.commit()
        curs.execute(
            "Update Athlete Set baseInfoId=%r Where userId=%r"
            % (baseInfoId, userid))
        conn.commit()
        curs.close()
        return "Success"

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Get the personal information for a given user
'''


def viewPerInf(userid):
    conn = openConnection()
    try:

        curs = conn.cursor()
        curs.execute("Select * from PerInfo where perInfoId in (Select perInfoId from Athlete where userId=%r)"
                     % (userid))
        row = curs.fetchone()
        if row is not None:
            # Return the personal information except personal information id
            country_inf = countries.get(str(row[8]))
            country_name = country_inf[4]
            perInf = [str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]),
                      country_name]
            curs.close()
            return perInf
        else:
            curs.close()
            return None

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Get the baseline information for a given user (Not Tested)
'''


def viewBaseInf(userid):
    conn = openConnection()
    try:

        curs = conn.cursor()
        curs.execute("Select * from BaseInfo where baseInfoId in (Select baseInfoId from Athlete where userId=%r)"
                     % (userid))
        row = curs.fetchone()
        if row is not None:
            # medHistory, medHisInput, medicine, takeMedicine, injHistory, injHisInput, surgery, surYear, concHis, concDes
            medHistory = str2list(str(row[2]))
            medHisInput = str2list(str(row[3]))
            medicinedata = str2list(str(row[4]))
            n = 0
            medicine = []
            takeMedicine = []
            for x in medicinedata:
                if n < 3:
                    medicine.append(x)
                else:
                    takeMedicine.append(x)
                n = n + 1
            injHistory = str2list(str(row[5]))
            injHisInput = str2list(str(row[6]))
            surgery = str2list(str(row[7]))
            surYear = str2list(str(row[8]))
            concHis = str2list(str(row[9]))
            concDes = str(row[10])
            baseInf = [medHistory, medHisInput, medicine, takeMedicine, injHistory, injHisInput, surgery, surYear,
                       concHis, concDes]
            curs.close()
            return baseInf
        else:
            curs.close()
            return None

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Update the personal information for a given user
'''


def updatePerInf(userid, address, mobile):
    conn = openConnection()
    try:
        curs = conn.cursor()
        curs.execute(
            "Update PerInfo Set address=%r, mobile=%r Where perInfoId in (Select perInfoId from Athlete where userId=%r)"
            % (address, mobile, userid))
        conn.commit()
        curs.close()
        return "Success"

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Get the invitation code for a given individual user
'''


def viewAthcode(userid):
    conn = openConnection()
    try:

        curs = conn.cursor()
        # Get the code with the given userId
        curs.execute(
            "SELECT code FROM Athlete WHERE userId=%r"
            % (userid))
        code = curs.fetchone()
        if code is not None:
            curs.close()
            return [userid, str(code[0])]
        else:
            curs.close()
            return None

    except mariadb.Error as e:
        print(e)
        return None


'''
Update the invitation code for a given individual user
'''


def updateAthcode(userid, code):
    conn = openConnection()
    try:
        curs = conn.cursor()
        curs.execute("Update Athlete Set code=%r Where userId=%r"
                     % (code, userid))
        conn.commit()
        curs.close()
        return "Success"

    except mariadb.Error as e:
        print(e)
        return "Fail"


'''
Insert a new injury report for a given user (ToDo)
'''


def addInj(userid, ):
    return "Success"


def addConc(userid, ):
    return "Success"


'''
Get all the injury report id and datetime for a given individual user (Not Tested)
'''


def viewAllDate(userid):
    conn = openConnection()
    date = []
    try:
        curs = conn.cursor()
        athleteId = getAthid(userid)
        curs.execute("Select injFormId, injFormTime from InjForm Where athleteId=%r"
                     % (athleteId))
        nr = 0
        row = curs.fetchone()
        while row is not None:
            nr += 1
            date.append([str(row[0]), str(row[1])])
            row = curs.fetchone()

        if nr == 0:
            return None
        curs.close()

    except mariadb.Error as e:
        print(e)
        return "Fail"

    date_list = [{
        "report_id": row[0],
        "date": row[1]
    } for row in date]
    return data_list


'''
Get all the injury report id and datetime for a given individual user and a range of date (Not Tested)
'''


def viewRangeDate(userid, startDate, endDate):
    conn = openConnection()
    date = []
    try:
        curs = conn.cursor()
        athleteId = getAthid(userid)
        curs.execute("Select injFormId, injFormTime from InjForm "
                     "Where athleteId=%r and injFormTime >= '%s 00:00:00' and injFormTime <= '%s 23:59:59'"
                     % (athleteId, startDate, endDate))
        nr = 0
        row = curs.fetchone()
        while row is not None:
            nr += 1
            date.append([str(row[0]), str(row[1])])
            row = curs.fetchone()

        if nr == 0:
            return None
        curs.close()

    except mariadb.Error as e:
        print(e)
        return "Fail"

    date_list = [{
        "report_id": row[0],
        "date": row[1]
    } for row in date]
    return data_list


'''
Get the injury report for a given report id (ToDo)
'''


def viewInj(injId):
    return "Success"


def viewConc(injId):
    return "Success"


'''
Sub-functions
'''


def getAthid(userid):
    conn = openConnection()
    try:

        curs = conn.cursor()
        # Get the athleteId with the given userId
        curs.execute(
            "SELECT athleteId FROM Athlete WHERE userId=%r"
            % (userid))
        athleteid = curs.fetchone()
        if athleteid is not None:
            curs.close()
            return str(athleteid[0])
        else:
            curs.close()
            return None

    except mariadb.Error as e:
        print(e)
        return None


def key(pkey, table):
    # Get the primary key for the new data to be inserted
    conn = openConnection()
    try:

        curs = conn.cursor()
        curs.execute(
            "Select max(%s) from %s"
            % (pkey, table)
        )
        row = curs.fetchone()
        max = int(row[0])
        next = max + 1

        curs.close()
    except mariadb.Error as e:
        print("Fail, error: " + e)

    return next


def list2str(input_list, delimiter="|"):
    """
    Convert a list into one single string with values separated by given delimiter.
    Support str, int and float lists.
    The delimiter character in input strings will be prefixed by a backslash.
    i.e.,  `|`  will become  `\|`
    """
    output = ""

    if len(input_list) < 1:
        return output

    for ele in input_list:
        # Escape delimiter characters from original input
        ele_converted = str(ele).replace(delimiter, "\\" + delimiter)
        # Concat the piece with a delimiter followed
        output += ele_converted + delimiter

    # Remove last char, which is a redundant delimiter
    output_len = len(output)
    if output[output_len - 1] == delimiter:
        output = output[:-1]

    return output


def str2list(input_str, delimiter="|", output_type="str"):
    """
    Convert a string including delimiters into a list of values.
    Elements in the returned list can be either "str", "int" or "float", which
    is specified in parameter `output_type`.
    Validation of input values will not be checked, therefore "int" and "float"
    may cause error if input contains non-numeric stuffs.
    """
    output = []

    # Separate on delimiter `|`, but not escaped ones
    input_frags = re.split(r'(?<!\\)[' + delimiter + r']', input_str)

    # Restore escaped delimiters `\|`, convert types and return values
    for frag in input_frags:
        frag_unescaped = frag.replace("\\|", "|")

        if output_type == "int":
            output.append(int(frag_unescaped))
        elif output_type == "float":
            output.append(float(frag_unescaped))
        else:
            output.append(frag_unescaped)

    return output