from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodmate.db'
db = SQLAlchemy(app)

def generate_random_id():
    return np.random.randint(0,1000000000)

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=2)
    name = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    city = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False, primary_key=True)
    availability = db.Column(db.Boolean())
    screening_status = db.Column(db.Boolean())
    donation_category = db.Column(db.String(3))
    

    def __repr__(self):
        return '<Donor %r>' % self.id

class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    city = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False)
    

    def __repr__(self):
        return '<Recipient %r>' % self.id


class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email_id = db.Column(db.String(50), nullable=False)
    

    def __repr__(self):
        return '<Administrator %r>' % self.id


class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    user_type = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Login %r>' % self.id



@app.route('/', methods=['POST', 'GET'])
def index():
    error=''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user_type=request.form['user']
        q=Login.query.filter_by(email_id=email,password=password,user_type=user_type).first()
        if q==None:
            error='Invalid Credentials!'
            return render_template('index.html',error=error)
        else:
            if user_type=='donor':
                return redirect('/donor')
            elif user_type=='admin':
                return redirect('/admin')
            else:
                return redirect('/recipient')
    else:
        return render_template('index.html',error=error)


@app.route('/donor')
def donor_portal():
    return 'Donor Login Successful!'

@app.route('/recipient')
def recipient_portal():
    return 'Recipient Login Successful!'

@app.route('/admin')
def admin_portal():
    return 'Admin Login Successful!'

@app.route('/register', methods=['POST', 'GET'])
def register():
    error=''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        user_type=request.form['user']
        name=request.form['name']
        contact=str(request.form['contact'])
        city=request.form['city']
        gender=request.form['gender']
        blood_type=request.form['blood_type']
        dob=request.form['dob']

        if len(name)==0:
            error='Invalid Name!'
            return render_template('register.html',error=error)

        if len(email)==0:
            error='Invalid Email!'
            return render_template('register.html',error=error)

        if len(password)<6:
            error='Invalid Password!'
            return render_template('register.html',error=error)

        if len(contact)!=11 or contact[:2]!='03':
            error='Invalid Contact!'
            return render_template('register.html',error=error)
        
        if len(city)==0:
            error='Invalid City!'
            return render_template('register.html',error=error)
        
        if dob=='':
            error='Invalid Date of Birth!'
            return render_template('register.html',error=error)

        dob=datetime.strptime(dob,'%Y-%m-%d')
        print(dob)

        print('aaaaaaaaaa')
        print(email,password,user_type,name,contact,city,gender,blood_type,dob)
        print('aaaaaaaaaa')
        q=Login.query.filter_by(email_id=email,user_type=user_type).first()
        if q==None:
            new_login = Login(id=generate_random_id(),email_id=email,password=password,user_type=user_type)
            if user_type=='donor':
                new_user=Donor(id=generate_random_id(),
                                email_id=email,
                                name=name,
                                gender=gender,
                                city=city,
                                blood_type=blood_type,
                                phone_number=contact,
                                date_of_birth=dob
                                )
            else:
                new_user=Recipient(id=generate_random_id(),
                                email_id=email,
                                name=name,
                                gender=gender,
                                city=city,
                                blood_type=blood_type,
                                phone_number=contact,
                                date_of_birth=dob
                                )
            try:
                db.session.add(new_user)
                db.session.add(new_login)
                db.session.commit()
                return render_template('index.html',error=error)
            except Exception as e:
                print(e)
                return 'There was an issue adding your task'

            
        else: 
            print('account already')
            # return 'account already'
            error='Email id used with this user type'
            return render_template('register.html',error=error)

    else:
        return render_template('register.html',error=error)



if __name__ == "__main__":
    app.run(debug=True)
