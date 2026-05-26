import streamlit as st

st.set_page_config(page_title="PLM 프레임워크", page_icon="🔄", layout="wide")

st.title("🔄 PLM 관점 프레임워크")
st.caption("Closed-Loop PLM · Lifecycle Cost · QCD · Information Loss — 교수님 강의 내용과의 연결")

# ── Closed-Loop PLM ──
st.subheader("🔁 Closed-Loop PLM에서의 연구 위치")

st.markdown("""
<div style="background:#111827; border:1px solid #1e2d3d; border-radius:16px; padding:2rem; margin:1rem 0">
    <div style="display:flex; justify-content:center; gap:0.5rem; flex-wrap:wrap; align-items:stretch">

        <div style="width:200px; padding:1rem; border:2px solid #3b82f6; border-radius:12px;
                    background:rgba(59,130,246,0.08); position:relative">
            <div style="position:absolute; top:-10px; right:10px; background:#3b82f6;
                        color:#0a0e17; font-size:0.6rem; font-weight:700; padding:2px 8px; border-radius:4px">
                본 연구
            </div>
            <div style="color:#3b82f6; font-weight:700; font-size:0.75rem">BOL — 설계</div>
            <div style="color:#e2e8f0; font-weight:700; font-size:1rem; margin:0.3rem 0">설계</div>
            <div style="background:rgba(59,130,246,0.15); border:1px solid rgba(59,130,246,0.3);
                        border-radius:6px; padding:0.4rem; font-size:0.7rem; color:#e2e8f0; margin-top:0.5rem">
                안정 공정 영역<br>(SHAP/PDP → 설계 피드백)
            </div>
        </div>

        <div style="display:flex; align-items:center; color:#334155; font-size:1.5rem">→</div>

        <div style="width:200px; padding:1rem; border:2px solid #00d4aa; border-radius:12px;
                    background:rgba(0,212,170,0.08); position:relative">
            <div style="position:absolute; top:-10px; right:10px; background:#00d4aa;
                        color:#0a0e17; font-size:0.6rem; font-weight:700; padding:2px 8px; border-radius:4px">
                본 연구 핵심
            </div>
            <div style="color:#00d4aa; font-weight:700; font-size:0.75rem">BOL — 생산</div>
            <div style="color:#e2e8f0; font-weight:700; font-size:1rem; margin:0.3rem 0">생산</div>
            <div style="background:rgba(0,212,170,0.15); border:1px solid rgba(0,212,170,0.3);
                        border-radius:6px; padding:0.4rem; font-size:0.7rem; color:#e2e8f0; margin-top:0.3rem">
                멀티모달 품질 예측<br>(CNN + MLP + Fusion)
            </div>
            <div style="background:rgba(0,212,170,0.15); border:1px solid rgba(0,212,170,0.3);
                        border-radius:6px; padding:0.4rem; font-size:0.7rem; color:#e2e8f0; margin-top:0.3rem">
                Risk-aware Scheduling<br>(비용 기반 최적화)
            </div>
        </div>

        <div style="display:flex; align-items:center; color:#334155; font-size:1.5rem">→</div>

        <div style="width:200px; padding:1rem; border:2px solid #334155; border-radius:12px;
                    background:rgba(255,255,255,0.02); opacity:0.5">
            <div style="color:#f59e0b; font-weight:700; font-size:0.75rem">MOL</div>
            <div style="color:#e2e8f0; font-weight:700; font-size:1rem; margin:0.3rem 0">유지보수</div>
            <div style="background:rgba(245,158,11,0.1); border-radius:6px; padding:0.4rem;
                        font-size:0.7rem; color:#94a3b8; margin-top:0.5rem">
                실시간 모니터링<br>(Digital Twin 연계)
            </div>
        </div>

        <div style="display:flex; align-items:center; color:#334155; font-size:1.5rem">→</div>

        <div style="width:200px; padding:1rem; border:2px solid #334155; border-radius:12px;
                    background:rgba(255,255,255,0.02); opacity:0.5">
            <div style="color:#8b5cf6; font-weight:700; font-size:0.75rem">EOL</div>
            <div style="color:#e2e8f0; font-weight:700; font-size:1rem; margin:0.3rem 0">폐기/재활용</div>
            <div style="background:rgba(139,92,246,0.1); border-radius:6px; padding:0.4rem;
                        font-size:0.7rem; color:#94a3b8; margin-top:0.5rem">
                재활용 의사결정
            </div>
        </div>

    </div>
    <div style="text-align:center; margin-top:1.5rem">
        <div style="display:inline-block; background:rgba(0,212,170,0.1); border:1px dashed rgba(0,212,170,0.4);
                    border-radius:8px; padding:0.5rem 2rem; color:#00d4aa; font-weight:600; font-size:0.85rem">
            ↩️ 생산 품질 데이터 → 설계 파라미터 피드백 (안정 공정 영역) ↩️
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── PLM Principles ──
st.subheader("📐 교수님 강의 핵심 원리와의 연결")

p1, p2 = st.columns(2)

with p1:
    st.markdown("""
    #### 💡 Lifecycle Cost의 ~90%는 설계 단계에서 결정

    > 교수님 3주차: *"상세설계까지 끝나면 라이프사이클 코스트의 약 90%가 확정된다.
    > 앞단에서 고칠 수 있는 비용은 싸지만, 뒤로 갈수록 어마무시하게 커진다."*

    **본 연구 연결**:
    - SHAP/PDP 분석으로 **안정 공정 영역** 도출
    - Force 85~105N, Current 2500~3500A → Good 확률 0.92
    - 이 범위를 **설계 단계 공정 파라미터 가이드라인**으로 활용
    - → **설계 단계에서 후속 품질 비용을 사전 최적화**하는 정량적 근거
    """)

    st.markdown("""
    #### ⚖️ QCD (Quality-Cost-Delivery) 통합

    > 교수님 02_동시공학 강의:
    > *"개발이 진행됨에 따라 Life-Cycle-QCD Determination은 급격히 증가하고,
    > QCD Reduction Opportunity는 감소한다."*

    **본 연구 연결**:
    - **Total Cost = Quality Cost + Time Cost + Energy Cost**
    - Quality(품질) + Time(납기/시간) + Cost(에너지/비용) 통합
    - 세 요소를 **하나의 목적함수**로 정량적 최적화
    - PLM의 QCD 원리를 **데이터 기반으로 실현**
    """)

with p2:
    st.markdown("""
    #### 🔄 Preventive → Proactive 패러다임 전환

    > 교수님 6주차: *"예전에는 time-based 예방보전이었다면, 지금은 proactive —
    > AI로 센서 데이터 분석해서 고장 나기 직전에 선제적으로 조치를 취하는 것이다."*

    **본 연구 연결**:
    - 멀티모달 센서 데이터 → AI 품질 확률 예측
    - 예측 결과 → **Risk-aware Scheduling**으로 고위험 작업 선처리
    - 시간 기반 예방이 아닌 **데이터 기반 선제적 생산 운영**
    - Proactive Maintenance의 **생산 스케줄링 확장 버전**
    """)

    st.markdown("""
    #### 📡 Information Loss 해소

    > 교수님 03_정보기술 강의:
    > *"BOL 이후 정보가 vague하거나 unrecognized 되어 MOL/EOL의 정보가
    > BOL로 피드백되지 못한다."*

    **본 연구 연결**:
    - **멀티모달 센서**(RGB + IR + Numeric)로 생산 단계 정보 가시성 확보
    - 품질 확률 + 불확실성(Entropy)까지 정량화 → 정보의 질적 향상
    - 생산 데이터가 설계 파라미터로 피드백되는 **Closed-Loop 구조** 형성
    - BOL 내 설계↔생산 간 **Information Loss 감소**
    """)

st.divider()

# ── Critical Review ──
st.subheader("⚠️ 비판적 검토 & 한계점")

lim1, lim2 = st.columns(2)

with lim1:
    st.error("""
    **🔴 Explode Recall 0.305**
    - 위험 샘플의 69.5%를 미탐지
    - 실제 현장 적용 시 **안전 리스크** 존재
    - 개선: class-balanced loss, threshold tuning, focal loss
    """)

    st.warning("""
    **🟡 Fusion ECE 0.129**
    - Surface 단독(0.030) 대비 과신뢰 성향
    - Temperature Scaling **미적용** → calibration 왜곡
    - DS Fusion의 확률 조합 과정에서 보정 손실
    """)

with lim2:
    st.warning("""
    **🟡 통계적 유의성 부족**
    - Random 1회 비교만 수행 (발표자료 기준)
    - 50회 Stochastic이지만 정책 간 **t-test/ANOVA** 미수행
    - 추후 다중 비교 검정으로 유의성 확보 필요
    """)

    st.info("""
    **🔵 Sample → Order 확장 미흡**
    - 현실 공정은 Lot/Order 단위 의사결정
    - 현재 Pseudo-order grouping은 heuristic 기반
    - 실제 MES 데이터와의 연계 필요
    """)

st.divider()

# ── Future Work ──
st.subheader("🚀 향후 연구 방향")

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    #### 🎯 모델 개선
    - Explode recall 향상
    - T-Scaling calibration
    - Class-balanced loss
    """)

with f2:
    st.markdown("""
    #### 🤖 스케줄링 고도화
    - 강화학습 기반 Dispatching
    - GA 기반 최적화
    - Dynamic re-scheduling
    """)

with f3:
    st.markdown("""
    #### 🏭 Digital Twin 연계
    - 실시간 공정 모니터링
    - CPS 구조 통합
    - Online uncertainty estimation
    """)

with f4:
    st.markdown("""
    #### 📊 PLM 확장
    - MOL/EOL 데이터 통합
    - Full Lifecycle 비용 최적화
    - 공급망(SCM) 연계
    """)
