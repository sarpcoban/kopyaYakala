import docx
from collections import Counter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import jpype as jp
import os
from random import *
import numpy as np
from sklearn.cluster import KMeans



kelime_dizi = []
kelime_kok = []
dosya_kelime = []
cumle_vektor = []
durak = ['açıkçası', 'ama', 'ancak', 'bile', 'çünkü', 'dahi', 'de', 'da', 'ki', 'fakat', 'gene', 'gerek', 'he', 'ha',
         'halbuki', 'hatta', 'hele', 'hem', 'ile', 'ise', 'kah', 'ki', 'lakin', 'nitekim', 'oysa', 've', 'veya',
         'veyahut', 'yahut', 'yine', 'yoksa', 'zira', 'için', '']


def benzerlik_hesabi(vektor,indis):

    for i in range(len(indis)):
        for j in range(len(indis[i])):
            for k in range(j+1,len(indis[i])):
                tum_kelime_1 = 0
                tum_kelime_2 = 0
                benzer_kelime = 0
                print(vektor[indis[i][j]][0])
                for l in range(len(vektor[0][0])):
                    tum_kelime_1 = sum(vektor[indis[i][j]][0])
                    tum_kelime_2 = sum(vektor[indis[i][k]][0])
                    if(vektor[indis[i][j]][0][l] == 0 or vektor[indis[i][k]][0][l]==0):
                        continue
                    else:
                        benzer_kelime = benzer_kelime + min(vektor[indis[i][j]][0][l],vektor[indis[i][k]][0][l])

                benzer_1 = 100*benzer_kelime/tum_kelime_1
                benzer_2 = 100*benzer_kelime/tum_kelime_2

                if(50 > benzer_1 >= 30):
                    print(vektor[indis[i][k]][1]+","+vektor[indis[i][j]][1]+"'ya %"+str(round(benzer_1,2))+" benziyor.Kopya olabilir.")
                elif(benzer_1>=50):
                    print(vektor[indis[i][k]][1] + "," + vektor[indis[i][j]][1] + "'ya %" + str(
                        round(benzer_1, 2)) + " benziyor.Kesinlikle kopya.")
                else:
                    print(vektor[indis[i][k]][1] + "," + vektor[indis[i][j]][1] + "'ya %" + str(
                        round(benzer_1, 2)) + " benziyor.Kopya değildir.")

                if (50 > benzer_2 >= 30):
                    print(vektor[indis[i][j]][1] + "," + vektor[indis[i][k]][1] + "'ya %" + str(
                        round(benzer_2, 2)) + " benziyor.Kopya olabilir.")
                elif (benzer_2 >= 50):
                    print(vektor[indis[i][j]][1] + "," + vektor[indis[i][k]][1] + "'ya %" + str(
                        round(benzer_2, 2)) + " benziyor.Kesinlikle kopya.")

                else:
                    print(vektor[indis[i][j]][1] + "," + vektor[indis[i][k]][1] + "'ya %" + str(
                        round(benzer_2, 2)) + " benziyor.Kopya değildir.")


def kok_al(kelimeler):

    Tr = jp.JClass("net.zemberek.tr.yapi.TurkiyeTurkcesi")
    Zemberek = jp.JClass("net.zemberek.erisim.Zemberek")
    turkce = Tr()
    zemberek = Zemberek(turkce)
    global kelime_kok
    kelime_kok_yerel = []

    for i in range(len(kelimeler)):
        try:
            yanit = zemberek.kelimeCozumle(kelimeler[i])
            yanit_kok = str(yanit[0])
            yanit_kok = yanit_kok.split(" ")
            if(kelime_kok.count(yanit_kok[3])==0):
                kelime_kok.append(yanit_kok[3])
            kelime_kok_yerel.append(yanit_kok[3])
        except:
            None
    return kelime_kok_yerel


