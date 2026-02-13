Otonom Sistemler İçin 3D LiDAR Veri İşleme ve Nesne Bölütleme Hattı (Pipeline)
"Bilgisayarlara sadece bakmayı değil, gördükleri 3 Boyutlu dünyayı anlamlandırmayı öğretiyoruz."
 İçindekiler
1.Projenin Amacı (Asansör Konuşması)
2.Yeni Başlayanlar İçin: Sorun Nedir?
3.Temel Kavramlar Sözlüğü (Analojilerle)
4.Teknik Mimari ve İşleyiş (Pipeline)
5.Görsel Kanıt: Öncesi ve Sonrası
6.Kurulum ve Kullanım

1. Projenin Amacı (Asansör Konuşması)
Bu proje, otonom araçların ve robotların "gözü" olan LiDAR sensörlerinden gelen milyonlarca karmaşık veri noktasını alır, işler ve bu kaotik veriyi anlamlı nesne gruplarına (duvar, zemin, ağaç, araç vb.) ayırır.
Teknik Özet: Ham 3B Nokta Bulutu (Point Cloud) verilerini voksel tabanlı (Voxel-based) bir yapıya indirgeyen, geometrik öznitelik mühendisliği (Feature Engineering) ile yüzey normallerini hesaplayan ve gözetimsiz makine öğrenmesi (DBSCAN) ile Nesne Bölütleme (Instance Segmentation) yapan modüler bir Python veri hattıdır.

2. Yeni Başlayanlar İçin: Sorun Nedir?
İnsanlar çevrelerine baktıklarında anında "Şurada bir ağaç var, yanında bir araba duruyor" diyebilirler. Beynimiz bunu otomatik yapar.
Ancak bir bilgisayarın (veya otonom aracın) gözleri yoktur; sadece sayıları işleyebilir. LiDAR sensörü ona saniyede milyonlarca nokta gönderir. Bilgisayar için bu, havada asılı duran milyonlarca anlamsız kum tanesinden farksızdır.
Bizim Görevimiz: Bu milyonlarca "kum tanesini" (noktayı) analiz edip, bilgisayara "Bak, şu birbirine benzeyen 5000 tanesi bir araya gelip bir Duvar oluşturuyor" demeyi öğretmektir.                                                                                                                                              
3. Temel Kavramlar Sözlüğü (Analojilerle)
Projeyi anlamak için gereken terimler, hem basit hem teknik açıklamalarıyla:
Terim	Basit Analoji (Ne Gibi?)	Teknik Açıklama
LiDAR	Yarasaların yön bulmak için ses kullanmasının, ışık (lazer) ile yapılan versiyonu.	Lazer darbeleri gönderip yansıma süresini ölçerek 3B harita çıkaran sensör teknolojisi.
Nokta Bulutu (Point Cloud)	Uzayda donmuş, havada asılı duran milyonlarca toz zerresi.	3B Kartezyen uzayda (X, Y, Z) koordinatlarına sahip veri noktaları kümesi.
Voksel (Voxel)	Minecraft oyunundaki gibi 3 boyutlu bir blok/küp.	Veriyi sadeleştirmek (downsampling) için kullanılan 3B hacimsel piksel.
Yüzey Normali	Bir kirpinin dikenleri. Yere yatarsa yukarı bakar, duvara tırmanırsa yana bakar.	Bir yüzeyin baktığı yönü gösteren dik vektör. Geometrik bir özniteliktir.
Öbekleme (Clustering)	Karışık legoları renklerine ve şekillerine göre kutulara ayırmak. Henüz ne olduklarını bilmeyiz ama gruplarız.	Veri noktalarını benzerliklerine göre gruplayan gözetimsiz makine öğrenmesi yöntemi (Örn: DBSCAN).


