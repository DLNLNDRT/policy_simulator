# Policy Simulation Assistant - Technical Architecture

> Comprehensive technical architecture documentation for the GenAI-powered healthcare policy simulation platform

## 🏗️ System Overview

The Policy Simulation Assistant is built as a **full-stack web application** with a **microservices-oriented architecture** that separates concerns between data processing, AI integration, and user interface layers.

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                          │
├─────────────────────────────────────────────────────────────────┤
│  React 18 + TypeScript + Tailwind CSS + Recharts              │
│  • Interactive UI Components                                   │
│  • Real-time Data Visualization                                │
│  • Responsive Design System                                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                       │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI + Pydantic + CORS Middleware                         │
│  • RESTful API Endpoints                                       │
│  • Request/Response Validation                                │
│  • Authentication & Authorization                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  Feature 1: Simulation Engine                                 │
│  Feature 2: Benchmark Dashboard                                │
│  Feature 3: Narrative Generator                                │
│  Feature 4: Data Quality Assurance                             │
│  Feature 5: Advanced Analytics & Reporting                     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Data Layer                               │
├─────────────────────────────────────────────────────────────────┤
│  • SQLite Database (Development)                              │
│  • Pandas DataFrames (In-Memory Processing)                   │
│  • CSV/Excel Data Sources                                      │
│  • Data Validation & Quality Monitoring                        │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML Layer                              │
├─────────────────────────────────────────────────────────────────┤
│  • OpenAI GPT-4 API Integration                                │
│  • Scikit-learn Regression Models                             │
│  • Statistical Analysis & Correlation                         │
│  • Natural Language Processing                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🎯 Feature Architecture

### Feature 1: Policy Simulation Engine

**Purpose**: Core simulation functionality for predicting life expectancy changes based on policy parameters.

**Components**:
- `SimulationEngine`: Regression model training and prediction
- `DataProcessor`: Data loading, cleaning, and preprocessing
- `SimulationAPI`: RESTful endpoints for simulation requests
- `SimulationCard`: Interactive UI with sliders and controls

**Data Flow**:
```
User Input → Parameter Validation → Baseline Data Retrieval → 
Model Prediction → Confidence Interval Calculation → 
Result Formatting → UI Display
```

**Key Models**:
- Linear regression with feature importance
- Confidence interval calculation
- Gender-specific model adjustments

### Feature 2: Health Benchmark Dashboard

**Purpose**: Cross-country health indicator comparison with anomaly detection and peer group analysis.

**Components**:
- `BenchmarkService`: Country comparison logic
- `AnomalyDetector`: Statistical outlier identification
- `PeerGroupAnalyzer`: Similarity-based clustering
- `RankingSystem`: Weighted scoring across metrics

**Data Flow**:
```
Country Selection → Data Aggregation → Statistical Analysis → 
Anomaly Detection → Peer Group Clustering → 
Ranking Calculation → Visualization Generation
```

**Key Algorithms**:
- Z-score based anomaly detection
- Cosine similarity for peer grouping
- Weighted scoring system

### Feature 3: Narrative Insight Generator

**Purpose**: AI-powered narrative generation with customizable templates and quality metrics.

**Components**:
- `NarrativeService`: AI integration and content generation
- `TemplateEngine`: Narrative template management
- `QualityMetrics`: Content quality assessment
- `NarrativeBuilder`: UI for narrative customization

**Data Flow**:
```
Simulation Results → Template Selection → AI Prompt Generation → 
GPT-4 API Call → Response Processing → Quality Assessment → 
Narrative Formatting → UI Display
```

**Key Features**:
- Multiple narrative templates
- Quality metrics calculation
- Multi-format export (PDF, DOCX, HTML)

### Feature 4: Data Quality Assurance

**Purpose**: Real-time quality monitoring, automated validation, and data provenance tracking.

**Components**:
- `QualityMonitor`: Real-time quality assessment
- `ValidationPipeline`: Automated data validation
- `ProvenanceTracker`: Data source tracking
- `QualityDashboard`: Quality metrics visualization

**Data Flow**:
```
Data Ingestion → Quality Assessment → Validation Rules → 
Anomaly Detection → Quality Scoring → 
Dashboard Update → Alert Generation
```

