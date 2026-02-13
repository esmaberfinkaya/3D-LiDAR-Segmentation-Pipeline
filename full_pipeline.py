import os
import tkinter as tk
from tkinter import filedialog, messagebox
import open3d as o3d
import numpy as np
import copy
import functions_library as fl 

def dosya_sec():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    yol = filedialog.askopenfilename(
        initialdir=r"C:\Users\esma4\lidarToVoxelProject\RESULTS",
        title="PCD Dosyası Seç", 
        filetypes=[("PCD", "*.pcd")]
    )
    root.destroy()
    return yol

def run_pipeline():
    print("--- Otonom Sistem Modüler Pipeline: Karşılaştırma Modu ---")
    
    pcd_yolu = dosya_sec()
    if not pcd_yolu: return

    # 1. Veriyi Yükleme ve Ham Halini Klonlama
    pcd_ham = o3d.io.read_point_cloud(pcd_yolu)
    coords = np.asarray(pcd_ham.points)
    
    # Ham halini siyah/gri yaparak analizden ayıralım
    pcd_ham.paint_uniform_color([0.2, 0.2, 0.2]) 

    # 2. Analiz Süreci (Mutfak Fonksiyonları)
    print("[1/3] Öznitelikler hesaplanıyor...")
    features = fl.extract_features(pcd_ham)

    print("[2/3] Nesne öbekleri (DBSCAN) tespit ediliyor...")
    labels = fl.apply_clustering(coords, features)

    print("[3/3] Renklendirilmiş model hazırlanıyor...")
    pcd_analiz = copy.deepcopy(pcd_ham) # Orijinal yapıyı bozmamak için kopya alıyoruz
    pcd_analiz = fl.colorize_clusters(pcd_analiz, labels)

    # 3. YAN YANA GÖRSELLEŞTİRME (VS MODU)
    print(f"\n>>> Analiz Tamamlandı! Nesne Sayısı: {labels.max() + 1}")
    
    # Sol tarafa ham veriyi, sağ tarafa analiz verisini kaydıralım
    # Nokta bulutunun genişliğine göre bir ofset belirliyoruz
    bbox = pcd_ham.get_axis_aligned_bounding_box()
    offset = (bbox.get_max_extent() * 1.2) 
    pcd_analiz.translate([offset, 0, 0])

    print("\n[EKRAN] Sol: Ham Voksel | Sağ: Algoritma Analizi")
    print("Pencere açılıyor...")
    
    # İki modeli de aynı listeye koyup gösteriyoruz
    o3d.visualization.draw_geometries([pcd_ham, pcd_analiz], 
                                      window_name="Ham Voksel vs Algoritma Analizi",
                                      width=1200, height=800)

if __name__ == "__main__":
    run_pipeline()