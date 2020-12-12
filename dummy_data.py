import string
import random
from datetime import datetime
from app import db,Administrator,generate_random_id,Login,Donor,Recipient,Screening_Appointment,Hospital,Stock,Donation_Request

email_counter=111111
password_counter=666666
phone_counter=77777
cities=['Lahore','Karachi','Multan','Islamabad','Faisalabad','Peshawar']
genders=['male','female']
blood_types=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
blood_categories=['Blood','WBC','RBC','Platelets','Plasma']

recipient_ids=[]
donor_ids=[]
test_center_ids=[]

#Donors
for i in range(5000):
    email_counter+=1
    password_counter+=1
    phone_counter+=1

    email=str(email_counter)+'@bloodmate.com'
    password=str(password_counter)
    user_type='donor'
    name=''
    for k in range(5):
        name+=random.choice(string.ascii_letters)

    contact='032012'+str(phone_counter)
    city=random.choice(cities)
    gender=random.choice(genders)
    blood_type=random.choice(blood_types)
    dob=datetime.strptime('1990-04-04','%Y-%m-%d')
    status_d = random.choice(['Active','Active','Active','Active','Inactive']) #status of donor
    screening_status=random.choice([True,True,True,True,False])

    id=generate_random_id()
    new_login = Login(id=id,email_id=email,password=password,user_type=user_type)
    new_user=Donor(id=id,
                    email_id=email,
                    name=name,
                    gender=gender,
                    city=city,
                    blood_type=blood_type,
                    phone_number=contact,
                    date_of_birth=dob,
                    screening_status=screening_status,
                    status = status_d,
                    )
    try:
        db.session.add(new_user)
        db.session.add(new_login)
        donor_ids.append(id)
    except Exception as e:
        print(e)
        print('There was an adding your donor',i)


#Recipients
for i in range(5000):
    email_counter+=1
    password_counter+=1
    phone_counter+=1

    email=str(email_counter)+'@bloodmate.com'
    password=str(password_counter)
    user_type='recipient'
    name=''
    for k in range(5):
        name+=random.choice(string.ascii_letters)

    contact='032012'+str(phone_counter)
    city=random.choice(cities)
    gender=random.choice(genders)
    blood_type=random.choice(blood_types)
    dob=datetime.strptime('1990-04-04','%Y-%m-%d')

    id=generate_random_id()
    new_login = Login(id=id,email_id=email,password=password,user_type=user_type)
    new_user=Recipient(id=id,
                    email_id=email,
                    name=name,
                    gender=gender,
                    city=city,
                    blood_type=blood_type,
                    phone_number=contact,
                    date_of_birth=dob,
                    )
    try:
        db.session.add(new_user)
        db.session.add(new_login)
        recipient_ids.append(id)
    except Exception as e:
        print(e)
        print('There was an error adding your recipient',i)


#Stock
for i in range(1000):
    bloodType = random.choice(blood_types)
    prodQuant = random.randint(1,10) 
    prodCat = random.choice(blood_types)
    expDate = '2021-'+str(random.randint(1,6))+'-'+str(random.randint(1,28))

    expDate= datetime.strptime(expDate,'%Y-%m-%d')
    new_prod = Stock(id= generate_random_id(), blood_type= bloodType, quantity= prodQuant, category= prodCat, expiry_date= expDate)

    try:
        db.session.add(new_prod)
    except Exception as e:
        print(e)
        print('There was an issue adding the blood product',i)
        

#Hospital
for i in range(50):
    phone_counter+=1

    id=generate_random_id()
    centerName = ''
    for k in range(5):
        centerName+=random.choice(string.ascii_letters)
    loc=random.choice(cities)
    phoneNum = '032012'+str(phone_counter)

    
    new_hosp = Hospital(id=id , test_center_name= centerName , location= loc, phone_number = phoneNum)

    try:
        db.session.add(new_hosp)
        test_center_ids.append(id)
    except Exception as e:
        print(e)
        print('There was an issue adding the Hospital',i)



#Donation Requests
for i in range(2000):
    bloodType = random.choice(blood_types)
    reqQuant = random.randint(1,4) 
    reqCat = random.choice(blood_categories)
    recipient_id=random.choice(recipient_ids)
    location=random.choice(cities)
    
    new_req = Donation_Request(request_id= generate_random_id(),location=location, blood_type= bloodType, quantity= reqQuant, request_category= reqCat,recipient_id=recipient_id)

    try:
        db.session.add(new_req)
    except Exception as e:
        print(e)
        print('There was an issue adding the donation request',i)


#Screening Requests
for i in range(100):
    # time_is = '2021-'+str(random.randint(1,6))+'-'+str(random.randint(1,28))

    donor_id=random.choice(donor_ids)
    test_center_id=random.choice(test_center_ids)
    # date_processing = time_is.replace('T', '-').replace(':', '-').split('-')
    # date_processing = [int(v) for v in date_processing]
    time_is = datetime(2021,random.randint(1,3),random.randint(1,25),random.randint(0,12),random.randint(0,59))
    # print('here3',time_is)
    # return('as')
    new_app = Screening_Appointment(id= generate_random_id(), appointment_time= time_is, donor_id = donor_id, test_center_id = test_center_id)

    try:
        db.session.add(new_app)
    except Exception as e:
        print('There was an issue adding the blood product :(',i)
        print('Error',e)


try:
    db.session.commit()
    print('done')
except Exception as e:
    print(e)
    print('There was an error in committing')