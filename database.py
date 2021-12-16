from typing import ValuesView
import psycopg2
from psycopg2 import connect, sql, extensions
import sys
from prettytable import PrettyTable

db = psycopg2.connect(
    user = "postgres",
    password = "02042001",
    host = "localhost",
    port = "5432",
    database = "otobusApp_db"
)

cursor = db.cursor()
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
db.set_isolation_level(autocommit)

class Fonksiyonlar:
    def subeGetir():
        query_Subeler_select = """
            SELECT * FROM subegetir()
            """
        cursor.execute(query_Subeler_select)
        subeler = cursor.fetchall()
        tablo = PrettyTable(['ŞubeID','Şube Adı'])
        for sube in subeler:
            tablo.add_row(sube)
        print(tablo)  
    def meslekGetir():
        query_CalisanlarTur_select = """
        SELECT * FROM meslekgetir()
        """
        cursor.execute(query_CalisanlarTur_select)
        turler = cursor.fetchall()
        tablo = PrettyTable(['MeslekID','Meslek Adı'])
        for tur in turler:
            tablo.add_row(tur)
        print(tablo)
    def markaGetir():
        query_Markalar_select = """
        SELECT * FROM markagetir() 
        """
        cursor.execute(query_Markalar_select)
        markalar = cursor.fetchall()
        tablo = PrettyTable(['MarkaID', 'Marka Adı','Marka Modeli'])
        for marka in markalar:
            tablo.add_row(marka)
        print(tablo)   
    def calisanGetir():
        query_Calisanlar_select = """
        SELECT * FROM calisangetir()
        """
        cursor.execute(query_Calisanlar_select)
        calisanlar = cursor.fetchall()
        tablo = PrettyTable(['PersonelID','İsim','Soyisim','Meslek'])
        for calisan in calisanlar:
            tablo.add_row(calisan)
        print(tablo)
    def cinsiyetGetir():
        query_Cinsiyetler_select = """
        SELECT * FROM cinsiyetgetir()
        """
        cursor.execute(query_Cinsiyetler_select)
        cinsiyetler = cursor.fetchall()
        tablo = PrettyTable(['CinsiyetID', 'Cinsiyet Adı'])
        for cinsiyet in cinsiyetler:
            tablo.add_row(cinsiyet)
        print(tablo)  
    def seferGetir():
        query_Seferler_select = """
        SELECT * FROM sefergetir()
        """
        cursor.execute(query_Seferler_select)
        seferler = cursor.fetchall()
        tablo = PrettyTable(['SeferID','Kalkış Zamanı','Varış Zamanı','Tutar','OtobusID'])
        for sefer in seferler:
            tablo.add_row(sefer)
        print(tablo)
    def koltukGetir():
        query_Koltuklar_select = """
        SELECT * FROM Koltuklar
        """
        cursor.execute(query_Koltuklar_select)
        koltuklar = cursor.fetchall()
        tablo = PrettyTable(['OtobusKoltukID','Boş Koltuk Sayısı', 'OtobusID'])
        for koltuk in koltuklar:
            tablo.add_row(koltuk)
        print(tablo)
    
