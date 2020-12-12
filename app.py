from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
from datetime import datetime
from datetime import timedelta 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloodmate.db'
db = SQLAlchemy(app)

def generate_random_id():
    return np.random.randint(0,1000000000)

class Donor(db.Model):
    __tablename__ = 'Donor'
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
    status = db.Column(db.String(8))
    #appointments = db.relationship('Screening_Appointment', backref='donor', lazy=True)

    

    def __repr__(self):
        return '<Donor %r>' % self.id

class Recipient(db.Model):
    __tablename__ = 'Recipient'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    city = db.Column(db.String(30))
    gender = db.Column(db.String(10))
    email_id = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(13), nullable=False)
    blood_type = db.Column(db.String(3), nullable=False)
    rec_date_created = db.Column(db.DateTime, default=datetime.utcnow)
    request_status = db.Column(db.String(30))
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
    __tablename__ = 'Hospital'
    id = db.Column(db.Integer, primary_key=True)
    test_center_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(30))
    phone_number = db.Column(db.String(13), nullable=False)
    #appointments = db.relationship('Screening_Appointment', backref='hospital', lazy=True)
    Screening_Appointment = db.relationship("Screening_Appointment", backref=db.backref("Screening_Appointment", uselist=False))

    def __repr__(self):
        return '<Hospital %r>' % self.id


class Screening_Appointment(db.Model):
    __tablename__ = 'Screening_Appointment'
    id = db.Column(db.Integer, primary_key=True)
    appointment_time = db.Column(db.DateTime)
    # appointment_date = db.Column(db.DateTime)
    screening_result = db.Column(db.Boolean())
    test_center_id = db.Column(db.Integer, db.ForeignKey('Hospital.id'))
    #test_center_name = db.Column(db.String(50))
    donor_id = db.Column(db.Integer, db.ForeignKey('Donor.id'))
    Hospital = db.relationship("Hospital", backref=db.backref("Hospital", uselist=False))
    Donor = db.relationship("Donor", backref=db.backref("Donor", uselist=False))
    
   # phone_number = db.Column(db.String(13))

    def __repr__(self):
        return '<Screening_Appointment %r>' % self.id


class Donation_Request(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(30), nullable=False)
    quantity =  db.Column(db.Integer,  nullable=False)     
    request_category = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(30))
    recipient_id = db.Column(db.Integer, db.ForeignKey('Recipient.id'), nullable=False)

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
            
            id=q.id
            if user_type=='donor':
                user = Donor.query.get_or_404(id)
                return render_template('donor.html',id=id ,status=user.screening_status)
            elif user_type=='admin':
                return render_template('admin.html',id=id)
            else:
                return render_template('recipient.html',id=id)
    else:
        return render_template('index.html',error=error)


@app.route('/donor')
def donor_portal():
    return render_template('donor.html')

@app.route('/search_donor', methods =['POST', 'GET'])
def search_donor():
    city_is = request.form['location']
    blood_type_is = request.form['blood_type']

    donors2 = Donor.query.filter_by(blood_type = blood_type_is, city= city_is, screening_status=True, status='Active').all()
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

@app.route('/make_request_recipient/<int:id>', methods=['POST','GET'])
def make_request_recipient(id):
    user = Recipient.query.get_or_404(id)
    if request.method == 'POST':
        bloodType = request.form['bloodType']
        reqQuant = request.form['reqQuant'] 
        reqCat = request.form['reqCat']
        location=request.form['location']

        if int(reqQuant)<=0:
            return render_template('make_request_recipient.html', id =id,error='Invalid Quantity')

        req_st = 'Pending' #changing status request of recipient from no request to pending
        new_req = Donation_Request(request_id= generate_random_id(), blood_type= bloodType, quantity= reqQuant, request_category= reqCat, recipient_id= user.id, location=location)

        try:
            user.request_status = req_st
            db.session.add(new_req)
            db.session.commit()
            return render_template('recipient.html',id=id)
        except Exception as e:
            'There was an issue adding the blood product :('
            print(e)
            return redirect('/')
    else:
        return render_template('make_request_recipient.html', id =id)


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

        if expDate=='':
            return render_template('addproduct.html',error='Expiry date not valid')
        

        expDate= datetime.strptime(expDate,'%Y-%m-%d')

        if int(prodQuant)<=0:
            return render_template('addproduct.html',error='Quantity should be positive')
        if expDate < datetime.utcnow()+ timedelta(hours=5):
            return render_template('addproduct.html',error='Expiry date not valid')

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


