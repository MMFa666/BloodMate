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
    blood_type = db.Column(db.String(3), nullable=False)
    availability = db.Column(db.Boolean())
    screening_status = db.Column(db.Boolean())
    donation_category = db.Column(db.String(3))
    new_date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #appointments = db.relationship('Screening_Appointment', backref='donor', lazy=True)

    

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
    rec_date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #appointments = db.relationship('Donation_Request', backref='recipient', lazy=True)
    

    def __repr__(self):
        return '<Recipient %r>' % self.id


class Administrator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email_id = db.Column(db.String(50), nullable=False)
    

    def __repr__(self):
        return '<Administrator %r>' % self.id


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(30), nullable=False)
    quantity =  db.Column(db.Integer,  nullable=False)     
    category = db.Column(db.String(20), nullable=False)
    expiry_date = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Stock %r>' % self.id

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    user_type = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Login %r>' % self.id

class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_center_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(30))
    phone_number = db.Column(db.String(13), nullable=False)
    #appointments = db.relationship('Screening_Appointment', backref='hospital', lazy=True)

    def __repr__(self):
        return '<Hospital %r>' % self.id


class Screening_Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime)
    appointment_date = db.Column(db.DateTime)
    screening_result = db.Column(db.Boolean())
    #test_center_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    test_center_name = db.Column(db.String(50))
    #donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    
    phone_number = db.Column(db.String(13), nullable=False)

    def __repr__(self):
        return '<Screening_Appointment %r>' % self.id


class Donation_Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(30), nullable=False)
    quantity =  db.Column(db.Integer,  nullable=False)     
    request_category = db.Column(db.String(20), nullable=False)
    #recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'), nullable=False)

    def __repr__(self):
        return '<Donation_Request %r>' % self.request_id




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
    return render_template('donor.html')

@app.route('/search_donor', methods =['POST', 'GET'])
def search_donor():
    city_is = request.form['location']
    blood_type_is = request.form['blood_type']

    donors2 = Donor.query.filter_by(blood_type = blood_type_is, city= city_is).all()
    return render_template('donors_search_result.html', donors2 = donors2)

@app.route('/donor_search_hospital_help', methods =['POST', 'GET'])
def donor_search_hospital_help():
   
    return render_template('donor_search_hospital.html')

@app.route('/donor_search_hospital', methods =['POST', 'GET'])
def donor_search_hospital():
    locs = request.form['location']

    tests2 = Hospital.query.filter_by(location= locs).all()
    return render_template('hospital_search_result.html', tests2 = tests2)

@app.route('/recipients_requests', methods =['POST', 'GET'])
def recipients_requests():
  
    reqs = Donation_Request.query.order_by(Donation_Request.quantity).all()
    return render_template('recipients_requests.html', reqs = reqs)

@app.route('/donate')
def donate():
    return 'Donate now!'    

@app.route('/recipient')
def recipient_portal():
    return render_template('recipient.html')

@app.route('/make_request_recipient', methods=['POST','GET'])
def make_request_recipient():
    if request.method == 'POST':
        bloodType = request.form['bloodType']
        reqQuant = request.form['reqQuant'] 
        reqCat = request.form['reqCat']
        
        new_req = Donation_Request(request_id= generate_random_id(), blood_type= bloodType, quantity= reqQuant, request_category= reqCat)

        try:
            db.session.add(new_req)
            db.session.commit()
            return redirect('/recipient')
        except Exception as e:
            'There was an issue adding the blood product :('
            print(e)
            return redirect('/')
    else:
        return render_template('make_request_recipient.html')


@app.route('/new_request')
def new_request():
    return 'Make a new request now!'


@app.route('/admin')
def admin_portal():
    return render_template('admin.html')