class Musteriler:
    def MusteriEkle():
        musteriAd = input("Müşteri adını giriniz: ")
        musteriSoyad = input("Müşteri soyadını giriniz: ")
        musteriEmail = input("Müşteri e-mailini giriniz (kamilkoc@koc.com gibi): ")
        musteriTelefon = input("Müşteri telefon numarasını giriniz (90123456789 gibi): ")
        Fonksiyonlar.cinsiyetGetir()
        musteriCinsiyet = input("Müşterinin Cinsiyet ID'sini seçiniz: ")
        musteriDogumTarihi = input("Müşteri doğum tarihini giriniz (01-01-1990 gibi): ")

        sql = "INSERT INTO Musteriler (name,surname,email,phoneNumber,dateBirth,cinsiyetID) VALUES(%s,%s,%s,%s,%s,%s)"
        values = (musteriAd,musteriSoyad,musteriEmail,musteriTelefon,musteriDogumTarihi,musteriCinsiyet)

        cursor.execute(sql,values)  
        print(f"\n{musteriAd} {musteriSoyad} adlı müşteri başarıyla eklendi.")  
    def MusteriGoruntule():
        query_Musteri_select = """
        SELECT musteriler.musteriid,musteriler.name,musteriler.surname,cinsiyet.cinsiyetAdi FROM musteriler 
        JOIN cinsiyet ON musteriler.cinsiyetid = cinsiyet.cinsiyetID
        """ 
        cursor.execute(query_Musteri_select)
        musteriler = cursor.fetchall()
        
        tablo = PrettyTable(['MüşteriID','İsim','Soyisim','Cinsiyet'])
        for musteri in musteriler:
            tablo.add_row(musteri)
        print(tablo)
    def MusteriGuncelle():
        Musteriler.MusteriGoruntule()

        print("Düzenlemek istediğiniz müşterinin ID'sini giriniz.")
        guncelleSecim = int(input("Lütfen ID giriniz: "))

        query_Musteri_select = """
        SELECT musteriler.musteriid,musteriler.name,musteriler.surname,cinsiyet.cinsiyetAdi FROM musteriler JOIN cinsiyet ON musteriler.cinsiyetid = cinsiyet.cinsiyetID
        """ 
        cursor.execute(query_Musteri_select)
        musteriler = cursor.fetchall()
        
        for musteri in musteriler:
            if(musteri[0] == guncelleSecim):
                musteriAd = input("Müşteri adını giriniz: ")
                musteriSoyad = input("Müşteri soyadını giriniz: ")
                musteriEmail = input("Müşteri e-mailini giriniz (kamilkoc@koc.com gibi): ")
                musteriTelefon = input("Müşteri telefon numarasını giriniz (90123456789 gibi): ")
                Fonksiyonlar.cinsiyetGetir()
                musteriCinsiyet = input("Müşterinin Cinsiyet ID'sini seçin: ")
                musteriDogumTarihi = input("Müşteri doğum tarihini giriniz (01-01-1990 gibi): ")

                query_Musteri_update = """
                UPDATE Musteriler SET name=%s, surname=%s, email=%s, phoneNumber=%s, dateBirth=%s, cinsiyetID=%s WHERE musteriid=%s
                """
                cursor.execute(query_Musteri_update,(musteriAd,musteriSoyad,musteriEmail,musteriTelefon,musteriDogumTarihi,musteriCinsiyet,guncelleSecim))

                count = cursor.rowcount
                print(f"\n{count} kayıt başarıyla güncellenmiştir.")
    def MusteriSil():
        Musteriler.MusteriGoruntule()

        print("Silmek istediğiniz müşterinin ID'sini giriniz.")
        silSecim = input("Lütfen ID giriniz: ")
        query_Musteri_delete = """
        DELETE FROM Musteriler WHERE musteriid={0}
        """.format(silSecim)
        cursor.execute(query_Musteri_delete,silSecim)

        count = cursor.rowcount
        print(f"\n{count} kayıt başarıyla silinmiştir.")
    def MusteriSayisi():
        sql = """
        SELECT * FROM toplammusteriler
        """
        cursor.execute(sql)
        musteriSayisi = cursor.fetchone()
        print("\nTOPLAM MÜŞTERİ SAYISI: ", musteriSayisi[0])
