create table administrator(
    id int(10),
    name varchar(30) not null,
    email_id varchar(50) not null,
    primary key(id)
);

create table login(
    id int(10),
    email_id varchar(50) not null,
    user_type varchar(10) check (user_type in ('donor', 'recipient')),
    password varchar(15) not null,
    primary key(id)
);

create table donor(
    id int(10),
    name varchar(30) not null,
    date_of_birth date, 
    city varchar(20),
    email_id varchar(50) not null,
    phone_number varchar(13) not null,
    blood_type varchar(3) check (blood_type in ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    availability bit, 
    screening_status bit, 
    donation_category varchar(20) check (donation_category in ('Blood', 'Red Blood Cells', 'White Blood Cells','Platelets', 'Plasma')),
    primary key(id, blood_type, donation_category)
);

create table recipient(
    id int(10),
    name varchar(30) not null,
    date_of_birth date, 
    city varchar(20),
    email_id varchar(50) not null,
    phone_number varchar(13) not null,
    blood_type varchar(3) check (blood_type in ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    primary key(id)
);


create table screening_appointments(
    appointment_id int(10),
    appointment_time datetime,
    screening_result bit,
    test_center_id int(10),
    donor_id int(10),
    primary key(appointment_id),
    foreign key(test_center_id) references hospitals on delete set null
);


create table hospitals(
    test_center_id int(10),
    test_center_name varchar(30) not null,
    location varchar(20), 
    contact_number varchar(13) not null,
    primary key(test_center_id)
);

create table stock(
    batch_id int(10),
    blood_type varchar(3) check (blood_type in ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    quantity int(1000), 
    expiry_date datetime,
    category varchar(20),
    primary key(batch_id, category, quantity, blood_type)
);

create table donation_requests(
    request_id int(10),
    recipient_id int(10) not null,
    request_category varchar(20) not null, 
    blood_type varchar(3) check (blood_type in ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    quantity int(1000) not null,
    primary key(request_id),
    foreign key(recipient_id) references recipient on delete cascade,
    foreign key(quantity, blood_type, category) references stock on delete set null,
    foreign key(donation_category, blood_type) references donor on delete set null
);