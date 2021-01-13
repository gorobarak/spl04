import atexit
import sqlite3

from DAOs import _Vaccines, _Suppliers, _Clinics, _Logistics


class _Repository:
    def __init__(self):
        print("create repo")
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE logistics (
            id                INT         PRIMARY KEY,
            name              TEXT        NOT NULL,
            count_sent        INT        NOT NULL,
            count_received    INT        NOT NULL
        );
 
        CREATE TABLE suppliers (
            id           INT     PRIMARY KEY,
            name         TEXT    NOT NULL,
            logistic     INT    NOT NULL,
            
            FOREIGN KEY(logistic) REFERENCES logistics(id)
        );
 
        CREATE TABLE clinics (
            id           INT     PRIMARY KEY,
            location     TEXT    NOT NULL,
            demand       INT    NOT NULL,
            logistic     INT    NOT NULL,
            
            FOREIGN KEY(logistic) REFERENCES logistics(id)
         );
         
         CREATE TABLE vaccines (
            id          INT     PRIMARY KEY,
            date        DATE    NOT NULL,
            supplier     INT    NOT NULL,
            quantity     INT    NOT NULL,
            
            FOREIGN KEY(supplier) REFERENCES suppliers(id)
         );
    """)

    def receive_shipment(self,name, amount, date):


repo = _Repository()
atexit.register(repo.close)
