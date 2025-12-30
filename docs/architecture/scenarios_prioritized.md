# Product Scenarios Prioritization — GenAI Health‑Data Platform

## 1. Executive Summary

**Scenarios Evaluated:** 10  
**Top 3 Selected:**  
1. **Policy Simulation Assistant (MVP)** – Forecast impact of workforce or spending changes on outcomes  
2. **Health Benchmark Dashboard** – Cross-country anomaly detection and peer comparison  
3. **Narrative Insight Generator** – AI-generated, citation-linked country health briefs  

**MVP Scope (Cursor-optimized):**  
A **GenAI Policy Simulation Assistant** that uses existing datasets to predict the directional effect of input changes (e.g., doctor density, nurse density, government spending) on life expectancy, returning **explanations, graphs, and narrative summaries**.  
Deployed as a **TypeScript + Supabase app** with **GPT-powered narrative layer**, **retrieval-based analytics**, and **simple what-if simulation UI**.

---

## 2. Scenario Catalog

| # | Scenario | Description | Value Proposition | Impact (1-5) | Effort (1-5) | Feasibility (H/M/L) | Notes |
|---|---|---|---|---:|---:|---|---|
| 1 | **Policy Simulation Assistant** | Simulate effect of changes in workforce/spending on life expectancy | Predictive planning tool for ministries & NGOs | 5 | 3 | **High** | Strong correlations & data readiness |
| 2 | **Health Benchmark Dashboard** | Compare countries on workforce, mortality, spending | Continuous monitoring & benchmarking | 4 | 2 | **High** | Uses existing normalized data |
| 3 | **Narrative Insight Generator** | Generate policy briefs and summaries from datasets | Speeds up report generation | 4 | 3 | **Medium** | Requires guardrails & citations |
| 4 | **Anomaly Detection System** | Detect outliers in national metrics | Prevents under/over-reporting | 3 | 3 | **Medium** | Needs baseline definitions |
| 5 | **Data Provenance Tracker** | Track data sources, versions, and freshness | Builds trust & compliance | 4 | 4 | **High** | Critical for credibility |
| 6 | **Public API / Embeddings Service** | Provide API access to normalized health indicators | Monetize data infrastructure | 3 | 4 | **Medium** | Infrastructure heavy |
| 7 | **Country Health Story Builder** | Visual storytelling with AI-generated charts | Enhances communication for donors | 3 | 2 | **Medium** | Built on existing GenAI layer |
| 8 | **Donor Impact Visualizer** | Show impact of investments per country | Supports advocacy & funding | 4 | 4 | **Low-Medium** | Needs donor-specific data |
| 9 | **Health Equity Index Generator** | Composite index across access, spending, workforce | Creates benchmark product | 5 | 4 | **Medium** | Needs normalization methodology |
| 10 | **Regulatory Insight Assistant** | Summarize health regulations & frameworks | Aids policy alignment | 2 | 3 | **Low** | Requires textual data ingestion |

**Top 3 Prioritized for MVP/Phase 1:**  
1. Policy Simulation Assistant  
2. Health Benchmark Dashboard  
3. Narrative Insight Generator  

---

## 3. Technical Feasibility Assessment

| Component | Description | Feasibility | Dependencies |
|---|---|---|---|
| **Data Readiness** | Life expectancy, workforce density, spending, mortality datasets cleaned & merged | ✅ High | Supabase tables from `merged_dataset.xlsx` |
| **AI/ML Layer** | Regression + correlation inference for simulation | ✅ High | Python + OpenAI fine-tuning or on-the-fly GPT |
| **Narrative Layer** | GPT-powered explanation with structured prompt templates | ✅ High | OpenAI GPT-4 API |
| **Infrastructure** | Supabase backend + TypeScript/React frontend in Cursor IDE | ✅ High | Already compatible stack |
| **Visualization** | Recharts + Tailwind integration for graphs | ✅ High | Local |
| **Monitoring / RLS** | Row Level Security in Supabase | ✅ Medium | Use policies per country/user |
| **Explainability Layer** | LIME-style local surrogate text output | ✅ Medium | Optional in Phase 2 |

**Conclusion:**  
The MVP can be built with **existing stack (Cursor IDE + Supabase + GPT-4)** and does not require new datasets or cloud migration. All major dependencies are ready.

---

## 4. MVP Definition

### MVP Name:  
**Policy Simulation Assistant (GenAI-powered “What-if” Engine)**

### Core Features  
1. User selects a **country** and modifies sliders for **doctor density**, **nurse density**, and **health spending**.  
2. System runs regression model and returns predicted **change in life expectancy**.  
3. GPT layer generates **explanatory narrative** with uncertainty and citations.  
4. Interactive chart displays baseline vs projected outcomes.  
5. Export as **policy brief PDF**.

### Acceptance Criteria  
- ✅ User can run simulation for at least 10 countries.  
- ✅ Output includes numerical prediction ± confidence interval.  
- ✅ Narrative includes causal context and footnotes.  
- ✅ Latency < 5 seconds per simulation.  
- ✅ Deployed securely with Supabase RLS.  

---

## 5. Development Sprint Plan

| Sprint | Duration | Key Deliverables | Resources |
|---|---|---|---|
| **Sprint 1 (2 weeks)** | Dataset normalization + Supabase schema | 1 dev, 1 data scientist |
| **Sprint 2 (2 weeks)** | Regression models + correlation layer | 1 ML engineer |
| **Sprint 3 (2 weeks)** | UI development in Cursor (TypeScript + Tailwind) | 1 front-end dev |
| **Sprint 4 (2 weeks)** | GPT narrative integration + testing | 1 full-stack dev |
| **Sprint 5 (1 week)** | QA, deployment, and monitoring setup | All |

**Total Time:** 9 weeks (~2 months)  
**Resource Load:** 3–4 contributors (founder + ML + front-end + part-time designer)

---

## 6. Risk Assessment

| Risk | Impact | Likelihood | Mitigation |
|---|---|---:|---:|---|
| Data incompleteness / inconsistency | High | Medium | Implement automated validation (Pandera/Great Expectations) |
| Model misinterpretation / “causal” misuse | High | Medium | Add uncertainty disclaimers & clear labeling |
| API rate limits or GPT cost overruns | Medium | Medium | Cache results, tier pricing, use streaming completions |
| Limited adoption by policymakers | Medium | Medium | Partner with NGOs / pilot with demo dashboards |
| Security / data integrity | High | Low | Supabase RLS + audit logs |
| Feature creep | Medium | High | Lock MVP scope; separate future roadmap |

---

## 7. Future Roadmap (Post-MVP)

| Phase | Feature | Description |
|---|---|---|
| **Phase 2** | Anomaly Detection Layer | Real-time deviation alerts on new data |
| **Phase 2** | Data Provenance Tracker | Dataset lineage, freshness, and confidence scoring |
| **Phase 3** | Donor Impact Visualizer | Connect funding inputs to predicted outcomes |
| **Phase 3** | White-Label API | Embeddable simulation endpoints |
| **Phase 4** | Natural Language Query Interface | “Ask about workforce trends in Africa” |
| **Phase 4** | Generative Visual Story Builder | Auto-create slides & reports |
| **Phase 5** | Health Equity Index | Composite metric for policy benchmarking |

---

## Validation Checklist

- [x] 10 scenarios evaluated with impact/effort scores  
- [x] Technical feasibility realistically assessed  
- [x] MVP scope clearly defined and bounded  
- [x] Development timeline achievable (≤ 9 weeks)  
- [x] Risk mitigation strategies concrete  

---
