import requests
import sqlite3
import os
from collections import Counter

os.system("figlet data.police")

url = "https://data.police.uk/api/forces"
response = requests.get(url)

def mahsuc(isim , olay , olay_tarihi , mudahale_tarihi , genel_tanim):
	isim = isim + ".db"
	baglanti = sqlite3.connect(isim)
	cursor = baglanti.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS suclar(olay TEXT , olay_tarihi TEXT , mudahale_tarihi TEXT , genel_tanim TEXT)")
	baglanti.commit()
	cursor.execute("INSERT INTO suclar VALUES(?,?,?,?)",(olay , olay_tarihi , mudahale_tarihi , genel_tanim))
	baglanti.commit()
	baglanti.close()

def mahallesuc(isim , tanim , baslik , adres , tur , baslangic , bitis):

	isim = isim + ".db"
	baglanti = sqlite3.connect(isim)
	cursor = baglanti.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS suclar(tanim TEXT , baslik TEXT , adres TEXT , tur TEXT , baslangic TEXT , bitis TEXT)")
	baglanti.commit()
	cursor.execute("INSERT INTO suclar VALUES(?,?,?,?,?,?)",(tanim , baslik , adres , tur , baslangic , bitis))
	baglanti.commit()
	baglanti.close()

def mahalle(isim , idd , name):

	isim = isim + ".db"
	baglanti = sqlite3.connect(isim)
	cursor = baglanti.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS mahalleler(id TEXT , isim TEXT)")
	baglanti.commit()
	cursor.execute("INSERT INTO mahalleler VALUES(?,?)",(idd , name))
	baglanti.commit()
	baglanti.close()

def veritabani(isim , bolge , karakol):
	isim = isim + ".db"
	baglanti = sqlite3.connect(isim)
	cursor = baglanti.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS karakollar1 (bolge TEXT , karakol TEXT)")
	baglanti.commit()
	cursor.execute("INSERT INTO karakollar1 VALUES(?,?)",(bolge , karakol))
	baglanti.commit()
	baglanti.close()


def uc(isim , kategori , idd , kalici_id , tarih):
	isim = isim + ".db"
	baglanti = sqlite3.connect(isim)
	cursor = baglanti.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS tablo3 (kategori TEXT , idd INT , kalici_id TEXT , tarih INT)")
	baglanti.commit()
	cursor.execute("INSERT INTO tablo3 VALUES(?,?,?,?)",(kategori , idd , kalici_id , tarih))
	baglanti.commit()
	baglanti.close()

def dort(isim , suc , sayi):
	isim = isim + ".db"
	baglanti = sqlite3.connect(isim)
	cursor = baglanti.cursor()
	cursor.execute("CREATE TABLE IF NOT EXISTS suclar (suc_adi TEXT , suc_sayisi INT)")
	baglanti.commit()
	cursor.execute("INSERT INTO suclar VALUES(?,?)",(suc , sayi))
	baglanti.commit()
	baglanti.close()

menu = """
	[1] b??lgeler ve karakollar
	[2] tarihe g??re i??lenen su??lar
	[3] kategori,id,kal??c?? id,tarih
	[4] y??la ve ??ehre g??re su?? say??s??
	[5] konuma g??re en yak??n karakol bulma
	[6] veri taban?? son g????ncellenme tarihi
	[7] mahalleler ve id leri
	[8] mahalle id ye g??re su?? bulma
	[9] mahalle id ye g??re su?? ayr??nt??lar??
	[clear] ekran?? temizle
	[exit]  ????k???? yap
"""

