from flask import Flask,request, render_template,redirect, url_for, session
#from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from flask_mysqldb import MySQLdb
import mysql.connector
import re
import random
from flask_opensearch import FlaskOpenSearch



app = Flask(__name__)

app.config["OPENSEARCH_HOST"] = "localhost"
app.config["OPENSEARCH_USER"] = "admin"
app.config["OPENSEARCH_PASSWORD"] = "admin"

opensearch = FlaskOpenSearch(
    app=app,
    use_ssl=True,
    verify_certs=False,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)
db = MySQLdb.connect(host="localhost", user="root", passwd="Sohamroy@9", db="DeviCandika")
cur = db.cursor()

@app.route('/login', methods =['GET'])
def login():
   return  render_template('login_register.html')


@app.route('/enter',methods=['GET','POST'])
def enter():
    if request.method == 'POST' and 'passwordorg' in request.form :
        email = request.form['email']
        print("email is ------->",email)
        passwordorg = request.form['passwordorg']
        #passwordretype = request.form['passwordretype']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT passwordorg,enckey FROM Login WHERE  email= % s', (email, ))
        fetchpassword = cur.fetchone()
        if(fetchpassword==None):
            msg='Invalid Email or Password!!!!!!'
            return render_template('login_register.html',msg=msg)

        print(fetchpassword)
        fetchkey=fetchpassword[1]
        cipher_suite_fetch = Fernet(fetchkey)
        ciphered_text_fetch=fetchpassword[0]
        unciphered_text = (cipher_suite_fetch.decrypt(ciphered_text_fetch)).decode()
        print(unciphered_text)
        if (passwordorg==unciphered_text):
            print(passwordorg==unciphered_text)

            msg="Welcome {} !!!".format(email)
            

            
            return render_template('index.html',msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            return render_template('login_register.html',msg=msg)
        elif  not passwordorg or not email:
            msg = 'Please fill out the form !'
            return render_template('login_register.html',msg=msg)
    
            #return render_template('login_register.html',msg=msg)




@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    print("result is -----------> ",request.method == 'POST' and 'passwordretype' in request.form and 'password' in request.form and 'email' in request.form)
    print("method is",request.method == 'POST')
    print("passwordretype is",'passwordretype' in request.form)
    print("passwordorg is ",'passwordorg' in request.form)
    print("email is ",'email' in request.form)
    
    
    
    
    
    if request.method == 'POST' and 'passwordretype' in request.form and 'passwordorg' in request.form  :
        email = request.form['email']
        print("email is ------->",email)
        passwordorg = request.form['passwordorg']
        passwordretype = request.form['passwordretype']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM Login WHERE email = % s', (email, ))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists !'
            return render_template('login_register.html',msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
            return render_template('login_register.html',msg=msg)
        elif  not passwordorg or not email:
            msg = 'Please fill out the form !'
            return render_template('login_register.html',msg=msg)
        else:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            ciphered_text = cipher_suite.encrypt(passwordorg.encode())   
            cur.execute('''INSERT INTO Login (email,passwordorg,passwordretype,enckey) VALUES ( % s, % s, % s, %s)''', (email, ciphered_text, ciphered_text, key ))
            db.commit()
            msg = 'You have successfully registered !'
            print(msg)
            return render_template('success.html')
        







@app.route('/submit',methods=['POST'])
def submit():

    if request.method=='POST' :
        name=request.form.get('fname')
        print(name)
        phonenumber=request.form.get('phonenumber')
        address=request.form.get('address')
        print(phonenumber)
        email=request.form.get('email')
        id=random.randint(0,100000)
        print(name)

    
    res_3 = opensearch.index(
        "durgapuja-index",
        body={
            'name': name,
            'phonenumber': phonenumber,
            'address':address,
            'email': email
        },
        id=id,
        refresh=True,
    )
    print(res_3) 
    return f'Hello , {name} , {phonenumber},{id},{email} is submitted '
  
    

if __name__ == "__main__":
    app.run(debug=True)
