
from pathlib import Path

import pandas as pd


# ============================================================
# İŞLEM DEDEKTİFİ - ANALİZ MOTORU
# ============================================================

KLASOR = Path(__file__).resolve().parent
GIRIS_DOSYASI = KLASOR / "islemler.csv"
CIKIS_DOSYASI = KLASOR / "analiz_sonuclari.csv"

YUKSEK_TUTAR_ESIGI = 100_000
ZAMAN_PENCERESI_DAKIKA = 10
MINIMUM_ISLEM_SAYISI = 5


# ============================================================
# 1. VERİYİ OKU
# ============================================================

if not GIRIS_DOSYASI.exists():
    print("HATA: islemler.csv dosyası bulunamadı.")
    print("Önce veri_uret.py dosyasını çalıştır.")
    raise SystemExit(1)


islemler = pd.read_csv(
    GIRIS_DOSYASI,
    encoding="utf-8-sig",
    dtype={
        "islem_id": str,
        "gonderen_hesap": str,
        "alici_hesap": str,
    },
)

gerekli_sutunlar = {
    "islem_id",
    "tarih",
    "gonderen_hesap",
    "alici_hesap",
    "tutar",
}

eksik_sutunlar = gerekli_sutunlar - set(islemler.columns)

if eksik_sutunlar:
    raise ValueError(
        "CSV dosyasında eksik sütunlar: "
        + ", ".join(sorted(eksik_sutunlar))
    )


islemler["tarih"] = pd.to_datetime(
    islemler["tarih"],
    errors="coerce",
)

islemler["tutar"] = pd.to_numeric(
    islemler["tutar"],
    errors="coerce",
)

if islemler["tarih"].isna().any():
    raise ValueError(
        "Bazı işlemlerin tarih bilgisi okunamadı."
    )

if islemler["tutar"].isna().any():
    raise ValueError(
        "Bazı işlemlerin tutar bilgisi okunamadı."
    )

islemler = islemler.sort_values(
    ["gonderen_hesap", "tarih", "islem_id"]
).reset_index(drop=True)


# ============================================================
# 2. YÜKSEK TUTARLI İŞLEMLER
# ============================================================

islemler["yuksek_tutar"] = (
    islemler["tutar"] >= YUKSEK_TUTAR_ESIGI
)


# ============================================================
# 3. KISA SÜREDE ÇOKLU TRANSFER ANALİZİ
#
# Aynı gönderen hesabın, seçilen işlem dahil
# önceki 10 dakika içinde kaç transfer yaptığına bakılır.
#
# Bu ilk sürümde en az 5 transfer varsa işlem işaretlenir.
# ============================================================

islemler["son_10_dk_islem_sayisi"] = 0

for hesap_id, grup in islemler.groupby(
    "gonderen_hesap",
    sort=False,
):
    grup = grup.sort_values(
        ["tarih", "islem_id"]
    )

    zamanlar = grup["tarih"].tolist()
    indeksler = grup.index.tolist()

    pencere_baslangici = 0

    for konum, islem_zamani in enumerate(zamanlar):

        while (
            islem_zamani - zamanlar[pencere_baslangici]
        ) > pd.Timedelta(
            minutes=ZAMAN_PENCERESI_DAKIKA
        ):
            pencere_baslangici += 1

        pencere_islem_sayisi = (
            konum - pencere_baslangici + 1
        )

        islemler.at[
            indeksler[konum],
            "son_10_dk_islem_sayisi",
        ] = pencere_islem_sayisi


islemler["coklu_transfer"] = (
    islemler["son_10_dk_islem_sayisi"]
    >= MINIMUM_ISLEM_SAYISI
)


# ============================================================
# 4. İNCELEME DURUMU VE AÇIKLAMA
# ============================================================

islemler["inceleme_gerekli"] = (
    islemler["yuksek_tutar"]
    | islemler["coklu_transfer"]
)


def aciklama_olustur(satir):
    nedenler = []

    if satir["yuksek_tutar"]:
        nedenler.append(
            "İşlem tutarı "
            f"{YUKSEK_TUTAR_ESIGI:,.0f} TL "
            "eşiğine eşit veya üzerinde."
        )

    if satir["coklu_transfer"]:
        nedenler.append(
            "Aynı gönderen hesaptan, bu işlem dahil "
            f"son {ZAMAN_PENCERESI_DAKIKA} dakika "
            "içinde "
            f"{satir['son_10_dk_islem_sayisi']} "
            "transfer yapılmış."
        )

    if nedenler:
        return " | ".join(nedenler)

    return "Tanımlı inceleme kuralları tetiklenmedi."


islemler["inceleme_nedeni"] = islemler.apply(
    aciklama_olustur,
    axis=1,
)

islemler["durum"] = islemler[
    "inceleme_gerekli"
].map(
    {
        True: "İnceleme öneriliyor",
        False: "Olağan",
    }
)


# ============================================================
# 5. SONUÇLARI KAYDET
# ============================================================

islemler = islemler.sort_values(
    ["tarih", "islem_id"]
).reset_index(drop=True)

islemler["tarih"] = islemler[
    "tarih"
].dt.strftime("%Y-%m-%d %H:%M:%S")

islemler.to_csv(
    CIKIS_DOSYASI,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# 6. KONTROL RAPORU
# ============================================================

toplam = len(islemler)

inceleme_sayisi = int(
    islemler["inceleme_gerekli"].sum()
)

yuksek_tutar_sayisi = int(
    islemler["yuksek_tutar"].sum()
)

coklu_transfer_sayisi = int(
    islemler["coklu_transfer"].sum()
)

print("\nİŞLEM DEDEKTİFİ - ANALİZ TAMAMLANDI")
print("=" * 48)

print(f"Toplam işlem: {toplam:,}")

print(
    "İnceleme için işaretlenen işlem: "
    f"{inceleme_sayisi:,}"
)

print(
    "Yüksek tutar kuralını tetikleyen: "
    f"{yuksek_tutar_sayisi:,}"
)

print(
    "Çoklu transfer kuralını tetikleyen: "
    f"{coklu_transfer_sayisi:,}"
)

print("\nÖRNEK İNCELEME SONUÇLARI")
print("-" * 48)

ornekler = islemler[
    islemler["inceleme_gerekli"]
].head(5)

for _, satir in ornekler.iterrows():
    print(f"\nİşlem: {satir['islem_id']}")
    print(f"Tarih: {satir['tarih']}")
    print(f"Gönderen: {satir['gonderen_hesap']}")
    print(f"Alıcı: {satir['alici_hesap']}")
    print(f"Tutar: {satir['tutar']:,.2f} TL")
    print(f"Neden: {satir['inceleme_nedeni']}")

print("\nSonuç dosyası oluşturuldu:")
print(CIKIS_DOSYASI)