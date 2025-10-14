"""
Narrative generation service with AI integration
"""

import openai
import time
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog
import re

from src.backend.models.narrative_models import (
    NarrativeRequest, NarrativeResponse, NarrativeSection, Citation, 
    Recommendation, QualityMetrics, NarrativeType, AudienceType, 
    ToneType, LengthType, FocusArea
)
from src.backend.core.config import settings
from src.backend.core.exceptions import PolicySimulationException

logger = structlog.get_logger()


class NarrativeService:
    """Service for AI-powered narrative generation"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.templates = self._load_templates()
        self.prompt_templates = self._load_prompt_templates()
        
    def generate_narrative(self, request: NarrativeRequest) -> NarrativeResponse:
        """Generate a narrative based on the request"""
        start_time = time.time()
        narrative_id = str(uuid.uuid4())
        
        logger.info("Starting narrative generation", 
                   narrative_id=narrative_id, 
                   narrative_type=request.narrative_type,
                   audience=request.audience)
        
        try:
            # Build the prompt based on request
            prompt = self._build_prompt(request)
            
            # Generate narrative with OpenAI
            response = self._call_openai(prompt, request)
            
            # Parse and structure the response
            narrative_content = self._parse_narrative_response(response, request)
            
            # Calculate quality metrics
            quality_metrics = self._calculate_quality_metrics(narrative_content, request)
            
            # Calculate cost and timing
            generation_time_ms = int((time.time() - start_time) * 1000)
            cost_usd = self._calculate_cost(response.usage)
            
            # Create response
            narrative_response = NarrativeResponse(
                narrative_id=narrative_id,
                title=narrative_content.get('title', 'Generated Narrative'),
                narrative_type=request.narrative_type,
                sections=narrative_content.get('sections', []),
                executive_summary=narrative_content.get('executive_summary', ''),
                key_insights=narrative_content.get('key_insights', []),
                recommendations=narrative_content.get('recommendations', []),
                citations=narrative_content.get('citations', []),
                quality_metrics=quality_metrics,
                metadata={
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens,
                    'model': 'gpt-4',
                    'temperature': 0.7
                },
                cost_usd=cost_usd,
                generation_time_ms=generation_time_ms
            )
            
            logger.info("Narrative generation completed successfully",
                       narrative_id=narrative_id,
                       generation_time_ms=generation_time_ms,
                       cost_usd=cost_usd,
                       quality_score=quality_metrics.overall_score)
            
            return narrative_response
            
        except Exception as e:
            logger.error("Narrative generation failed", 
                        narrative_id=narrative_id, 
                        error=str(e), 
                        exc_info=True)
            raise PolicySimulationException(
                error_code="NARRATIVE_GENERATION_FAILED",
                detail=f"Failed to generate narrative: {str(e)}",
                status_code=500
            )
    
    def _build_prompt(self, request: NarrativeRequest) -> str:
        """Build the prompt for narrative generation"""
        template = self.prompt_templates.get(request.narrative_type)
        if not template:
            raise PolicySimulationException(
                error_code="TEMPLATE_NOT_FOUND",
                detail=f"No template found for narrative type: {request.narrative_type}",
                status_code=400
            )
        
        # Get template-specific prompt
        base_prompt = template['prompt']
        
        # Add context based on data source
        context = self._build_context(request.data_source, request.narrative_type)
        
        # Add customization instructions
        customization = self._build_customization(request)
        
        # Combine all parts
        full_prompt = f"""
{base_prompt}

CONTEXT DATA:
{context}

CUSTOMIZATION INSTRUCTIONS:
{customization}

Please generate a comprehensive narrative following the template structure and incorporating the provided context data.
"""
        
        return full_prompt
    
    def _build_context(self, data_source: Dict[str, Any], narrative_type: NarrativeType) -> str:
        """Build context from data source"""
        if narrative_type == NarrativeType.SIMULATION_IMPACT:
            return self._build_simulation_context(data_source)
        elif narrative_type == NarrativeType.BENCHMARK_COMPARISON:
            return self._build_benchmark_context(data_source)
        elif narrative_type == NarrativeType.ANOMALY_ALERT:
            return self._build_anomaly_context(data_source)
        elif narrative_type == NarrativeType.TREND_ANALYSIS:
            return self._build_trend_context(data_source)
        else:
            return str(data_source)
    
    def _build_simulation_context(self, data: Dict[str, Any]) -> str:
        """Build context for simulation results"""
        context = f"""
