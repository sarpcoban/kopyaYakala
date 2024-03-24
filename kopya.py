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
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
kelime_dizi = []
kelime_kok = []
dosya_kelime = []
cumle_vektor = []

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
    TurkishMorphology = jp.JClass('zemberek.morphology.TurkishMorphology')
    Paths = jp.JClass('java.nio.file.Paths')
    morphology = TurkishMorphology.createWithDefaults()

    k = 0
    i = 0

    while k < len(kelimeler):

        while i < len(kelimeler[k]):
            analysis = morphology.analyzeSentence(kelimeler[k][i])

            results = morphology.disambiguate(kelimeler[k][i], analysis).bestAnalysis()

            results = results[0].getStems()

            kelimeler[k][i] = results[0]

            i += 1
        k += 1
        i = 0

    return kelimeler



def kelime_bol(cumle):
    
    kelime_dizi_yerel = []
    cevirici = str.maketrans('', '', punctuation)
    cumle = deger.translate(cevirici)
    cumle = cumle.lower()
    stop_words = set(stopwords.words('turkish'))
    word_tokens = word_tokenize(cumle)
    for words in word_tokens:
        if words not in stop_words:
            kelime_dizi_yerel.append(words)
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



