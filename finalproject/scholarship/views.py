from django.db import connection, models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

# Create your views here.
def Home(request):
    return render(request, 'scholarship_template/home.html')

def Home_Student(request):
    myScholarshipTypeList = Scholarship_Type.objects.all()
    context = { 'myScholarshipTypeList' : myScholarshipTypeList }
    return render(request, 'scholarship_template/home_student.html', context)

def Login_Student(request):
    context = {}
    if request.method == 'POST':
        myData = request.POST.copy()
        myStudentID = myData.get('myStudentID')
        myPassword = myData.get('myPassword')
        with connection.cursor() as myCursor:
            myCursor.execute("SELECT * FROM student WHERE studentID = %s AND password = %s", [myStudentID, myPassword])
            myFetchData = myCursor.fetchall()
            if len(myFetchData) > 0:
                print('Sign-in Successfully')
                print(myFetchData[0])
                request.session['signInUser'] = myFetchData[0]
                return redirect('home_student')
            else:
                print('Sign-in Error')
                context['returnMessage'] = 'Please check StudentID and Password'
    return render(request, 'scholarship_template/login_student.html', context)

def Register(request):
    context = {}
    if request.method == 'POST':
        myData = request.POST.copy()
        myStudentID = myData.get('myStudentID')
        myFirstName = myData.get('myFirstName')
        myLastName = myData.get('myLastName')
        myPhone = myData.get('myPhone')
        myEmail = myData.get('myEmail')
        myPassword = myData.get('myPassword')
        myMajor = myData.get('myMajor')
        with connection.cursor() as myCursor :
            myCursor.execute("INSERT INTO student(studentID, firstname, lastname, phone, email, password, major) VALUES (%s, %s, %s, %s, %s, %s, %s)", [myStudentID, myFirstName, myLastName, myPhone, myEmail, myPassword, myMajor])
            context['returnMessage'] = 'Register Complete'
    return render(request, 'scholarship_template/register_student.html', context)

def Login_Committee(request):
    context = {}
    if request.method == 'POST':
        myData = request.POST.copy()
        myUsername = myData.get('myUsername')
        myPassword = myData.get('myPassword')
        myRole = myData.get("myRole")
        with connection.cursor() as myCursor:
            myCursor.execute("SELECT * FROM committee WHERE username = %s AND password = %s AND role = %s", [myUsername, myPassword, myRole])
            myFetchData = myCursor.fetchall()
            if len(myFetchData) > 0:
                print('Sign-in Successfully')
                print(myFetchData[0])
                request.session['signInUser'] = myFetchData[0]
                if myRole == 'teacher':
                    return redirect('home_teacher')
                elif myRole == 'admin':
                    return redirect('home_admin')
            else:
                print('Sign-in Error')
                context['returnMessage'] = 'Please check StudentID, Password and Role'
    return render(request, 'scholarship_template/login_committee.html', context)

def Home_Admin(request):
    context = {}
    with connection.cursor() as myCursor :
        myCursor.execute("SELECT * FROM student")
        columns = [col[0] for col in myCursor.description]
        myFetchData = [dict(zip(columns, row)) for row in myCursor.fetchall()]
        context['StudentList'] = myFetchData
    return render(request, 'scholarship_template/home_admin.html', context)

def Home_Teacher(request):
    context = {}
    mySignInUser = request.session.get("signInUser")
    committeeID = str(mySignInUser[0])
    with connection.cursor() as myCursor :
        myCursor.execute("SELECT * FROM student INNER JOIN interview USING (studentID) INNER JOIN interview_committee USING (interviewID) WHERE committeeID = %s", [committeeID])
        columns = [col[0] for col in myCursor.description]
        myFetchData = [dict(zip(columns, row)) for row in myCursor.fetchall()]
        context['StudentList'] = myFetchData
    return render(request, 'scholarship_template/home_teacher.html', context)

