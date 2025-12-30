# Project Scope - Policy Simulation Assistant

> **Version:** 1.0  
> **Date:** October 2025  
> **Status:** MVP Development  
> **Framework:** ADAPT (Assess → Discover → Analyze → Prototype → Test)

## 🎯 Project Overview

The **Policy Simulation Assistant** is a GenAI-powered healthcare policy simulation tool that enables policy makers to explore the potential impact of workforce and spending changes on life expectancy outcomes. Built using the ADAPT framework, it transforms global health data into predictive insights for informed decision-making.

### Mission Statement
To democratize access to healthcare policy insights by combining high-quality global health data with advanced AI technology, enabling policy makers to make informed decisions that improve health outcomes for populations worldwide.

## 📋 Scope Definition

### In Scope (MVP)

#### Core Features
1. **Policy Simulation Engine**
   - Interactive parameter adjustment (doctor density, nurse density, government spending)
   - Country selection from 9+ countries with comprehensive health data
   - Real-time simulation with confidence intervals
   - Regression-based prediction models

2. **AI-Powered Narrative Generation**
   - GPT-4 generated explanations with contextual insights
   - Safety disclaimers and uncertainty measures
   - Data source citations and methodology transparency
   - Multiple narrative styles (professional, academic, policy)

3. **Data Visualization & Analytics**
   - Interactive charts showing baseline vs. predicted outcomes
   - Confidence interval visualization
   - Performance metrics dashboard
   - Export functionality for policy briefs

4. **Data Quality Assurance**
   - 98.4/100 overall data quality score
   - Automated validation pipeline
   - Data provenance tracking
   - Quality monitoring dashboard

#### Technical Scope
- **Frontend:** React 18 + TypeScript + Vite + Tailwind CSS
- **Backend:** Python 3.11 + FastAPI + SQLite/PostgreSQL
- **AI Integration:** OpenAI GPT-4 + Anthropic Claude API
- **Testing:** pytest (backend) + Jest + React Testing Library
- **Deployment:** Cursor IDE optimized development workflow

#### Data Sources
- WHO Global Health Observatory (life expectancy, workforce, government health spending, mortality)

### Out of Scope (Future Phases)

#### Phase 2 Features (Months 3-6)
- Anomaly detection for health indicators
- Data provenance tracking and transparency
- Advanced benchmarking and peer comparison
- API access for third-party integrations

#### Phase 3 Features (Months 6-12)
- White-label licensing for health IT vendors
- Natural language query interface
- Health equity index generation
- Enterprise features and multi-tenant support

#### Phase 4+ Features (Year 2+)
- Donor impact visualizer
- Regulatory insight assistant
- Generative visual story builder
- Global health equity index

## 🎯 Success Criteria

### Primary Success Metrics
- **Policy Insight Adoption Rate:** ≥60% monthly active usage within 3 months
- **Simulation Accuracy:** ≥75% directional correctness
- **Response Time:** ≤5 seconds per simulation
- **Cost Efficiency:** ≤$0.10 per simulation

### Acceptance Criteria
- ✅ User can run simulation for at least 10 countries
- ✅ Output includes numerical prediction ± confidence interval
- ✅ Narrative includes causal context and footnotes
- ✅ Latency < 5 seconds per simulation
- ✅ Deployed securely with proper authentication

### Quality Gates
- Feature works end-to-end in browser
- Unit tests pass with >80% coverage for new code
- Performance meets baseline requirements
- Documentation updated for feature
- Evidence provided (screenshots/logs/test results)

## 👥 Target Users

### Primary Users
1. **Health Ministry Planners**
   - Forecast workforce needs and budget allocations
   - Evidence-based policy planning
   - Scenario analysis for budget proposals

2. **Development Analysts**
   - Compare countries and evaluate funding impact
   - Cross-national benchmarking
   - International development work

3. **Policy Researchers**
   - Access clean, validated datasets
   - Academic research and policy evaluation
   - Data-driven policy recommendations

### Secondary Users
- NGO Program Managers
- Health Advocates
- Academic Researchers
- Health IT Vendors

## 🏗️ Technical Architecture

### Core Components
1. **Data Pipeline**
   - Health indicator ingestion and validation
   - Quality scoring and monitoring
   - Automated data freshness tracking

2. **Simulation Engine**
   - Regression-based prediction models
   - Confidence interval calculation
   - Parameter validation and range checking

3. **AI Integration**
   - GPT-4 narrative generation
   - Response validation and safety checks
   - Cost tracking and optimization

4. **User Interface**
   - Interactive simulation controls
   - Real-time visualization
   - Export and sharing functionality

### Technology Stack
- **Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Recharts
- **Backend:** Python 3.11, FastAPI, SQLite, Pandas, Scikit-learn
- **AI/ML:** OpenAI GPT-4, Anthropic Claude API
- **Testing:** pytest, Jest, React Testing Library
- **Development:** Cursor IDE with AI-assisted coding

