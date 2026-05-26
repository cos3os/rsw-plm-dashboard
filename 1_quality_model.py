import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="품질 예측 모델", page_icon="🧠", layout="wide")

st.title("🧠 멀티모달 품질 예측 모델")
st.caption("Surface CNN (RGB) + IR CNN (열화상) + Numeric ANN (공정수치) → Decision Fusion")

# ── Load Data ──
df = pd.read_csv("data/model_results.csv")
ablation = pd.read_csv("data/ablation.csv")

# ── KPI ──
c1, c2, c3, c4 = st.columns(4)
c1.metric("Best Fusion AUC", "0.884", "DS Fusion")
c2.metric("Best Single F1", "0.736", "Numeric ANN")
c3.metric("Explode Recall", "0.305", "핵심 개선 과제", delta_color="inverse")
c4.metric("Surface ECE", "0.030", "가장 잘 보정된 모달")

st.divider()

# ── Model Comparison ──
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📊 모델별 성능 비교")
    metric = st.radio("지표 선택", ["roc_auc", "f1_macro", "accuracy"], horizontal=True,
                       format_func=lambda x: {"roc_auc": "ROC-AUC", "f1_macro": "F1-score", "accuracy": "Accuracy"}[x])

    color_map = {"단일": "#3b82f6", "Fusion": "#00d4aa"}
    fig = px.bar(df, x="model", y=metric, color="type",
                 color_discrete_map=color_map,
                 text=df[metric].round(4),
                 labels={"model": "", metric: metric.upper().replace("_", " ")})
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"),
        xaxis=dict(tickangle=-20),
        yaxis=dict(range=[0.4, 1.0]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Confusion Matrix (DS Fusion)")
    conf = np.array([[129, 0, 4], [0, 70, 13], [66, 0, 29]])
    labels = ["Good", "Bad", "Explode"]

    fig_cm = go.Figure(data=go.Heatmap(
        z=conf, x=labels, y=labels,
        text=conf, texttemplate="%{text}",
        textfont={"size": 18, "color": "white"},
        colorscale=[[0, "#0f172a"], [0.5, "#1e40af"], [1, "#00d4aa"]],
        showscale=False,
    ))
    fig_cm.update_layout(
        xaxis_title="Predicted", yaxis_title="True",
        yaxis=dict(autorange="reversed"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), height=350,
    )
    st.plotly_chart(fig_cm, use_container_width=True)

    st.warning("⚠️ Explode 95개 중 66개가 Good으로 오분류 → 클래스 불균형, threshold, calibration 영향")

st.divider()

# ── Class Sensitivity ──
col3, col4 = st.columns(2)

with col3:
    st.subheader("🎯 클래스별 탐지 성능")
    sens_data = pd.DataFrame({
        "Class": ["Good", "Bad", "Explode"],
        "Sensitivity": [0.970, 0.843, 0.305],
        "MDR (미탐지율)": [0.030, 0.157, 0.695],
        "FAR (오탐지율)": [0.371, 0.000, 0.079],
    })

    fig_sens = go.Figure()
    colors = ["#10b981", "#f59e0b", "#ef4444"]
    for i, row in sens_data.iterrows():
        fig_sens.add_trace(go.Bar(
            name=row["Class"],
            x=[row["Sensitivity"]], y=[row["Class"]],
            orientation="h", marker_color=colors[i],
            text=f"{row['Sensitivity']:.1%}", textposition="inside",
            textfont=dict(size=14, color="white"),
        ))
    fig_sens.update_layout(
        showlegend=False, height=200,
        xaxis=dict(range=[0, 1.05], title="Sensitivity"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), margin=dict(l=80),
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    st.dataframe(sens_data.set_index("Class"), use_container_width=True)

with col4:
    st.subheader("🧪 Ablation Study — 모달 제거 영향")
    fig_ab = px.bar(ablation, x="config", y="f1_score",
                     text=ablation["f1_score"].round(3),
                     color="f1_score",
                     color_continuous_scale=["#ef4444", "#f59e0b", "#00d4aa"])
    fig_ab.update_traces(textposition="outside", textfont_size=13)
    fig_ab.update_layout(
        height=350,
        yaxis=dict(range=[0.5, 0.8], title="F1-score"),
        xaxis_title="",
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0"), coloraxis_showscale=False,
    )
    st.plotly_chart(fig_ab, use_container_width=True)

    st.markdown("""
    **핵심 발견**
    - **Surface 제외** 시 F1 **-0.11** → Surface가 핵심 모달
    - **Numeric 제외** 시 F1 **+0.04** → Surface+IR만으로도 경쟁력
    - **IR 제외** 시 F1 **+0.01** → IR은 보조적 역할
    """)

st.divider()

# ── Critical Review ──
st.subheader("⚠️ 비판적 검토 — AI 결과의 한계")
cr1, cr2 = st.columns(2)
with cr1:
    st.error("""
    **Explode Recall 0.305 — 위험 샘플 69.5% 미탐지**
    - 실제 현장 적용 시 안전 리스크 존재
    - 개선 방향: class-balanced loss, threshold tuning
    """)
    st.warning("""
    **Fusion ECE 0.129 — 과신뢰 성향**
    - Surface 단독 ECE(0.030) 대비 4배 이상
    - Temperature Scaling 미적용 → 향후 calibration 필수
    """)
with cr2:
    st.warning("""
    **클래스 불균형**
    - Good 클래스가 다수 → 모델이 Good 편향 학습
    - Adaptive Augmentation(70% 수준) 적용했으나 한계 존재
    """)
    st.info("""
    **Numeric 단독 > Fusion 현상**
    - Numeric ANN F1(0.736) > DS Fusion F1(0.647)
    - 이미지 모달의 노이즈가 Fusion 성능 저하 유발 가능
    - 모달별 신뢰도 기반 동적 가중치 적용 필요
    """)
