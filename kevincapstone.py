from tabulate import tabulate
from datetime import date
import regex as re

invoiceData = [{'invoiceId': 1, 'invoiceNo': 'inv-1', 'buyerName': 'kevin', 'items': [{'itemName': 'bantal', 'qty': 1, 'price': 500.0}, {'itemName': 'guling', 'qty': 1, 'price': 500.0}], 'grandTotal': 1000.0, 'transactionDate': '18/02/2024'},
               {'invoiceId': 2, 'invoiceNo': 'inv-2', 'buyerName': 'verine', 'items': [{'itemName': 'bantal', 'qty': 1, 'price': 500.0}, {'itemName': 'guling', 'qty': 1, 'price': 500.0}], 'grandTotal': 1000.0, 'transactionDate': '18/02/2024'}]

user = [{"username": "kevin", "password": "admin123"}]

items = []

def homePage():
    print("Selamat datang di applikasi kasir tokolakpisang \n silahkan login")
    username = input("Masukkan Username: ")
    password = input("Masukkan Password: ")
    isValid = checkUserPassword(username, password)
    if isValid:
        mainMenu()

def checkUserPassword(username, password):
    while True:
        for i in user:
            if username == i["username"] and password == i["password"]:
                return True
            else:
                print("password atau username salah")
                username = input("Masukkan Username: ")
                password = input("Masukkan Password: ")

def mainMenu():
    while True:
        try:
            printGrid()
            print('\n1. Lihat Transaksi')
            print('2. Tambah Transaksi')
            print('3. Filter Transaksi')
            print('4. Update Transaksi')
            print('5. Hapus Transaksi')
            print('6. exit')
            choose = int(input("mau lihat menu apa: "))
            if (choose < 1 or choose > 6):
                print("input angka 1-6")
            elif choose == 1:
               readTransaction()
            elif choose == 2:
                while True:
                    buyerName = input("masukkan nama pembeli: ")
                    if buyerName.isalpha():
                        break
                    else:
                        print("Nama harus alphabet")

                item = addItems()
                addTransaction(buyerName, item)
            elif choose == 3:
                readTransaction()
                if len(invoiceData) > 0:
                    print('1. Filter by tanggal')
                    print('2. Filter by nama Pembeli')
                    while True:
                        try:
                            filterBy = int(input("masukkan pilihannmu: "))
                            if (filterBy == 1 or filterBy == 2):
                                filteredTransaction(filterBy)
                                break
                            else:
                                print("Inputan harus 1/2")
                                continue
                        except:
                            print("Inputan Harus Angka")

            elif choose == 4:
                readTransaction()
                if len(invoiceData) > 0:
                    invoiceNo = input("Masukkan nomor invoice yang mau di update: ")
                    updateTransaction(invoiceNo)
            elif choose == 5:
                readTransaction()
                if len(invoiceData) > 0:
                    invoiceNo = input("Masukkan nomor invoice yang mau dihapus: ")
                    deleteTransaction(invoiceNo)
            else:
                break
        except:
            print('harus diisi dengan angka')

def printGrid():
    for i in range(1, 25):
        print("=", end="=")

def readTransaction():
    # printGrid()
    if len(invoiceData) == 0:
        print("\nBelum ada transaksi terbuat")
    else:
        readableList = []
        for i in invoiceData:
            readableList.append({
                "invoiceId": i["invoiceId"],
                "invoiceNo": i["invoiceNo"],
                "buyerName": i["buyerName"],
                "transactionDate": i["transactionDate"],
                **i["items"][0],
                "grandTotal": i["grandTotal"]
            })
            for detail in i["items"][1:]:
                readableList.append({
                     "invoiceId": "",
                     "invoiceNo": "",
                     "buyerName": "",
                     "transactionDate": "",
                     **detail,
                     "grandTotal": ""
                })
        headers = readableList[0].keys()
        data = [list(i.values()) for i in readableList]
        printGrid()
        print(tabulate(data, headers = headers, tablefmt='pretty'))


