##################################################################
# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması
##################################################################

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


# İş Problemi
# Facebook kısa süre önce mevcut "maximum bidding" adı verilen teklif verme türüne alternatif olarak yeni bir
# teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi ve average bidding'in maximum bidding'den daha fazla
# dönüşüm getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.
# A/B testi 1 aydır devam ediyor ve bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.
# Bombabomba.com için nihai başarı ölçütü Purchase'dır.
# Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.

# Veri Seti Hikayesi

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.
# Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır.
# Bu veri setleri ab_testing.xlsx excel’inin ayrı sayfalarında yer almaktadır.

# Kontrol grubuna Maximum Bidding, test grubuna Average Bidding uygulanmıştır.
#
# Değişkenler

# Impression : Reklam görüntüleme sayısı
# Click : Görüntülenen reklama tıklama sayısı
# Purchase : Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning : Satın alınan ürünler sonrası elde edilen kazanç


###########################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
###########################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.
#
df_test = pd.read_excel("Average_Bidding_Test_Group.xlsx")
df_test.head()

df_control = pd.read_excel("Maximum_Bidding_Control_Group.xlsx")
df_control.head()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
#
df_test.describe().T
df_control.describe().T


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.
#
df = pd.concat([df_test,df_control], ignore_index=True)


###########################################
#Görev 2:  A/B Testinin Hipotezinin Tanımlanması
###########################################

#Adım 1: Hipotezi tanımlayınız.
#
# H0 : M1 = M2 (Maximum Bidding ile Average Bidding arasında istatistiki olarak anlamlı bir fark yoktur.)
# H1 : M1!= M2 (... anlamlı bir fark vardır.)
#
# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz.

df_test["Purchase"].mean()
df_control["Purchase"].mean()

# Mean sonuçlarına baktığımızda test grubunun yani Average Bidding teklif verme türünün ortalaması daha yüksek çıkmış görünüyor.


###########################################
# Görev 3:  Hipotez Testinin Gerçekleştirilmesi
###########################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.



# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: Normal dağılım varsayımı sağlanmamaktadır.
#
df_control.columns

print("Test_Group")
for col in df_test.columns:
    test_stat , pvalue  = shapiro(df_test[col])
    print(col)
    print("Test Stat = %.4f, p-value = %.4f" % (test_stat, pvalue))
print()
print("Control_Group")
for col in df_control.columns:
    test_stat,pvalue = shapiro(df_control[col])
    print(col)
    print("Test Stat = %.4f, p-value = %.4f" % (test_stat,pvalue))


# p < 0.05 H0 RED ,
# p > 0.05 H0 REDDEDİLEMEZ

# Test sonucuna göre normallik varsayımı kontrol ve test grupları için sağlanıyor mu ?
# Elde edilen p-value değerlerini yorumlayınız.

#Test Grubu için pvalue değerleri > 0.05 Ho reddedilemez.Normal dağılım varsayımı sağlanmaktadır.
#Control Grubu için pvalue değerleri > 0.05 Ho reddedilemez. Normal dağılım varsayımı sağlanmaktadır.


# VaryansHomojenliği :
# H0: Varyanslar homojendir.
# H1: Varyanslar homojen Değildir.

for col in df.columns:
    test_stat, pvalue = levene(df_test[col],df_control[col])
    print(col)
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p < 0.05 H0 RED ,
# p > 0.05 H0 REDDEDİLEMEZ
#
# Kontrol ve test grubu için varyans homojenliğinin sağlanıp sağlanmadığını Purchase değişkeni üzerinden test ediniz.
# Test sonucuna göre normallik varsayımı sağlanıyor mu?
# Elde edilen p-value değerlerini yorumlayınız.

# Purchase değişkeni ve ek olarak Impression ve Earning değişkenleri için pvalue > 0.05 Ho reddedilemez.
# Varyanslar homojendir. Click değişkeni için pvalue < 0.05 Ho reddedilir. Varyanslar homojen değildir.


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

# Purchase değişkenine göre Normallik varsayımı sağlanmıştır ve varyanslar homojendir.
# Normallik varsayımı sağlandığı için parametrik test yani bağımsız iki örneklem t testi uygularız.