**Quality Metrics**:
- Completeness (missing data detection)
- Validity (value range validation)
- Consistency (cross-dataset validation)
- Freshness (data recency tracking)

### Feature 5: Advanced Analytics & Reporting

**Purpose**: Trend analysis, correlation matrices, and automated report generation with interactive visualizations.

**Components**:
- `TrendAnalyzer`: Time-series trend analysis
- `CorrelationEngine`: Statistical correlation calculation
- `ReportGenerator`: Automated report creation
- `VisualizationService`: Interactive chart generation

**Data Flow**:
```
Data Selection → Statistical Analysis → Trend Calculation → 
Correlation Matrix → Visualization Generation → 
Report Compilation → Export Processing
```

**Analytics Features**:
- Interactive trend charts
- Correlation heatmaps
- Automated report generation
- Multi-format export

## 🗄️ Data Architecture

### Data Sources

**Primary Datasets**:
- **Life Expectancy**: WHO Global Health Observatory
- **Doctor Density**: WHO Global Health Observatory
- **Nurse Density**: WHO Global Health Observatory
- **Health Spending**: World Bank Development Indicators
- **Access to Medicine**: WHO Essential Medicines List

**Data Quality Standards**:
- **Completeness**: ≥95% data coverage
- **Validity**: ≥98% value accuracy
- **Consistency**: ≤0.5% duplicate records
- **Freshness**: ≤3 months data age

### Data Processing Pipeline

```
Raw Data → Data Validation → Quality Assessment → 
Data Cleaning → Feature Engineering → 
Model Training → Prediction Service
```

**Validation Rules**:
- Country code validation (ISO3)
- Value range validation
- Temporal consistency checks
- Cross-dataset validation

## 🤖 AI/ML Architecture

### Model Architecture

**Simulation Engine**:
- **Algorithm**: Linear Regression with regularization
- **Features**: Doctor density, nurse density, health spending
- **Target**: Life expectancy change
- **Validation**: Cross-validation with time series split

**Narrative Generation**:
- **Model**: OpenAI GPT-4
- **Prompt Engineering**: Structured templates with context
- **Quality Control**: Automated fact-checking and disclaimers
- **Cost Management**: Response caching and rate limiting

### AI Safety & Governance

**Factual Grounding**:
- Source data validation
- Confidence interval reporting
- Uncertainty disclaimers
- Methodology transparency

**Quality Assurance**:
- Automated content validation
- Human review workflows
- Bias detection and mitigation
- Performance monitoring

## 🔧 Technical Stack

### Frontend Architecture

**Core Technologies**:
- **React 18**: Component-based UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization library

**Component Structure**:
```
src/frontend/
├── components/           # Reusable UI components
│   ├── simulation/      # Feature 1 components
│   ├── benchmark/       # Feature 2 components
│   ├── narrative/       # Feature 3 components
│   ├── quality/         # Feature 4 components
│   └── analytics/       # Feature 5 components
├── pages/               # Page-level components
├── hooks/               # Custom React hooks
├── types/               # TypeScript type definitions
└── utils/               # Utility functions
```

### Backend Architecture

**Core Technologies**:
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation and serialization
- **SQLite**: Lightweight database
- **Pandas**: Data manipulation and analysis

**Service Structure**:
```
src/backend/
├── api/routes/          # API endpoint definitions
├── core/               # Core configuration and middleware
├── models/             # Pydantic data models
├── services/           # Business logic services
└── tests/              # Backend test suite
```

### Data Layer

**Storage**:
- **SQLite**: Primary database for development
- **CSV/Excel**: Raw data sources
- **Pandas DataFrames**: In-memory data processing

**Processing**:
- **Data Validation**: Pandera/Great Expectations
- **Quality Monitoring**: Custom quality metrics
- **Provenance Tracking**: Data lineage management

## 🚀 Deployment Architecture

### Development Environment

**Local Development**:
```bash
# Backend API Server
python comprehensive_demo_server.py
# Runs on http://localhost:8005

# Streamlit Dashboard
streamlit run streamlit_eda_dashboard.py
# Runs on http://localhost:8503
```

**Demo Servers**:
- **Full Interactive Demo**: `http://localhost:8005/full`
- **API Documentation**: `http://localhost:8005/docs`
- **Health Check**: `http://localhost:8005/health`