def Application_New(request):
    context = {}
    mySignInUser = request.session.get("signInUser")
    myStudentID = str(mySignInUser[0])
    context['getstudentID'] = myStudentID
    if request.method == 'POST':
        myData = request.POST.copy()
        # StudentID = myData.get('StudentID')
        myFirstName = myData.get('firstName')
        myLastName = myData.get('lastName')
        myPhone = myData.get('myPhone')
        myEmail = myData.get('myEmail')
        currentAddress = myData.get('currentAddress')
        idcardAddress = myData.get('idcardAddress')
        myMajor = myData.get('major')
        year = myData.get('year')
        semester = myData.get('semester')
        gpax = myData.get('gpax')
        model = myData.get('model')
        income = myData.get('income')
        incomesource = myData.get('incomesource')
        otherincome = myData.get('otherincome')
        otherincomesource = myData.get('otherincomesource')
        debt = myData.get('debt')
        debtsource = myData.get('debtsource')
        dormfee = myData.get('dormfee')
        dadjob = myData.get('dadjob')
        dadincome = myData.get('dadincome')
        dadphone = myData.get('dadphone')
        momjob = myData.get('momjob')
        momincome = myData.get('momincome')
        momphone = myData.get('momphone')
        reason = myData.get('reason')
        file = myData.get('file')
        needLevel = myData.get('needLevel')
        with connection.cursor() as myCursor :
            myCursor.execute("INSERT INTO application(studentID, semester, studentYear, gpax, phoneModel, income, incomeSource, otherIncome, otherIncomeSource, dormFee, debt, debtSource, dadJob, dadIncome, dadPhone, momJob, momIncome, momPhone, reason, needLevel, file)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [myStudentID, semester, year, gpax, model, income, incomesource, otherincome, otherincomesource, dormfee, debt, debtsource, dadjob, dadincome, dadphone, momjob, momincome, momphone, reason, needLevel, file])
            myCursor.execute("UPDATE student SET currentAddress = %s, idcardAddress = %s, major = %s , firstname = %s , lastname = %s , phone = %s , email = %s WHERE (studentID = %s)", [currentAddress, idcardAddress, myMajor, myFirstName, myLastName, myPhone, myEmail, myStudentID])
            context['returnMessage'] = 'Submission Complete'
    return render(request, 'scholarship_template/application_new.html', context)

def Application_Old(request):
    context = {}
    mySignInUser = request.session.get("signInUser")
    myStudentID = str(mySignInUser[0])
    context['getstudentID'] = myStudentID
    with connection.cursor() as myCursor :
        myCursor.execute("SELECT * FROM student INNER JOIN application USING (studentID) WHERE studentID = %s", [myStudentID])
        columns = [col[0] for col in myCursor.description]
        myFetchData = [dict(zip(columns, row)) for row in myCursor.fetchall()]
        context['Lastest'] = myFetchData
    if request.method == 'POST':
        myData = request.POST.copy()
        myStudentID = myData.get('myStudentID')
        myFirstName = myData.get('firstName')
        myLastName = myData.get('lastName')
        myPhone = myData.get('myPhone')
        myEmail = myData.get('myEmail')
        currentAddress = myData.get('currentAddress')
        idcardAddress = myData.get('idcardAddress')
        myMajor = myData.get('major')
        year = myData.get('year')
        semester = myData.get('semester')
        gpax = myData.get('gpax')
        model = myData.get('model')
        income = myData.get('income')
        incomesource = myData.get('incomesource')
        otherincome = myData.get('otherincome')
        otherincomesource = myData.get('otherincomesource')
        debt = myData.get('debt')
        debtsource = myData.get('debtsource')
        dormfee = myData.get('dormfee')
        dadjob = myData.get('dadjob')
        dadincome = myData.get('dadincome')
        dadphone = myData.get('dadphone')
        momjob = myData.get('momjob')
        momincome = myData.get('momincome')
        momphone = myData.get('momphone')
        reason = myData.get('reason')
        file = myData.get('file')
        needLevel = myData.get('needLevel')
        with connection.cursor() as myCursor:
            myCursor.execute("INSERT INTO application(studentID, semester, studentYear, gpax, phoneModel, income, incomeSource, otherIncome, otherIncomeSource, dormFee, debt, debtSource, dadJob, dadIncome, dadPhone, momJob, momIncome, momPhone, reason, needLevel, file)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [myStudentID, semester, year, gpax, model, income, incomesource, otherincome, otherincomesource, dormfee, debt, debtsource, dadjob, dadincome, dadphone, momjob, momincome, momphone, reason, needLevel, file])
            myCursor.execute("UPDATE student SET currentAddress = %s AND idcardAddress = %s AND major = %s AND firstname = %s AND lastname = %s AND phone = %s AND email = %s WHERE (studentID = %s)", [currentAddress, idcardAddress, myMajor, myFirstName, myLastName, myPhone, myEmail, myStudentID])
            context['returnMessage'] = 'Submission Complete'
    return render(request, 'scholarship_template/application_old.html', context)