class Calisanlar:
    def calisanGoruntule():
        query_Calisanlar_select = """
        SELECT calisanlar.personelid,calisanlar.name,calisanlar.surname,subeler.subeadi,calisanlarturu.meslekadi FROM calisanlar 
        JOIN subeler ON calisanlar.subeid = subeler.subeid 
        JOIN calisanlarturu ON calisanlar.calisanlarturid = calisanlarturu.calisanlarturid
        """
        cursor.execute(query_Calisanlar_select)
        calisanlar = cursor.fetchall()
        tablo = PrettyTable(['PersonelID','İsim','Soyisim','Şube İsmi','Meslek'])
        for calisan in calisanlar:
            tablo.add_row(calisan)
        print(tablo)
    def calisanEkle():
        calisanAd = input("Çalışan ismini giriniz: ")
        calisanSoyad = input("Çalışan soyadını giriniz: ")
        calisanEmail = input("Çalışan e-mailini giriniz (kamilkoc@koc.com gibi): ")
        calisanTelefon = input("Çalışan telefon numarasını giriniz (90123456789 gibi): ")
        calisanAdres = input("Çalışan adresini yazınız: ")
        Fonksiyonlar.subeGetir()
        calisanSube = input("Çalışan kişinin Şube ID'sini seçiniz: ")
        Fonksiyonlar.meslekGetir()
        calisanTur = input("Çalışanın meslek ID'sini seçiniz: ")

        sql = "INSERT INTO Calisanlar (name,surname,email,phoneNumber,adress,subeid,calisanlarturID) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values = (calisanAd,calisanSoyad,calisanEmail,calisanTelefon,calisanAdres,calisanSube,calisanTur)
  
        cursor.execute(sql,values)
        print(f"\n{calisanAd} {calisanSoyad} adlı çalışan başarıyla eklendi.")        
    def calisanGuncelle():
        Calisanlar.calisanGoruntule()
        print("Düzenlemek istediğiniz çalışanın ID'sini giriniz.")
        guncelleSecim = int(input("Lütfen ID giriniz: "))

        query_Calisanlar_select = """
        SELECT * FROM Calisanlar
        """
        cursor.execute(query_Calisanlar_select)
        calisanlar = cursor.fetchall()

        for calisan in calisanlar:
            if(calisan[0] == guncelleSecim):
                calisanAd = input("Çalışan ismini giriniz: ")
                calisanSoyad = input("Çalışan soyadını giriniz: ")
                calisanEmail = input("Çalışan e-mailini giriniz (kamilkoc@koc.com gibi): ")
                calisanTelefon = input("Çalışan telefon numarasını giriniz (90123456789 gibi): ")
                calisanAdres = input("Çalışan adresini yazınız: ")
                Fonksiyonlar.subeGetir()
                calisanSube = input("Çalışan kişinin Şube ID'sini seçiniz: ")
                Fonksiyonlar.meslekGetir()
                calisanTur = input("Çalışanın meslek ID'sini seçiniz: ")

                sql = """
                UPDATE Calisanlar SET name=%s,surname=%s,email=%s,phonenumber=%s,adress=%s,subeid=%s,calisanlarturid=%s WHERE personelid=%s
                """
                cursor.execute(sql,(calisanAd,calisanSoyad,calisanEmail,calisanTelefon,calisanAdres,calisanSube,calisanTur,guncelleSecim))

                count = cursor.rowcount
                print(f"\n{count} kayıt başarıyla güncellenmiştir.")          
    def calisanSil():
        Calisanlar.calisanGoruntule()

        print("Silmek istediğiniz çalışanın ID'sini giriniz.")
        silSecim = input("Lütfen ID giriniz: ")
        query_Calisanlar_delete = """
        DELETE FROM Calisanlar WHERE personelid=%s
        """
        cursor.execute(query_Calisanlar_delete,silSecim)

        count = cursor.rowcount
        print(f"\n{count} kayıt başarıyla silinmiştir.")
    def calisanSayisi():
        sql = """
        SELECT * FROM toplamcalisanlar
        """
        cursor.execute(sql)
        calisanSayisi = cursor.fetchone()
        print("\nTOPLAM ÇALIŞAN SAYISI: ", calisanSayisi[0])