@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    if request.method == 'POST':
        bloodType = request.form['bloodType']
        prodQuant = request.form['prodQuant'] 
        prodCat = request.form['prodCat']
        expDate = request.form['expDate']

        expDate= datetime.strptime(expDate,'%Y-%m-%d')
        new_prod = Stock(id= generate_random_id(), blood_type= bloodType, quantity= prodQuant, category= prodCat, expiry_date= expDate)

        try:
            db.session.add(new_prod)
            db.session.commit()
            return redirect('/bloodproduct')
        except Exception as e:
            'There was an issue adding the blood product :('
            print(e)
            return redirect('/')
    else:
        return render_template('addproduct.html')


@app.route('/deleteproduct/<int:id>')
def deleteproduct(id):
    prod_del = Stock.query.get_or_404(id)

    try:
        db.session.delete(prod_del)
        db.session.commit()
        return redirect('/bloodproduct')
    except Exception as e:
        print(e)
        return 'Delete Failed'
    
@app.route('/bloodproduct', methods=['POST','GET'])
def blood_product():
    bps = Stock.query.order_by(Stock.date_created).all()
    return render_template('bloodproduct.html', bps=bps)

@app.route('/deletedonor/<int:id>')
def deletedonor(id):
    donor_del = Donor.query.get_or_404(id)
    print(id)
    try:
        db.session.delete(donor_del)
        db.session.commit()
        return redirect('/donors_admin')
    except Exception as e:
        print(e)
        return 'Delete Failed'
    
@app.route('/recipients_admin')
def recipients_admin():
    recipients = Recipient.query.order_by(Recipient.rec_date_created).all()
    return render_template('recipients_admin.html', recipients=recipients)

@app.route('/deleterecipient/<int:id>')
def deleterecipient(id):
    rec_del = Recipient.query.get_or_404(id)
    print(id)
    try:
        db.session.delete(rec_del)
        db.session.commit()
        return redirect('/recipients_admin')
    except Exception as e:
        print(e)
        return 'Delete Failed'

@app.route('/donors_admin', methods=['POST','GET'])
def donors_admin():
    donors = Donor.query.order_by(Donor.new_date_created).all()
    return render_template('donors_admin.html', donors=donors)


@app.route('/testcenters_admin', methods=['POST','GET'])
def testcenters_admin():
    tests = Hospital.query.order_by(Hospital.test_center_name).all()
    return render_template('testcenters_admin.html', tests = tests)    

@app.route('/addhospital', methods=['POST', 'GET'])
def addhospital():
   
    if request.method == 'POST':
        centerName = request.form['centerName'] 
        loc = request.form['loc']
        phoneNum = request.form['phoneNum']

        
        new_hosp = Hospital(id= generate_random_id(), test_center_name= centerName , location= loc, phone_number = phoneNum)

        try:
            db.session.add(new_hosp)
            db.session.commit()
            return redirect('/testcenters_admin')
        except Exception as e:
            'There was an issue adding the blood product :('
            print(e)
            return redirect('/')
    else:
        return render_template('addhospital.html')

@app.route('/deletehospital/<int:id>')
def deletehospital(id):
    hosp_del = Hospital.query.get_or_404(id)
    print(id)
    try:
        db.session.delete(hosp_del)
        db.session.commit()
        return redirect('/testcenters_admin')
    except Exception as e:
        print(e)
        return 'Delete Failed'

@app.route('/screening_admin')
def screening_admin():
    return render_template('screening_admin.html')
    

@app.route('/screening_donor', methods=['POST', 'GET'])
def screening_donor():
    if request.method == 'POST':
        time_is = request.form['time_is'] 
        app_date = request.form['app_date']
        hosp_name = request.form['hosp_name']

        
        new_app = Screening_Appointment(id= generate_random_id(), appointment_time= time_is , appointment_date= app_date, test_center_name =hosp_name)

        try:
            db.session.add(new_app)
            db.session.commit()
            return redirect('/donor')
        except Exception as e:
            'There was an issue adding the blood product :('
            print(e)
            return redirect('/')
    else:
        return render_template('screening_donor.html')  

@app.route('/product_input')
def product_input():
    return render_template('product_input.html')       



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
