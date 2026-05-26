import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="해석 & 설명가능성", page_icon="🔍", layout="wide")

st.title("🔍 품질 예측 해석 및 설명가능성 분석")
st.caption("SHAP · PDP · Grad-CAM · 공정 메커니즘 해석")

# ── Load Data ──
shap_df = pd.read_csv("data/shap_importance.csv")

# ── SHAP ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 SHAP 변수 영향력 (Good 기준 / RF)")
    shap_sorted = shap_df.sort_values("mean_shap_good", ascending=True)

    fig = px.bar(shap_sorted, x="mean_shap_good", y="feature",
                 orientation="h", text=shap_sorted["mean_shap_good"].round(4),
                 color="mean_shap_good",
                 color_continuous_scale=["#1e293b", "#00d4aa"])
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(
        height=350,
        xaxis_title="Mean |SHAP|", yaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), coloraxis_showscale=False,
        margin=dict(l=100),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    > **Thickness A/B**와 **Welding Time**, **Force**가 Good 예측에 주요 작용
    > · 값이 클수록 Good 확률을 **낮추는** 방향으로 작용하는 변수 존재
    """)

with col2:
    st.subheader("✅ PDP 기반 안정 공정 영역")

    process_data = [
        {"파라미터": "Force (N)", "위험 (Low)": "< 80", "안정 영역": "85 ~ 105", "위험 (High)": "> 110"},
        {"파라미터": "Current (A)", "위험 (Low)": "< 2,000", "안정 영역": "2,500 ~ 3,500", "위험 (High)": "> 3,500"},
        {"파라미터": "Welding Time (ms)", "위험 (Low)": "< 400", "안정 영역": "600 ~ 1,100", "위험 (High)": "> 1,200"},
    ]
    st.dataframe(pd.DataFrame(process_data).set_index("파라미터"), use_container_width=True)

    st.success("**최적 가공 윈도우**: Force 85-95N + Current 2500-3500A → Good 확률 **0.92 영역**")

    # 2D PDP 시뮬레이션
    st.markdown("##### Force × Current 관계 (2D PDP 등고선 개념)")
    force_range = list(range(75, 116))
    current_range = list(range(1500, 4500, 100))

    z_data = []
    for f in force_range:
        row = []
        for c in current_range:
            # 근사 Good 확률
            f_score = max(0, 1 - ((f - 92) / 15) ** 2)
            c_score = max(0, 1 - ((c - 3000) / 1200) ** 2)
            prob = 0.5 + 0.42 * f_score * c_score
            row.append(min(prob, 0.95))
        z_data.append(row)

    fig_2d = go.Figure(data=go.Contour(
        z=z_data, x=current_range, y=force_range,
        colorscale=[[0, "#ef4444"], [0.5, "#f59e0b"], [1, "#10b981"]],
        contours=dict(showlabels=True),
        colorbar=dict(title="P(Good)"),
    ))
    fig_2d.update_layout(
        xaxis_title="Current (A)", yaxis_title="Force (N)",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), height=350,
    )
    st.plotly_chart(fig_2d, use_container_width=True)

st.divider()

# ── Mechanism ──
st.subheader("⚙️ Good / Bad / Explode 공정 메커니즘 분석")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    ### ✅ Good
    **SHAP 조건**
    - Force 85-105N
    - Current 2.5-3.5kA
    - Time 600-1100ms

    **메커니즘**
    > 적정 가압 + 적정 입열
    > → 너겟 균일 형성 → 강도 확보

    **Grad-CAM**
    > 너겟 중심부 — 둥근 대칭 열분포
    """)

with c2:
    st.markdown("""
    ### ⚠️ Bad
    **SHAP 조건**
    - Force ↓ (< 80N)
    - Thickness ↑
    - Time < 400ms

    **메커니즘**
    > 접촉저항 ↑ → 발열 부족
    > → 용융 부족 → 강도 미달

    **Grad-CAM**
    > 불균일 열흔 — 한쪽 치우친 응고 패턴
    """)

with c3:
    st.markdown("""
    ### 💥 Explode
    **SHAP 조건**
    - Current ↑ (> 3.5kA)
    - Time ↑ (> 1200ms)

    **메커니즘**
    > 과입열 + 장시간 통전 → 과용융, 과압
    > → 금속 분출 (스패터)

    **Grad-CAM**
    > 너겟 외곽 산재 — 스패터 흔적
    """)

st.divider()

# ── PLM Connection ──
st.subheader("🔄 PLM 관점 — 안정 공정 영역의 Lifecycle Cost 의미")
st.markdown("""
교수님 3주차 강의에서 강조하신 핵심 원리:

> *"제품 설계 단계에서 라이프사이클 비용의 약 90%가 결정된다.
> 앞단에서 고칠 수 있는 비용은 싸지만, 뒤로 갈수록 어마무시하게 커진다."*

본 연구의 SHAP/PDP 분석에서 도출한 **안정 공정 영역**(Force 85~105N, Current 2500~3500A)은
**설계 단계에서 공정 파라미터를 이 범위로 설정해야 후속 품질 비용이 최소화된다**는 정량적 근거입니다.

이는 PLM의 **Lifecycle Cost Determination** 원리를 데이터 기반으로 실증한 것으로,
생산 단계(BOL)에서 수집된 품질 데이터가 다시 설계 파라미터에 피드백되는 **Closed-Loop PLM 구조**를 형성합니다.
""")
