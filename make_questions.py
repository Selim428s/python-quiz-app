import json
# [zorluk, soru, doğru, yanlış1, yanlış2, yanlış3]
Q = [
["kolay","Ekrana çıktı yazdırmak için hangi fonksiyon kullanılır?","print()","echo()","write()","show()"],
["kolay","Python'da liste hangi parantezle tanımlanır?","[ ]","( )","{ }","< >"],
["kolay","Python'da tek satırlık yorum nasıl yazılır?","# yorum","// yorum","/* yorum */","-- yorum"],
["kolay","type(5) ifadesinin sonucu nedir?","<class 'int'>","<class 'str'>","<class 'float'>","<class 'bool'>"],
["kolay","len('Python') kaç döndürür?","6","5","7","4"],
["kolay","7 // 2 işleminin sonucu nedir?","3","3.5","4","2"],
["kolay","Bir metni tam sayıya çeviren fonksiyon hangisidir?","int()","str()","float()","chr()"],
["kolay","Hangisi geçerli bir değişken adıdır?","_sayi","2sayi","my-var","class"],
["kolay","2 ** 3 işleminin sonucu nedir?","8","6","9","5"],
["kolay","Koşul kontrolü için hangi anahtar kelime kullanılır?","if","when","unless","check"],
["orta","[x*2 for x in range(3)] ifadesinin sonucu nedir?","[0, 2, 4]","[2, 4, 6]","[0, 1, 2]","[0, 2, 4, 6]"],
["orta","Sözlükte anahtar yoksa hata vermeden değer almak için ne kullanılır?","dict.get()","dict.find()","dict.fetch()","dict.seek()"],
["orta","Tuple'ın temel özelliği nedir?","Değiştirilemez (immutable)","Sadece sayı tutar","Tekrarlı eleman kabul etmez","Süslü parantezle tanımlanır"],
["orta","len(set([1, 2, 2, 3])) kaç döndürür?","3","4","2","1"],
["orta","'abc'[::-1] ifadesinin sonucu nedir?","'cba'","'abc'","'bca'","'acb'"],
["orta","with open(...) kullanmanın ana faydası nedir?","Dosyayı otomatik kapatır","Dosyayı şifreler","Okumayı hızlandırır","Belleği artırır"],
["orta","lambda ne işe yarar?","Anonim (isimsiz) fonksiyon tanımlar","Döngü başlatır","Sınıf tanımlar","Modül içe aktarır"],
["orta","*args neyi temsil eder?","Değişken sayıda konumsal argüman","Anahtar-değer argümanları","Sabit çarpan","Bellek işaretçisi"],
["orta","try/except yapısı ne için kullanılır?","Hataları yakalamak için","Döngüyü kırmak için","Tip dönüştürmek için","Modül yüklemek için"],
["orta","'is' ve '==' arasındaki fark nedir?","'is' kimliği, '==' değeri karşılaştırır","'is' değeri, '==' kimliği karşılaştırır","İkisi birebir aynıdır","'is' sadece sayılarda çalışır"],
["zor","def f(a, l=[]): l.append(a); return l  — f(1) sonra f(2) çağrılırsa ikinci sonuç nedir?","[1, 2]","[2]","[1]","Hata verir"],
["zor","CPython'daki GIL ne yapar?","Aynı anda yalnızca bir thread'in bayt kodu çalıştırmasına izin verir","Belleği otomatik temizler","Tip kontrolü yapar","Modülleri önbelleğe alır"],
["zor","'yield' anahtar kelimesi ne sağlar?","Değerleri tembel (lazy) üreten generator oluşturur","Fonksiyonu sonlandırıp hata fırlatır","Global değişken tanımlar","Sınıf kalıtımı sağlar"],
["zor","Bir sınıftaki __init__ metodunun rolü nedir?","Oluşturulan nesneyi başlatır","Nesneyi yok eder","Sınıf metodunu tanımlar","Modülü içe aktarır"],
["zor","@staticmethod ile tanımlanan metodun özelliği nedir?","self veya cls almaz","Her zaman özel (private) olur","Sadece sınıf içinde çağrılabilir","Otomatik olarak önbelleklenir"],
["zor","Decorator nedir?","Bir fonksiyonu sarmalayıp davranışını genişleten yapı","Sınıfı silen yapı","Değişken tipi belirten ifade","Döngü kısaltması"],
["zor","copy.deepcopy ile copy.copy arasındaki fark nedir?","deepcopy iç içe nesneleri de kopyalar","deepcopy daha hızlıdır","copy sadece sayılarda çalışır","Fark yoktur"],
["zor","Python'da MRO neyi belirler?","Çoklu kalıtımda metot arama sırasını","Bellek ayırma sırasını","Modül yükleme sırasını","Döngü hızını"],
["zor","a = [1]; b = [1]; a is b ifadesinin sonucu nedir?","False","True","Hata verir","None"],
["zor","0.1 + 0.2 == 0.3 ifadesinin sonucu nedir?","False","True","Hata verir","None"],
]
out = [{"zorluk":z,"soru":s,"dogru":d,"secenekler":[d,a,b,c]} for z,s,d,a,b,c in Q]
json.dump(out, open("questions.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "soru yazıldı")
