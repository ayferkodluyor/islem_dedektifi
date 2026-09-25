
from pathlib import Path
import math
import html

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# İŞLEM DEDEKTİFİ v3 — DİJİTAL İNCELEME MASASI
# Tamamen sentetik verilerle hazırlanmış öğrenme projesi.
# ============================================================

st.set_page_config(
    page_title="İşlem Dedektifi | Dijital İnceleme Masası",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

KLASOR = Path(__file__).resolve().parent
VERI_DOSYASI = KLASOR / "analiz_sonuclari.csv"

BG = "#07111e"
PANEL = "#0d2032"
CYAN = "#40e5dc"
BLUE = "#75b8ef"
ORANGE = "#ffae63"
RED = "#ff6977"
WHITE = "#edf8ff"


# ============================================================
# TASARIM
# ============================================================

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 82% 0%, #123653 0%, transparent 38%),
            radial-gradient(ellipse at 0% 60%, #102c3d 0%, transparent 35%),
            #07111e;
        color: #edf8ff;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1900px;
        padding-top: 1.2rem;
        padding-left: 1.4rem;
        padding-right: 1.4rem;
    }

    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] p,
    [data-testid="stMain"] label {
        color: #edf8ff !important;
    }

    [data-testid="stMain"] input,
    [data-testid="stMain"] [data-baseweb="select"] > div {
        background: #142d42 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border-color: #36546a !important;
    }

    [data-testid="stMain"] input::placeholder {
        color: #a9c1d0 !important;
        -webkit-text-fill-color: #a9c1d0 !important;
    }

    [data-testid="stMain"] button {
        border-radius: 9px;
        border-color: #35556b;
    }

    [data-testid="stMain"] button[kind="primary"] {
        background: #116c73 !important;
        color: #ffffff !important;
        border-color: #40e5dc !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #28495d !important;
        border-radius: 14px !important;
    }

    .hero {
        position: relative;
        overflow: hidden;
        min-height: 165px;
        padding: 26px 30px;
        border: 1px solid #276079;
        border-radius: 17px;
        background:
            radial-gradient(circle at 76% 35%, #135b71 0%, transparent 27%),
            linear-gradient(115deg, #102a40 0%, #081625 72%);
        margin-bottom: 16px;
    }

    .hero::before {
        content: "01001101 00101010 10110100 00110110 01001011 10100101";
        position: absolute;
        right: -5%;
        top: 18px;
        width: 48%;
        color: #4ce4e3;
        opacity: .15;
        font: 18px/2 monospace;
        letter-spacing: 9px;
        overflow-wrap: anywhere;
        animation: drift 13s linear infinite alternate;
        pointer-events: none;
    }

    .hero::after {
        content: "";
        position: absolute;
        right: 7%;
        top: -85px;
        width: 340px;
        height: 340px;
        border: 1px solid #40e5dc44;
        border-radius: 50%;
        box-shadow:
            0 0 0 38px #40e5dc0a,
            0 0 0 77px #40e5dc07,
            0 0 45px #40e5dc17;
        pointer-events: none;
    }

    @keyframes drift {
        from { transform: translateY(-8px); }
        to { transform: translateY(16px); }
    }

    .hero-content {
        position: relative;
        z-index: 1;
    }

    .eyebrow {
        color: #40e5dc;
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #ffffff;
        font-size: clamp(28px, 3vw, 42px);
        font-weight: 900;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }

    .hero-sub {
        color: #c5d9e7;
        font-size: 14px;
        max-width: 720px;
    }

    .hero-tag {
        display: inline-block;
        margin-top: 16px;
        padding: 6px 12px;
        border: 1px solid #2b857e;
        border-radius: 30px;
        background: #0e393d;
        color: #8cf8eb;
        font-size: 11px;
    }

    .kpi {
        min-height: 116px;
        border: 1px solid #2a5066;
        border-radius: 13px;
        background: linear-gradient(125deg, #15354b, #0d2032);
        padding: 16px 18px;
        position: relative;
        overflow: hidden;
    }

    .kpi::after {
        content: "";
        position: absolute;
        right: -16px;
        bottom: -37px;
        width: 105px;
        height: 105px;
        border: 1px solid #ffffff16;
        border-radius: 50%;
        box-shadow: 0 0 0 15px #ffffff05, 0 0 0 31px #ffffff04;
    }

    .kpi.orange {
        background: linear-gradient(125deg, #392a25, #192330);
        border-color: #79513c;
    }

    .kpi.purple {
        background: linear-gradient(125deg, #302746, #152338);
        border-color: #635180;
    }

    .kpi-label {
        color: #bed3df;
        font-size: 11px;
        letter-spacing: .7px;
        font-weight: 700;
    }

    .kpi-value {
        color: #ffffff;
        font-size: 32px;
        font-weight: 850;
        margin-top: 8px;
    }

    .kpi.orange .kpi-value {
        color: #ffb66f;
    }

    .kpi.purple .kpi-value {
        color: #d2b6ff;
    }

    .kpi-foot {
        color: #8aaebf;
        font-size: 10px;
        margin-top: 6px;
    }

    .section-label {
        color: #40e5dc;
        font-size: 11px;
        letter-spacing: 1.5px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .panel-heading {
        color: #ffffff;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .panel-sub {
        color: #9db8c9;
        font-size: 12px;
        margin-bottom: 13px;
    }

    .status-alert {
        background: #39251f;
        color: #ffe2c5;
        border: 1px solid #9a613b;
        border-left: 4px solid #ffae63;
        border-radius: 10px;
        padding: 13px;
        margin: 10px 0;
        overflow-wrap: anywhere;
    }

    .status-normal {
        background: #113832;
        color: #d0fff1;
        border: 1px solid #237a6b;
        border-left: 4px solid #40e5dc;
        border-radius: 10px;
        padding: 13px;
        margin: 10px 0;
    }

    .detail {
        background: #10283a;
        border: 1px solid #294a60;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 9px;
    }

    .detail-label {
        color: #91b4c8;
        font-size: 11px;
        margin-bottom: 5px;
    }

    .detail-value {
        color: #ffffff;
        font-size: 16px;
        font-weight: 750;
        overflow-wrap: anywhere;
    }

    .flow-strip {
        background: #091b2b;
        border: 1px solid #2d5267;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0 13px;
        font: 12px/1.9 monospace;
        color: #8ceee4;
        overflow-wrap: anywhere;
    }

    .small-note {
        color: #a7bdcc;
        font-size: 11px;
        line-height: 1.6;
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #40e5dc !important;
        border-bottom-color: #40e5dc !important;
    }

    @media (prefers-reduced-motion: reduce) {
        .hero::before { animation: none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# VERİ
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

    gerekli = [
        "islem_id",
        "tarih",
        "gonderen_hesap",
        "alici_hesap",
        "tutar",
        "inceleme_gerekli",
        "yuksek_tutar",
        "coklu_transfer",
        "inceleme_nedeni",
    ]

    eksik = [sutun for sutun in gerekli if sutun not in veri.columns]

    if eksik:
        raise ValueError(
            "Analiz dosyasında eksik sütunlar: " + ", ".join(eksik)
        )

    veri["tarih"] = pd.to_datetime(
        veri["tarih"], errors="coerce"
    )

    veri["tutar"] = pd.to_numeric(
        veri["tutar"], errors="coerce"
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
    st.error(f"Veri okunamadı: {hata}")
    st.stop()

if df.empty:
    st.warning("Analiz dosyasında gösterilecek işlem yok.")
    st.stop()


# ============================================================
# YARDIMCILAR
# ============================================================

def guvenli(deger):
    return html.escape(str(deger))


def tl(tutar):
    return (
        f"{float(tutar):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
        + " TL"
    )


def kpi(etiket, deger, aciklama, sinif=""):
    st.markdown(
        f"""
        <div class="kpi {sinif}">
            <div class="kpi-label">{guvenli(etiket)}</div>
            <div class="kpi-value">{guvenli(deger)}</div>
            <div class="kpi-foot">{guvenli(aciklama)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def bolum(kod, baslik, aciklama=""):
    st.markdown(
        f"""
        <div class="section-label">{guvenli(kod)}</div>
        <div class="panel-heading">{guvenli(baslik)}</div>
        <div class="panel-sub">{guvenli(aciklama)}</div>
        """,
        unsafe_allow_html=True,
    )


def detay(etiket, deger):
    st.markdown(
        f"""
        <div class="detail">
            <div class="detail-label">{guvenli(etiket)}</div>
            <div class="detail-value">{guvenli(deger)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hesap_islemleri(hesap):
    return df[
        (df["gonderen_hesap"] == hesap)
        | (df["alici_hesap"] == hesap)
    ].copy()


def hesap_ozeti(hesap):
    ilgili = hesap_islemleri(hesap)

    karsilar = set(
        ilgili.loc[
            ilgili["gonderen_hesap"] == hesap,
            "alici_hesap",
        ]
    ) | set(
        ilgili.loc[
            ilgili["alici_hesap"] == hesap,
            "gonderen_hesap",
        ]
    )

    karsilar.discard(hesap)

    return {
        "islem": len(ilgili),
        "inceleme": int(ilgili["inceleme_gerekli"].sum()),
        "tutar": float(ilgili["tutar"].sum()),
        "baglanti": len(karsilar),
    }


def inceleme_aciklamasi(islem):
    neden = str(islem["inceleme_nedeni"]).strip()

    if not islem["inceleme_gerekli"]:
        return (
            "Bu işlem, tanımladığımız yüksek tutar ve "
            "kısa sürede çoklu transfer kuralları "
            "tarafından işaretlenmedi."
        )

    if neden and neden.lower() not in ["nan", "none"]:
        return neden

    nedenler = []

    if islem["yuksek_tutar"]:
        nedenler.append("Yüksek tutar kuralı tetiklendi.")

    if islem["coklu_transfer"]:
        nedenler.append(
            "Kısa sürede çoklu transfer kuralı tetiklendi."
        )

    return " ".join(nedenler) or "İnceleme kuralı tetiklendi."


# ============================================================
# BAĞLANTI HARİTASI
# ============================================================

def harita_olustur(merkez, secili_islem):
    ilgili = hesap_islemleri(merkez)

    baglantilar = {}

    for _, satir in ilgili.iterrows():
        gonderen = satir["gonderen_hesap"]
        alici = satir["alici_hesap"]

        karsi = alici if gonderen == merkez else gonderen

        if karsi == merkez:
            continue

        if karsi not in baglantilar:
            baglantilar[karsi] = {
                "adet": 0,
                "tutar": 0.0,
                "giden": 0,
                "gelen": 0,
            }

        baglantilar[karsi]["adet"] += 1
        baglantilar[karsi]["tutar"] += float(satir["tutar"])

        if gonderen == merkez:
            baglantilar[karsi]["giden"] += 1
        else:
            baglantilar[karsi]["gelen"] += 1

    secili_karsi = (
        secili_islem["alici_hesap"]
        if secili_islem["gonderen_hesap"] == merkez
        else secili_islem["gonderen_hesap"]
    )

    # En yoğun bağlantılar öne çıkarılır.
    hesaplar = sorted(
        baglantilar,
        key=lambda h: (
            baglantilar[h]["adet"],
            baglantilar[h]["tutar"],
        ),
        reverse=True,
    )

    if secili_karsi in hesaplar:
        hesaplar.remove(secili_karsi)
        hesaplar.insert(0, secili_karsi)

    hesaplar = hesaplar[:12]

    fig = go.Figure()

    adet = len(hesaplar)

    for sira, hesap in enumerate(hesaplar):
        aci = (
            2 * math.pi * sira / max(adet, 1)
            - math.pi / 2
        )

        x = 1.65 * math.cos(aci)
        y = 1.42 * math.sin(aci)

        secili_mi = hesap == secili_karsi

        renk = ORANGE if secili_mi else "#4c83a4"

        fig.add_trace(
            go.Scatter(
                x=[0, x],
                y=[0, y],
                mode="lines",
                line=dict(
                    color=renk,
                    width=4 if secili_mi else 1.6,
                ),
                hoverinfo="skip",
                showlegend=False,
            )
        )

        # Ok, yalnızca seçili işlemin transfer yönünü gösterir.
        if secili_mi:
            merkezden_cikis = (
                secili_islem["gonderen_hesap"] == merkez
            )

            bas_x = 0.25 * x if merkezden_cikis else 0.80 * x
            bas_y = 0.25 * y if merkezden_cikis else 0.80 * y

            son_x = 0.80 * x if merkezden_cikis else 0.25 * x
            son_y = 0.80 * y if merkezden_cikis else 0.25 * y

            fig.add_annotation(
                x=son_x,
                y=son_y,
                ax=bas_x,
                ay=bas_y,
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=3,
                arrowsize=1.5,
                arrowwidth=3,
                arrowcolor=ORANGE,
                text="",
            )

        bilgi = baglantilar[hesap]

        hover = (
            f"<b>{guvenli(hesap)}</b><br>"
            f"Merkez hesapla toplam işlem: {bilgi['adet']}<br>"
            f"Merkezden bu hesaba: {bilgi['giden']}<br>"
            f"Bu hesaptan merkeze: {bilgi['gelen']}<br>"
            f"Toplam transfer tutarı: {tl(bilgi['tutar'])}"
            "<extra></extra>"
        )

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                text=[hesap],
                textposition="bottom center",
                textfont=dict(
                    color=WHITE,
                    size=12,
                ),
                marker=dict(
                    size=24 if secili_mi else 17,
                    color=ORANGE if secili_mi else BLUE,
                    line=dict(
                        color="#e6faff",
                        width=1.5,
                    ),
                ),
                hovertemplate=hover,
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers+text",
            text=[merkez],
            textposition="bottom center",
            textfont=dict(
                color=WHITE,
                size=15,
            ),
            marker=dict(
                size=39,
                color=CYAN,
                line=dict(
                    color="#ffffff",
                    width=2,
                ),
            ),
            hovertemplate=(
                f"<b>İncelenen hesap: {guvenli(merkez)}</b>"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    fig.update_layout(
        height=465,
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        margin=dict(l=5, r=5, t=10, b=10),
        font=dict(color=WHITE),
        xaxis=dict(
            visible=False,
            range=[-2.1, 2.1],
            fixedrange=True,
        ),
        yaxis=dict(
            visible=False,
            range=[-1.9, 1.9],
            fixedrange=True,
            scaleanchor="x",
            scaleratio=1,
        ),
        dragmode=False,
    )

    return fig, len(baglantilar)


# ============================================================
# AÇILIŞTA İNCELEME ÖNERİLEN İŞLEM
# ============================================================

if "v3_secili_islem" not in st.session_state:
    oncelikli = df[df["inceleme_gerekli"]].sort_values(
        ["tutar", "tarih"],
        ascending=[False, False],
    )

    ilk = oncelikli.iloc[0] if not oncelikli.empty else df.iloc[0]

    st.session_state["v3_secili_islem"] = ilk["islem_id"]

if "v3_filtre" not in st.session_state:
    st.session_state["v3_filtre"] = "İnceleme önerilen"


# ============================================================
# ÜST ALAN
# ============================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-content">
            <div class="eyebrow">DİJİTAL İNCELEME MASASI / 001</div>
            <div class="hero-title">🔎 İŞLEM DEDEKTİFİ</div>
            <div class="hero-sub">
                10.000 sentetik transferin içinden inceleme gerektirebilecek
                hareketleri keşfet. Bir işlem seç, neden işaretlendiğini
                gör ve ilgili hesabın bağlantılarını incele.
            </div>
            <div class="hero-tag">
                ● KURAL BAZLI ANALİZ &nbsp;·&nbsp;
                SENTETİK VERİ &nbsp;·&nbsp;
                ETKİLEŞİMLİ İNCELEME
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

toplam = len(df)
inceleme = int(df["inceleme_gerekli"].sum())
yuksek = int(df["yuksek_tutar"].sum())
coklu = int(df["coklu_transfer"].sum())

k1, k2, k3, k4 = st.columns(4, gap="small")

with k1:
    kpi(
        "◈ TARANAN İŞLEM",
        f"{toplam:,}",
        "Veri setindeki toplam transfer",
    )

with k2:
    kpi(
        "⚠ İNCELEME KUYRUĞU",
        f"{inceleme:,}",
        f"İşlemlerin %{inceleme / toplam * 100:.2f} kadarı",
        "orange",
    )

with k3:
    kpi(
        "↗ YÜKSEK TUTAR",
        f"{yuksek:,}",
        "Tutar kuralını tetikleyen işlem",
        "purple",
    )

with k4:
    kpi(
        "◎ ÇOKLU TRANSFER",
        f"{coklu:,}",
        "Çoklu transfer kuralını tetikleyen işlem",
    )

st.write("")

sekme_havuz, sekme_dosya, sekme_harita, sekme_rapor = st.tabs(
    [
        "◈ İşlem Havuzu",
        "▤ İnceleme Dosyası",
        "◎ Bağlantı Analizi",
        "▥ Raporlar",
    ]
)


# ============================================================
# İŞLEM SEÇİMİ
# ============================================================

def secili_islemi_getir():
    kimlik = st.session_state["v3_secili_islem"]
    eslesen = df[df["islem_id"] == kimlik]

    if eslesen.empty:
        return df.iloc[0]

    return eslesen.iloc[0]


def islem_detay_paneli(islem):
    bolum(
        "03 / DİJİTAL DEDEKTİF",
        "Seçili İşlem",
        "İşlem ayrıntıları ve kural değerlendirmesi",
    )

    detay("İŞLEM KİMLİĞİ", islem["islem_id"])

    detay(
        "PARA TRANSFERİ",
        f"{islem['gonderen_hesap']}  →  {islem['alici_hesap']}",
    )

    detay("İŞLEM TUTARI", tl(islem["tutar"]))

    detay(
        "İŞLEM ZAMANI",
        islem["tarih"].strftime("%d.%m.%Y · %H:%M:%S"),
    )

    if islem["inceleme_gerekli"]:
        st.markdown(
            """
            <div class="status-alert">
                <strong>⚠ İNCELEME ÖNERİLİYOR</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="status-normal">
                <strong>● MEVCUT KURALLARA GÖRE OLAĞAN</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("**Bu işlem neden bu durumda?**")
    st.write(inceleme_aciklamasi(islem))

    st.divider()

    hesap = islem["gonderen_hesap"]
    ozet = hesap_ozeti(hesap)

    st.markdown(f"#### Hesap özeti · {hesap}")

    a, b = st.columns(2)

    with a:
        st.metric("Toplam işlem", f"{ozet['islem']:,}")
        st.metric("Bağlantılı hesap", f"{ozet['baglanti']:,}")

    with b:
        st.metric("İnceleme önerilen", f"{ozet['inceleme']:,}")
        st.metric("Toplam tutar", tl(ozet["tutar"]))

    st.caption(
        "Bu özet, seçili işlemin gönderen hesabının "
        "veri setindeki gönderdiği ve aldığı transferleri kapsar."
    )


# ============================================================
# 1 — İŞLEM HAVUZU
# ============================================================

with sekme_havuz:

    sol, orta, sag = st.columns(
        [1.12, 1.5, 1.12],
        gap="medium",
    )

    with sol:
        with st.container(border=True):

            bolum(
                "01 / İŞLEM HAVUZU",
                "İşlem Listesi",
                "İşlemleri filtrele ve incelemek istediğini seç.",
            )

            filtreler = [
                "İnceleme önerilen",
                "Tümü",
                "Olağan",
                "Yüksek tutar",
                "Çoklu transfer",
            ]

            # Her filtre gerçek bir butondur.
            for baslangic in [0, 3]:
                satir_filtreleri = filtreler[baslangic:baslangic + 3]
                buton_kolonlari = st.columns(len(satir_filtreleri))

                for kolon, ad in zip(buton_kolonlari, satir_filtreleri):
                    with kolon:
                        st.button(
                            ad,
                            key=f"v3_filtre_{ad}",
                            width="stretch",
                            type=(
                                "primary"
                                if st.session_state["v3_filtre"] == ad
                                else "secondary"
                            ),
                            on_click=lambda yeni=ad: (
                                st.session_state.update(
                                    {
                                        "v3_filtre": yeni,
                                        "v3_sayfa": 1,
                                    }
                                )
                            ),
                        )

            st.caption(
                "Aktif filtre: "
                + st.session_state["v3_filtre"]
            )

            arama = st.text_input(
                "Hesap veya işlem ID ara",
                placeholder="Örn. H0095 veya I008399",
                key="v3_arama",
            ).strip().upper()

            liste = df.copy()
            aktif_filtre = st.session_state["v3_filtre"]

            if aktif_filtre == "İnceleme önerilen":
                liste = liste[liste["inceleme_gerekli"]]

            elif aktif_filtre == "Olağan":
                liste = liste[~liste["inceleme_gerekli"]]

            elif aktif_filtre == "Yüksek tutar":
                liste = liste[liste["yuksek_tutar"]]

            elif aktif_filtre == "Çoklu transfer":
                liste = liste[liste["coklu_transfer"]]

            if arama:
                eslesme = (
                    liste["islem_id"].str.contains(
                        arama, regex=False, na=False
                    )
                    | liste["gonderen_hesap"].str.contains(
                        arama, regex=False, na=False
                    )
                    | liste["alici_hesap"].str.contains(
                        arama, regex=False, na=False
                    )
                )

                liste = liste[eslesme]

            # İnceleme önerilenlerde en yüksek tutar önce gelir.
            # Diğer filtrelerde en yeni işlem önce gelir.
            if aktif_filtre == "İnceleme önerilen":
                liste = liste.sort_values(
                    ["tutar", "tarih"],
                    ascending=[False, False],
                )
            else:
                liste = liste.sort_values(
                    "tarih",
                    ascending=False,
                )

            st.caption(
                f"Filtreye uygun **{len(liste):,} işlem**"
            )

            if liste.empty:
                st.info("Bu filtreye uygun işlem bulunamadı.")

            else:
                sayfa_boyutu = 12
                toplam_sayfa = math.ceil(
                    len(liste) / sayfa_boyutu
                )

                if "v3_sayfa" not in st.session_state:
                    st.session_state["v3_sayfa"] = 1

                if st.session_state["v3_sayfa"] > toplam_sayfa:
                    st.session_state["v3_sayfa"] = 1

                sayfa = st.number_input(
                    "Liste sayfası",
                    min_value=1,
                    max_value=toplam_sayfa,
                    step=1,
                    key="v3_sayfa",
                )

                baslangic = (sayfa - 1) * sayfa_boyutu

                gorunen = liste.iloc[
                    baslangic:baslangic + sayfa_boyutu
                ]

                secenekler = gorunen["islem_id"].tolist()

                etiketler = {}

                for _, satir in gorunen.iterrows():
                    isaret = (
                        "🟠"
                        if satir["inceleme_gerekli"]
                        else "🟢"
                    )

                    etiketler[satir["islem_id"]] = (
                        f"{isaret} {satir['islem_id']}"
                        f" · {tl(satir['tutar'])}"
                    )

                mevcut = st.session_state["v3_secili_islem"]

                secim = st.selectbox(
                    "İncelenecek işlemi seç",
                    options=secenekler,
                    index=(
                        secenekler.index(mevcut)
                        if mevcut in secenekler
                        else 0
                    ),
                    format_func=lambda kimlik: etiketler[kimlik],
                    key="v3_liste_secimi",
                )

                st.session_state["v3_secili_islem"] = secim

                onizleme = gorunen[
                    [
                        "islem_id",
                        "gonderen_hesap",
                        "alici_hesap",
                        "tutar",
                    ]
                ].copy()

                onizleme["tutar"] = onizleme["tutar"].map(tl)

                onizleme.columns = [
                    "İşlem",
                    "Gönderen",
                    "Alıcı",
                    "Tutar",
                ]

                st.dataframe(
                    onizleme,
                    hide_index=True,
                    width="stretch",
                    height=385,
                )

                st.caption(
                    f"Sayfa {sayfa} / {toplam_sayfa}"
                )

    secili = secili_islemi_getir()
    merkez = secili["gonderen_hesap"]

    with orta:
        with st.container(border=True):

            bolum(
                "02 / BAĞLANTI ANALİZİ",
                "Hesap Bağlantı Haritası",
                f"İncelenen hesap: {merkez} · "
                "Seçili işlemin gönderen hesabı",
            )

            fig, baglanti_sayisi = harita_olustur(
                merkez,
                secili,
            )

            st.plotly_chart(
                fig,
                width="stretch",
                config={"displayModeBar": False},
                key="v3_ana_harita",
            )

            st.caption(
                "🟢 İncelenen hesap　"
                "🟠 Seçili işlemin karşı hesabı　"
                "🔵 Diğer bağlantılı hesaplar"
            )

            st.markdown(
                f"""
                <div class="flow-strip">
                    SEÇİLİ TRANSFER<br>
                    {guvenli(secili["gonderen_hesap"])}
                    &nbsp; → &nbsp;
                    {guvenli(secili["alici_hesap"])}
                    &nbsp; | &nbsp;
                    {guvenli(tl(secili["tutar"]))}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(
                f"{merkez} hesabının veri setinde "
                f"{baglanti_sayisi} farklı hesapla "
                "doğrudan transfer bağlantısı var. "
                "Haritada en fazla 12 karşı hesap gösterilir. "
                "Turuncu ok, seçili işlemin para akış yönünü gösterir."
            )

    with sag:
        with st.container(border=True):
            islem_detay_paneli(secili)


# ============================================================
# 2 — İNCELEME DOSYASI
# ============================================================

with sekme_dosya:

    secili = secili_islemi_getir()

    bolum(
        "İNCELEME DOSYASI / 002",
        "İşlemin Zaman Çizelgesi",
        "Seçili işlemden önce ve sonra aynı hesaptan "
        "yapılan transferleri incele.",
    )

    dosya_sol, dosya_sag = st.columns(
        [1, 1.5],
        gap="large",
    )

    with dosya_sol:
        with st.container(border=True):
            islem_detay_paneli(secili)

    with dosya_sag:
        with st.container(border=True):

            hesap = secili["gonderen_hesap"]
            zaman = secili["tarih"]

            yakin = df[
                (df["gonderen_hesap"] == hesap)
                & (
                    df["tarih"]
                    >= zaman - pd.Timedelta(minutes=10)
                )
                & (
                    df["tarih"]
                    <= zaman + pd.Timedelta(minutes=10)
                )
            ].sort_values("tarih")

            st.markdown(
                f"### {hesap} · Yakın Zamanlı Transferler"
            )

            fig_zaman = go.Figure()

            fig_zaman.add_trace(
                go.Scatter(
                    x=yakin["tarih"],
                    y=yakin["tutar"],
                    mode="lines+markers",
                    line=dict(color="#507b96", width=2),
                    marker=dict(
                        size=13,
                        color=[
                            ORANGE
                            if kimlik == secili["islem_id"]
                            else CYAN
                            for kimlik in yakin["islem_id"]
                        ],
                    ),
                    text=yakin["islem_id"],
                    hovertemplate=(
                        "İşlem: %{text}<br>"
                        "Tutar: %{y:,.2f} TL"
                        "<extra></extra>"
                    ),
                    showlegend=False,
                )
            )

            fig_zaman.update_layout(
                height=340,
                paper_bgcolor=PANEL,
                plot_bgcolor=PANEL,
                font=dict(color=WHITE),
                xaxis_title="İşlem zamanı",
                yaxis_title="Tutar (TL)",
                margin=dict(l=15, r=15, t=20, b=20),
            )

            st.plotly_chart(
                fig_zaman,
                width="stretch",
                key="v3_zaman_grafigi",
            )

            st.caption(
                "Turuncu nokta seçili işlemdir. "
                "Grafik, aynı gönderen hesabın "
                "10 dakika önceki ve sonraki transferlerini gösterir."
            )

            tablo = yakin[
                [
                    "islem_id",
                    "tarih",
                    "alici_hesap",
                    "tutar",
                    "inceleme_gerekli",
                ]
            ].copy()

            tablo["tutar"] = tablo["tutar"].map(tl)

            tablo["inceleme_gerekli"] = tablo[
                "inceleme_gerekli"
            ].map(
                {
                    True: "İnceleme önerilen",
                    False: "Olağan",
                }
            )

            tablo.columns = [
                "İşlem",
                "Tarih",
                "Alıcı",
                "Tutar",
                "Durum",
            ]

            st.dataframe(
                tablo,
                hide_index=True,
                width="stretch",
            )


# ============================================================
# 3 — BAĞLANTI ANALİZİ
# ============================================================

with sekme_harita:

    bolum(
        "BAĞLANTI ANALİZİ / 003",
        "Hesapların Transfer Ağı",
        "Bir hesap seçerek hangi hesaplarla para "
        "transferi ilişkisi olduğunu incele.",
    )

    hesaplar = sorted(
        set(df["gonderen_hesap"])
        | set(df["alici_hesap"])
    )

    secili = secili_islemi_getir()

    varsayilan = secili["gonderen_hesap"]

    hesap = st.selectbox(
        "İncelenecek hesap",
        options=hesaplar,
        index=(
            hesaplar.index(varsayilan)
            if varsayilan in hesaplar
            else 0
        ),
        key="v3_hesap_secimi",
    )

    ilgili = hesap_islemleri(hesap)

    if ilgili.empty:
        st.info("Bu hesaba ait işlem bulunamadı.")

    else:
        # Haritada seçilen hesaba ait en yeni işlem vurgulanır.
        harita_islemi = ilgili.sort_values(
            "tarih",
            ascending=False,
        ).iloc[0]

        h_sol, h_sag = st.columns(
            [1.8, 1],
            gap="large",
        )

        with h_sol:
            with st.container(border=True):

                st.subheader(
                    f"◎ {hesap} · Doğrudan Bağlantılar"
                )

                buyuk_harita, toplam_baglanti = harita_olustur(
                    hesap,
                    harita_islemi,
                )

                st.plotly_chart(
                    buyuk_harita,
                    width="stretch",
                    config={"displayModeBar": False},
                    key="v3_buyuk_harita",
                )

                st.caption(
                    f"Bu hesabın {toplam_baglanti} farklı "
                    "hesapla doğrudan transfer bağlantısı var. "
                    "Turuncu çizgi, bu hesaba ait en yeni "
                    "işlemin karşı hesabını vurgular."
                )

        with h_sag:
            with st.container(border=True):

                bolum(
                    "HESAP PROFİLİ",
                    hesap,
                    "Veri setindeki gönderilen ve alınan transferler",
                )

                ozet = hesap_ozeti(hesap)

                st.metric(
                    "Toplam işlem",
                    f"{ozet['islem']:,}",
                )

                st.metric(
                    "İnceleme önerilen",
                    f"{ozet['inceleme']:,}",
                )

                st.metric(
                    "Bağlantılı hesap",
                    f"{ozet['baglanti']:,}",
                )

                st.metric(
                    "Toplam transfer tutarı",
                    tl(ozet["tutar"]),
                )

        st.subheader("Hesabın İşlem Geçmişi")

        st.dataframe(
            ilgili.sort_values(
                "tarih",
                ascending=False,
            )[
                [
                    "islem_id",
                    "tarih",
                    "gonderen_hesap",
                    "alici_hesap",
                    "tutar",
                    "inceleme_gerekli",
                ]
            ],
            hide_index=True,
            width="stretch",
            height=350,
        )


# ============================================================
# 4 — RAPORLAR
# ============================================================

with sekme_rapor:

    bolum(
        "RAPORLAMA / 004",
        "İnceleme Özeti",
        "Kural sonuçlarını karşılaştır ve raporu indir.",
    )

    r1, r2 = st.columns(
        [1, 1.3],
        gap="large",
    )

    with r1:
        with st.container(border=True):

            st.subheader("Kural Dağılımı")

            fig_kural = go.Figure(
                go.Bar(
                    x=[
                        "Yüksek tutar",
                        "Çoklu transfer",
                    ],
                    y=[
                        yuksek,
                        coklu,
                    ],
                    marker_color=[
                        ORANGE,
                        CYAN,
                    ],
                    text=[
                        yuksek,
                        coklu,
                    ],
                    textposition="outside",
                )
            )

            fig_kural.update_layout(
                height=360,
                paper_bgcolor=PANEL,
                plot_bgcolor=PANEL,
                font=dict(color=WHITE),
                showlegend=False,
                yaxis_title="İşlem sayısı",
                margin=dict(l=10, r=10, t=25, b=15),
            )

            st.plotly_chart(
                fig_kural,
                width="stretch",
                key="v3_kural_grafigi",
            )

            st.caption(
                "Bir işlem birden fazla kuralı tetikleyebilir. "
                "Bu nedenle kural sayılarının toplamı, "
                "benzersiz inceleme önerilen işlem sayısından "
                "farklı olabilir."
            )

    with r2:
        with st.container(border=True):

            st.subheader("İnceleme Kuyruğu")

            rapor_df = df[
                df["inceleme_gerekli"]
            ].sort_values(
                ["tutar", "tarih"],
                ascending=[False, False],
            )

            st.dataframe(
                rapor_df[
                    [
                        "islem_id",
                        "tarih",
                        "gonderen_hesap",
                        "alici_hesap",
                        "tutar",
                        "inceleme_nedeni",
                    ]
                ],
                hide_index=True,
                width="stretch",
                height=390,
            )

            st.download_button(
                "⬇ İnceleme listesini CSV indir",
                data=rapor_df.to_csv(
                    index=False,
                ).encode("utf-8-sig"),
                file_name="islem_dedektifi_inceleme_raporu.csv",
                mime="text/csv",
                width="stretch",
            )

            st.caption(
                "İndirilen dosya yalnızca bu öğrenme "
                "projesindeki sentetik verileri içerir."
            )


# ============================================================
# ALT BİLGİ
# ============================================================

st.divider()

st.caption(
    "İşlem Dedektifi v3 · Python + Pandas + Streamlit + Plotly "
    "· Tamamen sentetik verilerle hazırlanmış öğrenme projesi"
)

st.caption(
    "İnceleme önerisi, tanımlanan kuralların tetiklendiğini "
    "gösterir; tek başına dolandırıcılık veya usulsüzlük "
    "tespiti anlamına gelmez. Ekrandaki hareketli arka plan "
    "dekoratiftir; canlı banka verisi gösterilmez."
)