SIMULATION RESULTS:
- Country: {data.get('country', 'N/A')}
- Baseline Life Expectancy: {data.get('baseline_life_expectancy', 'N/A')} years
- Predicted Change: {data.get('predicted_change', 'N/A')} years
- New Life Expectancy: {data.get('new_life_expectancy', 'N/A')} years
- Confidence Interval: {data.get('confidence_interval', 'N/A')}
- Policy Changes:
  * Doctor Density: {data.get('doctor_density_change', 'N/A')} per 1,000
  * Nurse Density: {data.get('nurse_density_change', 'N/A')} per 1,000
  * Health Spending: {data.get('spending_change', 'N/A')}% of GDP
"""
        return context
    
    def _build_benchmark_context(self, data: Dict[str, Any]) -> str:
        """Build context for benchmark comparison"""
        context = f"""
BENCHMARK COMPARISON:
- Countries Compared: {', '.join(data.get('countries', []))}
- Best Performer: {data.get('best_performer', 'N/A')}
- Worst Performer: {data.get('worst_performer', 'N/A')}
- Total Anomalies: {data.get('total_anomalies', 0)}
- High Severity Anomalies: {data.get('high_severity_anomalies', 0)}
- Peer Groups: {data.get('peer_groups', 0)}
- Average Score: {data.get('average_score', 'N/A')}
"""
        return context
    
    def _build_anomaly_context(self, data: Dict[str, Any]) -> str:
        """Build context for anomaly detection"""
        context = f"""
ANOMALY DETECTION RESULTS:
- Total Anomalies: {data.get('total_anomalies', 0)}
- High Severity: {data.get('high_severity', 0)}
- Medium Severity: {data.get('medium_severity', 0)}
- Low Severity: {data.get('low_severity', 0)}
- Detection Confidence: {data.get('detection_confidence', 'N/A')}
"""
        return context
    
    def _build_trend_context(self, data: Dict[str, Any]) -> str:
        """Build context for trend analysis"""
        context = f"""
TREND ANALYSIS:
- Time Period: {data.get('time_period', 'N/A')}
- Countries Analyzed: {', '.join(data.get('countries', []))}
- Key Trends: {data.get('key_trends', 'N/A')}
- Significant Changes: {data.get('significant_changes', 'N/A')}
"""
        return context
    
    def _build_customization(self, request: NarrativeRequest) -> str:
        """Build customization instructions"""
        customization = f"""