@app.route('/updateproduct/<int:id>', methods=['POST','GET'])
def updateproduct(id):
    prod = Stock.query.get_or_404(id)
    if request.method == 'POST':
        prodQuant = request.form['prodQuant']
        expDate = request.form['expDate']
        if expDate=='':
            return render_template('updateproduct.html',id=id, quantity= prod.quantity,expiry_date=prod.expiry_date,error='Expiry date not valid')
        
        expDate= datetime.strptime(expDate,'%Y-%m-%d')

        if int(prodQuant)<=0:
            return render_template('updateproduct.html',id=id, quantity= prod.quantity,expiry_date=prod.expiry_date,error='Quantity should be positive')
        if expDate < datetime.utcnow()+ timedelta(hours=5):
            return render_template('updateproduct.html',id=id, quantity= prod.quantity,expiry_date=prod.expiry_date,error='Expiry date not valid')

        prod.quantity=prodQuant
        prod.expiry_date=expDate

        try:
            db.session.commit()
            return redirect('/bloodproduct')
        except Exception as e:
            print(e)
            return 'Update Failed'
    else:
        return render_template('updateproduct.html',id=id, quantity= prod.quantity,expiry_date=prod.expiry_date)
    
@app.route('/bloodproduct', methods=['POST','GET'])
def blood_product():
    bps = Stock.query.order_by(Stock.date_created).all()
    return render_template('bloodproduct.html', bps=bps)

@app.route('/deletedonor/<int:id>')
def deletedonor(id):
    donor_del = Donor.query.get_or_404(id)
    login_del = Login.query.get_or_404(id)
    print(id)
    try:
        donor_del.status = 'Inactive'
        db.session.delete(donor_del)
        db.session.delete(login_del)
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
    login_del = Login.query.get_or_404(id)
    print(id)
    try:
        db.session.delete(rec_del)
        db.session.delete(login_del)
        db.session.commit()
        return redirect('/recipients_admin')
    except Exception as e:
        print(e)
        return 'Delete Failed'

@app.route('/deleterecipientrequest/<int:id>/<int:rid>')
def deleterecipientrequest(id,rid):
    rid = Recipient.query.get_or_404(rid)
    print(rid)
    #print(idd)
    #ru = Recipient.query.get_or_404(idd)
    #req_del = Recipient.query.get_or_404(id)
    print(id)
    req_del2 = Donation_Request.query.get_or_404(id)
    print(id)
    #print(idd)
    try:
        rid.request_status= 'No request'
        db.session.delete(req_del2)
        db.session.commit()
        return redirect('/recipients_requests')
    except Exception as e:
        print(e)
        return 'Delete Failed'

@app.route('/perform_screening/<int:id>/<int:rid>')
def perform_screening(id,rid):
    app_del = Screening_Appointment.query.get_or_404(id)
    don_del =Donor.query.get_or_404(rid)
    log_del = Login.query.get_or_404(rid)
    try:
        db.session.delete(app_del)
        db.session.delete(don_del)
        db.session.delete(log_del)
        db.session.commit()
        # return render_template('screening_admin.html')
        return redirect('/screening_admin')
    except Exception as e:
        print(e)
        return 'Delete Failed'