def addTransaction(buyerName, soldItems):
    grandTotal = calculateGrandTotal(soldItems)
    if len(invoiceData) == 0:
        lastId = 1
        invoiceNo = f'inv-{lastId}'
    else:
        lastId = invoiceData[-1]["invoiceId"]+1
        invoiceNo = f'inv-{invoiceData[-1]["invoiceId"]+1}'

    i = {
        "invoiceId": lastId,
        "invoiceNo": invoiceNo,
        "buyerName": buyerName,
        "items": soldItems,
        "grandTotal": grandTotal,
        "transactionDate": date.today().strftime("%d/%m/%Y")
    }
    invoiceData.append(i)
    res = invoiceData
    print('data berhasil ditambahkan')
    # print(res)
    return res

def addItems():
    while True:
        itemName = input("masukkan item: ")
        while True:
            try:
                qty = int(input("berapa? "))
                break
            except:
                print('harus int')
        while True:
            try:
                price = float(input("harga satuan: "))
                break
            except:
                print("harus numeric")
        i = {
            "itemName": itemName,
            "qty": qty,
            "price": price
        }
        items.append(i)
        while True:
            addMoreItems = input("apakah mau nambah barang?: ")
            if addMoreItems.lower() == 'y':
                break
            elif addMoreItems.lower() == 'n':
                res = items.copy()
                items.clear()
                return res
            else:
                print("harus y/n")
        
def calculateGrandTotal(soldItems):
    grandTotal = 0
    for item in soldItems:
        grandTotal += item["qty"] * item["price"]
    return grandTotal
        
def readOneTransaction(invoiceNo):
        for i in invoiceData:
            if invoiceNo.lower() == i["invoiceNo"].lower():
                return i
            else:
                continue

def deleteTransaction(invoiceNo):
    while True:
        isValid = readOneTransaction(invoiceNo)
        if isValid:
            for i in invoiceData:
                    if i["invoiceNo"].lower() == invoiceNo.lower():
                        invoiceData.remove(i)
                        print("berhasil dihapus")
                        return True
        else:
            print('invoice tidak ada')
            invoiceNo = input("masukkan transaksi yang mau dihapus: ")

def updateTransaction(invoiceNo): 
    while True: 
        isValid = readOneTransaction(invoiceNo)
        if isValid:
            for i in invoiceData:
                if i["invoiceNo"].lower() == invoiceNo.lower():
                    itemsUpdate = addItems()
                    i["items"].extend(itemsUpdate)
                    grandTotal = calculateGrandTotal(i["items"])
                    i['grandTotal'] = grandTotal
                    print("Data berhasil di Update")
                    return True
        else:
            print("invoice tidak ada")
            invoiceNo = input("Masukkan nomor invoice yang mau di update: ")

def readFilteredTransaciton(type):
    readableList = []
    for i in invoiceData:
        if (type.lower() == i["buyerName"].lower() or type == i['transactionDate']):
            readableList.append({
                 "invoiceId": i["invoiceId"],
                 "invoiceNo": i["invoiceNo"],
                 "buyerName": i["buyerName"],
                 "transactionDate": i["transactionDate"],
                 **i["items"][0],
                 "grandTotal": i["grandTotal"]
            })
            for detail in i["items"][1:]:
                readableList.append({
                    "invoiceId": "",
                    "invoiceNo": "",
                    "buyerName": "",
                    "transactionDate": "",
                    **detail,
                    "grandTotal": ""
            })
    if len(readableList) > 0:
        headers = readableList[0].keys()
        data = [list(i.values()) for i in readableList]
        printGrid()
        print()
        print(tabulate(data, headers = headers, tablefmt='pretty'))
    else:
        print("tidak ada data yg sesuai")

def filteredTransaction(filter):
    if filter  == 1:
        while True:
            tanggal = input("masukkan tanggal transaksi: ")
            if re.fullmatch(r'\d{2}/\d{2}/\d{4}', tanggal):
                break
            else:
                print("format tanggal harus dd/mm/yyyy")
        readFilteredTransaciton(tanggal)
    elif filter == 2:
       while True:
        name = input("Masukkan Nama: ")
        if name.isalpha():
            break
        else:
            print("Nama Harus alphabet")
       readFilteredTransaciton(name)

homePage()