from Repository import repo
import sys
from DTOs import Vaccine, Supplier, Clinic, Logistic

def fixDate(date):
    v = date.split('-')
    v[-1] = '0' + v[-1] if len(v[-1]) == 1 else v[-1]
    return "-".join(v)


def parseConfig(file):
    with open(file) as configFile:
        entries = configFile.readline().split(',')
        # vaccines
        print(entries)
        for i in range(0, int(entries[0])):
            nextline = configFile.readline().split(',')
            date = fixDate(nextline[1].replace('−','-'))
            quantity = int(nextline[3])
            vac = Vaccine(int(nextline[0]), date, int(nextline[2]), quantity)
            repo.vaccines.insert(vac)
            repo.inventory += quantity

        # suppliers
        for i in range(0, int(entries[1])):
            nextline = configFile.readline().split(',')
            supplier = Supplier(int(nextline[0]), nextline[1], int(nextline[2]))
            repo.suppliers.insert(supplier)

        # clinics
        for i in range(0, int(entries[2])):
            nextline = configFile.readline().split(',')
            demand = int(nextline[2])
            clinic = Clinic(int(nextline[0]), nextline[1], demand, int(nextline[3]))
            repo.clinics.insert(clinic)
            repo.demand += demand

        # logistics
        for i in range(0, int(entries[3])):
            nextline = configFile.readline().split(',')
            logistic = Logistic(int(nextline[0]), nextline[1], int(nextline[2]), int(nextline[3]))
            repo.logistics.insert(logistic)

def executeOrders(orders, output):
    with open(orders) as ordersFile, open(output,'w') as outputFile:
        for line in ordersFile:
            order = line.split(",")

            # recieve shipment
            if len(order) == 3:
                order[1] = int(order[1])
                order[2] = fixDate(order[2].replace('−','-'))
                repo.receive_shipment(*order)

            # send shipment
            if len(order) == 2:
                order[1] = int(order[1])
                repo.send_shipment(*order)

            outputFile.write(repo.getStatus() + '\n')



def main():
    repo.create_tables()
    parseConfig(sys.argv[1])
    executeOrders(sys.argv[2], sys.argv[3])



if __name__ == '__main__':
    main()

