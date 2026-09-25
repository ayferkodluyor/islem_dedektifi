
from pathlib import Path
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# İŞLEM DEDEKTİFİ v2
# Dijital İnceleme Masası
# Tamamen sentetik verilerle hazırlanmış öğrenme projesidir.
# ============================================================

st.set_page_config(
    page_title="İşlem Dedektifi | Dijital İnceleme Masası",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

KLASOR = Path(__file__).resolve().parent
VERI_DOSYASI = KLASOR / "analiz_sonuclari.csv"

ARKA_PLAN = "#081421"
PANEL = "#102235"
TURKUAZ = "#43E0D0"
TURUNCU = "#FFB15E"
MAVI = "#74AEE0"
YAZI = "#F0F6FF"


# ============================================================
# GÖRÜNÜM
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #081421;
        color: #F0F6FF;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1900px;
        padding-top: 1.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
    }

    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] p,
    [data-testid="stMain"] label {
        color: #F0F6FF !important;
    }

    [data-testid="stMain"] input,
    [data-testid="stMain"] textarea,
    [data-testid="stMain"] [data-baseweb="select"] > div {
        background: #183047 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-color: #36536A !important;
    }

    [data-testid="stMain"] input::placeholder {
        color: #B6C7D8 !important;
        -webkit-text-fill-color: #B6C7D8 !important;
    }

    [data-testid="stMain"] button {
        border-radius: 9px;
        border: 1px solid #36536A;
    }

    [data-testid="stMain"] button[kind="primary"] {
        background: #147B7A !important;
        color: #FFFFFF !important;
        border-color: #43E0D0 !important;
    }

    [data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #29435A !important;
    }

    [data-testid="stMetric"] {
        background: #142A40;
        border: 1px solid #29435A;
        border-radius: 11px;
        padding: 12px;
    }

    [data-testid="stMetricLabel"] *,
    [data-testid="stMetricValue"] * {
        color: #FFFFFF !important;
    }

    .ana-baslik {
        background: linear-gradient(110deg, #143348, #0A1A2A);
        border: 1px solid #2A5266;
        border-radius: 15px;
        padding: 19px 23px;
        margin-bottom: 17px;
    }

    .ana-baslik h1 {
        color: #FFFFFF !important;
        font-size: 29px;
        margin: 0 0 6px 0;
    }

    .ana-baslik p {
        color: #BFD0DE !important;
        margin: 0;
        font-size: 13px;
    }

    .bilgi-karti {
        background: linear-gradient(120deg, #142D42, #102033);
        border: 1px solid #2D4B61;
        border-radius: 12px;
        padding: 15px;
        min-height: 91px;
    }

    .bilgi-karti.uyari {
        background: linear-gradient(120deg, #3A2A21, #1C2431);
        border-color: #76513B;
    }

    .bilgi-karti.mor {
        background: linear-gradient(120deg, #2C2444, #182138);
        border-color: #57417C;
    }

    .bilgi-karti .etiket {
        color: #BFD0DE;
        font-size: 12px;
        font-weight: 600;
    }

    .bilgi-karti .deger {
        color: #FFFFFF;
        font-size: 26px;
        font-weight: 800;
        margin-top: 6px;
    }

    .bilgi-karti.uyari .deger {
        color: #FFB15E;
    }

    .bolum-baslik {
        color: #43E0D0;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .inceleme-uyarisi {
        background: #39291F;
        border: 1px solid #946039;
        border-left: 5px solid #FFB15E;
        border-radius: 10px;
        padding: 14px;
        color: #FFE0B8;
        overflow-wrap: anywhere;
    }

    .inceleme-normal {
        background: #123B38;
        border: 1px solid #287E73;
        border-left: 5px solid #43E0D0;
        border-radius: 10px;
        padding: 14px;
        color: #C2FFF2;
        overflow-wrap: anywhere;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: #43E0D0 !important;
        border-bottom-color: #43E0D0 !important;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #29435A;
        border-radius: 9px;
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

    gerekli_sutunlar = [
        "islem_id",
        "tarih",
        "gonderen_hesap",
        "alici_hesap",
        "tutar",
        "inceleme_gerekli",
        "yuksek_tutar",
        "coklu_transfer",
        "durum",
        "inceleme_nedeni",
    ]

    eksikler = [
        sutun
        for sutun in gerekli_sutunlar
        if sutun not in veri.columns
    ]

    if eksikler:
        raise ValueError(
            "CSV dosyasında eksik sütunlar: "
            + ", ".join(eksikler)
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
            .str.strip()
            .str.lower()
            .isin(["true", "1", "evet"])
        )

    veri["inceleme_nedeni"] = (
        veri["inceleme_nedeni"]
        .fillna("")
        .astype(str)
    )

    veri = veri.dropna(
        subset=[
            "islem_id",
            "tarih",
            "gonderen_hesap",
            "alici_hesap",
            "tutar",
        ]
    )

    return veri


if not VERI_DOSYASI.exists():
    st.error(
        "analiz_sonuclari.csv bulunamadı. "
        "Önce analiz_motoru.py dosyasını çalıştır."
    )
    st.stop()

try:
    df = veri_oku()
except Exception as hata:
    st.error(f"Veriler okunamadı: {hata}")
    st.stop()

if df.empty:
    st.warning("Analiz dosyasında gösterilecek işlem bulunamadı.")
    st.stop()


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def tl(tutar):
    return (
        f"{float(tutar):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
        + " TL"
    )


def bilgi_karti(etiket, deger, sinif=""):
    # HTML tek satırda tutuluyor; ekranda kod gibi görünmez.
    st.markdown(
        (
            f'<div class="bilgi-karti {sinif}">'
            f'<div class="etiket">{etiket}</div>'
            f'<div class="deger">{deger}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )


def baslik(metin):
    st.markdown(
        f'<div class="bolum-baslik">{metin}</div>',
        unsafe_allow_html=True,
    )


def secili_islem_getir():
    islem_id = st.session_state.get("secili_islem_id")

    eslesen = df[df["islem_id"] == islem_id]

    if eslesen.empty:
        return df.iloc[0]

    return eslesen.iloc[0]


def hesap_ozeti(hesap):
    ilgili = df[
        (df["gonderen_hesap"] == hesap)
        | (df["alici_hesap"] == hesap)
    ]

    karsi_hesaplar = set()

    for _, islem in ilgili.iterrows():
        if islem["gonderen_hesap"] == hesap:
            karsi_hesaplar.add(islem["alici_hesap"])
        else:
            karsi_hesaplar.add(islem["gonderen_hesap"])

    karsi_hesaplar.discard(hesap)

    return {
        "islem_sayisi": len(ilgili),
        "inceleme_sayisi": int(
            ilgili["inceleme_gerekli"].sum()
        ),
        "toplam_tutar": float(ilgili["tutar"].sum()),
        "baglanti_sayisi": len(karsi_hesaplar),
    }


def baglanti_haritasi(veri, merkez_hesap, secili_islem):
    ilgili = veri[
        (veri["gonderen_hesap"] == merkez_hesap)
        | (veri["alici_hesap"] == merkez_hesap)
    ].copy()

    secili_karsi_hesap = (
        secili_islem["alici_hesap"]
        if secili_islem["gonderen_hesap"] == merkez_hesap
        else secili_islem["gonderen_hesap"]
    )

    ilgili["secili_mi"] = (
        ilgili["islem_id"] == secili_islem["islem_id"]
    )

    ilgili = ilgili.sort_values(
        ["secili_mi", "inceleme_gerekli", "tarih"],
        ascending=[False, False, False],
    )

    baglantilar = {}

    for _, islem in ilgili.iterrows():
        diger = (
            islem["alici_hesap"]
            if islem["gonderen_hesap"] == merkez_hesap
            else islem["gonderen_hesap"]
        )

        if diger == merkez_hesap:
            continue

        if diger not in baglantilar:
            baglantilar[diger] = {
                "adet": 0,
                "tutar": 0.0,
            }

        baglantilar[diger]["adet"] += 1
        baglantilar[diger]["tutar"] += float(
            islem["tutar"]
        )

    hesaplar = list(baglantilar.keys())

    # Seçilen işlemin karşı hesabı ilk sırada.
    if secili_karsi_hesap in hesaplar:
        hesaplar.remove(secili_karsi_hesap)
        hesaplar.insert(0, secili_karsi_hesap)

    # Haritanın kalabalıklaşmaması için ilk 12 bağlantı.
    hesaplar = hesaplar[:12]

    fig = go.Figure()

    adet = len(hesaplar)

    konumlar = {}

    for sira, hesap in enumerate(hesaplar):
        aci = (
            2 * math.pi * sira / max(adet, 1)
            - math.pi / 2
        )

        konumlar[hesap] = (
            1.65 * math.cos(aci),
            1.40 * math.sin(aci),
        )

    # Bağlantı çizgileri
    for hesap in hesaplar:
        x, y = konumlar[hesap]

        secili_baglanti = (
            hesap == secili_karsi_hesap
        )

        fig.add_trace(
            go.Scatter(
                x=[0, x],
                y=[0, y],
                mode="lines",
                line=dict(
                    color=(
                        TURUNCU
                        if secili_baglanti
                        else "#47728D"
                    ),
                    width=(
                        4
                        if secili_baglanti
                        else 1.5
                    ),
                ),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Karşı hesaplar
    for hesap in hesaplar:
        x, y = konumlar[hesap]

        secili_baglanti = (
            hesap == secili_karsi_hesap
        )

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                text=[hesap],
                textposition="bottom center",
                textfont=dict(
                    color=YAZI,
                    size=12,
                ),
                marker=dict(
                    size=(
                        23
                        if secili_baglanti
                        else 17
                    ),
                    color=(
                        TURUNCU
                        if secili_baglanti
                        else MAVI
                    ),
                    line=dict(
                        color="#E8F6FF",
                        width=1,
                    ),
                ),
                hovertemplate=(
                    f"<b>{hesap}</b><br>"
                    f"Merkez hesapla işlem: "
                    f"{baglantilar[hesap]['adet']}<br>"
                    f"Toplam tutar: "
                    f"{tl(baglantilar[hesap]['tutar'])}"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

    # Merkez hesap
    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers+text",
            text=[merkez_hesap],
            textposition="bottom center",
            textfont=dict(
                color="#FFFFFF",
                size=15,
            ),
            marker=dict(
                size=37,
                color=TURKUAZ,
                line=dict(
                    color="#E7FFFB",
                    width=2,
                ),
            ),
            hovertemplate=(
                f"<b>Merkez hesap: {merkez_hesap}</b>"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        height=440,
        margin=dict(l=8, r=8, t=10, b=10),
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=YAZI),
        xaxis=dict(
            visible=False,
            range=[-2.15, 2.15],
            fixedrange=True,
        ),
        yaxis=dict(
            visible=False,
            range=[-1.95, 1.95],
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1,
        ),
        dragmode=False,
    )

    return fig, len(baglantilar)


def inceleme_paneli(islem):
    """
    HTML yerine Streamlit bileşenleri kullanılır.
    Böylece işlem bilgilerinin kod olarak görünmesi önlenir.
    """

    baslik("03 / DİJİTAL DEDEKTİF")

    st.subheader("Seçili İşlem")

    with st.container(border=True):
        st.caption("İŞLEM KİMLİĞİ")
        st.markdown(f"### {islem['islem_id']}")

        st.divider()

        st.caption("GÖNDEREN → ALICI")
        st.markdown(
            f"**{islem['gonderen_hesap']}**"
            "　→　"
            f"**{islem['alici_hesap']}**"
        )

        st.caption("İŞLEM TUTARI")
        st.markdown(
            f"### {tl(islem['tutar'])}"
        )

        st.caption("İŞLEM ZAMANI")
        st.write(
            islem["tarih"].strftime(
                "%d.%m.%Y · %H:%M:%S"
            )
        )

    if islem["inceleme_gerekli"]:
        st.warning("⚠️ İNCELEME ÖNERİLİYOR")

        st.write(
            islem["inceleme_nedeni"]
            or "İnceleme kurallarından en az biri tetiklendi."
        )

    else:
        st.success("● OLAĞAN İŞLEM")

        st.write(
            "Bu işlem mevcut inceleme kuralları "
            "tarafından işaretlenmedi."
        )

    st.divider()

    hesap = islem["gonderen_hesap"]
    ozet = hesap_ozeti(hesap)

    st.markdown(f"#### Hesap özeti · {hesap}")

    st.write(
        f"**Toplam işlem:** {ozet['islem_sayisi']:,}"
    )

    st.write(
        "**İnceleme önerilen:** "
        f"{ozet['inceleme_sayisi']:,}"
    )

    st.write(
        "**Toplam işlem tutarı:** "
        f"{tl(ozet['toplam_tutar'])}"
    )

    st.write(
        "**Bağlantılı hesap:** "
        f"{ozet['baglanti_sayisi']:,}"
    )

    st.caption(
        "Hesap özeti, veri setindeki gönderilen ve "
        "alınan transferler üzerinden hesaplanır."
    )


# ============================================================
# BAŞLIK
# ============================================================

st.markdown(
    (
        '<div class="ana-baslik">'
        "<h1>🔎 İŞLEM DEDEKTİFİ</h1>"
        "<p>Her işlem bir iz bırakır. "
        "Sıra dışı transferleri incele, "
        "hesap bağlantılarını keşfet.</p>"
        "</div>"
    ),
    unsafe_allow_html=True,
)


# ============================================================
# BİLGİ ŞERİDİ
# ============================================================

toplam_islem = len(df)

inceleme_sayisi = int(
    df["inceleme_gerekli"].sum()
)

yuksek_tutar_sayisi = int(
    df["yuksek_tutar"].sum()
)

coklu_transfer_sayisi = int(
    df["coklu_transfer"].sum()
)

kart1, kart2, kart3, kart4 = st.columns(
    4,
    gap="small",
)

with kart1:
    bilgi_karti(
        "◈ TOPLAM İŞLEM",
        f"{toplam_islem:,}",
    )

with kart2:
    bilgi_karti(
        "⚠ İNCELEME ÖNERİLEN",
        f"{inceleme_sayisi:,}",
        "uyari",
    )

with kart3:
    bilgi_karti(
        "↗ YÜKSEK TUTARLI",
        f"{yuksek_tutar_sayisi:,}",
        "mor",
    )

with kart4:
    bilgi_karti(
        "◎ ÇOKLU TRANSFER",
        f"{coklu_transfer_sayisi:,}",
    )

st.write("")


# ============================================================
# ÜST MENÜ
# ============================================================

sekme_havuz, sekme_dosya, sekme_harita = st.tabs(
    [
        "◈ İşlem Havuzu",
        "▤ İnceleme Dosyası",
        "◎ Bağlantı Haritası",
    ]
)


# ============================================================
# İLK SEÇİLİ İŞLEM
# ============================================================

if "secili_islem_id" not in st.session_state:
    oncelikli = df[
        df["inceleme_gerekli"]
    ].sort_values(
        "tarih",
        ascending=False,
    )

    if not oncelikli.empty:
        st.session_state["secili_islem_id"] = (
            oncelikli.iloc[0]["islem_id"]
        )
    else:
        st.session_state["secili_islem_id"] = (
            df.iloc[0]["islem_id"]
        )


# ============================================================
# 1. İŞLEM HAVUZU
# ============================================================

with sekme_havuz:

    sol, orta, sag = st.columns(
        [1.05, 1.55, 1.05],
        gap="medium",
    )

    # --------------------------------------------------------
    # SOL PANEL
    # --------------------------------------------------------

    with sol:
        with st.container(border=True):
            baslik("01 / İŞLEM HAVUZU")

            st.subheader("İşlem listesi")

            st.caption("Hızlı filtre")

            filtre = st.radio(
                "İşlem filtresi",
                [
                    "İnceleme önerilen",
                    "Tümü",
                    "Olağan",
                    "Yüksek tutar",
                    "Çoklu transfer",
                ],
                horizontal=True,
                label_visibility="collapsed",
                key="havuz_filtresi",
            )

            arama = st.text_input(
                "Hesap veya işlem ID ara",
                placeholder="Örn. H0001",
                key="havuz_arama",
            ).strip().upper()

            liste = df.copy()

            if filtre == "İnceleme önerilen":
                liste = liste[
                    liste["inceleme_gerekli"]
                ]

            elif filtre == "Olağan":
                liste = liste[
                    ~liste["inceleme_gerekli"]
                ]

            elif filtre == "Yüksek tutar":
                liste = liste[
                    liste["yuksek_tutar"]
                ]

            elif filtre == "Çoklu transfer":
                liste = liste[
                    liste["coklu_transfer"]
                ]

            if arama:
                liste = liste[
                    liste["islem_id"].str.contains(
                        arama,
                        regex=False,
                        na=False,
                    )
                    | liste["gonderen_hesap"].str.contains(
                        arama,
                        regex=False,
                        na=False,
                    )
                    | liste["alici_hesap"].str.contains(
                        arama,
                        regex=False,
                        na=False,
                    )
                ]

            liste = liste.sort_values(
                "tarih",
                ascending=False,
            )

            st.caption(
                f"Filtreye uygun {len(liste):,} işlem"
            )

            if liste.empty:
                st.info(
                    "Bu filtreye uygun işlem bulunamadı."
                )

            else:
                # 10.000 işlemi tek bir seçim kutusuna
                # doldurmak yerine sayfalama kullanıyoruz.
                sayfa_boyutu = 20

                sayfa_sayisi = math.ceil(
                    len(liste) / sayfa_boyutu
                )

                sayfa = st.number_input(
                    "Liste sayfası",
                    min_value=1,
                    max_value=sayfa_sayisi,
                    value=1,
                    step=1,
                    key="havuz_sayfa",
                )

                baslangic = (
                    sayfa - 1
                ) * sayfa_boyutu

                gorunen = liste.iloc[
                    baslangic:
                    baslangic + sayfa_boyutu
                ]

                secenekler = gorunen[
                    "islem_id"
                ].tolist()

                # Filtre değiştiğinde seçili işlem,
                # yeni listede bulunmayabilir.
                if (
                    st.session_state["secili_islem_id"]
                    not in secenekler
                ):
                    st.session_state[
                        "secili_islem_id"
                    ] = secenekler[0]

                etiketler = {}

                for _, islem in gorunen.iterrows():
                    simge = (
                        "🟠"
                        if islem["inceleme_gerekli"]
                        else "🟢"
                    )

                    etiketler[islem["islem_id"]] = (
                        f"{simge} {islem['islem_id']}"
                        f" · {tl(islem['tutar'])}"
                    )

                st.selectbox(
                    "İncelenecek işlemi seç",
                    options=secenekler,
                    format_func=lambda kimlik: (
                        etiketler[kimlik]
                    ),
                    key="secili_islem_id",
                )

                st.caption(
                    f"Sayfa {sayfa} / {sayfa_sayisi}"
                )

                onizleme = gorunen[
                    [
                        "islem_id",
                        "gonderen_hesap",
                        "alici_hesap",
                        "tutar",
                    ]
                ].copy()

                st.dataframe(
                    onizleme,
                    hide_index=True,
                    width="stretch",
                    height=340,
                    column_config={
                        "islem_id": "İşlem",
                        "gonderen_hesap": "Gönderen",
                        "alici_hesap": "Alıcı",
                        "tutar": (
                            st.column_config.NumberColumn(
                                "Tutar (TL)",
                                format="%.2f",
                            )
                        ),
                    },
                )

                st.caption(
                    "Yukarıdan işlem seçtiğinde "
                    "harita ve sağdaki inceleme "
                    "dosyası güncellenir."
                )

    # --------------------------------------------------------
    # ORTA PANEL
    # --------------------------------------------------------

    secili = secili_islem_getir()

    merkez_hesap = secili["gonderen_hesap"]

    fig, baglanti_sayisi = baglanti_haritasi(
        df,
        merkez_hesap,
        secili,
    )

    with orta:
        with st.container(border=True):
            baslik("02 / BAĞLANTI ANALİZİ")

            st.subheader(
                "Hesap Bağlantı Haritası"
            )

            st.caption(
                f"Merkez hesap: {merkez_hesap} · "
                f"Bağlantılı hesap: {baglanti_sayisi}"
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={
                    "displayModeBar": False,
                },
                key="ana_harita",
            )

            st.caption(
                "🟢 Merkez hesap　"
                "🟠 Seçili işlemin karşı hesabı　"
                "🔵 Diğer bağlantılar"
            )

    # --------------------------------------------------------
    # SAĞ PANEL
    # --------------------------------------------------------

    with sag:
        with st.container(border=True):
            inceleme_paneli(secili)


# ============================================================
# 2. İNCELEME DOSYASI
# ============================================================

with sekme_dosya:

    secili = secili_islem_getir()

    st.subheader("▤ İşlem İnceleme Dosyası")

    st.caption(
        "Seçilen işlemin ayrıntıları ve aynı gönderen "
        "hesabın yakın zamanlı transferleri."
    )

    dosya_sol, dosya_sag = st.columns(
        [1, 1.5],
        gap="large",
    )

    with dosya_sol:
        inceleme_paneli(secili)

    with dosya_sag:
        st.subheader("⏱ İşlem Zaman Çizelgesi")

        hesap = secili["gonderen_hesap"]
        zaman = secili["tarih"]

        baslangic = zaman - pd.Timedelta(
            minutes=10
        )

        bitis = zaman + pd.Timedelta(
            minutes=10
        )

        yakin = df[
            (df["gonderen_hesap"] == hesap)
            & (df["tarih"] >= baslangic)
            & (df["tarih"] <= bitis)
        ].sort_values("tarih")

        fig_zaman = go.Figure()

        fig_zaman.add_trace(
            go.Scatter(
                x=yakin["tarih"],
                y=yakin["tutar"],
                mode="lines+markers",
                marker=dict(
                    size=12,
                    color=[
                        TURUNCU
                        if kimlik == secili["islem_id"]
                        else TURKUAZ
                        for kimlik in yakin["islem_id"]
                    ],
                ),
                line=dict(
                    color="#54768C",
                    width=2,
                ),
                text=yakin["islem_id"],
                customdata=yakin[
                    ["alici_hesap"]
                ].to_numpy(),
                hovertemplate=(
                    "İşlem: %{text}<br>"
                    "Alıcı: %{customdata[0]}<br>"
                    "Tutar: %{y:,.2f} TL"
                    "<extra></extra>"
                ),
                showlegend=False,
            )
        )

        fig_zaman.update_layout(
            height=330,
            paper_bgcolor=PANEL,
            plot_bgcolor=PANEL,
            font=dict(color=YAZI),
            xaxis_title="İşlem zamanı",
            yaxis_title="Tutar (TL)",
            margin=dict(
                l=15,
                r=15,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig_zaman,
            width="stretch",
            key="zaman_cizelgesi",
        )

        st.caption(
            "Turuncu nokta seçilen işlemi gösterir. "
            "Grafik, aynı gönderen hesabın seçilen "
            "işlemden 10 dakika önceki ve sonraki "
            "transferlerini kapsar."
        )

        st.dataframe(
            yakin[
                [
                    "islem_id",
                    "tarih",
                    "alici_hesap",
                    "tutar",
                    "durum",
                ]
            ],
            hide_index=True,
            width="stretch",
            column_config={
                "islem_id": "İşlem",
                "tarih": (
                    st.column_config.DatetimeColumn(
                        "Tarih",
                        format="DD.MM.YYYY HH:mm:ss",
                    )
                ),
                "alici_hesap": "Alıcı",
                "tutar": (
                    st.column_config.NumberColumn(
                        "Tutar (TL)",
                        format="%.2f",
                    )
                ),
                "durum": "Durum",
            },
        )


# ============================================================
# 3. BAĞLANTI HARİTASI
# ============================================================

with sekme_harita:

    st.subheader("◎ Hesap Bağlantı Haritası")

    st.caption(
        "Bir hesabı seçerek veri setindeki doğrudan "
        "transfer bağlantılarını inceleyebilirsin."
    )

    hesaplar = sorted(
        set(df["gonderen_hesap"])
        | set(df["alici_hesap"])
    )

    secili = secili_islem_getir()

    varsayilan_hesap = (
        secili["gonderen_hesap"]
        if secili["gonderen_hesap"] in hesaplar
        else hesaplar[0]
    )

    hesap_secimi = st.selectbox(
        "İncelenecek hesap",
        options=hesaplar,
        index=hesaplar.index(varsayilan_hesap),
        key="harita_hesap_secimi",
    )

    hesap_islemleri = df[
        (df["gonderen_hesap"] == hesap_secimi)
        | (df["alici_hesap"] == hesap_secimi)
    ].sort_values(
        "tarih",
        ascending=False,
    )

    if hesap_islemleri.empty:
        st.info(
            "Bu hesaba ait işlem bulunamadı."
        )

    else:
        harita_islemi = hesap_islemleri.iloc[0]

        buyuk_fig, _ = baglanti_haritasi(
            df,
            hesap_secimi,
            harita_islemi,
        )

        harita_sol, harita_sag = st.columns(
            [1.8, 1],
            gap="large",
        )

        with harita_sol:
            with st.container(border=True):
                st.subheader(
                    f"{hesap_secimi} · Bağlantı Ağı"
                )

                st.plotly_chart(
                    buyuk_fig,
                    width="stretch",
                    config={
                        "displayModeBar": False,
                    },
                    key="buyuk_harita",
                )

        with harita_sag:
            st.subheader("Hesap Özeti")

            ozet = hesap_ozeti(
                hesap_secimi
            )

            st.metric(
                "Toplam işlem",
                f"{ozet['islem_sayisi']:,}",
            )

            st.metric(
                "İnceleme önerilen",
                f"{ozet['inceleme_sayisi']:,}",
            )

            st.metric(
                "Bağlantılı hesap",
                f"{ozet['baglanti_sayisi']:,}",
            )

            st.metric(
                "Toplam işlem tutarı",
                tl(ozet["toplam_tutar"]),
            )

            st.caption(
                "Haritada en fazla 12 karşı hesap "
                "gösterilir. İşlem tablosu ise "
                "seçilen hesabın tüm işlemlerini içerir."
            )

        st.subheader("Hesabın İşlem Geçmişi")

        st.dataframe(
            hesap_islemleri[
                [
                    "islem_id",
                    "tarih",
                    "gonderen_hesap",
                    "alici_hesap",
                    "tutar",
                    "durum",
                ]
            ],
            hide_index=True,
            width="stretch",
            height=350,
        )


# ============================================================
# ALT BİLGİ
# ============================================================

st.divider()

st.caption(
    "İşlem Dedektifi v2.1 · Python + Pandas + Streamlit "
    "+ Plotly · Öğrenme amaçlı prototip · "
    "Tamamen sentetik veriler"
)

st.caption(
    "İnceleme önerisi, belirlenen kuralların "
    "tetiklendiğini gösterir; tek başına "
    "dolandırıcılık veya usulsüzlük tespiti değildir."
)