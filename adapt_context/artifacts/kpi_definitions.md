# KPI Definitions — Policy Simulation Assistant (GenAI Health-Data MVP)

## 1. Executive Summary

**Primary Success Metric:**  
> **Policy Insight Adoption Rate** — % of pilot users (ministries, NGOs, researchers) who actively use the simulation tool and export insights at least once per month.

**Target:** ≥ 60 % monthly active usage by pilot organizations within 3 months post-launch.  
**Measurement Frequency:** Weekly (internal), Monthly (executive summary).  
**Secondary Objective:** Demonstrate measurable *decision acceleration* — reduction in analysis/report generation time by ≥ 40 %.

---

## 2. KPI Hierarchy

| Level | KPI | Definition | Rationale |
|---|---|---|---|
| **Business KPIs** | **User Adoption Rate** | Active organizations ÷ total onboarded | Reflects market traction and value delivery |
|  | **Contract Conversion Rate** | Paid / pilot accounts | Monetization readiness |
|  | **Decision Acceleration** | Avg. time from query to insight vs baseline | Demonstrates efficiency impact |
|  | **Stakeholder Satisfaction (NPS)** | Post-use survey (1–10) | Qualitative validation of usefulness |
| **Product KPIs** | **Simulation Accuracy** | Predicted vs actual life expectancy trend direction | Core functional reliability |
|  | **Narrative Coherence Score** | Manual + AI eval (clarity, correctness) | GenAI explainability success |
|  | **Feature Adoption** | % usage of top 3 features (simulation, export, benchmark) | Identifies engagement focus |
|  | **Data Freshness Compliance** | % datasets updated within target lag (≤ 3 months) | Trustworthiness indicator |
| **Technical KPIs** | **API Response Time** | 95th percentile latency (sec) | User experience performance |
|  | **System Uptime** | Availability of backend API | Reliability baseline |
|  | **Cost per Simulation** | GPT + infra cost ÷ total simulations | Profitability tracking |
|  | **Error Rate** | 4xx/5xx errors ÷ total requests | System health |

---

## 3. Measurement Framework

| Category | Metric | Data Source | Tooling / Collection Method | Frequency |
|---|---|---|---|---|
| Business | Adoption, Retention, Conversion | Supabase user table, Stripe | Supabase analytics + Stripe dashboard | Weekly |
| Business | Decision Time | Time delta logs from query to export | Supabase logs | Monthly |
| Product | Simulation Accuracy | Pred vs historical data | Python evaluation job | Weekly |
| Product | Narrative Quality | LLM eval via rubric (clarity, accuracy, empathy) | DeepEval / custom script | Bi-weekly |
| Product | Data Freshness | Dataset update timestamp | Supabase metadata | Monthly |
| Technical | Latency, Errors | Supabase logs + Cursor telemetry | Automated logging | Continuous |
| Technical | Cost per Simulation | OpenAI usage logs + Supabase billing | Automated ETL | Weekly |

**Automation Note:**  
All KPIs can be logged and monitored automatically using **Supabase Functions** or **Cron Jobs** integrated with **OpenAI usage data** and **Stripe**.

---

## 4. Baseline Establishment

| KPI | Current Baseline | Target (3 Months) | Stretch Target (6 Months) |
|---|---:|---:|---:|
| User Adoption Rate | 0 % | 60 % | 80 % |
| Decision Acceleration | n/a | −40 % time to report | −60 % |
| Simulation Accuracy | N/A (prototype) | ≥ 75 % directional correctness | ≥ 85 % |
| Narrative Coherence | n/a | ≥ 4.0 / 5 avg score | ≥ 4.5 |
| Data Freshness | Manual updates | ≤ 3 months lag | ≤ 1 month lag |
| API Response Time | TBD | ≤ 5 s @ 95th | ≤ 3 s |
| Cost per Simulation | $0.12 | ≤ $0.10 | ≤ $0.07 |

Baselines will be validated in Sprint 1 using synthetic runs and early pilot users.

---

## 5. Success Criteria

| Category | Must Have | Should Have | Nice to Have | Failure Criteria |
|---|---|---|---|---|
| Business | ≥ 60 % adoption | ≥ 1 paid partner | ≥ 1 academic collaboration | < 30 % adoption or 0 renewals |
| Product | ≥ 75 % accuracy, ≥ 4.0 narrative score | Export & benchmark stable | Early anomaly alerts | Repeated inaccurate or nonsensical output |
| Technical | ≤ 5 s latency, ≥ 99 % uptime | Cost ≤ $0.10/run | Near real-time dashboards | Frequent downtime, runaway API cost |

---

## 6. Monitoring & Alerting

### Dashboard Design
To be implemented in **Supabase + Recharts UI** and **Cursor IDE preview**:
- **Real-time Metrics Panel:** Latency, Error Rate, Simulation Volume  
- **Business Dashboard:** Adoption, Conversion, Revenue  
- **Quality Panel:** Accuracy %, Narrative Coherence, Data Freshness  

### Alert Configuration
| Metric | Threshold | Notification Channel |
|---|---|---|
| API Latency > 5 s | Slack alert | `#tech-alerts` |
| Accuracy < 70 % (7-day avg) | Email + Jira ticket | QA/ML lead |
| Monthly Active Users < 50 % | Email summary | CEO/Product |
| GPT Cost > Budget threshold | Finance dashboard | CFO/Founder |

Alerts automated via **Supabase Edge Functions + Webhooks** or **Zapier**.

---

## 7. Reporting Schedule

| Cadence | Report Type | Owner | Audience | Purpose |
|---|---|---|---|---|
| **Weekly** | Technical Health Summary | Tech Lead | Founders | Performance & stability |
| **Bi-Weekly** | Product KPIs Snapshot | Product Lead | Team | Sprint planning & prioritization |
| **Monthly** | Business Review | CEO | Stakeholders/Partners | Adoption, revenue, satisfaction |
| **Quarterly** | Strategic Review | CEO + Advisors | Investors, Partners | Direction, scaling roadmap |

All reports aggregated via **Supabase Analytics + Notion dashboards**, exported to PDF automatically via scheduled scripts.

---

## Validation Checklist

- [x] Primary KPIs linked to business objectives  
- [x] Measurement methods practical and automatable  
- [x] Targets realistic based on baselines  
- [x] Monitoring strategy operationally feasible  
- [x] Success/failure criteria clearly defined  

---

✅ This framework ensures continuous, evidence-based iteration — measurable impact, traceable data quality, and transparent AI performance aligned with your GenAI platform’s growth goals.
