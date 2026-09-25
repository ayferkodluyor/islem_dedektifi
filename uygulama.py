
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# İŞLEM DEDEKTİFİ - İŞLEM KONTROL MERKEZİ
# Tamamen sentetik verilerle hazırlanmış öğrenme projesidir.
# ============================================================

st.set_page_config(
    page_title="İşlem Dedektifi",
    page_icon="🔎",
    layout="wide",
)

KLASOR = Path(__file__).resolve().parent
VERI_DOSYASI = KLASOR / "analiz_sonuclari.csv"


# ============================================================
# GÖRÜNÜM
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1726;
        color: #edf4ff;
    }

    [data-testid="stSidebar"] {
        background-color: #142238;
    }

    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] p,
    [data-testid="stMain"] label {
        color: #edf4ff;
    }

    [data-testid="stMetric"] {
        background: #1a2b43;
        border: 1px solid #314761;
        border-radius: 14px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"] * {
        color: #ffffff !important;
    }

    .ust-baslik {
        background: linear-gradient(110deg, #173650, #102135);
        border: 1px solid #34546c;
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 22px;
    }

    .ust-baslik h1 {
        color: #ffffff !important;
        margin-bottom: 6px;
    }

    .ust-baslik p {
        color: #c8d8e8 !important;
        margin: 0;
    }

    .bilgi-kutusu {
        background: #1a2b43;
        border-left: 4px solid #40c9ba;
        border-radius: 8px;
        padding: 15px;
        color: #ffffff;
        margin: 12px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# VERİYİ OKU
# ============================================================

@st.cache_data
def veri_oku():
    veri = pd.read_csv(
        VERI_DOSYASI,
        encoding="utf-8-sig",
        dtype={
            "islem_id": str,
            "gonderen_hesap": str,
            "alici_hesap": str,
        },
    )

    veri["tarih"] = pd.to_datetime(
        veri["tarih"],
        errors="coerce",
    )

    veri["tutar"] = pd.to_numeric(
        veri["tutar"],
        errors="coerce",
    )

    for sutun in [
        "inceleme_gerekli",
        "yuksek_tutar",
        "coklu_transfer",
    ]:
        veri[sutun] = (
            veri[sutun]
            .astype(str)
            .str.lower()
            .eq("true")
        )

    return veri


if not VERI_DOSYASI.exists():
    st.error(
        "analiz_sonuclari.csv bulunamadı. "
        "Önce analiz_motoru.py dosyasını çalıştır."
    )
    st.stop()


try:
    islemler = veri_oku()

except Exception as hata:
    st.error(f"Veri okunamadı: {hata}")
    st.stop()


# ============================================================
# BAŞLIK VE SOL MENÜ
# ============================================================

st.markdown(
    """
    <div class="ust-baslik">
        <h1>🔎 İŞLEM DEDEKTİFİ</h1>
        <p>İşlem Kontrol Merkezi · Sıra dışı hareket analizi</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.title("🔎 İşlem Dedektifi")

    st.caption("Sentetik işlem verileri")

    st.divider()

    st.markdown("### İnceleme ekranları")

    st.markdown("🟢 İşlem Kontrol Merkezi")

    st.markdown("⚪ İşlem İnceleme — sonraki aşama")

    st.markdown("⚪ Bağlantı Haritası — sonraki aşama")

    st.divider()

    st.caption(
        "Bu uygulama gerçek işlem veya "
        "müşteri verisi içermez."
    )


# ============================================================
# GENEL GÖRÜNÜM
# ============================================================

st.header("📊 İşlem Kontrol Merkezi")

toplam_islem = len(islemler)

inceleme_sayisi = int(
    islemler["inceleme_gerekli"].sum()
)

toplam_tutar = islemler["tutar"].sum()

inceleme_orani = (
    inceleme_sayisi / toplam_islem * 100
    if toplam_islem
    else 0
)

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Toplam işlem",
    f"{toplam_islem:,}",
)

k2.metric(
    "İnceleme önerilen",
    f"{inceleme_sayisi:,}",
)

k3.metric(
    "Toplam işlem tutarı",
    f"{toplam_tutar / 1_000_000:,.1f} Mn TL",
)

k4.metric(
    "İnceleme oranı",
    f"%{inceleme_orani:.2f}",
)

st.divider()


# ============================================================
# GRAFİKLER
# ============================================================

sol, sag = st.columns(2)

with sol:
    durum_tablosu = (
        islemler["durum"]
        .value_counts()
        .rename_axis("Durum")
        .reset_index(name="İşlem sayısı")
    )

    fig = px.bar(
        durum_tablosu,
        x="Durum",
        y="İşlem sayısı",
        color="Durum",
        text="İşlem sayısı",
        title="İşlem inceleme dağılımı",
        color_discrete_map={
            "Olağan": "#36c5b3",
            "İnceleme öneriliyor": "#ffae57",
        },
    )

    fig.update_traces(
        textposition="outside",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#142238",
        plot_bgcolor="#142238",
        font=dict(
            color="#edf4ff",
            size=14,
        ),
        showlegend=False,
        height=390,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


with sag:
    nedenler = pd.DataFrame(
        {
            "Kural": [
                "Yüksek tutar",
                "Kısa sürede çoklu transfer",
            ],
            "İşlem sayısı": [
                int(islemler["yuksek_tutar"].sum()),
                int(islemler["coklu_transfer"].sum()),
            ],
        }
    )

    fig = px.bar(
        nedenler,
        x="İşlem sayısı",
        y="Kural",
        orientation="h",
        text="İşlem sayısı",
        title="İnceleme kurallarının tetiklenmesi",
        color_discrete_sequence=["#ffae57"],
    )

    fig.update_traces(
        textposition="outside",
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#142238",
        plot_bgcolor="#142238",
        font=dict(
            color="#edf4ff",
            size=14,
        ),
        height=390,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# FİLTRELER
# ============================================================

st.divider()

st.subheader("📋 İşlem listesi")

f1, f2, f3 = st.columns(3)

with f1:
    durum_secimi = st.selectbox(
        "İnceleme durumu",
        [
            "Tümü",
            "İnceleme öneriliyor",
            "Olağan",
        ],
    )

with f2:
    hesap_arama = st.text_input(
        "Gönderen veya alıcı hesap ara",
        placeholder="Örn. H0001",
    ).strip().upper()

with f3:
    min_tutar = st.number_input(
        "En düşük işlem tutarı (TL)",
        min_value=0.0,
        value=0.0,
        step=1000.0,
    )


filtreli = islemler.copy()

if durum_secimi != "Tümü":
    filtreli = filtreli[
        filtreli["durum"] == durum_secimi
    ]

if hesap_arama:
    filtreli = filtreli[
        filtreli["gonderen_hesap"].str.contains(
            hesap_arama,
            regex=False,
            na=False,
        )
        |
        filtreli["alici_hesap"].str.contains(
            hesap_arama,
            regex=False,
            na=False,
        )
    ]

filtreli = filtreli[
    filtreli["tutar"] >= min_tutar
]


st.write(
    f"**Filtreye uygun işlem sayısı:** {len(filtreli):,}"
)

gosterilecek_sutunlar = [
    "islem_id",
    "tarih",
    "gonderen_hesap",
    "alici_hesap",
    "tutar",
    "durum",
    "inceleme_nedeni",
]

st.dataframe(
    filtreli[gosterilecek_sutunlar].sort_values(
        "tarih",
        ascending=False,
    ),
    use_container_width=True,
    hide_index=True,
    height=430,
    column_config={
        "islem_id": "İşlem ID",
        "tarih": st.column_config.DatetimeColumn(
            "Tarih",
            format="DD.MM.YYYY HH:mm",
        ),
        "gonderen_hesap": "Gönderen",
        "alici_hesap": "Alıcı",
        "tutar": st.column_config.NumberColumn(
            "Tutar (TL)",
            format="%.2f",
        ),
        "durum": "Durum",
        "inceleme_nedeni": st.column_config.TextColumn(
            "İnceleme nedeni",
            width="large",
        ),
    },
)


# ============================================================
# İLK SÜRÜM BİLGİSİ
# ============================================================

st.markdown(
    """
    <div class="bilgi-kutusu">
        <strong>İlk aşama tamamlandı:</strong>
        İşlem verileri, inceleme kuralları ve filtrelenebilir
        işlem tablosu hazır. Sonraki aşamada bir işlemi seçerek
        ayrıntılarını inceleyebileceğiz.
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Öğrenme amaçlı prototip · Tamamen sentetik veriler · "
    "İnceleme işareti, dolandırıcılık tespiti anlamına gelmez."
)