## 📊 Data Requirements

### Health Indicators
- **Life Expectancy:** WHO Global Health Observatory
- **Workforce Density:** Doctors, nurses, pharmacists per population
- **Government Spending:** Health expenditure as % of GDP
- **Access to Medicine:** Essential medicine affordability indices
- **Mortality Data:** Cause-specific death rates by country

### Data Quality Standards
- **Completeness:** ≥95% for critical fields
- **Validity:** ≥98% for numeric fields
- **Consistency:** ≥95% internal consistency
- **Freshness:** ≤3 months data lag

### Countries Covered
- Portugal, Spain, Sweden, Germany, France, Italy, United Kingdom, United States, Canada
- Additional countries to be added based on data availability

## 🚀 Development Timeline

### Sprint 1 (Weeks 1-2): Data Foundation
- Dataset normalization and Supabase schema setup
- Data quality validation pipeline
- Basic API endpoints

### Sprint 2 (Weeks 3-4): Simulation Engine
- Regression models and correlation analysis
- Simulation API development
- Parameter validation

### Sprint 3 (Weeks 5-6): User Interface
- React components and simulation controls
- Interactive charts and visualizations
- Responsive design implementation

### Sprint 4 (Weeks 7-8): AI Integration
- GPT-4 narrative generation
- Response validation and safety checks
- Cost tracking implementation

### Sprint 5 (Week 9): Testing & Deployment
- QA testing and bug fixes
- Performance optimization
- Production deployment

## 🔒 Security & Compliance

### Data Protection
- No personal health data collection
- Aggregate indicators only
- Source attribution and citations
- Audit logging for all access

### AI Safety
- Factual grounding with source data
- Uncertainty disclaimers
- Methodology transparency
- Human oversight for policy-critical outputs

### Technical Security
- Row Level Security (RLS) for multi-tenant access
- API rate limiting and authentication
- Input validation and sanitization
- Secure environment variable management

## 📈 Success Metrics & KPIs

### Business KPIs
- **User Adoption Rate:** Active organizations ÷ total onboarded
- **Contract Conversion Rate:** Paid / pilot accounts
- **Decision Acceleration:** Reduction in analysis time ≥40%
- **Stakeholder Satisfaction (NPS):** Post-use survey ≥4.0/5

### Product KPIs
- **Simulation Accuracy:** Predicted vs actual trend direction ≥75%
- **Narrative Coherence Score:** AI evaluation ≥4.0/5
- **Feature Adoption:** Usage of top 3 features
- **Data Freshness Compliance:** Datasets updated ≤3 months

### Technical KPIs
- **API Response Time:** 95th percentile ≤5 seconds
- **System Uptime:** Availability ≥99.5%
- **Cost per Simulation:** ≤$0.10 USD
- **Error Rate:** 4xx/5xx errors ≤5%

## 🚫 Constraints & Limitations

### Technical Constraints
- Response time must be <5 seconds
- Cost per simulation must be ≤$0.10
- Must work on mobile devices
- Must support 100+ concurrent users

### Business Constraints
- Must maintain 98.4% data quality score
- Must include appropriate disclaimers
- Must not provide clinical recommendations
- Must be accessible to non-technical users

### Resource Constraints
- Development team: 3-4 contributors
- Timeline: 9 weeks for MVP
- Budget: Cost per simulation ≤$0.10
- Data sources: Limited to publicly available datasets

## 🔄 Change Management

### Scope Change Process
1. **Request:** Document scope change request with rationale
2. **Impact Assessment:** Evaluate impact on timeline, resources, and quality
3. **Approval:** Require approval from product lead and technical lead
4. **Documentation:** Update scope document and communicate changes
5. **Implementation:** Adjust development plan and resources

### Version Control
- All scope changes tracked in version history
- Major changes require stakeholder approval
- Minor adjustments can be made by product lead
- Regular scope reviews during sprint planning

## 📚 References

- [ADAPT Framework Analysis](../adapt_context/analysis_summary.md)
- [Data Quality Report](../adapt_context/artifacts/data_quality_report.md)
- [KPI Definitions](../adapt_context/artifacts/kpi_definitions.md)
- [Market Analysis](../adapt_context/artifacts/market_analysis.md)
- [Scenario Prioritization](../adapt_context/artifacts/scenarios_prioritized.md)
- [Technical Architecture](../ARCHITECTURE.md)
- [Requirements Specification](../REQUIREMENTS.md)

---

**Document Owner:** Product Lead (Mafalda Delgado)  
**Last Updated:** October 2025  
**Next Review:** End of Sprint 2  
**Approval:** CEO, Technical Lead, Data Lead
