class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self.currentId = 1
        self.usedIds = set()

    def insert(self, vaccine):
        self._conn.execute("""
                    INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?,?,?)
                    """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])
        self.usedIds.add(vaccine.id)

    def getNextAvaliableId(self):
        if self.currentId in self.usedIds:
            while self.currentId in self.usedIds:
                self.currentId += 1
        self.currentId += 1
        return self.currentId - 1

    def sendVaccines(self, amount):
        c = self._conn.cursor()
        while amount > 0:
            oldestVac = c.execute("""SELECT id, quantity FROM vaccines
                                WHERE date = (SELECT MIN(date) FROM vaccines)""").fetchone()
            id = oldestVac[0]
            availableQuantity = oldestVac[1]
            if availableQuantity > amount:
                self.reduceQuantity(id, amount)
                amount = 0
            else:
                amount = amount - availableQuantity
                self.deleteBatch(id)

    def reduceQuantity(self, id, amount):
        self._conn.execute("UPDATE vaccines SET quantity = quantity - ? WHERE id = ?", (amount, id))

    def deleteBatch(self, id):
        self._conn.execute("DELETE FROM vaccines WHERE id = ?", (id,))


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                    INSERT INTO suppliers (id, name, logistic) VALUES (?,?,?)
                    """, [supplier.id, supplier.name, supplier.logistic])

    def getId(self, supplierName):
        c = self._conn.cursor()
        return int(c.execute("SELECT id FROM suppliers WHERE name = ?", (supplierName,)).fetchone()[0])

    def getLogistic(self, supplierId):
        c = self._conn.cursor()
        return int(c.execute("SELECT logistic FROM suppliers WHERE id = ?", (supplierId,)).fetchone()[0])


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
                    INSERT INTO clinics (id, location, demand, logistic) VALUES (?,?,?,?)
                    """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def getId(self, location):
        c = self._conn.cursor()
        return int(c.execute("SELECT id FROM clinics WHERE location = ?", (location,)).fetchone()[0])

    def getLogisticId(self, clinicId):
        c = self._conn.cursor()
        return int(c.execute("SELECT logistic FROM clinics WHERE id = ?", (clinicId,)).fetchone()[0])

    def reduceDemand(self, amount, clinicId):
        self._conn.execute("UPDATE clinics SET demand = demand - ? WHERE id = ?", (amount, clinicId))


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
                    INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?,?,?,?)
                    """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def increaseCountReceived(self, logisticId, amount):
        self._conn.execute("UPDATE logistics SET count_received = count_received + ? WHERE id = ?",
                           (amount, logisticId))

    def increaseCountSent(self, amount, logisticId):
        self._conn.execute("UPDATE logistics SET count_sent = count_sent + ? WHERE id = ?", (amount, logisticId))