class Otobusler:
    def OtobusEkle():
        plaka = input("Otobüs plakasını giriniz (34GGH445 gibi): ")
        Fonksiyonlar.markaGetir()
        markaSecim = input("Otobüsün Marka ID'sini seçiniz: ")

        sql = "INSERT INTO Otobusler (plaka,markaid) VALUES(%s,%s)"
        values = (plaka,markaSecim)
        cursor.execute(sql,values)

        sql = "SELECT otobusid,plaka FROM Otobusler"
        cursor.execute(sql)
        otobusler = cursor.fetchall()
        tablo = PrettyTable(['OtobusID','Plaka'])
        for otobus in otobusler:
            tablo.add_row(otobus)
        print(tablo)
        otobusid = input("Yeni eklenen otobusun ID'sini giriniz: ")
        koltuk = input("Koltuk sayısını giriniz: ")
        sql = "INSERT INTO Koltuklar (boskoltuk,otobusid) VALUES (%s,%s)"
        values = (koltuk,otobusid)
        cursor.execute(sql,values)


        print(f"\n{plaka} plakalı otobüs başarıyla eklendi.") 
    def OtobusGoruntule():
        query_Otubus_select = """
        SELECT otobusler.otobusid, otobusler.plaka, markalar.markaAdi, markalar.markamodeli FROM Otobusler
        JOIN markalar ON otobusler.markaid = markalar.markaid
        """
        cursor.execute(query_Otubus_select)
        otobusler = cursor.fetchall()
        
        tablo = PrettyTable(['OtobüsID','Plaka','Marka Adı','Modeli'])
        for otobus in otobusler:
            tablo.add_row(otobus)
        print(tablo)
    def OtobusGuncelle():
        Otobusler.OtobusGoruntule()

        guncelleSecim = int(input("Düzenlemek istediğiniz OtobusID giriniz: "))

        query_Otobus_select = """
        SELECT * FROM Otobusler
        """
        cursor.execute(query_Otobus_select)
        otobusler = cursor.fetchall()

        for otobus in otobusler:
            if(otobus[0] == guncelleSecim):
                plaka = input("Otobüs plakasını giriniz (34GGH445 gibi): ")
                Fonksiyonlar.markaGetir()
                markaid = input("Marka ID seçiniz: ")
                query_Otobus_update = """
                UPDATE Otobusler SET plaka=%s, markaid=%s WHERE otobusid=%s
                """
                cursor.execute(query_Otobus_update,(plaka,markaid,guncelleSecim))
                count = cursor.rowcount
                print(f"\n{count} kayıt başarıyla güncellenmiştir.")
    def OtobusSil():
        Otobusler.OtobusGoruntule()
        silSecim = input("Silmek istediğiniz otobüsün ID'sini giriniz: ")
        query_Otobus_delete = """
        SET session_replication_role = 'replica';
        DELETE FROM Otobusler WHERE otobusid=%s;
        DELETE FROM Seferler WHERE otobusid=%s;
        DELETE FROM Koltuklar WHERE otobusid=%s;
        SET session_replication_role = 'origin';
        """
        cursor.execute(query_Otobus_delete,(silSecim,silSecim,silSecim))

        print("Seçilen otobüs başarıyla silinmiştir.")

