# Policy Simulation Assistant

> GenAI-powered healthcare policy simulation tool for policy makers, ministries, and NGOs

[![Built with ADAPT Framework](https://img.shields.io/badge/Built%20with-ADAPT%20Framework-blue)](./adapt_context/analysis_summary.md)
[![Tech Stack](https://img.shields.io/badge/Stack-React%20%7C%20FastAPI%20%7C%20GPT--5-green)](#tech-stack)
[![Data Quality](https://img.shields.io/badge/Data%20Quality-98.4%2F100-brightgreen)](./adapt_context/artifacts/data_quality_report.md)

## 🌐 Live Applications

### 🚀 **Interactive React Frontend (Vercel)**
👉 [Open the Frontend](https://project-root-nr18cpcgs-dlnlndrts-projects.vercel.app/)

Modern React-based interface with all 5 features:
- **Policy Simulation**: Interactive sliders for workforce and spending changes
- **Benchmark Analysis**: Cross-country health indicator comparison  
- **Narrative Generation**: AI-powered policy insights with customizable templates
- **Data Quality Dashboard**: Real-time quality monitoring and validation
- **Advanced Analytics**: Trend analysis and correlation matrices

### 📊 **Data Exploration Dashboard (Streamlit)**
👉 [Open the Dashboard](https://projectroo-jnjwo6vcxpj33bygawnbhh.streamlit.app/)


Interactive data exploration and analysis dashboard:
- **Data Quality Analysis**: Comprehensive quality metrics and validation
- **Correlation Matrices**: Health indicator relationships and patterns
- **Country Comparisons**: Cross-national health indicator analysis
- **Temporal Analysis**: Time-series trends and patterns
- **Interactive Visualizations**: Plotly charts and statistical insights

*Note: The React frontend requires the backend API to be running for full functionality.*

---

## 🎯 Project Overview

The Policy Simulation Assistant is an MVP developed using the **ADAPT Framework** (Assess → Discover → Analyze → Prototype → Test) to create a GenAI-powered tool that helps policy makers understand the potential impact of healthcare workforce and spending changes on life expectancy outcomes.

### Key Features

- **🎯 Policy Simulation Engine**: Interactive sliders to model workforce density and spending changes with real-time predictions
- **📊 Health Benchmark Dashboard**: Cross-country health indicator comparison with anomaly detection and peer group analysis
- **📝 Narrative Insight Generator**: AI-powered narrative generation with customizable templates and quality metrics
- **🛡️ Data Quality Assurance**: Real-time quality monitoring, automated validation, and data provenance tracking
- **📈 Advanced Analytics & Reporting**: Trend analysis, correlation matrices, and automated report generation with interactive visualizations

### Target Users

- **Health Ministry Planners**: Forecast workforce needs and budget allocations
- **Development Analysts**: Compare countries and evaluate funding impact
- **Researchers**: Access clean, cross-national health indicator datasets
- **Policy Advocates**: Generate data-driven narratives for reports and presentations

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend development)

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Start the main server
python comprehensive_demo_server.py

# Access the API documentation
open http://localhost:8005/docs
```

### Frontend Development
```bash
# Navigate to frontend directory
cd src/frontend

# Install frontend dependencies
npm install

# Start development server
npm run dev
```

### Streamlit Dashboard
```bash
# Run the data exploration dashboard
python examples/streamlit_eda_dashboard.py
```


## 📁 Project Structure

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for detailed file organization.

## 🔧 Configuration

- **Environment Variables**: Copy `env.example` to `.env` and configure as needed
- **API Keys**: Add your OpenAI API key for narrative generation features

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd project_root

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies (optional)
cd src/frontend
npm install

# Set up environment variables
cp env.example .env
# Edit .env with your API keys and configuration

# Start the demo server
python comprehensive_demo_server.py
```

### Environment Variables

```bash
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_DEBUG=true

# Database Configuration
DATABASE_URL=sqlite:///./data/health_indicators.db

# AI Integration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Security
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🏗️ Architecture

### Tech Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts
- **Backend**: Python 3.11, FastAPI, SQLite, Pandas, Scikit-learn
- **AI/ML**: OpenAI GPT-5, Anthropic Claude API
- **Testing**: pytest (backend), Jest + React Testing Library (frontend)
- **Development**: Cursor IDE with AI-assisted coding

### Data Sources

The platform integrates 9 health indicator datasets:

- **Life Expectancy**: WHO Global Health Observatory
- **Workforce Density**: Doctors, nurses, and pharmacists per population
- **Government Spending**: Health expenditure as % of GDP
- **Access to Medicine**: Essential medicine affordability indices
- **Mortality Data**: Cause-specific death rates by country

*See [DATA_PIPELINE.md](./DATA_PIPELINE.md) for detailed data processing information.*

## 📊 Data Quality & Validation

Our ADAPT analysis achieved a **98.4/100 data quality score** with:

- ✅ **100% Completeness** across all datasets
- ✅ **100% Consistency** with no duplicates
- ✅ **97-100% Validity** with appropriate value ranges
- ✅ **Automated Validation** using Pandera/Great Expectations

*See [adapt_context/artifacts/data_quality_report.md](./adapt_context/artifacts/data_quality_report.md) for detailed analysis.*

## 🎯 Success Metrics

### Primary KPIs

- **Policy Insight Adoption Rate**: ≥60% monthly active usage
- **Simulation Accuracy**: ≥75% directional correctness
- **Response Time**: ≤5 seconds per simulation
- **Cost Efficiency**: ≤$0.10 per simulation

### Monitoring

- Real-time KPI dashboards in the application
- Weekly technical health reports
- Monthly business performance reviews
- Quarterly strategic assessments

*See [adapt_context/artifacts/kpi_definitions.md](./adapt_context/artifacts/kpi_definitions.md) for complete metrics framework.*

## 🛠️ Development

### Project Structure

```
src/
├── backend/              # FastAPI backend
│   ├── api/             # API routes
│   ├── core/            # Core configuration
│   ├── models/          # Pydantic models
│   ├── services/        # Business logic
│   └── tests/           # Backend tests
├── frontend/            # React frontend
│   ├── components/      # React components
│   ├── pages/           # Page components
│   ├── hooks/           # Custom hooks
│   └── utils/           # Utility functions
└── tests/               # Integration tests
```

### Available Scripts

```bash
# Development
npm run dev              # Start both frontend and backend
npm run dev:frontend     # Start frontend only
npm run dev:backend      # Start backend only

# Building
npm run build            # Build both frontend and backend
npm run build:frontend   # Build frontend only
npm run build:backend    # Build backend only

# Testing
npm test                 # Run all tests
npm run test:frontend    # Run frontend tests
npm run test:backend     # Run backend tests
npm run test:integration # Run integration tests
npm run test:e2e         # Run end-to-end tests

# Database
npm run db:migrate       # Run database migrations
npm run db:seed          # Seed database with sample data

# Data Pipeline
npm run data:ingest      # Ingest health indicator data
npm run data:validate    # Validate data quality

# Code Quality
npm run lint             # Run linting
npm run format           # Format code
npm run type-check       # TypeScript type checking
```

### Development Guidelines

- Follow the [.cursorrules](./.cursorrules) configuration for Cursor IDE
- Maintain ≥80% test coverage for core business logic
- Use conventional commits with clear descriptions
- Include JSDoc comments for all public functions
- Validate data quality on every ingestion

## 📈 Market Analysis

### Opportunity Size

- **Global Healthcare Analytics Market**: $43.1B → $167B by 2030 (22% CAGR)
- **GenAI in Healthcare**: $25.6B in 2024 across software & services
- **Target Addressable Market**: $1-5M ARR potential in policy simulation segment

### Competitive Advantage

- **Cross-national Transparency**: Open data with explainable AI
- **Policy-grade Accuracy**: Validated against WHO/OECD benchmarks
- **Rapid Iteration**: Cursor IDE + FastAPI for fast development cycles

*See [adapt_context/artifacts/market_analysis.md](./adapt_context/artifacts/market_analysis.md) for detailed market research.*

## 🎯 MVP Roadmap

### Phase 1: Core MVP (Completed ✅)
- [x] **Feature 1**: Policy Simulation Engine with interactive sliders and real-time predictions
- [x] **Feature 2**: Health Benchmark Dashboard with cross-country comparison and anomaly detection
- [x] **Feature 3**: Narrative Insight Generator with AI-powered content and quality metrics
- [x] **Feature 4**: Data Quality Assurance with real-time monitoring and validation
- [x] **Feature 5**: Advanced Analytics & Reporting with trend analysis and interactive visualizations
- [x] Complete interactive demo with all 5 features working
- [x] Streamlit EDA dashboard for data exploration

### Phase 2: Enhanced Analytics (In Progress)
- [x] Interactive trend analysis with dynamic chart generation
- [x] Correlation matrix visualization with heatmaps
- [x] Automated report generation with multiple export formats
- [ ] Real-time data pipeline integration
- [ ] Advanced statistical modeling

### Phase 3: Scale & Monetization (Future)
- [ ] White-label licensing for health IT vendors
- [ ] Natural language query interface
- [ ] Health equity index generation
- [ ] Enterprise features and multi-tenant support

*See [adapt_context/artifacts/scenarios_prioritized.md](./adapt_context/artifacts/scenarios_prioritized.md) for complete roadmap.*

## 🔒 Security & Compliance

### Data Protection

- **No Personal Data**: Only aggregate health indicators
- **Source Attribution**: Maintain data provenance and citations
- **Audit Logging**: Track all data access and modifications

### AI Safety

- **Factual Grounding**: GPT responses validated against source data
- **Uncertainty Disclaimers**: Clear limitations and confidence intervals
- **Transparency**: Methodology and assumptions clearly documented
- **Human Oversight**: Expert review for policy-critical outputs

## 📚 Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)**: Technical architecture decisions
- **[REQUIREMENTS.md](./REQUIREMENTS.md)**: Functional and non-functional requirements  
- **[DATA_PIPELINE.md](./DATA_PIPELINE.md)**: Data processing and integration guide
- **[TESTING.md](./TESTING.md)**: Testing strategy and success validation
- **[ADAPT Analysis](./adapt_context/)**: Complete framework analysis artifacts

## 🤝 Contributing

### Development Process

1. **Fork** the repository and create a feature branch
2. **Follow** the [.cursorrules](./.cursorrules) configuration
3. **Write** tests for new functionality
4. **Validate** data quality and AI safety
5. **Submit** a pull request with clear description

### Code Review Focus

- Data accuracy and validation
- AI safety and disclaimers
- Performance and scalability
- User experience and accessibility

## 📞 Support

### Getting Help

- **Documentation**: Check the docs/ directory for detailed guides
- **Issues**: Use GitHub Issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas

### Contact

- **Product Lead**: Mafalda Delgado (CEO)
- **Technical Questions**: Create an issue with the `technical` label
- **Business Inquiries**: Contact through the project repository

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **WHO Global Health Observatory** for health indicator datasets
- **World Bank** for government spending data
- **OpenAI** for GPT-5 API access
- **Cursor IDE** for AI-assisted development

---

**Built with ❤️ using the ADAPT Framework**

*This is a policy simulation tool for exploratory analysis. Always consult domain experts and consider multiple data sources when making policy decisions.*
