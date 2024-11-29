from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)

Base = declarative_base()
engine = create_engine("sqlite:///mydb.db", echo=True)
Session = sessionmaker(bind=engine)

class Person(Base):
    __tablename__ = "people"
    ssn = Column(Integer, primary_key=True)
    firstname = Column("Firstname", String)
    lastname = Column(String)
    gender = Column(CHAR(1))
    age = Column(Integer)
    password = Column(String)
    role = Column(String)

    def __init__(self, _ssn, firstname, lastname, gender, age, password, role):
        self.ssn = _ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age
        self.password = password
        self.role = role

    def __repr__(self):
        return (f"Person(ssn={self.ssn}, firstname='{self.firstname}', "
                f"lastname='{self.lastname}', gender='{self.gender}', age='{self.age}', password='{self.password}', role='{self.role}')")
    
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)




@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ssn = request.form.get('ssn')
        password = request.form.get('password')



        db_session = Session()

        person = db_session.query(Person).filter_by(ssn=ssn, password=password).first()

        print("---------------------------------------------------")
        print(ssn)
        print(password)
        print(person)
        print("---------------------------------------------------")

        
        db_session.close()

        
        if person.role=="admin" and person:
            return redirect(url_for('admin'))
        elif person.role=="teacher" and person:
            return redirect(url_for('teacher'))
        elif person.role=="student" and person:
            return redirect(url_for('student'))

        else:
            return render_template('login.html', title="Login", text="Invalid SSN or password. Please try again.")
    
    return render_template('login.html', title="Login", text="Welcome to the login page!")

@app.route('/admin')
def admin():
    return render_template('admin.html', title="admin", text="Successful!")

@app.route('/teacher')
def teacher():
    return render_template('teacher.html', title="teacher", text="Successful!")

@app.route('/student')
def student():
    return render_template('student.html', title="student", text="Successful!")

@app.route('/viewuser', methods=['GET', 'POST'])
def viewuser():
    session = Session()
    try:
        all_people = session.query(Person).all()
        print("----------------------------------")
        print(all_people)

        # Pass all_people to the template
        if all_people:
            return render_template('viewuser.html', title="View Users", people=all_people)
        else:
            return render_template('viewuser.html', title="View Users", people=None, text="No users found.")
    finally:
        session.close()



@app.route('/updateuser', methods=['GET', 'POST'])
def updateuser(): 
    if request.method == 'POST':
        session = Session()
        user_update = request.form.get('ssn')
        new_firstname = request.form.get('firstname')
        new_lastname = request.form.get('lastname')
        new_gender = request.form.get('gender')
        new_age = request.form.get('age')
        new_password = request.form.get('password')
        new_role = request.form.get('role')

        try:
            person = session.query(Person).filter_by(ssn=user_update).first()

            if person:
                person.firstname = new_firstname or person.firstname
                person.lastname = new_lastname or person.lastname
                person.gender = new_gender or person.gender
                person.age = new_age or person.age
                person.password = new_password or person.password
                person.role = new_role or person.role

                person.firstname = new_firstname
                person.lastname = new_lastname
                person.gender = new_gender
                person.age = new_age
                person.password = new_password
                person.role = new_role

                session.commit()
                print(f"Updated: {person}")

            else:
                print("No person found with that SSN.")

        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()

        finally:
            session.close()
            
    return render_template('updateuser.html', title="updateuser", text="Successful!")

@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        session = Session()
        ssn = request.form.get('ssn')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        gender = request.form.get('gender')
        age = request.form.get('age')
        password = request.form.get('password')
        role = request.form.get('role')
        try:
            

            new_person = Person(ssn, firstname, lastname, gender, age, password, role)

            session.add(new_person)
            session.commit()
            print(f"Added: {new_person}")

        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()

        finally:
            session.close()

    return render_template('adduser.html', title="adduser", text="Successful!")

@app.route('/deleteuser', methods=['GET', 'POST'])
def deleteuser():
     if request.method == 'POST':
        session = Session()
        delete = request.form.get('delete')
        try:
            user_sign = delete
            person = session.query(Person).filter_by(ssn=user_sign).first()
            if person:
                session.delete(person)
                session.commit()
                print(f"Removed: {person}")
            else:
                print("Invalid user")
        finally:
            session.close()


     return render_template('deleteuser.html', title="deleteuser", text="Successful!")





if __name__ == '__main__':
    app.run(debug=True)
