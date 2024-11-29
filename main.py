from sqlalchemy import create_engine, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

Base = declarative_base()


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


def add_person():
    session = Session()
    a,b,c = display_people()
    try:
        ssn = int(input("Enter SSN: "))
        firstname = input("Enter First Name: ")
        lastname = input("Enter Last Name: ")
        gender = input("Enter Gender (M/F): ").upper()
        age = int(input("Enter Age: "))
        password = input("Create password: ")
        role = input("Enter their position: ")

        new_person = Person(ssn, firstname, lastname, gender, age, password, role)

        session.add(new_person)
        session.commit()
        print(f"Added: {new_person}")

    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()

    finally:
        session.close()


def remove_person():
    session = Session()
    a,b,c = display_people()
    try:
        user_sign = input("Enter user to remove: ")
        person = session.query(Person).filter_by(ssn=user_sign).first()
        if person:
            session.delete(person)
            session.commit()
            print(f"Removed: {person}")
        else:
            print("Invalid user")
    finally:
        session.close()


def sign_in():
    global role
    session = Session()
    a,b,c = display_people()

    try:
        user_sign = input("1. Enter SSN to sign in: ")
        password_sign = input("2. Enter password: ")
        print("-------------------------------------------------")

        person = session.query(Person).filter_by(ssn=user_sign, password=password_sign).first()

        if person:
            print(f"Sign-in successful! Welcome, {person.firstname}.")
            role = person.role
            return "valid"
        else:
            print("Invalid SSN or password.")
            return "invalid"
    finally:
        session.close()


def display_people():
    session = Session()
    try:
        all_people = session.query(Person).all()
        for person in all_people:
            print(person)  # This will now show detailed info for each person
        print("----------------------------------")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()
    return "Done"


def update_user():
    session = Session()
    a,b,c = display_people()
    try:
        user_update = input("Enter SSN of the person to update: ")
        person = session.query(Person).filter_by(ssn=user_update).first()

        if person:
            print("--------------------------------------------------------------------------------------------------")
            print(f"Found: {person}")

            new_firstname = input(f"""--------------------------------------------------------------------------------------------------
1. Enter new First Name (leave blank to keep '{person.firstname}'): """) or person.firstname
            new_lastname = input(
                f"2. Enter new Last Name (leave blank to keep '{person.lastname}'): ") or person.lastname
            new_gender = input(
                f"3. Enter new Gender (M/F) (leave blank to keep '{person.gender}'): ").upper() or person.gender
            new_age = input(f"4. Enter new Age (leave blank to keep '{person.age}'): ") or person.age
            new_password = input(f"5. Enter new Password (leave blank to keep current): ") or person.password
            new_role = input(f"6. Enter new role (leave blank to keep current): ") or person.role
            print("--------------------------------------------------------------------------------------------------")

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


# use the role part which shows what role it is to decide the output

def grades():
    if role == "teacher":
        print("teacher all student grades")
    elif role == "student":
        print("student grades")
    else:
        pass


def timetable():
    if role == "teacher":
        print("teacher timetable")
    elif role == "student":
        print("student timetable")
    else:
        pass


def teacher_menu():
    while True:
        menu_choice = int(input("""\
-------------------------------------------------
1. view your students grades
2. view timetable
3. Exit
-------------------------------------------------
Enter your choice: """))
        print("-------------------------------------------------")
        if menu_choice == 1:
            grades()
        elif menu_choice == 2:
            timetable()
        elif menu_choice == 3:
            print("""-------------------------------------------------
                    Exiting
-------------------------------------------------""")
            sys.exit()
        else:
            print("""-------------------------------------------------
                    Invalid input
-------------------------------------------------""")


def student_menu():
    while True:
        menu_choice = int(input("""\
-------------------------------------------------
1. view grades
2. view timetable 
3. Exit
-------------------------------------------------
Enter your choice: """))
        print("-------------------------------------------------")
        if menu_choice == 1:
            grades()
        elif menu_choice == 2:
            timetable()
        elif menu_choice == 3:
            print("""-------------------------------------------------
                    Exiting
-------------------------------------------------""")
            sys.exit()
        else:
            print("""-------------------------------------------------
                    Invalid input
-------------------------------------------------""")


def admin_menu():
    while True:
        menu_choice = int(input("""\
-------------------------------------------------
1. Add a new person to the database
2. Remove a person from the database 
3. Display people
4. Update user data
5. Exit
-------------------------------------------------
Enter your choice: """))
        print("-------------------------------------------------")
        if menu_choice == 1:
            add_person()
        elif menu_choice == 2:
            remove_person()
        elif menu_choice == 3:
            display_people()
        elif menu_choice == 4:
            update_user()
        elif menu_choice == 5:
            print("""-------------------------------------------------
                    Exiting
-------------------------------------------------""")
            sys.exit()
        else:
            print("""-------------------------------------------------
                Invalid input
-------------------------------------------------""")


def menu_selector():

    password_sign_in = sign_in()  # Update this line to store the return value

    if password_sign_in == "valid" and role == "admin":
        return "admin"
    elif password_sign_in == "valid" and role == "teacher":
        return "teacher"
    elif password_sign_in == "valid" and role == "student":
        return "student"
    else:
        print("Invalid login. Please try again.")
        return None


def send_menu():
    global savedrole
    savedrole = menu_selector()

    if savedrole == "admin":
        admin_menu()
    elif savedrole == "teacher":
        teacher_menu()
    elif savedrole == "student":
        student_menu()
    else:
        send_menu()

# In your main program flow, you can simply call send_menu()
if __name__ == "__main__":
    send_menu()
