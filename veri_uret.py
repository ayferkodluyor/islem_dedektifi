
from pathlib import Path
import numpy as np
import pandas as pd


# ==================================================
# İŞLEM DEDEKTİFİ - SENTETİK VERİ ÜRETİMİ
# ==================================================

KLASOR = Path(__file__).resolve().parent
RASTGELE = np.random.default_rng(42)

HESAP_SAYISI = 1000
ISLEM_SAYISI = 10000

BASLANGIC = pd.Timestamp("2026-01-01")
BITIS = pd.Timestamp("2026-03-31 23:59:59")


# 1. Hayalî hesaplar

hesaplar = pd.DataFrame({
    "hesap_id": [
        f"H{i:04d}" for i in range(1, HESAP_SAYISI + 1)
    ],
    "musteri_tipi": RASTGELE.choice(
        ["Bireysel", "Ticari", "KOBİ"],
        size=HESAP_SAYISI,
        p=[0.45, 0.20, 0.35],
    ),
})

hesaplar.to_csv(
    KLASOR / "hesaplar.csv",
    index=False,
    encoding="utf-8-sig",
)


# 2. Normal işlem kayıtları

tarih_araligi = int(
    (BITIS - BASLANGIC).total_seconds()
)

zamanlar = BASLANGIC + pd.to_timedelta(
    RASTGELE.integers(
        0,
        tarih_araligi + 1,
        size=ISLEM_SAYISI,
    ),
    unit="s",
)

gonderenler = RASTGELE.choice(
    hesaplar["hesap_id"].to_numpy(),
    size=ISLEM_SAYISI,
)

alicilar = RASTGELE.choice(
    hesaplar["hesap_id"].to_numpy(),
    size=ISLEM_SAYISI,
)

# Bir hesabın kendisine transfer yapmasını önle.
ayni_hesap = gonderenler == alicilar

while ayni_hesap.any():
    alicilar[ayni_hesap] = RASTGELE.choice(
        hesaplar["hesap_id"].to_numpy(),
        size=int(ayni_hesap.sum()),
    )
    ayni_hesap = gonderenler == alicilar

tutarlar = RASTGELE.lognormal(
    mean=8.2,
    sigma=0.75,
    size=ISLEM_SAYISI,
)

tutarlar = np.clip(
    tutarlar,
    100,
    50000,
).round(2)

islemler = pd.DataFrame({
    "islem_id": [
        f"I{i:06d}" for i in range(1, ISLEM_SAYISI + 1)
    ],
    "tarih": zamanlar,
    "gonderen_hesap": gonderenler,
    "alici_hesap": alicilar,
    "tutar": tutarlar,
    "para_birimi": "TRY",
    "senaryo": "Olağan işlem",
})


# 3. Kontrollü sıra dışı işlem örnekleri

# A) Yüksek tutarlı işlemler
yuksek_indeksler = RASTGELE.choice(
    islemler.index.to_numpy(),
    size=30,
    replace=False,
)

islemler.loc[
    yuksek_indeksler,
    "tutar",
] = RASTGELE.uniform(
    150000,
    450000,
    size=30,
).round(2)

islemler.loc[
    yuksek_indeksler,
    "senaryo",
] = "Yüksek tutar örneği"


# B) Kısa sürede art arda transferler
# Aynı gönderen hesaptan farklı alıcılara 8 transfer.

hizli_indeksler = RASTGELE.choice(
    islemler.index.difference(yuksek_indeksler).to_numpy(),
    size=8,
    replace=False,
)

ortak_gonderen = "H0001"
ortak_zaman = pd.Timestamp("2026-02-15 14:00:00")

farkli_alicilar = [
    f"H{i:04d}" for i in range(2, 10)
]

for sira, indeks in enumerate(hizli_indeksler):
    islemler.loc[indeks, "gonderen_hesap"] = ortak_gonderen
    islemler.loc[indeks, "alici_hesap"] = farkli_alicilar[sira]
    islemler.loc[indeks, "tarih"] = (
        ortak_zaman + pd.Timedelta(minutes=sira)
    )
    islemler.loc[indeks, "tutar"] = 12000 + sira * 1500
    islemler.loc[indeks, "senaryo"] = (
        "Kısa sürede çoklu transfer örneği"
    )


# 4. İşlemleri tarihe göre sırala

islemler = islemler.sort_values(
    ["tarih", "islem_id"]
).reset_index(drop=True)

islemler["tarih"] = islemler["tarih"].dt.strftime(
    "%Y-%m-%d %H:%M:%S"
)

islemler.to_csv(
    KLASOR / "islemler.csv",
    index=False,
    encoding="utf-8-sig",
)


# 5. Kontrol

print("\nİŞLEM DEDEKTİFİ - VERİ ÜRETİMİ TAMAMLANDI")
print("-" * 45)
print(f"Hesap sayısı: {len(hesaplar):,}")
print(f"İşlem sayısı: {len(islemler):,}")
print("\nSenaryo dağılımı:")
print(islemler["senaryo"].value_counts())
print("\nDosyalar:")
print(KLASOR / "hesaplar.csv")
print(KLASOR / "islemler.csv")