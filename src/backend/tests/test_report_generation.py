"""
Tests for Report Generation Engine
"""

import pytest
import json
from unittest.mock import MagicMock, patch, mock_open
from pathlib import Path

from src.backend.services.report_generation import ReportGenerationEngine

class TestReportGenerationEngine:
    """Test cases for ReportGenerationEngine"""
    
    @pytest.fixture
    def report_engine(self, tmp_path):
        """Report generation engine instance for testing"""
        templates_dir = tmp_path / "templates"
        return ReportGenerationEngine(str(templates_dir))
    
    @pytest.fixture
    def sample_data(self):
        """Sample data for report generation"""
        return {
            "simulation_results": {
                "predicted_change": 0.75,
                "confidence_score": 0.85,
                "country": "PRT"
            },
            "analytics_results": {
                "trend_analysis": {
                    "trend_direction": "increasing",
                    "trend_strength": 0.78
                },
                "correlation_analysis": {
                    "correlation_matrix": [[1.0, 0.8], [0.8, 1.0]]
                }
            },
            "data_sources": [
                "WHO Global Health Observatory"
            ]
        }
    
    @pytest.fixture
    def sample_config(self):
        """Sample configuration for report generation"""
        return {
            "title": "Test Report",
            "branding": {
                "logo": "test-logo.png",
                "primaryColor": "#3498db",
                "secondaryColor": "#2c3e50"
            }
        }
    
    def test_initialization(self, tmp_path):
        """Test report engine initialization"""
        templates_dir = tmp_path / "templates"
        engine = ReportGenerationEngine(str(templates_dir))
        
        assert engine.templates_dir == templates_dir
        assert hasattr(engine, 'templates')
        assert hasattr(engine, 'jinja_env')
        assert 'executive_summary' in engine.templates
        assert 'detailed_analysis' in engine.templates
    
    def test_generate_executive_summary_success(self, report_engine, sample_data, sample_config):
        """Test successful executive summary generation"""
        result = report_engine.generate_executive_summary(sample_data, sample_config)
        
        assert 'error' not in result
        assert 'report_id' in result
        assert result['title'] == sample_config['title']
        assert result['format'] == 'html'
        assert 'content' in result
        assert 'metadata' in result
        assert isinstance(result['content'], str)
        assert len(result['content']) > 0
        assert 'executive_summary' in result['content'].lower()
    
    def test_generate_executive_summary_error_handling(self, report_engine, sample_data, sample_config):
        """Test error handling in executive summary generation"""
        with patch.object(report_engine.jinja_env, 'get_template', side_effect=Exception("Template error")):
            result = report_engine.generate_executive_summary(sample_data, sample_config)
            
            assert 'error' in result
            assert 'Report generation failed' in result['error']
    
    def test_create_detailed_report_success(self, report_engine, sample_data, sample_config):
        """Test successful detailed report creation"""
        result = report_engine.create_detailed_report(sample_data, sample_config)
        
        assert 'error' not in result
        assert 'report_id' in result
        assert result['title'] == sample_config['title']
        assert result['format'] == 'html'
        assert 'content' in result
        assert 'metadata' in result
        assert isinstance(result['content'], str)
        assert len(result['content']) > 0
        assert 'detailed' in result['content'].lower() or 'analysis' in result['content'].lower()
    
    def test_create_detailed_report_error_handling(self, report_engine, sample_data, sample_config):
        """Test error handling in detailed report creation"""
        with patch.object(report_engine.jinja_env, 'get_template', side_effect=Exception("Template error")):
            result = report_engine.create_detailed_report(sample_data, sample_config)
            
            assert 'error' in result
            assert 'Report generation failed' in result['error']
    
    def test_export_to_pdf_success(self, report_engine):
        """Test successful PDF export"""
        html_content = "<html><body>Test content</body></html>"
        filename = "test_report.pdf"
        
        result = report_engine.export_to_pdf(html_content, filename)
        
        assert 'error' not in result
        assert result['success'] is True
        assert result['filename'] == filename
        assert result['format'] == 'pdf'
        assert 'size_bytes' in result
        assert 'download_url' in result
        assert 'message' in result
    
    def test_export_to_docx_success(self, report_engine):
        """Test successful DOCX export"""
        html_content = "<html><body>Test content</body></html>"
        filename = "test_report.docx"
        
        result = report_engine.export_to_docx(html_content, filename)
        
        assert 'error' not in result
        assert result['success'] is True
        assert result['filename'] == filename
        assert result['format'] == 'docx'
        assert 'size_bytes' in result
        assert 'download_url' in result
        assert 'message' in result
    
    def test_export_to_powerpoint_success(self, report_engine, sample_data):
        """Test successful PowerPoint export"""
        filename = "test_report.pptx"
        
        result = report_engine.export_to_powerpoint(sample_data, filename)
        
        assert 'error' not in result
        assert result['success'] is True
        assert result['filename'] == filename
        assert result['format'] == 'pptx'
        assert 'slides_count' in result
        assert 'download_url' in result
        assert 'message' in result
    
    def test_batch_report_generation_success(self, report_engine, sample_data):
        """Test successful batch report generation"""
        report_configs = [
            {
                "template": "executive_summary",
                "title": "Report 1",
                "config": {"branding": {}}
            },
            {
                "template": "detailed_analysis",
                "title": "Report 2",
                "config": {"branding": {}}
            }
        ]
        
        result = report_engine.batch_report_generation(report_configs, sample_data)
        
        assert 'error' not in result
        assert result['success'] is True
        assert result['total_reports'] == 2
        assert result['successful_reports'] == 2
        assert result['failed_reports'] == 0
        assert len(result['results']) == 2
        assert all('report_id' in r for r in result['results'])
    
    def test_batch_report_generation_with_errors(self, report_engine, sample_data):
        """Test batch report generation with some errors"""
        report_configs = [
            {
                "template": "executive_summary",
                "title": "Report 1",
                "config": {"branding": {}}
            },
            {
                "template": "unknown_template",
                "title": "Report 2",
                "config": {"branding": {}}
            }
        ]
        
        result = report_engine.batch_report_generation(report_configs, sample_data)
        
        assert 'error' not in result
        assert result['success'] is True
        assert result['total_reports'] == 2
        assert result['successful_reports'] == 1
        assert result['failed_reports'] == 1
        assert len(result['results']) == 2
        assert 'error' in result['results'][1]
    
    def test_batch_report_generation_error_handling(self, report_engine, sample_data):
        """Test error handling in batch report generation"""
        report_configs = [{"template": "executive_summary", "title": "Report 1", "config": {}}]
        
        with patch.object(report_engine, 'generate_executive_summary', side_effect=Exception("Batch error")):
            result = report_engine.batch_report_generation(report_configs, sample_data)
            
            assert 'error' in result
            assert 'Batch report generation failed' in result['error']
    
    def test_generate_executive_summary_content(self, report_engine, sample_data):
        """Test executive summary content generation"""
        content = report_engine._generate_executive_summary_content(sample_data)
        
        assert isinstance(content, str)
        assert len(content) > 0
        assert 'positive impact' in content or 'negative impact' in content or 'Analysis completed' in content
    
    def test_extract_key_findings(self, report_engine, sample_data):
        """Test key findings extraction"""
        findings = report_engine._extract_key_findings(sample_data)
        
        assert isinstance(findings, list)
        assert len(findings) > 0
        assert all('title' in finding for finding in findings)
        assert all('description' in finding for finding in findings)
    
    def test_generate_recommendations(self, report_engine, sample_data):
        """Test recommendations generation"""
        recommendations = report_engine._generate_recommendations(sample_data)
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all('title' in rec for rec in recommendations)
        assert all('description' in rec for rec in recommendations)
        assert all('priority' in rec for rec in recommendations)
    
    def test_generate_methodology_content(self, report_engine, sample_data):
        """Test methodology content generation"""
        content = report_engine._generate_methodology_content(sample_data)
        
        assert isinstance(content, str)
        assert len(content) > 0
        assert 'statistical methods' in content.lower()
    
    def test_extract_data_sources(self, report_engine, sample_data):
        """Test data sources extraction"""
        sources = report_engine._extract_data_sources(sample_data)
        
        assert isinstance(sources, list)
        assert len(sources) > 0
        assert 'WHO Global Health Observatory' in sources
    
    def test_extract_analytical_methods(self, report_engine, sample_data):
        """Test analytical methods extraction"""
        methods = report_engine._extract_analytical_methods(sample_data)
        
        assert isinstance(methods, list)
        assert len(methods) > 0
        assert 'Linear Regression Analysis' in methods
        assert 'Correlation Analysis' in methods
    
    def test_extract_analysis_results(self, report_engine, sample_data):
        """Test analysis results extraction"""
        results = report_engine._extract_analysis_results(sample_data)
        
        assert isinstance(results, list)
        assert len(results) > 0
        assert all('title' in result for result in results)
        assert all('description' in result for result in results)
    
    def test_extract_statistical_analyses(self, report_engine, sample_data):
        """Test statistical analyses extraction"""
        analyses = report_engine._extract_statistical_analyses(sample_data)
        
        assert isinstance(analyses, list)
        assert len(analyses) > 0
        assert all('title' in analysis for analysis in analyses)
        assert all('description' in analysis for analysis in analyses)
    
    def test_generate_appendix_items(self, report_engine, sample_data):
        """Test appendix items generation"""
        items = report_engine._generate_appendix_items(sample_data)
        
        assert isinstance(items, list)
        assert len(items) > 0
        assert all('title' in item for item in items)
        assert all('content' in item for item in items)
    
    def test_template_creation(self, tmp_path):
        """Test that default templates are created"""
        templates_dir = tmp_path / "templates"
        engine = ReportGenerationEngine(str(templates_dir))
        
        # Check that template files exist
        assert (templates_dir / "executive_summary.html").exists()
        assert (templates_dir / "detailed_analysis.html").exists()
        assert (templates_dir / "policy_brief.html").exists()
        
        # Check that templates contain expected content
        exec_summary_content = (templates_dir / "executive_summary.html").read_text()
        assert "executive_summary" in exec_summary_content.lower()
        assert "html" in exec_summary_content.lower()
    
    def test_templates_property(self, report_engine):
        """Test templates property"""
        templates = report_engine.templates
        
        assert isinstance(templates, dict)
        assert 'executive_summary' in templates
        assert 'detailed_analysis' in templates
        assert 'policy_brief' in templates
        assert 'research_report' in templates
        
        # Check template structure
        for template_id, template_info in templates.items():
            assert 'name' in template_info
            assert 'description' in template_info
            assert 'sections' in template_info
            assert isinstance(template_info['sections'], list)
    
    def test_jinja_environment(self, report_engine):
        """Test Jinja2 environment setup"""
        env = report_engine.jinja_env
        
        assert env is not None
        assert hasattr(env, 'get_template')
        assert hasattr(env, 'loader')
    
    def test_error_handling_in_export_methods(self, report_engine):
        """Test error handling in export methods"""
        html_content = "<html><body>Test</body></html>"
        filename = "test.pdf"
        
        # Test PDF export error handling
        with patch('builtins.open', side_effect=Exception("File error")):
            result = report_engine.export_to_pdf(html_content, filename)
            assert 'error' in result
        
        # Test DOCX export error handling
        with patch('builtins.open', side_effect=Exception("File error")):
            result = report_engine.export_to_docx(html_content, filename)
            assert 'error' in result
        
        # Test PowerPoint export error handling
        with patch('builtins.open', side_effect=Exception("File error")):
            result = report_engine.export_to_powerpoint({}, filename)
            assert 'error' in result