class Biletler:
    def biletEkle():
        Musteriler.MusteriGoruntule()
        musteri = input("Bilet almak isteyen MüşteriID'sini giriniz: ")
        Fonksiyonlar.seferGetir()
        sefer = input("SeferID seçiniz: ")
        Fonksiyonlar.koltukGetir()
        otobus = input("Uygun olan OtobusKoltukID seçiniz: ")
        
        sql = "INSERT INTO Biletler (musteriid,seferid,otobuskoltukid) VALUES(%s,%s,%s)"
        values = (musteri,sefer,otobus)
        cursor.execute(sql,values)
        print("Bilet başarıyla eklendi.") 
    def biletGoruntule():
        query_Biletler_secelt = """
        SELECT yolcuid, musteriler.name,musteriler.surname,seferler.kalkiszamani,seferler.iniszamani FROM Biletler
        JOIN musteriler ON biletler.musteriid = musteriler.musteriid
        JOIN seferler ON biletler.seferid = seferler.seferid
        """
        cursor.execute(query_Biletler_secelt)
        biletler = cursor.fetchall()
        tablo = PrettyTable(['BiletID','Müşteri Adı','Müşteri Soyadı','Kalkış Zamanı','İniş Zamanı'])
        for bilet in biletler:
            tablo.add_row(bilet)
        print(tablo)
    def biletGuncelle():
        query_Biletler_select = """
        SELECT musteriler.musteriid,musteriler.name, musteriler.surname,biletler.yolcuid FROM Musteriler
        JOIN biletler ON musteriler.musteriid = biletler.musteriid
        """
        cursor.execute(query_Biletler_select)
        biletler = cursor.fetchall()
        tablo = PrettyTable(['MüşteriID','Müşteri Adı', 'Müşteri Soyadı', 'Müşteri YolcuID'])
        for bilet in biletler:
            tablo.add_row(bilet)
        print(tablo)

        guncelleSecim = int(input("Düzenlemek istediğiniz MusteriID giriniz: "))
    
        for bilet in biletler:
            if(bilet[0] == guncelleSecim):
                Musteriler.MusteriGoruntule()
                musteri = input("Bilet almak isteyen MüşteriID'sini giriniz: ")
                Fonksiyonlar.seferGetir()
                sefer = input("SeferID seçiniz: ")
                Fonksiyonlar.koltukGetir()
                otobus = input("Uygun olan OtobusKoltukID seçiniz: ")
                sql = "UPDATE Biletler SET musteriid=%s, seferid=%s, otobuskoltukid=%s WHERE yolcuid=%s"
                values = (guncelleSecim,sefer,otobus,bilet[3])
                cursor.execute(sql,values)
                count = cursor.rowcount
                print(f"\n{count} kayıt başarıyla güncellenmiştir.")    
    def biletSil():
        Biletler.biletGoruntule()
        silSecim = input("Silmek istediğiniz biletin yolcu ID'sini giriniz: ")
        query_Bilet_delete = "DELETE FROM Biletler WHERE yolcuid={0}".format(silSecim)
        cursor.execute(query_Bilet_delete)

        print("Seçilen bilet başarıyla silinmiştir.")
    def seferEkle():
        kalkiszamani = input("Kalkış Zamanını Giriniz(GG/AA/YYYY Şeklinde): ")
        iniszamani = input("İniş Zamanını Giriniz(GG/AA/YYYY Şeklinde): ")
        ucret = input("Ücreti giriniz: ")
        Otobusler.OtobusGoruntule()
        otobus = input("Görevli Otobus ID'sini giriniz: ")

        sql = """
        INSERT INTO Seferler (kalkiszamani,iniszamani,ucret,otobusid) VALUES (%s,%s,%s,%s)
        """
        values = (kalkiszamani,iniszamani,ucret,otobus)
        cursor.execute(sql,values)
        print("Sefer başarıyla eklendi.")   
    def seferSayisi():
        sql = """
        SELECT * FROM toplamseferler
        """
        cursor.execute(sql)
        seferSayisi = cursor.fetchone()
        print("\nTOPLAM SEFER SAYISI: ", seferSayisi[0])
    def biletSayisi():
        sql = """
        SELECT * FROM toplambiletler
        """
        cursor.execute(sql)
        biletSayisi = cursor.fetchone()
        print("\nTOPLAM BİLET SAYISI: ", biletSayisi[0])


def anaMenu():
    print("#########################################")
    print("Otobüs Firması Admin Paneline Hoşgeldiniz.\n")
    print("[1]Müşteri Menüsü")
    print("[2]Bilet Menüsü")
    print("[3]Otobüs Menüsü")
    print("[4]Şube Menüsü")
    print("[5]Çıkış\n")

def musteriMenu():
    print("\n------------Müşteri Menüsü------------")
    print("[1]Müşterileri Göster")
    print("[2]Müşteri Ekle")
    print("[3]Müşteri Güncelle")
    print("[4]Müşteri Sil")
    print("[5]Müşteri Sayısını Gör")
    print("[6]Anamenüye Dön")
    musteriSecim = int(input("Lütfen seçenek giriniz: "))
    if musteriSecim == 1:
        Musteriler.MusteriGoruntule()
        musteriMenu()
    elif musteriSecim == 2:
        Musteriler.MusteriEkle()
        musteriMenu()
    elif musteriSecim == 3:
        Musteriler.MusteriGuncelle()
        musteriMenu()
    elif musteriSecim == 4:
        Musteriler.MusteriSil()
        musteriMenu()
    elif musteriSecim == 5:
        Musteriler.MusteriSayisi()
        musteriMenu()
    elif musteriSecim == 6:
        return
    else:
        print("Yanlış girdi.")
        musteriMenu()

