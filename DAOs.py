class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self.currentId = 0
        self.usedIds = set()

    def insert(self, vaccine):
        self._conn.execute("""
                    INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?,?,?)
                    """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])


    def getNextAvaliableId(self):
        if self.currentId in self.usedIds:
            while self.currentId in self.usedIds:
                self.currentId += 1
        self.currentId += 1
        return self.currentId - 1


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                    INSERT INTO suppliers (id, name, logistics) VALUES (?,?,?)
                    """, [supplier.id, supplier.name, supplier.logistics])


    def getId(self, supplierName):
        c = self._conn.cursor()
        return c.exexute("SELECT id FROM suppliers WHERE name = ?", supplierName).fetchone()

    def getLogistic(self, supplierId):
        c = self._conn.cursor()
        return c.exexute("SELECT logistic FROM suppliers WHERE id = ?", supplierId).fetchone()


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
                    INSERT INTO clinics (id, location, demand, logistic) VALUES (?,?,?,?)
                    """, [clinic.id, clinic.slocation, clinic.demand, clinic.logistic])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
                    INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?,?,?,?)
                    """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def updateCountReceived(self, logisticId, amount):
        self._conn.execute("UPDATE logistics SET count_received = count_received + ? WHERE id = ?", (amount, logisticId))