def kelime_bol(cumle):
    cumle = cumle.lower()
    cumle = cumle.replace(",", " ")
    cumle = cumle.replace("\n", " ")
    cumle = cumle.replace(".", " ")
    cumle = cumle.replace("!", " ")
    cumle = cumle.replace("'", " ")
    cumle = cumle.replace("/", " ")
    cumle = cumle.replace("(", " ")
    cumle = cumle.replace(")", " ")
    cumle = cumle.replace("%", " ")
    cumle = cumle.replace("&", " ")
    cumle = cumle.replace("^", " ")
    cumle = cumle.replace("\\", " ")
    cumle = cumle.replace("{", " ")
    cumle = cumle.replace("}", " ")
    cumle = cumle.replace("[", " ")
    cumle = cumle.replace("]", " ")
    cumle = cumle.replace("+", " ")
    cumle = cumle.replace("-", " ")
    cumle = cumle.replace("*", " ")
    cumle = cumle.replace("_", " ")
    cumle = cumle.replace("#", " ")
    cumle = cumle.replace("$", " ")
    cumle = cumle.replace("<", " ")
    cumle = cumle.replace(">", " ")
    cumle = cumle.replace("|", " ")
    cumle = cumle.replace("=", " ")
    cumle = cumle.replace("£"," ")
    cumle = cumle.replace("½", " ")
    cumle = cumle.replace("@", " ")
    cumle = cumle.replace("€", " ")
    cumle = cumle.replace("₺", " ")
    cumle = cumle.replace("¨", " ")
    cumle = cumle.replace("~", " ")
    cumle = cumle.split(" ")
    kelime_dizi_yerel = []
    global kelime_dizi
    for i in range(len(cumle)):
        kelime_dizi_yerel.append(cumle[i])
    for i in range(len(durak)):
        if(kelime_dizi_yerel.count(durak[i])>0):
            for j in range(kelime_dizi_yerel.count(durak[i])):
                kelime_dizi_yerel.remove(durak[i])

    return kelime_dizi_yerel

def docxOku(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    fullText = ' \n'.join(fullText)
    kelime_havuz = kelime_bol(fullText)
    global dosya_kelime
    dosya_kelime.append(kok_al(kelime_havuz))



def pdfOku(file):
    cikti = StringIO()
    kaynak_yonetici = PDFResourceManager()
    lapara = LAParams()
    donustur = TextConverter(kaynak_yonetici, cikti, laparams=lapara, codec="utf-8")
    yorumlayici = PDFPageInterpreter(kaynak_yonetici, donustur)
    dosya = open(file, "rb")
    for sayfa in PDFPage.get_pages(dosya):
        yorumlayici.process_page(page=sayfa)
    kelime_havuz = kelime_bol(cikti.getvalue())
    global dosya_kelime
    dosya_kelime.append(kok_al(kelime_havuz))

def txtOku(file):
    file = open(file, "r")
    icerik = file.read()
    kelime_havuz = kelime_bol(icerik)
    global dosya_kelime
    dosya_kelime.append(kok_al(kelime_havuz))

def vektor(cumleler,dosya_adi):
    global cumle_vektor
    temp_dizi2 = []
    for i in range(len(cumleler)):
        temp_dizi = []
        for j in range(len(kelime_kok)):
            temp_dizi.append(0)
        kelime_sayi = Counter(kelime_kok)
        indis = 0
        for kelimeler in kelime_sayi:
            if(cumleler[i].count(kelimeler)>0):
                temp_dizi[indis] = cumleler[i].count(kelimeler)
            indis += 1
        temp_dizi2.append(temp_dizi)
    for i in range(len(cumleler)):
        temp_dizi3 = []
        temp_dizi3.append(temp_dizi2[i])
        temp_dizi3.append(dosya_adi[i])
        cumle_vektor.append(temp_dizi3)



def hesapla(cumle):
    shuffle(cumle)
    vektor = []
    dosya = []
    k = 10
    for i in range(len(cumle)):
        vektor.append(cumle[i][0])
        dosya.append(cumle[i][1])
    kumele = KMeans(n_clusters=k,random_state=0).fit(vektor)
    k_grup = []
    for i in range(k):
        kume=kumele.labels_
        k_grup.append(np.nonzero(kume == i)[0])
    benzerlik_hesabi(cumle,k_grup)




jp.startJVM(jp.getDefaultJVMPath(), "-ea", "-Djava.class.path=zemberek-tum-2.0.jar")
dosyalar = [f for f in os.listdir("veriseti")]

for i in range(len(dosyalar)):
    if(dosyalar[i][-3:]=='txt'):
        txtOku("veriseti/"+dosyalar[i])
    elif(dosyalar[i][-3:]=='pdf'):
        pdfOku('veriseti/'+dosyalar[i])
    elif(dosyalar[i][-4:]=='docx'):
        docxOku('veriseti/'+dosyalar[i])
vektor(dosya_kelime,dosyalar)
hesapla(cumle_vektor)
