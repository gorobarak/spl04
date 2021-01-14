import atexit
import sqlite3

from DAOs import _Vaccines, _Suppliers, _Clinics, _Logistics
from DTOs import Vaccine, Supplier, Clinic, Logistic


class _Repository:


    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)
        self.inventory = 0
        self.demand = 0
        self.received = 0
        self.sent = 0


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

    def receive_shipment(self, name, amount, date):
        id = self.vaccines.getNextAvaliableId()
        supplierId = self.suppliers.getId(name)
        supplierLogisticId = self.suppliers.getLogistic(supplierId)
        self.vaccines.insert(Vaccine(id, date, supplierId, amount))  # new batch of vaccines
        self.logistics.increaseCountReceived(supplierLogisticId, amount)  # update count received for supplier
        self.inventory += amount
        self.received += amount

    # reduce amount from demand in clinic=location
    # add amount to count_sent of logistic working with clinic
    # send vaccines oldest first, delete batch if it becomes empty
    # assume enough vaccines in center
    #update status
    def send_shipment(self, location, amount):
        clinicId = self.clinics.getId(location)
        logisticId = self.clinics.getLogisticId(clinicId)
        self.clinics.reduceDemand(amount, clinicId)
        self.logistics.increaseCountSent(amount, logisticId)
        self.vaccines.sendVaccines(amount)
        self.inventory -= amount
        self.sent += amount
        self.demand -= amount

    def getStatus(self):
        return str(self.inventory) + ',' + str(self.demand) + ',' + str(self.received) + ',' + str(self.sent)




repo = _Repository()
atexit.register(repo.close)