test_stat, pvalue = ttest_ind(df_test["Purchase"] ,
                              df_control["Purchase"] ,
                              equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
f"Test Stat = {round(test_stat,4)}, p-value = {round(pvalue, 4)}"
#for col in df.columns :
    #test_stat, pvalue = ttest_ind(df_test[col],df_control[col])
    #print(col)
    #print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma ortalamaları
# arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# Purchase değişkeni için pvalue değeri = 0.3493 > 0.05 Ho reddedilemez . Maximum Bidding ile Average Bidding arasında
#istatistiki olarak anlamlı bir fark yoktur.

# H0 : M1 = M2 (Maximum Bidding ile Average Bidding arasında istatistiki olarak anlamlı bir fark yoktur.)
# H1 : M1!= M2 (... anlamlı bir fark vardır.)

################################
# Görev 4:  Sonuçların Analizi
###############################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
#
# Purchase değişkeninin öncelikle normallik varsayımını sağlayıp sağlamadığını kontrol ettim.
# Normal dağıldığını shapiro wilk testi analiz ettim ve varyans homojenliği için de levene testi uyguladım.
#Hem normal dağıldığı hem de varyanslar homojen olduğu için parametrik yani bağımsız iki örneklem testi uyguladım.


# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

#Bağımsız iki örneklem test sonucunda Ho reddedilemedi yani Maximum Bidding teklifi ile Average Bidding teklifi
#arasında istatistiki olarak anlamlı bir fark bulunamamıştır.


# Sürecin Fonksiyonlaştırılması

def ab_assumption_check(df1, df2, x="Purchase" ,plot=False):
    sns.distplot(df1[x])
    sns.distplot(df2[x])
    print(10*"#", "1. grup için Normallik Varsayımı Test Sonuçları" ,10*"#")
    test_stat_test, pvalue_test = shapiro(df1[x])
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat_test, pvalue_test))
    if pvalue_test > 0.05 :
        print("p > 0.05 Ho REDDEDİLEMEZ . 1. Grup için  Normallik Varsayımı sağlanmaktadır. 2. Grup için Normallik Varsayımını kontrol ediniz.")
    else:
        print("p < 0.05 Ho reddedilir. Non-Parametrik test uygulayınız.")
    print(10 * "#", "2. grup için Normallik Varsayımı Test Sonuçları", 10 * "#")
    test_stat_control, pvalue_control = shapiro(df2[x])
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat_control, pvalue_control))
    if pvalue_control > 0.05 :
        print("p > 0.05 Ho REDDEDİLEMEZ, 2. Grup için Normallik varsayımı sağlanmaktadır.Varyans Homojenliğini kontrol ediniz.")
    else:
        print("p < 0.05 Ho REDDEDİLİR. Non-Parametrik test uygulayınız.")
    print(10 * "#", "Varyans Homojenliği Test Sonuçları", 10 * "#")
    test_stat_levene, pvalue_levene = levene(df1[x], df2[x])
    print('Test Stat = %.4f, p-value = %.4f' % (test_stat_levene, pvalue_levene))
    if pvalue_levene > 0.05 :
        print("p > 0.05 Ho REDDEDİLEMEZ,Varyanslar homojendir. Normallik varsayımı sağlanıyorsa Parametrik Test uygulayınız")
    else:
        print("p < 0.05 Ho REDDEDİLİR. Varyanslar homojen değildir. Normallik varsayımı sağlanmıyorsa Non-Parametrik test uygulayınız.")

ab_assumption_check(df_test,df_control)

def ab_testing(df1,df2, x="Purchase" ,parametrik=True):
    if parametrik:
        print(10*"#" , "Parametrik Bağımsız İki Örneklem Test Sonuçları" , 10*"#")
        test_stat_parametrik, pvalue_parametrik = ttest_ind(df1[x],df2[x],equal_var=True)
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat_parametrik, pvalue_parametrik))
        if pvalue_parametrik > 0.05 :
            print("p value > 0.05 Ho REDDEDİLEMEZ. 1. ve 2. grup arasında anlamlı bir fark yoktur.")
        else:
            print("p value < 0.05 Ho REDDEDİLİR. 1. ve 2. grup arasında istatistiki olarak anlamlı bir fark vardır.")
    else:
        print(10 * "#", "Non-Parametrik Man Whitney Test Sonuçları", 10 * "#")
        test_stat_nonparametrik, pvalue_nonparametrik = mannwhitneyu(df1[x],df2[x])
        print('Test Stat = %.4f, p-value = %.4f' % (test_stat_nonparametrik, pvalue_nonparametrik))
        if pvalue_nonparametrik > 0.05 :
            print("p value > 0.05 Ho REDDEDİLEMEZ. 1. ve 2. grup arasında anlamlı bir fark yoktur.")
        else:
            print("p value < 0.05 Ho REDDEDİLİR. 1. ve 2. grup arasında istatistiki olarak anlamlı bir fark vardır.")

ab_testing(df_test,df_control, parametrik=False)