import streamlit as st

st.set_page_config(
    page_title="RSW PLM Dashboard",
    page_icon="🔩",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

    .stApp {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        border: 1px solid #334155;
    }

    .main-title {
        font-size: 1.8rem;
        font-weight: 900;
        color: #f1f5f9;
        line-height: 1.3;
        margin-bottom: 0.3rem;
    }

    .main-accent {
        color: #00d4aa;
    }

    .main-sub {
        font-size: 0.85rem;
        color: #94a3b8;
    }

    .kpi-card {
        background: #111827;
        border: 1px solid #1e2d3d;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        font-family: 'JetBrains Mono', monospace;
    }

    .kpi-label {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 0.2rem;
    }

    div[data-testid="stMetric"] {
        background: #111827;
        border: 1px solid #1e2d3d;
        border-radius: 12px;
        padding: 1rem;
    }

    .pipeline-step {
        background: rgba(0, 212, 170, 0.08);
        border: 1px solid rgba(0, 212, 170, 0.25);
        border-radius: 10px;
        padding: 0.8rem;
        text-align: center;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown("""
<div class="main-header">
    <div class="main-title">
        멀티모달 딥러닝 기반 RSW 공정의<br>
        <span class="main-accent">기대손실 최소화</span> 스케줄링 최적화
    </div>
    <div class="main-sub">
        2026 KSIE 한국산업경영시스템학회 · 홍익대학교 산업및데이터공학과 김다인<br>
        PLM 기말과제 · 전홍배 교수님
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Row ──
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Best Fusion AUC", "0.884", "DS Fusion")
with col2:
    st.metric("Makespan 단축", "-3.23%", "Cost-based vs Random")
with col3:
    st.metric("Total Expected Cost", "₩41.8M", "전체 작업 통합")
with col4:
    st.metric("Stochastic 시뮬레이션", "50회", "반복 검증")

st.divider()

# ── Pipeline ──
st.subheader("🔁 연구 파이프라인")
cols = st.columns(6)
steps = [
    ("📥", "멀티모달 입력", "RGB + IR + Numeric"),
    ("🧠", "품질 예측", "CNN + MLP"),
    ("🔗", "Decision Fusion", "DS / Voting"),
    ("📐", "확률 보정", "Calibration + Entropy"),
    ("💰", "비용 변환", "Quality + Time + Energy"),
    ("📊", "Risk-aware\nScheduling", "P6 병렬 최적화"),
]
for i, (icon, title, sub) in enumerate(steps):
    with cols[i]:
        st.markdown(f"""
        <div class="pipeline-step">
            <div style="font-size:1.5rem">{icon}</div>
            <div style="font-weight:700; margin:0.3rem 0; font-size:0.8rem">{title}</div>
            <div style="font-size:0.65rem; color:#94a3b8">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Quick Summary ──
st.subheader("📋 연구 요약")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("""
    **연구 배경**
    - 저항 점용접(RSW)은 자동차 차체 생산의 핵심 공정
    - 너겟 불량 및 Explode 발생 시 재작업, 설비 정지, 에너지 손실
    - 기존 스케줄링은 공정 시간 중심 → 품질 불확실성 미반영

    **연구 목적**
    - 멀티모달 품질 확률 추정 → 생산 리스크 정량화
    - 품질 + 시간 + 탄소 비용 통합 Risk-aware Scheduling
    """)

with col_right:
    st.markdown("""
    **PLM 관점 의의**
    - 🔄 **Closed-Loop PLM**: 생산 데이터 → 설계 파라미터 피드백
    - 💡 **Lifecycle Cost**: 안정 공정 영역 도출로 설계 단계 비용 결정 지원
    - ⚖️ **QCD 통합**: Total Cost = Quality + Time + Energy
    - 📡 **Information Loss 해소**: 멀티모달 센서 → 정보 가시성 확보

    **핵심 성과**: Makespan 3.23% 단축 (Random 대비 276분 절감)
    """)

st.info("👈 왼쪽 사이드바에서 세부 분석 페이지를 탐색하세요.")
