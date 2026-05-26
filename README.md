# 🔩 RSW 공정 품질 예측 및 스케줄링 최적화 — PLM 관점 분석

> 멀티모달 딥러닝 기반 품질 불확실성 정량화를 통한 RSW 공정의 기대손실 최소화 스케줄링 최적화

**2026 KSIE 한국산업경영시스템학회 경진대회**  
홍익대학교 산업및데이터공학과 · 제품생애관리(PLM) 기말과제

## 📋 프로젝트 개요

저항 점용접(RSW) 공정에서 수집되는 멀티모달 데이터(RGB 이미지, IR 열화상, 공정 수치)를 활용하여:

1. **품질 예측**: 멀티모달 CNN+MLP + Decision Fusion으로 Good/Bad/Explode 3-class 분류
2. **비용 변환**: 품질 확률 → Quality + Time + Energy 통합 비용 함수
3. **스케줄링 최적화**: Risk-aware Dispatching으로 P6 병렬 기계 Makespan 최소화
4. **PLM 해석**: Closed-Loop PLM, Lifecycle Cost, QCD 관점에서의 연구 의의 분석

## 🚀 대시보드 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📊 주요 결과

| 지표 | 값 |
|---|---|
| Best Fusion AUC | 0.884 (DS Fusion) |
| Makespan 단축 | -3.23% (Cost-based vs Random) |
| Total Expected Cost | ₩41,770,136 |
| 안정 공정 영역 | Force 85-105N, Current 2500-3500A |

## 🔗 PLM 관점

- **Closed-Loop PLM**: 생산 품질 데이터 → 설계 파라미터 피드백
- **Lifecycle Cost**: 설계 단계에서 ~90% 비용 결정 → 안정 공정 영역으로 사전 최적화
- **QCD 통합**: Total Cost = Quality + Time + Energy
- **Proactive 운영**: 품질 불확실성 기반 선제적 스케줄링

## 📁 프로젝트 구조

```
├── app.py                          # Streamlit 메인
├── pages/
│   ├── 1_🧠_품질예측모델.py
│   ├── 2_🔍_해석_설명가능성.py
│   ├── 3_💰_비용_의사결정.py
│   ├── 4_📊_스케줄링_최적화.py
│   └── 5_🔄_PLM_프레임워크.py
├── data/                           # 분석 결과 데이터
├── .streamlit/config.toml          # 다크 테마 설정
├── requirements.txt
└── README.md
```
