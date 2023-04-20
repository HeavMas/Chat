from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session


engine = create_engine('sqlite:///chatbase.db')

class Base(DeclarativeBase): pass

class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(15))
    login = Column(String(15))
    password = Column(String(10))

Base.metadata.create_all(bind=engine)

def reg_usr(log, pas, name):
    with Session(autoflush=False, bind=engine) as db:
        new_user = Users(login=log, name=name, password=pas)
        db.add(new_user)
        db.commit()
    db.close()
def usr_list():
    with Session(autoflush=False, bind=engine) as db:
        request = db.query(Users)
        for user in request:
            print(user.name, user.login, user.password)
    db.close()

def del_usr(log):
    with Session(autoflush=False, bind=engine) as db:
        film = db.query(Users).filter(Users.login == log).first()
        db.delete(film)
        db.commit()
        db.close()

def find_usr(log, paswd):
    with Session(autoflush=False, bind=engine) as db:
        answ = False
        usrpas = db.query(Users.password).where(Users.login.like(log))
        for i in usrpas:
            if paswd == i[0]:
                answ = True
                return answ
            else:
                return answ
        answ = "WL"
        return answ

def find_name(log):
    with Session(autoflush=False, bind=engine) as db:
        usrpas = db.query(Users.name).where(Users.login.like(log))
        for i in usrpas:
            return i[0]