4.Teknik Mimari ve İşleyiş (Pipeline) 
Proje, spagetti kod karmaşasını önlemek için Modüler Bir Mimari üzerine inşa edilmiştir. Veri bir fabrikadaki üretim bandı gibi aşamalardan geçer.
Dosya Yapısı
CODE/functions_library.py 🧠 (Motor/Mutfak): Tüm matematiksel hesaplamaların, normal vektör analizlerinin ve DBSCAN algoritmasının çalıştığı kütüphanedir.
CODE/full_pipeline.py 🎬 (Yönetici/Şef): Kullanıcıdan dosyayı alan, sırasıyla mutfaktaki işlemleri çağıran ve sonucu ekrana yansıtan ana kontrol dosyasıdır.
Veri İşleme Adımları
Adım 1: Vokselizasyon (Ham Veriyi Sadeleştirme)
Devasa boyutlardaki .laz formatındaki ham veri, işlenmesi daha kolay olan .pcd formatındaki Voksel ızgaralarına dönüştürülür. (Veri boyutu %90+ azalır).
Aşağıda, sadeleştirilmiş ancak henüz hiçbir anlam ifade etmeyen, tek renkli ham voksel verisini görmektesiniz:

<img src="Ekran görüntüsü 2026-02-13 150027.png" width="800" alt="Yan Yana Karşılaştırma">
(Görsel 1: İşlem öncesi ham nokta bulutu. Bilgisayar için sadece bir koordinat yığını.)
Adım 2: Geometrik Öznitelik Mühendisliği (Feature Engineering)
Sadece konuma (X,Y,Z) bakmak nesneleri ayırmak için yetmez. Algoritmamız, her vokselin komşularına bakarak yerel geometrisini analiz eder.
Yüzey Normalleri Hesaplanır: Noktanın yere mi paralel, duvara mı dik olduğu bulunur.
Ağırlıklandırma (Weighting): Duvardaki küçük pürüzlerin aşırı bölünmeye yol açmaması için normal vektörlerin etkisi matematiksel olarak dengelenir.
Adım 3: Nesne İlişkilendirme ve Bölütleme (DBSCAN)
Çıkarılan geometrik özellikler, DBSCAN (Density-Based Spatial Clustering) algoritmasına beslenir. Algoritma, hem konumu yakın olan hem de geometrik özellikleri (yönü, açısı) birbirine benzeyen noktaları aynı "Nesne" olarak etiketler.

5.   Görsel Kanıt: Öncesi ve Sonrası
<img src="Ekran görüntüsü 2026-02-13 145813.png" width="800" alt="Yan Yana Karşılaştırma">
(Görsel 2: İşlem sonrası bölütlenmiş veri. Her renk farklı bir fiziksel nesneyi temsil eder.)
Projenin başarısını en iyi anlatan şey, ham veri ile işlenmiş verinin yan yana karşılaştırmasıdır. Sistemimiz bu karşılaştırmayı otomatik olarak sunar.
Sol Taraf (Ham Veri): Bilgisayarın ilk gördüğü karmaşa.
Sağ Taraf (İşlenmiş Veri): Algoritmanın anlamlandırdığı, nesneleri ayrıştırdığı düzenli dünya 

<img src="Ekran görüntüsü 2026-02-13 145522.png" width="800" alt="Yan Yana Karşılaştırma">

(Görsel 3: Pipeline çıktısı. Sol: Ham gri vokseller. Sağ: Renklendirilmiş nesne öbekleri. Algoritmanın duvarları (mavi/gri) ve diğer yapıları başarıyla ayırdığı görülüyor.)

6. Kurulum ve Kullanım
Gereksinimler
Python 3.8+
Open3D
NumPy
Scikit-Learn
Matplotlib
Çalıştırma
1.Repoyu klonlayın.
2.Gerekli kütüphaneleri yükleyin: pip install open3d numpy scikit-learn matplotlib
3.Ana pipeline dosyasını çalıştırın:python CODE/full_pipeline.py
4.Açılan pencereden işlemek istediğiniz .pcd dosyasını seçin.

 Gelecek Çalışmalar (Future Work)
Şu anki sistem "Gözetimsiz" (Unsupervised) çalışarak nesnelerin sınırlarını belirlemektedir. Bir sonraki aşamada, bu ayrıştırılmış renkli blokların ne olduğunu (Örn: "Bu mavi blok bir duvardır") anlamak için Derin Öğrenme (Sparse CNN) tabanlı sınıflandırma modelleri entegre edilecektir.   
