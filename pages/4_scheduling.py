import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="스케줄링 최적화", page_icon="📊", layout="wide")

st.title("📊 비용 기반 스케줄링 최적화")
st.caption("P6 병렬 동일 기계 환경 · 50회 Stochastic 시뮬레이션 · 4개 정책 비교")

# ── Load Data ──
sched_df = pd.read_csv("data/schedule_results.csv")

# ── KPI ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("Cost-based Makespan", "8,273 min", "-3.23%")
c2.metric("절감 시간", "-276 min", "vs Random")
c3.metric("설비 대수", "6대", "Identical Stations")
c4.metric("시뮬레이션", "50회", "Stochastic 반복")

st.divider()

# ── Policy Comparison ──
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📉 스케줄링 정책별 Makespan 비교")

    colors = ["#00d4aa", "#3b82f6", "#f59e0b", "#64748b"]
    fig = go.Figure()
    for i, row in sched_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["avg_makespan"]], y=[row["policy"]],
            orientation="h", marker_color=colors[i],
            text=f"{row['avg_makespan']:,.0f} min", textposition="outside",
            textfont=dict(size=14, color="white"),
            name=row["policy"],
            showlegend=False,
        ))
    fig.update_layout(
        xaxis=dict(range=[8000, 8800], title="Makespan (min)"),
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), height=300,
        margin=dict(l=120),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        sched_df.rename(columns={
            "policy": "정책",
            "avg_makespan": "평균 Makespan (min)",
            "improvement_pct": "개선율 (%)",
            "description": "설명",
        }).set_index("정책"),
        use_container_width=True,
    )

with col2:
    st.subheader("🏭 P6 설비 가동률 (추정)")

    station_util = pd.DataFrame({
        "Station": [f"M{i+1}" for i in range(6)],
        "Utilization": [92, 88, 91, 85, 89, 87],
    })

    fig_util = px.bar(station_util, x="Utilization", y="Station",
                       orientation="h", text="Utilization",
                       color="Utilization",
                       color_continuous_scale=["#1e293b", "#00d4aa"])
    fig_util.update_traces(texttemplate="%{text}%", textposition="inside",
                            textfont_size=14)
    fig_util.update_layout(
        xaxis=dict(range=[0, 100], title="가동률 (%)"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), height=300,
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed"),
    )
    st.plotly_chart(fig_util, use_container_width=True)

    st.markdown("""
    **스케줄링 환경**
    - 6대 동일 스테이션 (Parallel Identical Machine)
    - **High-risk** (P_explode > 0.4) 작업 → **인접 2개 스테이션 동시 점유**
    - 목적: Makespan (C_max) 최소화
    """)

st.divider()

# ── Strategy ──
st.subheader("📋 Risk-aware Dispatching 전략")

s1, s2 = st.columns(2)

with s1:
    st.markdown("""
    #### 핵심 전략

    | 단계 | 내용 | 효과 |
    |:---:|---|---|
    | 1️⃣ | Total Cost 기준 내림차순 정렬 | 고위험 작업 선처리 |
    | 2️⃣ | P(Explode) > 0.4 → 2-station 점유 | 설비 안전 확보 |
    | 3️⃣ | Stochastic quality event sampling | 현실적 불확실성 반영 |
    | 4️⃣ | LFJ (Least Finish time Job) 배정 | 설비 밸런싱 |
    """)

with s2:
    st.markdown("""
    #### Stochastic 시뮬레이션 구조

    ```python
    # 매 시뮬레이션마다:
    sampled_time = N(base_time_mean, base_time_std)
    bad_event = Binomial(1, P_bad)
    explode_event = Binomial(1, P_explode)

    process_time = sampled_time
                 + bad_event × T_rework      # 2 min
                 + explode_event × T_explode  # 10 min
    ```

    > 50회 반복으로 **확률적 품질 이벤트**의 영향을 평균화
    """)

st.divider()

# ── Results Summary ──
st.subheader("📈 개선 결과 요약")

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown("""
    <div style="text-align:center; background:#111827; border:1px solid #1e2d3d;
                border-radius:12px; padding:2rem">
        <div style="font-size:2.5rem; font-weight:800; color:#00d4aa; font-family:monospace">
            -276 min
        </div>
        <div style="color:#94a3b8; margin-top:0.5rem">Random 대비 Makespan 단축</div>
    </div>
    """, unsafe_allow_html=True)

with r2:
    st.markdown("""
    <div style="text-align:center; background:#111827; border:1px solid #1e2d3d;
                border-radius:12px; padding:2rem">
        <div style="font-size:2.5rem; font-weight:800; color:#f59e0b; font-family:monospace">
            -3.23%
        </div>
        <div style="color:#94a3b8; margin-top:0.5rem">생산시간 절감률</div>
    </div>
    """, unsafe_allow_html=True)

with r3:
    st.markdown("""
    <div style="text-align:center; background:#111827; border:1px solid #1e2d3d;
                border-radius:12px; padding:2rem">
        <div style="font-size:2.5rem; font-weight:800; color:#8b5cf6; font-family:monospace">
            ~90%
        </div>
        <div style="color:#94a3b8; margin-top:0.5rem">평균 설비 가동률</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
> **PLM 관점**: 이 Risk-aware Scheduling은 교수님이 6주차에서 설명하신
> **Preventive → Proactive 유지보수 전환**의 생산 스케줄링 버전입니다.
> 품질 불확실성을 사전에 정량화하여 고위험 작업을 선처리하는 것 = **선제적 생산 운영**
""")
