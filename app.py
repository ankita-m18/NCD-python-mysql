from tkinter import scrolledtext
from flask import Flask, render_template, request, url_for, redirect

from flask_mysqldb import MySQL 
import MySQLdb.cursors

import sys
print(sys.path)

app = Flask(__name__)

#mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Ankita@18Riya'
app.config['MYSQL_DB'] = 'ncdpython'

mysql = MySQL(app)


@app.route('/')
def welcome():
    return render_template('registration.html')

def making_global(aadh):
    global aadhaar
    aadhaar=aadh
    


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method=="POST":

        firstname=""
        lastname=""
        gender=""
        aadhaar=""
        phone=""
        birthday=""
        pincode=""
        total=0
        screening=""
        msg = " "

        firstname=request.form['firstname']
        lastname=request.form['lastname']
        gender=request.form['gender']
        aadhaar=request.form['aadhaar']
        phone=request.form['phone']
        birthday=request.form['birthday']
        pincode=request.form['pincode']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO patient VALUES (NULL, % s, % s, % s, % s, % s, % s, % s,%s,%s)',(firstname, lastname, gender , aadhaar, phone, birthday, pincode, total, screening,))
    mysql.connection.commit()
    msg='You have successfully registered !'

    making_global(aadhaar)

    return render_template('question.html')

@app.route('/submit', methods=['GET','POST'])
def ncd_rac():
    if request.method == "POST":
        total=0
        age=-1
        smoke=-1
        alcohol=-1
        waist=-1
        phy_act=-1
        fam_his=-1
        
        age = int(request.form['age'])
        if (age ==-1):
            return redirect(url_for('fail'))
        
        smoke = int(request.form['smoke'])
        if (smoke == -1):
            return redirect(url_for('fail'))

        alcohol = int(request.form['smoke'])
        if (alcohol == -1):
            return redirect(url_for('fail'))

        waist = int(request.form['waist'])
        if (waist ==-1):
            return redirect(url_for('fail'))

        phy_act = int(request.form['phy_act'])
        if (phy_act == -1):
            return redirect(url_for('fail'))

        fam_his = int(request.form['fam_his'])
        if (fam_his == -1):
            return redirect(url_for('fail'))   

        total = age + smoke + alcohol + waist + phy_act + fam_his

        res=""
        screening=""
        
        if total>4:
            res="The person may be at higher risk of NCDs and needs to be prioritized for attending screening."
            screening ="yes";
        else:
            res="The person is not at risk of NCDs and doesn't need screening."
            screening ="no";

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE patient SET score =% s,screening =% s WHERE aadhaar_uid =% s',(total,screening,aadhaar))
    mysql.connection.commit()   

    return render_template('result.html',result=res,total=total, age=age,smoke=smoke,alcohol=alcohol,
                            waist=waist,phy_act=phy_act,fam_his=fam_his)              
    

@app.route('/fail')
def fail():
    str="Please answer all the questions."
    return render_template('error.html',str=str)

#back to registration.html page
@app.route('/back',methods=['POST','GET'])
def back():
    if request.method=='POST':
        return render_template('registration.html')


if __name__ == "__main__":  
    app.run(debug=True, port=8000)



'''@app.route('/success/<int:score>')
def success(score):
    res=""
    #print(score)
    if score>4:
        res="The person may be at higher risk of NCDs and needs to be prioritized for attending screening."
    else:
        res="The person is not at risk of NCDs and doesn't need screening."

    return render_template('result.html',result=res,sc=score)'''