while True:

	print(menu)
	islem = input("i??lem se??iniz : ")

	if islem == "1":
		print("url : {}".format(response.url))
		print("kod : {}".format(response.status_code))
		islem1 = input("????kt?? veri taban??na kaydedilsinmi : y/n : ")
		if (islem1 == "y" or islem1 == "Y"):
			isim = input("veri taban?? ad?? girin : ")		
			sayac = 0
			for i in response.json():
				sayac+=1				
				print("{}. b??lge ad??  : {}\n{}.karakol ad?? : {}\n**********************************************************".format(sayac,i["id"],sayac,i["name"]))
				veritabani(isim , i["id"] , i["name"])
		else:
			sayac = 0
			for i in response.json():
				sayac+=1				
				print("{}. b??lge ad??  : {}\n{}.karakol ad?? : {}\n**********************************************************".format(sayac,i["id"],sayac,i["name"]))
	
	elif islem == "2":

		url = "https://data.police.uk/api/crime-categories"
		tarih = input("tarih girin (??rnek tarih : 2012-04) : ")
		sonuc = {"date" : tarih}
		response = requests.get(url , params = sonuc)
		print(response.status_code)
		print(response.url)
		sayac = 0
		for i in response.json():
			sayac+=1
			print("{} : {}".format(sayac,i["name"]))
	
	elif islem == "3":
		url = "https://data.police.uk/api/crimes-no-location"
		kategori = input("su?? kategorisini giriniz : ")
		sehir = input("??ehir ad?? giriniz : ")
		tarih = input("tarih giriniz : ")
		sonuc = {'category' : kategori,
				 'force' : sehir,
				 'date' : tarih}
		response = requests.get(url , params = sonuc)
		kaydet = input("sonu??lar?? veri taban??na kaydetmek istermisiniz : y/n : ")
		if (kaydet == "y" or kaydet == "Y"): 
			isim = input("veri taban?? ad?? giriniz : ")
			for i in response.json():
				print("kategori : {}\nid : {}\nkal??c?? id : {}\ntarih : {}\n***********************".format(i["category"],i["id"],i["persistent_id"],i["month"]))
				uc(isim , i["category"] , i["id"] , i["persistent_id"] , i["month"])
		else:
			for i in response.json():
				print("kategori : {}\nid : {}\nkal??c?? id : {}\ntarih : {}\n***********************".format(i["category"],i["id"],i["persistent_id"],i["month"]))
	
	elif islem == "4":	
		kaydet = input("sonucu veri taban??na kaydetmek istermisiniz : (y/n) : ")
		if (kaydet == "y" or kaydet == "Y"):
			isim = input("veri taban?? ad?? giriniz : ")
			url = "https://data.police.uk/api/crimes-no-location"
			kategori = 'all-crime'
			sehir = input("??ehir ad?? giriniz : ")
			tarih = input("tarih giriniz : ")
			sonuc = {'category' : kategori,
					 'force' : sehir,
					 'date' : tarih}
			response = requests.get(url , params = sonuc)
			liste = []
			for i in response.json():
				liste.append(i["category"])
			a = Counter(liste)
			sozluk = dict(a)
			for i,j in sozluk.items():
				print("su?? ad?? : {}\nsu?? say??s?? : {}\n**************".format(i,j))
				dort(isim , i ,j)
		else:
			url = "https://data.police.uk/api/crimes-no-location"
			kategori = 'all-crime'
			sehir = input("??ehir ad?? giriniz : ")
			tarih = input("tarih giriniz : ")
			sonuc = {'category' : kategori,
					 'force' : sehir,
					 'date' : tarih}
			response = requests.get(url , params = sonuc)
			liste = []
			for i in response.json():
				liste.append(i["category"])
			a = Counter(liste)
			sozluk = dict(a)
			for i,j in sozluk.items():
				print("su?? ad?? : {}\nsu?? say??s?? : {}\n**************".format(i,j))
	
	elif islem == "5":

		url = "https://data.police.uk/api/locate-neighbourhood"
		konum = input("konum giriniz : ")
		sonuc = {'q' : konum}
		response = requests.get(url , params = sonuc)
		print(response.json())
	
	elif islem == "6":

		url = "https://data.police.uk/api/crime-last-updated"
		response = requests.get(url)
		print(response.json())

	elif islem == "7":

		url = "https://data.police.uk/api/leicestershire/neighbourhoods"
		response = requests.get(url)
		sonuc = input("sonu??lar veri taban??na kaydedilsinmi : (y/n) : ")
		if (sonuc == "y" or sonuc == "Y"):
			isim = input("veri taban?? isim giriniz : ")
			for i in response.json():
				print("mahalle id : {}\nmahalle ad?? : {}\n********************".format(i["id"],i["name"]))
				mahalle(isim , i["id"],i["name"])

		else:
			for i in response.json():
				print("mahalle id : {}\nmahalle ad?? : {}\n********************".format(i["id"],i["name"]))

	elif islem == "8":

		idd = input("mahalle id giriniz : ")
		url = "https://data.police.uk/api/leicestershire/" + idd + "/events"
		response = requests.get(url)
		secim = input("sonu??lar?? veri taban??na kaydetmek istermisin : (y/n) : ")
		if (secim == "y" or secim == "Y"):
			isim = input("veri taban?? ismi giriniz : ")
			for i in response.json():
				print("tan??m : {}\nba??l??k : {}\nadres : {}\nt??r : {}\nba??lang???? tarihi : {}\nbiti?? tarihi : {}\n**********************".format(i["description"],i["title"],i["address"],i["type"],i["start_date"],i["end_date"]))
				mahallesuc(isim , i["description"],i["title"],i["address"],i["type"],i["start_date"],i["end_date"])
		else:

			for i in response.json():
				print("tan??m : {}\nba??l??k : {}\nadres : {}\nt??r : {}\nba??lang???? tarihi : {}\nbiti?? tarihi : {}\n**********************".format(i["description"],i["title"],i["address"],i["type"],i["start_date"],i["end_date"]))
		

	
	elif islem == "9":

		idd = input("mahalle id giriniz : ")
		url = "https://data.police.uk/api/leicestershire/" + idd + "/priorities"
		response = requests.get(url)
		secim = input("sonu??lar?? veri taban??na kaydetmek istermisin : (y/n) : ")
		if (secim == "y" or secim == "Y"):
			isim = input("veri taban?? ismi giriniz : ")
			for i in response.json():
				print("olay : {}\nolay tarihi : {}\nm??dahale tarihi : {}\ngenel tan??m : {}\n**********************".format(i["action"],i["issue-date"],i["action-date"],i["issue"]))
				mahsuc(isim,i["action"],i["issue-date"],i["action-date"],i["issue"])
		else:
			for i in response.json():
				print("olay : {}\nolay tarihi : {}\nm??dahale tarihi : {}\ngenel tan??m : {}\n**********************".format(i["action"],i["issue-date"],i["action-date"],i["issue"]))
		

	elif islem == "clear":

		os.system("clear")

	elif islem == "exit":

		break

	else:
		print("hatal?? giri?? yapt??n??z.")

