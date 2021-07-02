try:
    from userbot.modules.sql_helper import SESSION, BASE
except ImportError:
    raise AttributeError

from sqlalchemy import Column, String, UnicodeText


class gbtban(BASE):
    __tablename__ = "gbtban"
    chat_id = Column(String(14), primary_key=True)
    gbt_name = Column(UnicodeText)

    def __init__(self, chat_id, gbt_name):
        self.chat_id = str(chat_id)
        self.gbt_name = gbt_name


gbtban.__table__.create(checkfirst=True)


def get_gbtlist():
    try:
        return SESSION.query(gbtban).all()
    finally:
        SESSION.close()


def add_gbtlist(chat_id, gbt_name):
    adder = gbtban(str(chat_id), gbt_name)
    SESSION.add(adder)
    SESSION.commit()


def del_gbtlist(chat_id):
    rem = SESSION.query(gbtban).get(str(chat_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def del_gbtlist_all():
    SESSION.execute("""TRUNCATE TABLE gbtban""")
    SESSION.commit()