### Production Considerations

**Scalability**:
- Horizontal scaling with load balancers
- Database connection pooling
- Caching layer for API responses
- CDN for static assets

**Security**:
- API authentication and authorization
- Rate limiting and DDoS protection
- Data encryption at rest and in transit
- Audit logging and monitoring

**Monitoring**:
- Application performance monitoring
- Error tracking and alerting
- Business metrics dashboard
- Cost tracking for AI services

## 🔄 Integration Patterns

### API Integration

**RESTful Design**:
- Resource-based URLs
- HTTP status codes
- JSON request/response format
- OpenAPI documentation

**Error Handling**:
- Structured error responses
- Validation error details
- Graceful degradation
- User-friendly error messages

### AI Integration

**OpenAI API Integration**:
- Structured prompt templates
- Response validation
- Cost optimization
- Error handling and retries

**Model Management**:
- Version control for models
- A/B testing capabilities
- Performance monitoring
- Rollback procedures

## 📊 Performance Architecture

### Performance Targets

**Response Times**:
- API endpoints: <2 seconds (95th percentile)
- Simulation calculations: <5 seconds
- AI narrative generation: <10 seconds
- Data visualization: <1 second

**Scalability**:
- Concurrent users: 100+ simultaneous
- Data volume: 10,000+ health records
- API throughput: 100+ requests/minute

### Optimization Strategies

**Caching**:
- API response caching
- Model prediction caching
- Static asset caching
- Database query optimization

**Data Processing**:
- Lazy loading for large datasets
- Pagination for large result sets
- Background processing for heavy tasks
- Memory-efficient data structures

## 🔒 Security Architecture

### Data Protection

**Privacy by Design**:
- No personal health data storage
- Aggregate data only
- Source attribution required
- Data retention policies

**Access Control**:
- Role-based permissions
- API key management
- Rate limiting per user
- Audit trail logging

### AI Safety

**Content Safety**:
- Factual accuracy validation
- Bias detection and mitigation
- Uncertainty quantification
- Human oversight workflows

**Model Security**:
- Input validation and sanitization
- Output filtering and validation
- Prompt injection protection
- Model versioning and rollback

## 📈 Monitoring & Observability

### Application Monitoring

**Metrics Collection**:
- API response times
- Error rates and types
- User engagement metrics
- Business KPI tracking

**Alerting**:
- Performance degradation alerts
- Error rate thresholds
- Cost overrun warnings
- Data quality issues

### Business Intelligence

**Analytics Dashboard**:
- User behavior tracking
- Feature adoption rates
- Performance metrics
- Cost analysis

**Reporting**:
- Weekly technical health reports
- Monthly business reviews
- Quarterly strategic assessments
- Annual performance analysis

## 🔄 Development Workflow

### Code Organization

**Repository Structure**:
```
project_root/
├── src/                    # Source code
│   ├── backend/           # FastAPI backend
│   └── frontend/          # React frontend
├── docs/                  # Documentation
├── adapt_context/         # ADAPT framework analysis
├── tests/                 # Test suites
└── scripts/               # Build and deployment scripts
```

**Development Standards**:
- TypeScript strict mode
- ESLint and Prettier configuration
- Conventional commit messages
- Comprehensive test coverage

### Testing Strategy

**Test Pyramid**:
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **End-to-End Tests**: Full user workflow testing
- **Performance Tests**: Load and stress testing

**Quality Gates**:
- Code coverage ≥80%
- Performance benchmarks
- Security vulnerability scanning
- Accessibility compliance

---

## 📚 Additional Resources

- **[README.md](./README.md)**: Project overview and quick start
- **[REQUIREMENTS.md](./REQUIREMENTS.md)**: Functional and non-functional requirements
- **[DATA_PIPELINE.md](./DATA_PIPELINE.md)**: Data processing and integration guide
- **[TESTING.md](./TESTING.md)**: Testing strategy and validation
- **[ADAPT Analysis](./adapt_context/)**: Complete framework analysis artifacts

---

**Built with ❤️ using the ADAPT Framework**

*This architecture supports the Policy Simulation Assistant's mission to provide transparent, accurate, and actionable insights for healthcare policy decision-making.*
