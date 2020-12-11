from app import db,Administrator,generate_random_id,Login

email='admin@bloodmate.com'
password='qwerty'
user_type='admin'
name='King'
id=generate_random_id()
new_user=Administrator(id=id,email_id=email,name=name)

new_login = Login(id=id,email_id=email,password=password,user_type=user_type)

try:
    db.session.add(new_user)
    db.session.add(new_login)
    db.session.commit()
    print('done')
except Exception as e:
    print(e)
    print('Not Done')