def biletMenu():
    print("\n------------Bilet Menüsü------------")
    print("[1]Biletleri Göster")
    print("[2]Bilet Ekle")
    print("[3]Bilet Güncelle")
    print("[4]Bilet Sil")
    print("[5]Sefer Ekle")
    print("[6]Sefer Sayısını Gör")
    print("[7]Bilet Sayısını Gör")
    print("[8]Anamenüye Dön")
    biletSecim = int(input("Lütfen seçenek giriniz: "))
    if biletSecim == 1:
        Biletler.biletGoruntule()
        biletMenu()
    elif biletSecim == 2:
        Biletler.biletEkle()
        biletMenu()
    elif biletSecim == 3:
        Biletler.biletGuncelle()
        biletMenu()
    elif biletSecim == 4:
        Biletler.biletSil()
        biletMenu()
    elif biletSecim == 5:
        Biletler.seferEkle()
        biletMenu()
    elif biletSecim == 6:
        Biletler.seferSayisi()
        biletMenu()
    elif biletSecim == 7:
        Biletler.biletSayisi()
        biletMenu()
    elif biletSecim == 8:
        return
    else:
        print("Yanlış girdi.")
        biletMenu()

def otobusMenu():
    print("\n------------Otobüs Menüsü------------")
    print("[1]Otobüsleri Göster")
    print("[2]Otobüs Ekle")
    print("[3]Otobüs Güncelle")
    print("[4]Otobüs Sil")
    print("[5]Anamenüye Dön")
    otobusSecim = int(input("Lütfen seçenek giriniz: "))
    if otobusSecim == 1:
        Otobusler.OtobusGoruntule()
        otobusMenu()
    elif otobusSecim == 2:
        Otobusler.OtobusEkle()
        otobusMenu()
    elif otobusSecim == 3:
        Otobusler.OtobusGuncelle()
        otobusMenu()
    elif otobusSecim == 4:
        Otobusler.OtobusSil()
        otobusMenu()
    elif otobusSecim == 5:
        return
    else:
        print("Yanlış girdi.")
        otobusMenu()
        
def subeMenu():
    print("\n------------Şube Menüsü------------")
    print("[1]Çalışanları Göster")
    print("[2]Çalışan Ekle")
    print("[3]Çalışan Güncelle")
    print("[4]Çalışan Sil")
    print("[5]Çalışan Sayısını Gör")
    print("[6]Anamenüye Dön")
    calisanSecim = int(input("Lütfen seçenek giriniz: "))

    if calisanSecim == 1:
        Calisanlar.calisanGoruntule()
        subeMenu()
    elif calisanSecim == 2:
        Calisanlar.calisanEkle()
        subeMenu()
    elif calisanSecim == 3:
        Calisanlar.calisanGuncelle()
        subeMenu()
    elif calisanSecim == 4:
        Calisanlar.calisanSil()
        subeMenu()
    elif calisanSecim == 5:
        Calisanlar.calisanSayisi()
        subeMenu()
    elif calisanSecim == 6:
        return
    else:
        print("Yanlış girdi.")
        subeMenu()

def create():
    pass
        
def main():
    while True:
        anaMenu()
        menuSecim = int(input("Lütfen seçenek giriniz: "))
        if menuSecim == 1:
            musteriMenu()
        elif menuSecim == 2:
            biletMenu()
        elif menuSecim == 3:
            otobusMenu()
        elif menuSecim == 4:
            subeMenu()
        elif menuSecim == 5:
            break
        else:
            return
    if db != None:
            cursor.close()
            db.close()
            print("PostgreSQL veritabani su an kapatilmistir.")
            

if __name__ == "__main__":    
    main()