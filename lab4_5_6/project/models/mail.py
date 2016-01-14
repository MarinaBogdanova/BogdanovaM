import psycopg2

from lab4_5_6.project.models.fields.EmailField import EmailField
from lab4_5_6.project.models.fields.IdField import IdField
from lab4_5_6.project.models.fields.MessageField import MessageField
from lab4_5_6.project.models.fields.ThemeField import ThemeField

db = psycopg2.connect("dbname=db user=postgres password=hack_my_password_1234567890@qweqwe host=127.0.0.1 port=5432")


class Mail:
    # def __init__(self, **kwargs):
    #     if self.Check(theme + subject + from + to):
    #         self.theme = theme
    #     else:
    #         Errors += E.ggg
    #     try:
    #        self.theme = self.Check(theme)
    #     except:
    #         Errors += E.ggg
    #
    #     try:
    #        self.subject = self.Check(theme)
    #     except:
    #         Errors += E.hhhh
    #
    # if Errors is not empty:
    #     raise NotValidMail(Errors)

    def findById(self, id):
        try:
            cur = db.cursor()
            query = 'SELECT "id","to","from","theme","message" FROM mail WHERE id=%s LIMIT 1'
            cur.execute(query, [str(id)])
            res = cur.fetchone()
            cur.close()
            if res:
                self.id = IdField(res[0])
                self.to = EmailField(res[1])
                self.from_ = EmailField(res[2])
                self.theme = ThemeField(res[3])
                self.message = MessageField(res[4])
        except:
            raise

    def findByOffset(self, offset):
        try:
            cur = db.cursor()
            query = 'SELECT "id","to","from","theme","message" FROM mail LIMIT 1 OFFSET %s'
            cur.execute(query, [str(offset)])
            res = cur.fetchone()
            cur.close()
            if res:
                self.id = IdField(res[0])
                self.to = EmailField(res[1])
                self.from_ = EmailField(res[2])
                self.theme = ThemeField(res[3])
                self.message = MessageField(res[4])
                return 1
            return 0
        except:
            raise

    def save(self):
        try:
            cur = db.cursor()
            if hasattr(self, 'id'):
                query = 'UPDATE "mail" SET "theme"=%s,"to"=%s,"from"=%s,"message"=%s WHERE "id"=%s'
                cur.execute(query, [str(self.theme), str(self.to), str(self.from_), str(self.message), str(self.id)])
            else:
                query = 'INSERT INTO "mail" ("theme", "to", "from", "message") VALUES (%s, %s, %s, %s)'
                cur.execute(query, [str(self.theme), str(self.to), str(self.from_), str(self.message)])
            db.commit()
            cur.close()
        except:
            raise

    @staticmethod
    def count():
        try:
            cur = db.cursor()
            cur.execute("SELECT last_value FROM mail_id")
            res = cur.fetchone()[0]
            cur.close()
            return res
        except:
            raise




##########################
if __name__ == "__main__":
    try:
        m = Mail()
        m.from_ = EmailField("test@qwe.ru")
        m.to = EmailField("asd@asd.ru")
        m.theme = ThemeField("theme")
        m.message = MessageField("wow")
        m.save()
    except:
        raise