@app.route('/approve_screening/<int:id>/<int:rid>')
def approve_screening(id,rid):
    app_del = Screening_Appointment.query.get_or_404(id)
    don =Donor.query.get_or_404(rid)
    don.screening_status=True
    try:
        db.session.delete(app_del)
        db.session.commit()
        # return render_template('screening_admin.html')
        return redirect('/screening_admin')
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
    sc_apps = Screening_Appointment.query.order_by(Screening_Appointment.appointment_time).all()
    return render_template('screening_admin.html', sc_apps = sc_apps)
    

@app.route('/screening_donor/<int:id>', methods=['POST', 'GET'])
def screening_donor(id):
    user = Donor.query.get_or_404(id)
    hosp=Hospital.query.order_by(Hospital.test_center_name).all()
    names=[]
    for h in hosp:
        names.append(h.test_center_name)
    print('here1')
    if request.method == 'POST':
        print('here2')
        time_is = request.form['time_is'] 
        name = request.form['name']
        # app_date=datetime.strptime(app_date,'%Y-%m-%d')
        # time_is = datetime.strptime(time_is, '%Y-%m-%d%H:%M')
        if time_is=='':
            return render_template('screening_donor.html',error='Invalid Appointment time',id=id)
        date_processing = time_is.replace('T', '-').replace(':', '-').split('-')
        date_processing = [int(v) for v in date_processing]
        time_is = datetime(*date_processing)

        if time_is < datetime.utcnow()+ timedelta(hours=5):
            return render_template('screening_donor.html',error='Invalid Appointment time',id=id,names=names)
        # print('here3',time_is)
        # return('as')
        
        q=Hospital.query.filter_by(test_center_name=name).first()

        new_app = Screening_Appointment(id= generate_random_id(), appointment_time= time_is, donor_id = user.id, test_center_id = q.id)

        try:
            print('here')
            db.session.add(new_app)
            db.session.commit()
            return render_template('donor.html', id=id,status=user.screening_status)
        except Exception as e:
            'There was an issue adding the blood product :('
            print('Error',e)
            return redirect('/')
    else:
        
        return render_template('screening_donor.html', id=id,names=names)  

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
        status_d = 'Active' #status of donor
        req_status = 'No request'

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
            id=generate_random_id()
            new_login = Login(id=id,email_id=email,password=password,user_type=user_type)
            if user_type=='donor':
                new_user=Donor(id=id,
                                email_id=email,
                                name=name,
                                gender=gender,
                                city=city,
                                blood_type=blood_type,
                                phone_number=contact,
                                date_of_birth=dob,
                                status = status_d,
                                screening_status=False,
                                )
            else:
                new_user=Recipient(id=id,
                                email_id=email,
                                name=name,
                                gender=gender,
                                city=city,
                                blood_type=blood_type,
                                phone_number=contact,
                                date_of_birth=dob,
                                request_status = req_status
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

@app.route('/change_info_donor/<int:id>', methods=['POST', 'GET'])
def change_info_donor(id):
    # return render_template('product_input.html')
    login = Login.query.get_or_404(id)
    user = Donor.query.get_or_404(id)
    error=''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        name=request.form['name']
        contact=str(request.form['contact'])
        city=request.form['city']
        status = request.form['sd']

        if len(name)==0:
            error='Invalid Name!'
            return render_template('change_info_donor.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password, status = user.status, error=error)

        if len(email)==0:
            error='Invalid Email!'
            return render_template('change_info_donor.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password, status = user.status ,error=error)

        if len(password)<6:
            error='Invalid Password!'
            return render_template('change_info_donor.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password,status = user.status,error=error)

        if len(contact)!=11 or contact[:2]!='03':
            error='Invalid Contact!'
            return render_template('change_info_donor.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password, status = user.status , error=error)
        
        if len(city)==0:
            error='Invalid City!'
            return render_template('change_info_donor.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password, status = user.status, error=error)
        
        try:
            login.email_id=email
            login.password=password

            user.name=name
            user.email_id=email
            user.phone_number=contact
            user.city=city
            user.password=password
            user.status = status

            db.session.commit()
            return render_template('donor.html',id=id)
        except:
            return 'There was an issue updating your info'
    else:

        return render_template('change_info_donor.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password, status = user.status)


@app.route('/change_info_recipient/<int:id>', methods=['POST', 'GET'])
def change_info_recipient(id):
    # return render_template('product_input.html')
    login = Login.query.get_or_404(id)
    user = Recipient.query.get_or_404(id)
    error=''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        name=request.form['name']
        contact=str(request.form['contact'])
        city=request.form['city']

        if len(name)==0:
            error='Invalid Name!'
            return render_template('change_info_recipient.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password,error=error)

        if len(email)==0:
            error='Invalid Email!'
            return render_template('change_info_recipient.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password,error=error)

        if len(password)<6:
            error='Invalid Password!'
            return render_template('change_info_recipient.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password,error=error)

        if len(contact)!=11 or contact[:2]!='03':
            error='Invalid Contact!'
            return render_template('change_info_recipient.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password,error=error)
        
        if len(city)==0:
            error='Invalid City!'
            return render_template('change_info_recipient.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password,error=error)
        
        try:
            login.email_id=email
            login.password=password

            user.name=name
            user.email_id=email
            user.phone_number=contact
            user.city=city
            user.password=password

            db.session.commit()
            return render_template('recipient.html',id=id)
        except:
            return 'There was an issue updating your info'
    else:

        return render_template('change_info_recipient.html',id=id , email=user.email_id,city=user.city,phone_number=user.phone_number,name=user.name,password=login.password)



@app.route('/change_info_admin/<int:id>', methods=['POST', 'GET'])
def change_info_admin(id):
    # return render_template('product_input.html')
    login = Login.query.get_or_404(id)
    user = Administrator.query.get_or_404(id)
    error=''
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        name=request.form['name']

        if len(name)==0:
            error='Invalid Name!'
            return render_template('change_info_admin.html',id=id , email=user.email_id,name=user.name,password=login.password,error=error)

        if len(email)==0:
            error='Invalid Email!'
            return render_template('change_info_admin.html',id=id , email=user.email_id,name=user.name,password=login.password,error=error)

        if len(password)<6:
            error='Invalid Password!'
            return render_template('change_info_admin.html',id=id , email=user.email_id,name=user.name,password=login.password,error=error)

        
        try:
            login.email_id=email
            login.password=password

            user.name=name
            user.email_id=email
            user.password=password

            db.session.commit()
            return render_template('admin.html',id=id)
        except:
            return 'There was an issue updating your info'
    else:

        return render_template('change_info_admin.html',id=id , email=user.email_id,name=user.name,password=login.password)

@app.route('/recipient_request_status/<int:id>', methods=['GET', 'POST'])
def recipient_request_status(id):
    user = Recipient.query.get_or_404(id)
    return render_template('recipient_request_status.html', id=id, req = user.request_status )

@app.route('/donor_search_recipient_requests', methods=['GET', 'POST'])
def donor_search_recipient_requests():
    if request.method == 'POST':
        bloodType = request.form['bloodType']
        reqCat = request.form['reqCat']
        location=request.form['location']

        reqs = Donation_Request.query.filter_by(location=location, blood_type= bloodType, request_category= reqCat).order_by(Donation_Request.request_id).all()
        return render_template('donors_search_result_requests.html', reqs = reqs)



    else:
        return render_template('donor_search_recipient_requests.html')
        
@app.route('/donor_search_recipient_requests_first', methods=['GET', 'POST'])
def donor_search_recipient_requests_first():
    if request.method == 'POST':
        return render_template('donor_search_recipient_requests.html')
    else:
        return render_template('donor_search_recipient_requests.html')


if __name__ == "__main__":
    app.run(debug=False)
