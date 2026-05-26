import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="비용 의사결정", page_icon="💰", layout="wide")

st.title("💰 비용 기반 의사결정 모델")
st.caption("품질 확률 → 비용 함수 변환 → 우선순위 정렬")

# ── Load Data ──
cost_df = pd.read_csv("data/cost_results.csv")

# ── KPI ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Expected Cost", "₩41.8M", "전체 작업 통합")
c2.metric("High Explode Risk", "4건", "P(Explode) > 0.4")
c3.metric("High Bad Risk", "4건", "P(Bad) > 0.3")
c4.metric("비용 구성", "Q + T + E", "Quality + Time + Energy")

st.divider()

# ── Cost Flow ──
col1, col2 = st.columns(2)

with col1:
    st.subheader("📐 비용 함수 변환 흐름")

    steps = [
        ("🎯 품질 비용", "E[C_quality] = P × Cost Matrix", "Good(C=0) / Bad(C=1) / Explode(C=3)", "#ef4444"),
        ("⏱️ 시간 비용", "T = T_base + P_bad × T_rework + P_exp × T_explode", "Rework 2min / Scrap+Reset+Inspect 10min", "#3b82f6"),
        ("⚡ 에너지 비용", "EC = 0.198 + 0.0258 × I(kA) × t(s)", "Literature-based RSW energy model", "#f59e0b"),
        ("📊 Total Cost", "Total = Quality + Time + Energy", "우선순위 = argsort(Total Cost) ↓", "#00d4aa"),
    ]

    for emoji_label, formula, desc, color in steps:
        st.markdown(f"""
        <div style="background:#111827; border-left:4px solid {color};
                    border-radius:8px; padding:1rem; margin-bottom:0.8rem">
            <div style="color:{color}; font-weight:700; font-size:0.9rem">{emoji_label}</div>
            <code style="color:#e2e8f0; font-size:0.8rem">{formula}</code>
            <div style="color:#94a3b8; font-size:0.7rem; margin-top:0.3rem">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    **품질 비용 행렬 (Cost Matrix)**

    |  | Pred Good | Pred Bad | Pred Explode |
    |---|---:|---:|---:|
    | **True Good** | ₩0 | ₩3,000 | ₩30,000 |
    | **True Bad** | ₩30,000 | ₩0 | ₩12,000 |
    | **True Explode** | ₩100,000 | ₩70,000 | ₩0 |
    """)

with col2:
    st.subheader("🚨 고위험 주문 식별")

    # Risk classification colors
    high_risk = cost_df[cost_df["risk_type"] != "Normal"]
    normal = cost_df[cost_df["risk_type"] == "Normal"]

    st.dataframe(
        cost_df[["sample_id", "p_good", "p_bad", "p_explode", "total_cost_krw", "risk_type"]]
        .rename(columns={
            "sample_id": "Sample",
            "p_good": "P(Good)",
            "p_bad": "P(Bad)",
            "p_explode": "P(Explode)",
            "total_cost_krw": "Total Cost (₩)",
            "risk_type": "Risk",
        })
        .style.format({
            "P(Good)": "{:.3f}",
            "P(Bad)": "{:.3f}",
            "P(Explode)": "{:.3f}",
            "Total Cost (₩)": "₩{:,.0f}",
        }),
        use_container_width=True,
    )

    # Scatter: Risk vs Cost
    fig_scatter = px.scatter(
        cost_df, x="p_explode", y="total_cost_krw",
        size="p_bad", color="risk_type",
        color_discrete_map={"High Bad": "#f59e0b", "High Explode": "#ef4444", "Normal": "#3b82f6"},
        labels={"p_explode": "P(Explode)", "total_cost_krw": "Total Cost (₩)", "risk_type": "Risk Type"},
        hover_data=["sample_id"],
    )
    fig_scatter.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), height=350,
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# ── Cost Composition ──
st.subheader("📊 비용 구성 분석")

cc1, cc2 = st.columns(2)

with cc1:
    pie_data = pd.DataFrame({
        "구성": ["Quality Cost", "Time Cost", "Energy Cost"],
        "비중": [65, 25, 10],
    })
    fig_pie = px.pie(pie_data, values="비중", names="구성",
                      color_discrete_sequence=["#ef4444", "#3b82f6", "#f59e0b"],
                      hole=0.45)
    fig_pie.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), height=300,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with cc2:
    st.markdown("""
    **비용 구성 해석**

    1. **품질 비용 (65%)** — 지배적 요소
       - Explode 발생 시 ₩100,000 손실 (Good으로 오분류 시)
       - Bad 미탐지 시 ₩30,000 손실

    2. **시간 비용 (25%)**
       - 기본 공정시간 + 품질 이벤트 지연
       - Explode 발생 시 +10min (Scrap + Reset + Inspection)

    3. **에너지 비용 (10%)**
       - 전류 × 통전시간 기반 에너지 소모
       - Sustainability proxy로 활용
    """)

    st.info("""
    **PLM 관점**: 이 Total Cost 모델은 교수님이 강조하신
    **QCD(Quality-Cost-Delivery) 프레임워크**를 정량적으로 통합한 것입니다.
    품질(Q) + 시간=납기(D) + 비용(C)을 하나의 목적함수로 최적화합니다.
    """)
