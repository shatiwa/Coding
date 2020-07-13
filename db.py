
import sqlite3


class DB:
    def __init__(self, dbname="details.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS INFO(Name text, College text, Sideproject text, Language text, Framework text, Board text, Confirm text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, Name, City, Locality, Pincode, Modeofcontact, MailID, Phone_Number, Requirements, Board, Standard, Medium, Subjects, Deal_Type):
        stmt = "INSERT INTO INFO (Name, College, Sideproject, Language, Framework, Confirm) VALUES (?, ?, ?, ?, ?, ?)"
        args = ( Name, College, Sideproject, Language, Framework, Confirm)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT Name, College, Sideproject, Language, Framework, Confirm FROM INFO"
        return [x for x in self.conn.execute(stmt)]