AUDIENCE: {request.audience.value}
TONE: {request.tone.value}
LENGTH: {request.length.value}
FOCUS AREAS: {', '.join([area.value for area in request.focus_areas])}
INCLUDE CITATIONS: {request.include_citations}
INCLUDE RECOMMENDATIONS: {request.include_recommendations}
"""
        
        if request.custom_instructions:
            customization += f"\nCUSTOM INSTRUCTIONS: {request.custom_instructions}"
        
        return customization
    
    def _call_openai(self, prompt: str, request: NarrativeRequest) -> Any:
        """Call OpenAI API for narrative generation"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert policy analyst and narrative writer specializing in healthcare policy communication. Generate clear, actionable, and evidence-based narratives for policy makers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            return response.choices[0].message
            
        except Exception as e:
            logger.error("OpenAI API call failed", error=str(e))
            raise PolicySimulationException(
                error_code="OPENAI_API_ERROR",
                detail=f"OpenAI API call failed: {str(e)}",
                status_code=500
            )
    
    def _parse_narrative_response(self, response: Any, request: NarrativeRequest) -> Dict[str, Any]:
        """Parse OpenAI response into structured narrative"""
        content = response.content
        
        # Extract sections using regex patterns
        sections = self._extract_sections(content)
        
        # Extract executive summary
        executive_summary = self._extract_executive_summary(content)
        
        # Extract key insights
        key_insights = self._extract_key_insights(content)
        
        # Extract recommendations
        recommendations = self._extract_recommendations(content)
        
        # Extract citations
        citations = self._extract_citations(content)
        
        # Extract title
        title = self._extract_title(content)
        
        return {
            'title': title,
            'sections': sections,
            'executive_summary': executive_summary,
            'key_insights': key_insights,
            'recommendations': recommendations,
            'citations': citations
        }
    
    def _extract_sections(self, content: str) -> List[NarrativeSection]:
        """Extract sections from narrative content"""
        sections = []
        
        # Look for section headers (## or ###)
        section_pattern = r'##\s+(.+?)\n(.*?)(?=##|\Z)'
        matches = re.findall(section_pattern, content, re.DOTALL)
        
        for i, (title, content_text) in enumerate(matches):
            section = NarrativeSection(
                title=title.strip(),
                content=content_text.strip(),
                order=i + 1,
                word_count=len(content_text.split()),
                key_points=self._extract_key_points(content_text)
            )
            sections.append(section)
        
        return sections
    
    def _extract_executive_summary(self, content: str) -> str:
        """Extract executive summary from content"""
        # Look for executive summary section
        summary_pattern = r'(?:Executive Summary|Summary)[:\s]*(.*?)(?=\n\n|\Z)'
        match = re.search(summary_pattern, content, re.IGNORECASE | re.DOTALL)
        
        if match:
            return match.group(1).strip()
        
        # Fallback: use first paragraph
        paragraphs = content.split('\n\n')
        return paragraphs[0] if paragraphs else ""
    
    def _extract_key_insights(self, content: str) -> List[str]:
        """Extract key insights from content"""
        insights = []
        
        # Look for bullet points or numbered lists
        bullet_pattern = r'[-*•]\s+(.+?)(?=\n[-*•]|\n\n|\Z)'
        matches = re.findall(bullet_pattern, content, re.DOTALL)
        
        for match in matches:
            insight = match.strip()
            if len(insight) > 10:  # Filter out very short items
                insights.append(insight)
        
        return insights[:5]  # Limit to 5 key insights
    
    def _extract_recommendations(self, content: str) -> List[Recommendation]:
        """Extract recommendations from content"""
        recommendations = []
        
        # Look for recommendation sections
        rec_pattern = r'(?:Recommendation|Action|Next Step)[:\s]*(.+?)(?=\n\n|\Z)'
        matches = re.findall(rec_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for i, match in enumerate(matches):
            rec = Recommendation(
                title=f"Recommendation {i + 1}",
                description=match.strip(),
                priority="medium",  # Default priority
                timeline=None,
                resources_needed=None,
                expected_impact=None
            )
            recommendations.append(rec)
        
        return recommendations
    
    def _extract_citations(self, content: str) -> List[Citation]:
        """Extract citations from content"""
        citations = []
        
        # Look for citation patterns
        citation_pattern = r'\[(\d+)\]\s*(.+?)(?=\[|\Z)'
        matches = re.findall(citation_pattern, content, re.DOTALL)
        
        for num, source in matches:
            citation = Citation(
                source=source.strip(),
                url=None,
                date=None,
                type="reference",
                relevance="Supporting evidence"
            )
            citations.append(citation)
        
        return citations
    
    def _extract_title(self, content: str) -> str:
        """Extract title from content"""
        # Look for title in first line
        first_line = content.split('\n')[0]
        if first_line and not first_line.startswith('#'):
            return first_line.strip()
        
        # Fallback: generate title based on content
        return "Generated Policy Narrative"
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from section content"""
        points = []
        
        # Look for bullet points within the section
        bullet_pattern = r'[-*•]\s+(.+?)(?=\n[-*•]|\n\n|\Z)'
        matches = re.findall(bullet_pattern, content, re.DOTALL)
        
        for match in matches:
            point = match.strip()
            if len(point) > 5:  # Filter out very short items
                points.append(point)
        
        return points[:3]  # Limit to 3 key points per section
    
    def _calculate_quality_metrics(self, narrative_content: Dict[str, Any], request: NarrativeRequest) -> QualityMetrics:
        """Calculate quality metrics for the narrative"""
        # Simple quality calculation based on content structure
        sections = narrative_content.get('sections', [])
        total_word_count = sum(section.word_count for section in sections)
        
        # Calculate scores based on content quality indicators
        coherence_score = min(5.0, 3.0 + len(sections) * 0.5)  # More sections = better structure
        accuracy_score = 4.0  # Default high score (would need fact-checking in production)
        actionability_score = min(5.0, 3.0 + len(narrative_content.get('recommendations', [])) * 0.5)
        readability_score = 4.0  # Default good readability
        
        # Calculate reading time (average 200 words per minute)
        reading_time_minutes = max(1, total_word_count // 200)
        
        overall_score = (coherence_score + accuracy_score + actionability_score + readability_score) / 4
        
        return QualityMetrics(
            coherence_score=coherence_score,
            accuracy_score=accuracy_score,
            actionability_score=actionability_score,
            readability_score=readability_score,
            overall_score=overall_score,
            word_count=total_word_count,
            reading_time_minutes=reading_time_minutes
        )
    
    def _calculate_cost(self, usage: Any) -> float:
        """Calculate cost based on token usage"""
        # GPT-4 pricing: $0.03 per 1K input tokens, $0.06 per 1K output tokens
        input_cost = (usage.prompt_tokens / 1000) * 0.03
        output_cost = (usage.completion_tokens / 1000) * 0.06
        return input_cost + output_cost
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load narrative templates"""
        return {
            NarrativeType.SIMULATION_IMPACT: {
                'name': 'Policy Impact Analysis',
                'description': 'Analyzes the impact of policy changes on health outcomes',
                'sections': ['Executive Summary', 'Policy Context', 'Impact Analysis', 'Recommendations']
            },
            NarrativeType.BENCHMARK_COMPARISON: {
                'name': 'Country Performance Comparison',
                'description': 'Compares country performance across health indicators',
                'sections': ['Executive Summary', 'Performance Overview', 'Key Findings', 'Recommendations']
            },
            NarrativeType.ANOMALY_ALERT: {
                'name': 'Anomaly Detection Report',
                'description': 'Reports on detected anomalies in health data',
                'sections': ['Executive Summary', 'Anomaly Overview', 'Analysis', 'Recommended Actions']
            },
            NarrativeType.TREND_ANALYSIS: {
                'name': 'Trend Analysis Report',
                'description': 'Analyzes trends in health indicators over time',
                'sections': ['Executive Summary', 'Trend Overview', 'Analysis', 'Future Projections']
            }
        }
    
    def _load_prompt_templates(self) -> Dict[NarrativeType, Dict[str, str]]:
        """Load prompt templates for different narrative types"""
        return {
            NarrativeType.SIMULATION_IMPACT: {
                'prompt': """
Generate a comprehensive policy impact narrative based on the simulation results provided. The narrative should:

1. **Executive Summary**: Provide a clear, concise summary of the key findings and implications
2. **Policy Context**: Explain the current policy landscape and why these changes matter
3. **Impact Analysis**: Analyze the predicted impact of the policy changes on health outcomes
4. **Recommendations**: Provide specific, actionable recommendations for policy makers

Focus on:
- Clear communication of the predicted impact
- Contextual explanation of why these changes matter
- Practical implications for policy implementation
- Risk assessment and mitigation strategies
- Evidence-based recommendations

Use a professional, accessible tone that balances technical accuracy with clarity for policy makers.
"""
            },
            NarrativeType.BENCHMARK_COMPARISON: {
                'prompt': """
Generate a comprehensive benchmark comparison narrative based on the provided data. The narrative should:

1. **Executive Summary**: Summarize the key findings from the country comparison
2. **Performance Overview**: Provide a clear overview of how countries compare
3. **Key Findings**: Highlight the most important insights and patterns
4. **Recommendations**: Suggest specific actions based on the comparison

Focus on:
- Clear ranking and performance explanations
- Identification of best practices and areas for improvement
- Contextual analysis of why certain countries perform better
- Actionable insights for policy makers
- Peer group analysis and lessons learned

Use a professional tone that helps policy makers understand both the data and its implications.
"""
            },
            NarrativeType.ANOMALY_ALERT: {
                'prompt': """
Generate a comprehensive anomaly detection report based on the provided data. The narrative should:

1. **Executive Summary**: Summarize the key anomalies detected and their significance
2. **Anomaly Overview**: Provide detailed information about each anomaly
3. **Analysis**: Explain the potential causes and implications of these anomalies
4. **Recommended Actions**: Suggest specific steps to address the anomalies

Focus on:
- Clear explanation of what constitutes an anomaly
- Assessment of the severity and potential impact
- Root cause analysis and contributing factors
- Immediate and long-term response strategies
- Prevention measures for future anomalies

Use a professional, urgent tone that emphasizes the importance of addressing these issues.
"""
            },
            NarrativeType.TREND_ANALYSIS: {
                'prompt': """
Generate a comprehensive trend analysis narrative based on the provided data. The narrative should:

1. **Executive Summary**: Summarize the key trends and their implications
2. **Trend Overview**: Provide a clear overview of the trends observed
3. **Analysis**: Analyze the significance and potential causes of these trends
4. **Future Projections**: Project future developments based on current trends

Focus on:
- Clear identification and explanation of trends
- Analysis of contributing factors and drivers
- Assessment of positive and negative implications
- Future projections and scenarios
- Strategic recommendations for trend management

Use a professional, analytical tone that helps policy makers understand both current patterns and future implications.
"""
            }
        }
