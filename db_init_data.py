"""
JUST A SAMPLE SCRIPT.
NEEDS TO BE MODIFIED FOR YOUR PARTICULAR DB/MODEL STRUCTURE.
"""
from app.db_models import db, Member # RELEVANT TABLES


def init_data():
    'Centres first, Administrators second'
    if db.session.query(Member).count() == 0:
        donal = Member(firstname='donal', surname='carville', email='d@gmail.com',
                       password='dash', adminr=True)
        matt = Member(firstname='matt', surname='sheridan', email='m@gmail.com',
                      password='mash', adminr=True)
        db.session.add_all([donal, matt])
    db.session.commit()


if __name__ == '__main__':
    init_data()
