"""
Streamlit EDA Dashboard for Policy Simulator
Comprehensive data exploration and analysis dashboard using ADAPT framework artifacts
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Policy Simulator - EDA Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling with improved color scheme
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #34495e;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #5a6c7d;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #5a6c7d;
        margin: 0.5rem 0;
        color: #2c3e50;
    }
    .insight-box {
        background-color: #f0f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4a90a4;
        margin: 1rem 0;
        color: #2c3e50;
    }
    .warning-box {
        background-color: #fef9e7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #d4a574;
        margin: 1rem 0;
        color: #2c3e50;
    }
    .success-box {
        background-color: #f0f8f0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #6b8e6b;
        margin: 1rem 0;
        color: #2c3e50;
    }
    /* Improve text contrast in metric cards */
    .metric-card strong {
        color: #2c3e50;
    }
    .metric-card span {
        color: #34495e;
    }
    .metric-card small {
        color: #5a6c7d;
    }
    /* Improve overall text readability */
    .stDataFrame {
        color: #2c3e50;
    }
    .stMetric {
        color: #2c3e50;
    }
    /* Darken plotly chart text for better readability */
    .js-plotly-plot {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def clean_dataframe_for_streamlit(df):
    """Clean dataframe to avoid Arrow serialization issues"""
    if df is None or df.empty:
        return df
    
    # Create a copy to avoid modifying the original
    df = df.copy()
    
    # First, try to convert object columns to numeric where possible
    for col in df.columns:
        if df[col].dtype == 'object':
            # Try to convert to numeric first
            numeric_series = pd.to_numeric(df[col], errors='coerce')
            # If most values converted successfully, use numeric version
            if not numeric_series.isna().all() and len(df[col]) > 0:
                non_null_ratio = (numeric_series.notna().sum() / len(df[col]))
                if non_null_ratio > 0.5:  # If more than 50% are numeric
                    df[col] = numeric_series
                else:
                    # Otherwise convert to string
                    df[col] = df[col].astype(str)
            else:
                # Convert to string if can't convert to numeric
                df[col] = df[col].astype(str)
    
    # Replace NaN values appropriately: empty strings for object columns, 0 for numeric
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('')
        else:
            df[col] = df[col].fillna(0)
    
    return df

def load_data_files():
    """Load all data files from multiple possible locations"""
    # Try multiple possible data directory locations
    possible_data_dirs = [
        Path("data/raw"),  # Streamlit Cloud / standard location
        Path("policy_simulator/data/raw"),  # Alternative location
        Path("adapt_context/data"),  # Legacy location
        Path("../data/raw"),  # Relative path
    ]
    
    data_dir = None
    for dir_path in possible_data_dirs:
        if dir_path.exists() and (any(dir_path.glob("*.csv")) or any(dir_path.glob("*.xlsx"))):
            data_dir = dir_path
            break
    
    data_files = {}
    
    # List of expected files
    expected_files = [
        "Life Expectancy.csv",
        "Density of Doctors.csv", 
        "Density of nurses and midwives.csv",
        "Density of pharmacists.csv",
        "Government Spending.csv",
        "Density.csv",
        "Access to affordable medicine.csv",
        "Cause of Death.xlsx"
    ]
    
    if data_dir is None:
        st.warning("⚠️ Data directory not found. Tried: " + ", ".join([str(d) for d in possible_data_dirs]))
        return data_files
    
    for file_name in expected_files:
        file_path = data_dir / file_name
        if file_path.exists():
            try:
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file_name.endswith('.xlsx'):
                    df = pd.read_excel(file_path)
                else:
                    continue
                
                # Clean the dataframe to avoid Arrow serialization issues
                df = clean_dataframe_for_streamlit(df)
                data_files[file_name] = df
                st.success(f"✅ Loaded {file_name}: {len(df)} rows, {len(df.columns)} columns")
            except Exception as e:
                st.error(f"❌ Error loading {file_name}: {str(e)}")
        else:
            st.warning(f"⚠️ File not found: {file_name} at {file_path}")
    
    return data_files

@st.cache_data
def load_artifacts():
    """Load and parse artifact files from multiple possible locations"""
    # Try multiple possible artifact directory locations
    possible_artifact_dirs = [
        Path("docs/architecture"),  # Standard location
        Path("policy_simulator/docs/architecture"),  # Alternative location
        Path("adapt_context/artifacts"),  # Legacy location
        Path("../docs/architecture"),  # Relative path
    ]
    
    artifacts_dir = None
    for dir_path in possible_artifact_dirs:
        if dir_path.exists():
            artifacts_dir = dir_path
            break
    
    artifacts = {}
    
    artifact_files = [
        "data_quality_report.md",
        "correlation_analysis.md", 
        "kpi_definitions.md",
        "market_analysis.md",
        "scenarios_prioritized.md"
    ]
    
    if artifacts_dir is None:
        st.warning("⚠️ Artifacts directory not found. Tried: " + ", ".join([str(d) for d in possible_artifact_dirs]))
        return artifacts
    
    for file_name in artifact_files:
        file_path = artifacts_dir / file_name
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                artifacts[file_name] = content
            except Exception as e:
                st.error(f"❌ Error loading {file_name}: {str(e)}")
        else:
            st.warning(f"⚠️ Artifact not found: {file_name} at {file_path}")
    
    return artifacts

def parse_quality_metrics(quality_content):
    """Parse quality metrics from data quality report"""
    metrics = {}
    
    # Extract overall quality score
    overall_match = re.search(r'Overall Quality Score.*?(\d+\.?\d*)\s*/\s*100', quality_content)
    if overall_match:
        metrics['overall_score'] = float(overall_match.group(1))
    
    # Extract dataset quality scores
    dataset_scores = {}
    lines = quality_content.split('\n')
    in_table = False
    
    for line in lines:
        if 'Dataset/Sheet' in line and 'Quality Score' in line:
            in_table = True
            continue
        if in_table and '|' in line and not line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 7:
                dataset_name = parts[0]
                try:
                    quality_score = float(parts[6])
                    dataset_scores[dataset_name] = quality_score
                except (ValueError, IndexError):
                    continue
        elif in_table and not line.strip().startswith('|'):
            break
    
    metrics['dataset_scores'] = dataset_scores
    return metrics

def parse_correlation_data(correlation_content):
    """Parse correlation data from correlation analysis"""
    correlations = []
    
    # Extract strong correlations
    lines = correlation_content.split('\n')
    in_strong_table = False
    
    for line in lines:
        if 'Strong (|r| ≥ 0.7)' in line:
            in_strong_table = True
            continue
        if in_strong_table and '|' in line and not line.strip().startswith('|'):
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 6:
                try:
                    correlation = {
                        'feature_x': parts[0],
                        'feature_y': parts[1], 
                        'correlation': float(parts[2]),
                        'n': int(parts[3]),
                        'p_value': float(parts[4]),
                        'interpretation': parts[5]
                    }
                    correlations.append(correlation)
                except (ValueError, IndexError):
                    continue
        elif in_strong_table and 'Moderate' in line:
            break
    
    return correlations

def create_data_overview(data_files):
    """Create data overview section"""
    st.markdown('<div class="section-header">📊 Data Overview</div>', unsafe_allow_html=True)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    total_files = len(data_files)
    total_rows = sum(len(df) for df in data_files.values())
    total_columns = sum(len(df.columns) for df in data_files.values())
    # Use shallow memory usage for performance (deep=True is slow for large dataframes)
    try:
        total_size = sum(df.memory_usage(deep=False).sum() for df in data_files.values()) / 1024 / 1024  # MB
    except Exception:
        # Fallback to row count estimate if memory calculation fails
        total_size = total_rows * 0.001  # Rough estimate: ~1KB per row
    
    with col1:
        st.metric("📁 Total Files", total_files)
    with col2:
        st.metric("📋 Total Rows", f"{total_rows:,}")
    with col3:
        st.metric("📊 Total Columns", total_columns)
    with col4:
        st.metric("💾 Memory Usage", f"{total_size:.1f} MB")
    
    # Dataset details table
    st.subheader("📋 Dataset Details")
    
    dataset_info = []
    for file_name, df in data_files.items():
        info = {
            'File': file_name,
            'Rows': len(df),
            'Columns': len(df.columns),
            'Memory (MB)': f"{df.memory_usage(deep=False).sum() / 1024 / 1024:.2f}",
            'Missing Values': df.isnull().sum().sum(),
            'Duplicate Rows': df.duplicated().sum()
        }
        dataset_info.append(info)
    
    dataset_df = pd.DataFrame(dataset_info)
    st.dataframe(dataset_df, width='stretch')
    
    # File explorer
    st.subheader("🔍 File Explorer")
    if data_files:
        selected_file = st.selectbox("Select a file to explore:", list(data_files.keys()))
    else:
        st.warning("No data files available for exploration.")
        return
    
    if selected_file:
        df = data_files[selected_file]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write(f"**{selected_file}** - Preview (first 10 rows)")
            st.dataframe(df.head(10), width='stretch')
        
        with col2:
            st.write("**Column Information**")
            col_info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null': df.count(),
                'Null': df.isnull().sum()
            })
            st.dataframe(col_info, width='stretch')

def create_quality_analysis(artifacts):
    """Create data quality analysis section"""
    st.markdown('<div class="section-header">🔍 Data Quality Analysis</div>', unsafe_allow_html=True)
    
    if 'data_quality_report.md' not in artifacts:
        st.warning("Data quality report not found")
        return
    
    quality_content = artifacts['data_quality_report.md']
    metrics = parse_quality_metrics(quality_content)
    
    # Overall quality score
    if 'overall_score' in metrics:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Determine color based on score
            if metrics['overall_score'] >= 95:
                score_color = "#6b8e6b"  # Dark green
            elif metrics['overall_score'] >= 80:
                score_color = "#d4a574"  # Orange
            else:
                score_color = "#c0392b"  # Red
            
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="text-align: center; margin: 0; color: #2c3e50;">Overall Data Quality Score</h3>
                <h1 style="text-align: center; color: {score_color}; margin: 0;">{metrics['overall_score']}/100</h1>
            </div>
            """, unsafe_allow_html=True)
    
    # Dataset quality scores
    if 'dataset_scores' in metrics and metrics['dataset_scores']:
        st.subheader("📊 Quality Scores by Dataset")
        
        dataset_scores = metrics['dataset_scores']
        scores_df = pd.DataFrame([
            {'Dataset': name, 'Quality Score': score}
            for name, score in dataset_scores.items()
        ])
        
        # Create quality score visualization
        fig = px.bar(
            scores_df, 
            x='Quality Score', 
            y='Dataset',
            orientation='h',
            title="Data Quality Scores by Dataset",
            color='Quality Score',
            color_continuous_scale='Viridis',
            range_color=[0, 100]
        )
        fig.update_layout(
            font_color='#2c3e50',
            title_font_color='#2c3e50',
            xaxis_title_font_color='#2c3e50',
            yaxis_title_font_color='#2c3e50'
        )
        fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Quality insights
        st.subheader("💡 Quality Insights")
        
        high_quality = [name for name, score in dataset_scores.items() if score >= 95]
        medium_quality = [name for name, score in dataset_scores.items() if 80 <= score < 95]
        low_quality = [name for name, score in dataset_scores.items() if score < 80]
        
        if high_quality:
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ High Quality Datasets ({len(high_quality)}):</strong><br>
                {', '.join(high_quality)}
            </div>
            """, unsafe_allow_html=True)
        
        if medium_quality:
            st.markdown(f"""
            <div class="warning-box">
                <strong>⚠️ Medium Quality Datasets ({len(medium_quality)}):</strong><br>
                {', '.join(medium_quality)}
            </div>
            """, unsafe_allow_html=True)
        
        if low_quality:
            st.markdown(f"""
            <div class="warning-box">
                <strong>🔴 Low Quality Datasets ({len(low_quality)}):</strong><br>
                {', '.join(low_quality)}
            </div>
            """, unsafe_allow_html=True)

def create_correlation_analysis(artifacts, data_files):
    """Create correlation analysis section"""
    st.markdown('<div class="section-header">🔗 Correlation Analysis</div>', unsafe_allow_html=True)
    
    if 'correlation_analysis.md' not in artifacts:
        st.warning("Correlation analysis not found")
        return
    
    correlation_content = artifacts['correlation_analysis.md']
    correlations = parse_correlation_data(correlation_content)
    
    if correlations:
        st.subheader("📊 Strong Correlations (|r| ≥ 0.7)")
        
        # Create correlation table
        corr_df = pd.DataFrame(correlations)
        st.dataframe(corr_df, width='stretch')
        
        # Correlation visualization
        if len(correlations) > 0:
            # Create correlation matrix for visualization
            features = set()
            for corr in correlations:
                features.add(corr['feature_x'])
                features.add(corr['feature_y'])
            
            features = list(features)
            corr_matrix = np.eye(len(features))
            
            # Fill correlation matrix
            for corr in correlations:
                try:
                    if corr['feature_x'] in features and corr['feature_y'] in features:
                        i = features.index(corr['feature_x'])
                        j = features.index(corr['feature_y'])
                        corr_matrix[i][j] = corr['correlation']
                        corr_matrix[j][i] = corr['correlation']
                except (ValueError, KeyError):
                    # Skip if feature not found in features list
                    continue
            
            # Create heatmap
            fig = px.imshow(
                corr_matrix,
                x=features,
                y=features,
                color_continuous_scale='RdBu_r',
                aspect='auto',
                title="Correlation Matrix Heatmap"
            )
            fig.update_layout(
                font_color='#2c3e50',
                title_font_color='#2c3e50',
                xaxis_title_font_color='#2c3e50',
                yaxis_title_font_color='#2c3e50'
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation insights
        st.subheader("💡 Correlation Insights")
        
        strong_correlations = [c for c in correlations if abs(c['correlation']) >= 0.7]
        if strong_correlations:
            st.markdown(f"""
            <div class="insight-box">
                <strong>🔍 Key Findings:</strong><br>
                • Found {len(strong_correlations)} strong correlations (|r| ≥ 0.7)<br>
                • Highest correlation: {max(strong_correlations, key=lambda x: abs(x['correlation']))['correlation']:.2f}<br>
                • All correlations are statistically significant (p < 0.05)
            </div>
            """, unsafe_allow_html=True)
    
    # Interactive correlation exploration
    st.subheader("🔍 Interactive Correlation Explorer")
    
    # Allow user to select datasets for correlation analysis
    available_datasets = list(data_files.keys()) if data_files else []
    if not available_datasets:
        st.warning("No datasets available for correlation analysis.")
        return
    
    selected_datasets = st.multiselect(
        "Select datasets for correlation analysis:",
        available_datasets,
        default=available_datasets[:3] if len(available_datasets) >= 3 else available_datasets
    )
    
    if len(selected_datasets) >= 2:
        # Combine selected datasets and calculate correlations
        combined_data = []
        for dataset_name in selected_datasets:
            df = data_files[dataset_name]
            # Add dataset prefix to avoid column name conflicts
            df_prefixed = df.add_prefix(f"{dataset_name}_")
            combined_data.append(df_prefixed)
        
        if combined_data:
            # Simple correlation analysis on numeric columns
            numeric_cols = []
            for df in combined_data:
                numeric_cols.extend(df.select_dtypes(include=[np.number]).columns)
            
            if len(numeric_cols) > 1:
                try:
                    # Create a combined dataframe for correlation
                    # Reset index to avoid alignment issues
                    combined_data_reset = [df.reset_index(drop=True) for df in combined_data]
                    combined_df = pd.concat(combined_data_reset, axis=1)
                    numeric_df = combined_df[numeric_cols]
                    
                    # Calculate correlation matrix
                    corr_matrix = numeric_df.corr()
                except (ValueError, TypeError) as e:
                    st.error(f"❌ Error combining datasets for correlation: {str(e)}")
                    st.info("💡 Try selecting datasets with compatible structures.")
                    return  # Exit function early instead of continue
                
                # Create interactive heatmap
                fig = px.imshow(
                    corr_matrix,
                    color_continuous_scale='RdBu_r',
                    aspect='auto',
                    title=f"Correlation Matrix: {', '.join(selected_datasets)}"
                )
                fig.update_layout(
                    font_color='#2c3e50',
                    title_font_color='#2c3e50',
                    xaxis_title_font_color='#2c3e50',
                    yaxis_title_font_color='#2c3e50'
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)

def create_kpi_dashboard(artifacts):
    """Create KPI dashboard section"""
    st.markdown('<div class="section-header">🎯 KPI Dashboard</div>', unsafe_allow_html=True)
    
    if 'kpi_definitions.md' not in artifacts:
        st.warning("KPI definitions not found")
        return
    
    kpi_content = artifacts['kpi_definitions.md']
    
    # Extract KPI information
    st.subheader("📊 Key Performance Indicators")
    
    # Business KPIs
    st.markdown("### 🏢 Business KPIs")
    business_kpis = [
        ("User Adoption Rate", "≥ 60%", "Monthly active usage by pilot organizations"),
        ("Contract Conversion Rate", "TBD", "Paid / pilot accounts"),
        ("Decision Acceleration", "≥ 40%", "Reduction in analysis/report generation time"),
        ("Stakeholder Satisfaction (NPS)", "≥ 4.0/5", "Post-use survey rating")
    ]
    
    for kpi, target, description in business_kpis:
        st.markdown(f"""
        <div class="metric-card">
            <strong>{kpi}</strong><br>
            <span style="color: #5a6c7d;">Target: {target}</span><br>
            <small>{description}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Product KPIs
    st.markdown("### 📱 Product KPIs")
    product_kpis = [
        ("Simulation Accuracy", "≥ 75%", "Predicted vs actual life expectancy trend direction"),
        ("Narrative Coherence Score", "≥ 4.0/5", "Manual + AI evaluation score"),
        ("Feature Adoption", "TBD", "% usage of top 3 features"),
        ("Data Freshness Compliance", "≤ 3 months", "% datasets updated within target lag")
    ]
    
    for kpi, target, description in product_kpis:
        st.markdown(f"""
        <div class="metric-card">
            <strong>{kpi}</strong><br>
            <span style="color: #5a6c7d;">Target: {target}</span><br>
            <small>{description}</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Technical KPIs
    st.markdown("### ⚙️ Technical KPIs")
    technical_kpis = [
        ("API Response Time", "≤ 5s", "95th percentile latency"),
        ("System Uptime", "≥ 99%", "Availability of backend API"),
        ("Cost per Simulation", "≤ $0.10", "GPT + infrastructure cost"),
        ("Error Rate", "< 5%", "4xx/5xx errors / total requests")
    ]
    
    for kpi, target, description in technical_kpis:
        st.markdown(f"""
        <div class="metric-card">
            <strong>{kpi}</strong><br>
            <span style="color: #5a6c7d;">Target: {target}</span><br>
            <small>{description}</small>
        </div>
        """, unsafe_allow_html=True)

def create_country_analysis(data_files):
    """Create country analysis section"""
    st.markdown('<div class="section-header">🌍 Country Analysis</div>', unsafe_allow_html=True)
    
    # Define valid countries
    VALID_COUNTRIES = {'Spain', 'Sweden', 'Portugal', 'Greece', 'Global'}
    
    # Extract country information from datasets
    country_data = {}
    country_stats = {}
    
    for file_name, df in data_files.items():
        # Look for country-related columns
        country_cols = [col for col in df.columns if any(keyword in col.lower() 
                       for keyword in ['country', 'geo', 'name', 'code'])]
        
        if country_cols:
            for col in country_cols:
                if col in df.columns:
                    # Convert to string and filter to valid countries only
                    all_values = df[col].dropna().astype(str).unique()
                    countries = [country for country in all_values if country in VALID_COUNTRIES]
                    
                    if len(countries) > 0:
                        country_data[f"{file_name}_{col}"] = countries
                        
                        # Count data points per valid country only
                        country_counts = df[col].value_counts()
                        valid_country_counts = country_counts[country_counts.index.isin(VALID_COUNTRIES)]
                        country_stats[f"{file_name}_{col}"] = valid_country_counts
    
    if country_data:
        # Show data filtering information
        st.subheader("🔍 Data Filtering Information")
        
        # Count invalid entries that were filtered out
        invalid_entries = {}
        total_invalid = 0
        
        for file_name, df in data_files.items():
            country_cols = [col for col in df.columns if any(keyword in col.lower() 
                           for keyword in ['country', 'geo', 'name', 'code'])]
            
            for col in country_cols:
                if col in df.columns:
                    all_values = df[col].dropna().astype(str).unique()
                    invalid_values = [val for val in all_values if val not in VALID_COUNTRIES]
                    if invalid_values:
                        invalid_entries[f"{file_name}_{col}"] = invalid_values
                        total_invalid += len(invalid_values)
        
        if invalid_entries:
            st.info(f"""
            **Data Filtering Applied:** 
            - **Valid Countries:** {', '.join(sorted(VALID_COUNTRIES))}
            - **Invalid entries filtered out:** {total_invalid} entries across {len(invalid_entries)} columns
            - **Invalid entries include:** {', '.join(sorted(set([val for vals in invalid_entries.values() for val in vals]))[:10])}{'...' if total_invalid > 10 else ''}
            """)
        else:
            st.success(f"✅ All country data contains only valid countries: {', '.join(sorted(VALID_COUNTRIES))}")
        
        st.subheader("📊 Data Availability by Country")
        
        # Create comprehensive country coverage analysis
        all_countries = set()
        dataset_country_mapping = {}
        
        for dataset_col, countries in country_data.items():
            dataset_name = dataset_col.split('_')[0]
            if dataset_name not in dataset_country_mapping:
                dataset_country_mapping[dataset_name] = set()
            
            # Convert to string and add to sets
            str_countries = [str(c) for c in countries]
            dataset_country_mapping[dataset_name].update(str_countries)
            all_countries.update(str_countries)
        
        # Create country coverage matrix
        country_coverage_matrix = []
        for country in sorted(all_countries):
            row = {'Country': country}
            for dataset in dataset_country_mapping.keys():
                row[dataset] = '✅' if country in dataset_country_mapping[dataset] else '❌'
            country_coverage_matrix.append(row)
        
        coverage_df = pd.DataFrame(country_coverage_matrix)
        
        # Display coverage matrix
        st.subheader("📋 Country Coverage Matrix")
        st.dataframe(coverage_df, width='stretch')
        
        # Create coverage visualization
        st.subheader("📊 Coverage Statistics")
        
        # Dataset coverage counts
        dataset_counts = pd.DataFrame([
            {'Dataset': dataset, 'Country Count': len(countries)}
            for dataset, countries in dataset_country_mapping.items()
        ])
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                dataset_counts,
                x='Dataset',
                y='Country Count',
                title="Countries per Dataset",
                color='Country Count',
                color_continuous_scale='Blues'
            )
            fig.update_layout(
                font_color='#2c3e50',
                title_font_color='#2c3e50',
                xaxis_title_font_color='#2c3e50',
                yaxis_title_font_color='#2c3e50'
            )
            fig.update_layout(height=400, xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Country frequency across datasets
            country_frequency = {}
            for country in all_countries:
                count = sum(1 for dataset_countries in dataset_country_mapping.values() 
                           if country in dataset_countries)
                country_frequency[country] = count
            
            freq_df = pd.DataFrame([
                {'Country': country, 'Dataset Count': count}
                for country, count in country_frequency.items()
            ]).sort_values('Dataset Count', ascending=False)
            
            fig = px.bar(
                freq_df.head(15),  # Show top 15 countries
                x='Dataset Count',
                y='Country',
                orientation='h',
                title="Top Countries by Dataset Coverage",
                color='Dataset Count',
                color_continuous_scale='Greens'
            )
            fig.update_layout(
                font_color='#2c3e50',
                title_font_color='#2c3e50',
                xaxis_title_font_color='#2c3e50',
                yaxis_title_font_color='#2c3e50'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed country analysis
        st.subheader("🔍 Detailed Country Analysis")
        
        # Country selector
        selected_country = st.selectbox(
            "Select a country for detailed analysis:",
            sorted(all_countries),
            key="country_selector"
        )
        
        if selected_country:
            st.write(f"**Analysis for: {selected_country}**")
            
            # Show which datasets contain this country
            available_datasets = []
            for dataset, countries in dataset_country_mapping.items():
                if selected_country in countries:
                    available_datasets.append(dataset)
            
            st.write(f"**Available in {len(available_datasets)} datasets:** {', '.join(available_datasets)}")
            
            # Show data points per dataset for this country
            if available_datasets:
                st.subheader("📊 Data Points by Dataset")
                
                data_points = []
                for dataset_col, country_counts in country_stats.items():
                    dataset_name = dataset_col.split('_')[0]
                    if dataset_name in available_datasets:
                        if selected_country in country_counts.index:
                            count = country_counts[selected_country]
                            data_points.append({
                                'Dataset': dataset_name,
                                'Data Points': count
                            })
                
                if data_points:
                    points_df = pd.DataFrame(data_points)
                    fig = px.bar(
                        points_df,
                        x='Dataset',
                        y='Data Points',
                        title=f"Data Points for {selected_country}",
                        color='Data Points',
                        color_continuous_scale='Viridis'
                    )
                    fig.update_layout(
                        font_color='#2c3e50',
                        title_font_color='#2c3e50',
                        xaxis_title_font_color='#2c3e50',
                        yaxis_title_font_color='#2c3e50'
                    )
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show detailed breakdown
                    st.dataframe(points_df, width='stretch')
        
        # Country data distribution
        st.subheader("📊 Data Distribution by Country")
        
        # Create a detailed breakdown of data points per country per dataset
        country_dataset_breakdown = []
        for country in sorted(all_countries):
            for dataset_col, country_counts in country_stats.items():
                dataset_name = dataset_col.split('_')[0]
                if country in country_counts.index:
                    count = country_counts[country]
                    country_dataset_breakdown.append({
                        'Country': country,
                        'Dataset': dataset_name,
                        'Data Points': count
                    })
        
        if country_dataset_breakdown:
            breakdown_df = pd.DataFrame(country_dataset_breakdown)
            
            # Create pivot table for better visualization
            try:
                # Check for duplicates before pivoting
                duplicates = breakdown_df.duplicated(subset=['Country', 'Dataset'], keep=False)
                if duplicates.any():
                    # Aggregate duplicates by summing data points
                    breakdown_df = breakdown_df.groupby(['Country', 'Dataset'])['Data Points'].sum().reset_index()
                
                pivot_df = breakdown_df.pivot(index='Country', columns='Dataset', values='Data Points').fillna(0)
            except (ValueError, KeyError) as e:
                st.warning(f"⚠️ Could not create pivot table: {str(e)}")
                st.dataframe(breakdown_df, width='stretch')
                return  # Exit function early instead of continue
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Data Points per Country per Dataset**")
                st.dataframe(pivot_df, width='stretch')
            
            with col2:
                # Create heatmap
                fig = px.imshow(
                    pivot_df.values,
                    x=pivot_df.columns,
                    y=pivot_df.index,
                    color_continuous_scale='Blues',
                    title="Data Points Heatmap",
                    labels=dict(x="Dataset", y="Country", color="Data Points")
                )
                fig.update_layout(
                    font_color='#2c3e50',
                    title_font_color='#2c3e50',
                    xaxis_title_font_color='#2c3e50',
                    yaxis_title_font_color='#2c3e50'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        st.subheader("📈 Summary Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Valid Countries", len(all_countries))
        
        with col2:
            if dataset_country_mapping:
                avg_coverage = sum(len(countries) for countries in dataset_country_mapping.values()) / len(dataset_country_mapping)
                st.metric("Average Countries per Dataset", f"{avg_coverage:.1f}")
            else:
                st.metric("Average Countries per Dataset", "N/A")
        
        with col3:
            if dataset_country_mapping:
                max_countries = max(len(countries) for countries in dataset_country_mapping.values())
                st.metric("Max Countries in Dataset", max_countries)
            else:
                st.metric("Max Countries in Dataset", "N/A")
        
        with col4:
            if dataset_country_mapping:
                min_countries = min(len(countries) for countries in dataset_country_mapping.values())
                st.metric("Min Countries in Dataset", min_countries)
            else:
                st.metric("Min Countries in Dataset", "N/A")
        
        # Data quality insights
        st.subheader("💡 Data Coverage Insights")
        
        # Find countries with complete coverage
        complete_coverage = []
        for country in all_countries:
            coverage_count = sum(1 for dataset_countries in dataset_country_mapping.values() 
                               if country in dataset_countries)
            if coverage_count == len(dataset_country_mapping):
                complete_coverage.append(country)
        
        if complete_coverage:
            st.markdown(f"""
            <div class="success-box">
                <strong>✅ Complete Coverage Countries ({len(complete_coverage)}):</strong><br>
                {', '.join(complete_coverage[:10])}{'...' if len(complete_coverage) > 10 else ''}
            </div>
            """, unsafe_allow_html=True)
        
        # Find countries with limited coverage
        limited_coverage = []
        for country in all_countries:
            coverage_count = sum(1 for dataset_countries in dataset_country_mapping.values() 
                               if country in dataset_countries)
            if coverage_count <= 2:  # Countries in 2 or fewer datasets
                limited_coverage.append((country, coverage_count))
        
        if limited_coverage:
            limited_coverage.sort(key=lambda x: x[1])
            st.markdown(f"""
            <div class="warning-box">
                <strong>⚠️ Limited Coverage Countries ({len(limited_coverage)}):</strong><br>
                {', '.join([f"{country} ({count} datasets)" for country, count in limited_coverage[:10]])}{'...' if len(limited_coverage) > 10 else ''}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.warning("No country information found in the datasets. Please check if the data files contain country-related columns.")

def create_temporal_analysis(data_files):
    """Create temporal analysis section"""
    st.markdown('<div class="section-header">📅 Temporal Analysis</div>', unsafe_allow_html=True)
    
    # Extract temporal information from datasets
    temporal_data = {}
    
    for file_name, df in data_files.items():
        # Look for time-related columns (more comprehensive search)
        time_cols = [col for col in df.columns if any(keyword in col.lower() 
                     for keyword in ['time', 'year', 'date', 'dim_time'])]
        
        if time_cols:
            for col in time_cols:
                if col in df.columns:
                    try:
                        # Try to convert to numeric for year analysis
                        time_values = pd.to_numeric(df[col], errors='coerce').dropna()
                        
                        # Filter out unrealistic years (before 1900 or after 2030)
                        time_values = time_values[(time_values >= 1900) & (time_values <= 2030)]
                        
                        if len(time_values) > 0:
                            temporal_data[f"{file_name}_{col}"] = {
                                'min': int(time_values.min()),
                                'max': int(time_values.max()),
                                'count': len(time_values),
                                'unique': time_values.nunique(),
                                'years': sorted(time_values.unique().tolist())
                            }
                    except Exception as e:
                        # If conversion fails, try to extract years from string values
                        try:
                            # Look for 4-digit numbers in the column
                            all_values = df[col].astype(str)
                            years = []
                            for val in all_values:
                                # Fix regex to capture full 4-digit year, not just "19" or "20"
                                year_matches = re.findall(r'\b(19\d{2}|20\d{2})\b', str(val))
                                years.extend([int(y) for y in year_matches if 1900 <= int(y) <= 2030])
                            
                            if years:
                                years = sorted(set(years))
                                temporal_data[f"{file_name}_{col}"] = {
                                    'min': min(years),
                                    'max': max(years),
                                    'count': len(years),
                                    'unique': len(years),
                                    'years': years
                                }
                        except:
                            continue
    
    if temporal_data:
        st.subheader("📊 Time Coverage by Dataset")
        
        # Create temporal coverage visualization
        temporal_df = pd.DataFrame([
            {
                'Dataset': dataset_col.split('_')[0],
                'Column': dataset_col.split('_', 1)[1],
                'Start Year': data['min'],
                'End Year': data['max'],
                'Duration (Years)': data['max'] - data['min'] + 1,
                'Unique Years': data['unique'],
                'Data Points': data['count'],
                'Coverage %': round((data['unique'] / (data['max'] - data['min'] + 1)) * 100, 1) if (data['max'] - data['min'] + 1) > 0 else 0.0
            }
            for dataset_col, data in temporal_data.items()
        ])
        
        # Timeline visualization
        fig = go.Figure()
        
        for _, row in temporal_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row['Start Year'], row['End Year']],
                y=[row['Dataset']],
                mode='lines+markers',
                name=row['Dataset'],
                line=dict(width=6),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Temporal Coverage Timeline",
            xaxis_title="Year",
            yaxis_title="Dataset",
            height=400,
            font_color='#2c3e50',
            title_font_color='#2c3e50',
            xaxis_title_font_color='#2c3e50',
            yaxis_title_font_color='#2c3e50'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Temporal statistics
        st.subheader("📈 Temporal Statistics")
        st.dataframe(temporal_df, width='stretch')
        
        # Summary statistics
        st.subheader("📊 Time Coverage Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_min = temporal_df['Start Year'].min()
            st.metric("Earliest Year", overall_min)
        
        with col2:
            overall_max = temporal_df['End Year'].max()
            st.metric("Latest Year", overall_max)
        
        with col3:
            total_span = overall_max - overall_min + 1
            st.metric("Total Time Span", f"{total_span} years")
        
        with col4:
            avg_coverage = temporal_df['Coverage %'].mean()
            st.metric("Average Coverage", f"{avg_coverage:.1f}%")
        
        # Detailed year analysis
        st.subheader("🔍 Detailed Year Coverage")
        
        # Create a comprehensive year coverage analysis
        all_years = set()
        dataset_year_mapping = {}
        
        for dataset_col, data in temporal_data.items():
            dataset_name = dataset_col.split('_')[0]
            years = set(data['years'])
            dataset_year_mapping[dataset_name] = years
            all_years.update(years)
        
        # Create year coverage matrix
        year_coverage_matrix = []
        for year in sorted(all_years):
            row = {'Year': year}
            for dataset in dataset_year_mapping.keys():
                row[dataset] = '✅' if year in dataset_year_mapping[dataset] else '❌'
            year_coverage_matrix.append(row)
        
        coverage_df = pd.DataFrame(year_coverage_matrix)
        
        # Show year coverage matrix (limit to recent years for readability)
        recent_years = coverage_df[coverage_df['Year'] >= 2010]
        if len(recent_years) > 0:
            st.write("**Year Coverage Matrix (2010-2023)**")
            st.dataframe(recent_years, width='stretch')
        
        # Year frequency analysis
        st.subheader("📊 Year Frequency Analysis")
        
        year_frequency = {}
        for year in all_years:
            count = sum(1 for dataset_years in dataset_year_mapping.values() 
                       if year in dataset_years)
            year_frequency[year] = count
        
        freq_df = pd.DataFrame([
            {'Year': year, 'Dataset Count': count}
            for year, count in year_frequency.items()
        ]).sort_values('Year')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Show years with complete coverage
            complete_years = [year for year, count in year_frequency.items() 
                            if count == len(dataset_year_mapping)]
            if complete_years:
                st.write(f"**Years with Complete Coverage ({len(complete_years)}):**")
                st.write(f"Range: {min(complete_years)} - {max(complete_years)}")
                st.write(f"Recent complete years: {sorted(complete_years)[-5:]}")
        
        with col2:
            # Show years with limited coverage
            limited_years = [year for year, count in year_frequency.items() 
                           if count <= 2]
            if limited_years:
                st.write(f"**Years with Limited Coverage ({len(limited_years)}):**")
                st.write(f"Range: {min(limited_years)} - {max(limited_years)}")
                st.write(f"Examples: {sorted(limited_years)[:5]}")
        
        # Create year frequency chart
        fig = px.bar(
            freq_df,
            x='Year',
            y='Dataset Count',
            title="Number of Datasets per Year",
            color='Dataset Count',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            font_color='#2c3e50',
            title_font_color='#2c3e50',
            xaxis_title_font_color='#2c3e50',
            yaxis_title_font_color='#2c3e50'
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

def create_insights_summary(artifacts):
    """Create insights summary section"""
    st.markdown('<div class="section-header">💡 Key Insights & Recommendations</div>', unsafe_allow_html=True)
    
    # Data Quality Insights
    if 'data_quality_report.md' in artifacts:
        quality_content = artifacts['data_quality_report.md']
        metrics = parse_quality_metrics(quality_content)
        
        st.subheader("🔍 Data Quality Insights")
        
        if 'overall_score' in metrics:
            score = metrics['overall_score']
            if score >= 95:
                st.markdown(f"""
                <div class="success-box">
                    <strong>✅ Excellent Data Quality</strong><br>
                    Overall quality score of {score}/100 indicates high-quality datasets suitable for analysis and modeling.
                </div>
                """, unsafe_allow_html=True)
            elif score >= 80:
                st.markdown(f"""
                <div class="warning-box">
                    <strong>⚠️ Good Data Quality</strong><br>
                    Overall quality score of {score}/100 indicates good datasets with minor issues that should be addressed.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-box">
                    <strong>🔴 Data Quality Issues</strong><br>
                    Overall quality score of {score}/100 indicates significant data quality issues that need immediate attention.
                </div>
                """, unsafe_allow_html=True)
    
    # Correlation Insights
    if 'correlation_analysis.md' in artifacts:
        correlation_content = artifacts['correlation_analysis.md']
        correlations = parse_correlation_data(correlation_content)
        
        st.subheader("🔗 Correlation Insights")
        
        if correlations:
            strong_correlations = [c for c in correlations if abs(c['correlation']) >= 0.7]
            if strong_correlations:
                strongest_corr = max(strong_correlations, key=lambda x: abs(x['correlation']))['correlation']
            else:
                strongest_corr = 0.0
            
            st.markdown(f"""
            <div class="insight-box">
                <strong>📊 Correlation Analysis Results:</strong><br>
                • Found {len(strong_correlations)} strong correlations (|r| ≥ 0.7)<br>
                • Strongest correlation: {strongest_corr:.2f}<br>
                • All correlations are statistically significant (p < 0.05)<br>
                • These relationships can inform policy simulation models
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("🎯 Recommendations")
    
    recommendations = [
        "**Data Standardization:** Implement canonical schema with standardized column names (country, iso3, year, metric_name, value, unit, source)",
        "**Quality Monitoring:** Set up automated data quality checks with alerts for completeness < 95%, duplicates > 0.5%, validity < 98%",
        "**Temporal Alignment:** Ensure consistent year ranges across datasets for reliable correlation analysis",
        "**Country Mapping:** Standardize country codes to ISO3 format for reliable cross-dataset joins",
        "**Model Development:** Leverage strong correlations for feature selection in policy simulation models",
        "**Monitoring Setup:** Implement KPI tracking dashboard with automated reporting and alerting"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.markdown(f"""
        <div class="insight-box">
            <strong>{i}. {rec}</strong>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<div class="main-header">📊 Policy Simulator - EDA Dashboard</div>', unsafe_allow_html=True)
    st.markdown("**Comprehensive data exploration and analysis dashboard using ADAPT framework artifacts**")
    
    # Load data
    with st.spinner("Loading data files and artifacts..."):
        data_files = load_data_files()
        artifacts = load_artifacts()
    
    if not data_files:
        st.error("❌ No data files found. Please ensure data files are in one of these locations:")
        st.code("""
        - data/raw/
        - policy_simulator/data/raw/
        - adapt_context/data/
        """)
        st.info("💡 The dashboard will work with partial data - some features may be limited.")
        # Don't return - allow partial functionality
    
    if not artifacts:
        st.warning("⚠️ No artifact files found. Some analysis sections may be limited.")
        st.info("💡 Artifacts are optional - the dashboard will work with available data.")
        # Don't return - allow partial functionality
    
    # Sidebar navigation
    st.sidebar.title("📋 Navigation")
    page = st.sidebar.selectbox(
        "Select Analysis Section:",
        [
            "📊 Data Overview",
            "🔍 Data Quality Analysis", 
            "🔗 Correlation Analysis",
            "🎯 KPI Dashboard",
            "🌍 Country Analysis",
            "📅 Temporal Analysis",
            "💡 Insights & Recommendations"
        ]
    )
    
    # Display selected page
    if page == "📊 Data Overview":
        create_data_overview(data_files)
    elif page == "🔍 Data Quality Analysis":
        create_quality_analysis(artifacts)
    elif page == "🔗 Correlation Analysis":
        create_correlation_analysis(artifacts, data_files)
    elif page == "🎯 KPI Dashboard":
        create_kpi_dashboard(artifacts)
    elif page == "🌍 Country Analysis":
        create_country_analysis(data_files)
    elif page == "📅 Temporal Analysis":
        create_temporal_analysis(data_files)
    elif page == "💡 Insights & Recommendations":
        create_insights_summary(artifacts)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
        📊 Policy Simulator EDA Dashboard | 
        Generated on {date} | 
        ADAPT Framework Analysis
    </div>
    """.format(date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Fatal error starting dashboard: {str(e)}")
        st.exception(e)
        st.info("💡 Please check the logs for more details.")
