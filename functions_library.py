import torch
import numpy as np
import open3d as o3d  # İşte eksik olan kilit parça buydu!
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

def extract_features(pcd):
    """
    Ağırlıklı Geometrik Özellik Çıkarımı
    Amaç: Küçük detayları (çıkıntıları) göz ardı edip ana şekillere odaklanmak.
    """
    print("   [+] Normaller hesaplanıyor...")
    
    # Artık 'o3d' tanımlı olduğu için bu satır çalışacak
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=2.0, max_nn=50))
    
    normals = np.asarray(pcd.normals)
    points = np.asarray(pcd.points)
    z_coords = points[:, 2].reshape(-1, 1)
    
    # --- MÜHENDİSLİK DOKUNUŞU: ÖZNİTELİK AĞIRLIKLANDIRMA ---
    # Eğim farkı, konum farkının yarısı kadar önemli olsun (Pürüzleri yoksaymak için)
    weighted_normals = normals * 0.5
    
    # Yükseklik bilgisini (z) güçlendiriyoruz. 
    weighted_z = z_coords * 1.5
    
    # Geri kalan boş kanallar (Sparse CNN için yer tutucu)
    dummy_features = np.zeros((len(points), 12)) 
    
    # Birleştir
    combined_features = np.hstack((weighted_normals, weighted_z, dummy_features))
    
    return combined_features

def apply_clustering(coords, features, eps=0.5, min_samples=30):
    """
    Daha kararlı öbekleme için parametreler güncellendi.
    """
    # 1. Veriyi Birleştir
    data_to_cluster = np.hstack((coords, features))
    
    # 2. Ölçeklendirme (StandardScaler)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_to_cluster)
    
    # 3. DBSCAN (Geniş toleranslı ayarlar)
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_scaled)
    
    return db.labels_

def colorize_clusters(pcd, labels):
    max_label = labels.max()
    if max_label < 0:
        print("   [!] Uyarı: Hiç nesne bulunamadı!")
        return pcd
        
    # Renk paleti
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels == -1] = [0.1, 0.1, 0.1, 1] # Gürültü noktalarını koyu gri yap
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    return pcd