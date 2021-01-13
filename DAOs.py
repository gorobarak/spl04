class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
                    INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?,?,?,?)
                    """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                    INSERT INTO suppliers (id, name, logistics) VALUES (?,?,?)
                    """, [supplier.id, supplier.name, supplier.logistics])


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


