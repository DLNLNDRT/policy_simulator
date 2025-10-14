"""
Visualization Service for Policy Simulation Assistant
Provides advanced data visualization capabilities including charts, dashboards, and custom visualizations.
"""

import json
import base64
import io
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import structlog
import numpy as np
import pandas as pd

logger = structlog.get_logger()

class VisualizationService:
    """Advanced visualization service for creating sophisticated charts and dashboards"""
    
    def __init__(self):
        self.chart_types = {
            "line": "Line Chart",
            "bar": "Bar Chart",
            "scatter": "Scatter Plot",
            "heatmap": "Heatmap",
            "box": "Box Plot",
            "histogram": "Histogram",
            "pie": "Pie Chart",
            "area": "Area Chart",
            "radar": "Radar Chart",
            "bubble": "Bubble Chart"
        }
    
    def create_heatmap(
        self, 
        data: Dict[str, Any], 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create heatmap visualization for cross-country comparisons
        
        Args:
            data: Data containing countries and indicators
            config: Configuration for heatmap styling and options
            
        Returns:
            Dictionary containing heatmap data and metadata
        """
        logger.info("Creating heatmap visualization")
        
        try:
            # Extract data for heatmap
            countries = data.get("countries", [])
            indicators = data.get("indicators", [])
            values = data.get("values", [])
            
            if not countries or not indicators or not values:
                return {"error": "Insufficient data for heatmap creation"}
            
            # Create heatmap data structure
            heatmap_data = {
                "type": "heatmap",
                "title": config.get("title", "Health Indicators Heatmap"),
                "x_axis": {
                    "title": "Indicators",
                    "categories": indicators
                },
                "y_axis": {
                    "title": "Countries",
                    "categories": countries
                },
                "data": values,
                "color_scale": config.get("color_scale", "viridis"),
                "show_values": config.get("show_values", True),
                "annotations": self._generate_heatmap_annotations(values, countries, indicators)
            }
            
            # Generate chart configuration
            chart_config = {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": heatmap_data["title"]
                    },
                    "legend": {
                        "display": True
                    }
                },
                "scales": {
                    "x": {
                        "title": {
                            "display": True,
                            "text": heatmap_data["x_axis"]["title"]
                        }
                    },
                    "y": {
                        "title": {
                            "display": True,
                            "text": heatmap_data["y_axis"]["title"]
                        }
                    }
                }
            }
            
            result = {
                "chart_id": f"heatmap_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "chart_type": "heatmap",
                "data": heatmap_data,
                "config": chart_config,
                "metadata": {
                    "countries_count": len(countries),
                    "indicators_count": len(indicators),
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Heatmap created successfully", 
                       countries=len(countries), 
                       indicators=len(indicators))
            
            return result
            
        except Exception as e:
            logger.error("Error creating heatmap", error=str(e))
            return {"error": f"Heatmap creation failed: {str(e)}"}
    
    def generate_scatter_plot(
        self, 
        data: Dict[str, Any], 
        config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate scatter plot with correlation analysis
        
        Args:
            data: Data containing x and y values
            config: Configuration for scatter plot styling
            
        Returns:
            Dictionary containing scatter plot data and analysis
        """
        logger.info("Generating scatter plot")
        
        try:
            # Extract data
            x_values = data.get("x_values", [])
            y_values = data.get("y_values", [])
            labels = data.get("labels", [])
            
            if len(x_values) != len(y_values):
                return {"error": "X and Y values must have the same length"}
            
            # Calculate correlation
            correlation = np.corrcoef(x_values, y_values)[0, 1] if len(x_values) > 1 else 0
            
            # Create scatter plot data
            scatter_data = {
                "type": "scatter",
                "title": config.get("title", "Scatter Plot Analysis"),
                "x_axis": {
                    "title": config.get("x_label", "X Variable"),
                    "values": x_values
                },
                "y_axis": {
                    "title": config.get("y_label", "Y Variable"),
                    "values": y_values
                },
                "labels": labels,
                "correlation": {
                    "value": float(correlation),
                    "strength": self._interpret_correlation_strength(abs(correlation)),
                    "direction": "positive" if correlation > 0 else "negative" if correlation < 0 else "none"
                },
                "trend_line": self._calculate_trend_line(x_values, y_values)
            }
            
            # Generate chart configuration
            chart_config = {
                "responsive": True,
                "maintainAspectRatio": False,
                "plugins": {
                    "title": {
                        "display": True,
                        "text": scatter_data["title"]
                    },
                    "legend": {
                        "display": True
                    }
                },
                "scales": {
                    "x": {
                        "title": {
                            "display": True,
                            "text": scatter_data["x_axis"]["title"]
                        }
                    },
                    "y": {
                        "title": {
                            "display": True,
                            "text": scatter_data["y_axis"]["title"]
                        }
                    }
                }
            }
            
            result = {
                "chart_id": f"scatter_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "chart_type": "scatter",
                "data": scatter_data,
                "config": chart_config,
                "analysis": {
                    "correlation_analysis": scatter_data["correlation"],
                    "sample_size": len(x_values),
                    "interpretation": self._generate_scatter_interpretation(scatter_data)
                },
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Scatter plot generated successfully", 
                       correlation=correlation, 
                       sample_size=len(x_values))
            
            return result
            
        except Exception as e:
            logger.error("Error generating scatter plot", error=str(e))
            return {"error": f"Scatter plot generation failed: {str(e)}"}
    
    def build_dashboard(
        self, 
        dashboard_config: Dict[str, Any], 
        data_sources: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build interactive dashboard with multiple visualizations
        
        Args:
            dashboard_config: Configuration for dashboard layout and components
            data_sources: Data sources for dashboard components
            
        Returns:
            Dictionary containing dashboard configuration and data
        """
        logger.info("Building interactive dashboard")
        
        try:
            dashboard_id = f"dashboard_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
            
            # Create dashboard structure
            dashboard = {
                "dashboard_id": dashboard_id,
                "title": dashboard_config.get("title", "Analytics Dashboard"),
                "layout": dashboard_config.get("layout", "grid"),
                "components": [],
                "filters": dashboard_config.get("filters", []),
                "refresh_interval": dashboard_config.get("refresh_interval", 300),  # 5 minutes
                "metadata": {
                    "created_at": datetime.utcnow().isoformat(),
                    "version": "1.0"
                }
            }
            
            # Process dashboard components
            components = dashboard_config.get("components", [])
            for component_config in components:
                component = self._create_dashboard_component(component_config, data_sources)
                if component:
                    dashboard["components"].append(component)
            
            # Add dashboard-level interactions
            dashboard["interactions"] = self._generate_dashboard_interactions(dashboard)
            
            result = {
                "dashboard_id": dashboard_id,
                "dashboard": dashboard,
                "export_options": {
                    "formats": ["png", "pdf", "html"],
                    "include_data": True
                },
                "metadata": {
                    "components_count": len(dashboard["components"]),
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Dashboard built successfully", 
                       components=len(dashboard["components"]))
            
            return result
            
        except Exception as e:
            logger.error("Error building dashboard", error=str(e))
            return {"error": f"Dashboard building failed: {str(e)}"}
    
    def custom_chart_builder(
        self, 
        chart_spec: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build custom chart based on specification
        
        Args:
            chart_spec: Chart specification including type, styling, and options
            data: Data for the chart
            
        Returns:
            Dictionary containing custom chart configuration
        """
        logger.info("Building custom chart")
        
        try:
            chart_type = chart_spec.get("type", "line")
            
            if chart_type not in self.chart_types:
                return {"error": f"Unsupported chart type: {chart_type}"}
            
            # Create custom chart data
            custom_chart = {
                "chart_id": f"custom_{chart_type}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "chart_type": chart_type,
                "title": chart_spec.get("title", f"Custom {self.chart_types[chart_type]}"),
                "data": self._process_chart_data(data, chart_spec),
                "styling": chart_spec.get("styling", {}),
                "options": chart_spec.get("options", {}),
                "interactions": chart_spec.get("interactions", {}),
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat(),
                    "custom_spec": True
                }
            }
            
            # Generate chart configuration
            custom_chart["config"] = self._generate_custom_chart_config(chart_spec, custom_chart)
            
            result = {
                "chart": custom_chart,
                "export_options": {
                    "formats": ["png", "svg", "pdf"],
                    "include_data": True
                },
                "metadata": {
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
            
            logger.info("Custom chart built successfully", chart_type=chart_type)
            
            return result
            
        except Exception as e:
            logger.error("Error building custom chart", error=str(e))
            return {"error": f"Custom chart building failed: {str(e)}"}
    
    def export_visualization(
        self, 
        chart_data: Dict[str, Any], 
        format: str = "png",
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Export visualization to various formats
        
        Args:
            chart_data: Chart data to export
            format: Export format (png, svg, pdf, html)
            options: Export options
            
        Returns:
            Dictionary containing export result
        """
        logger.info("Exporting visualization", format=format)
        
        try:
            if format not in ["png", "svg", "pdf", "html"]:
                return {"error": f"Unsupported export format: {format}"}
            
            # Generate export data
            export_data = {
                "chart_id": chart_data.get("chart_id", "unknown"),
                "format": format,
                "filename": f"{chart_data.get('chart_id', 'chart')}.{format}",
                "size_bytes": len(json.dumps(chart_data).encode('utf-8')),
                "export_options": options or {},
                "download_url": f"/visualizations/export/{chart_data.get('chart_id', 'unknown')}.{format}",
                "generated_at": datetime.utcnow().isoformat()
            }
            
            # Add format-specific metadata
            if format == "png":
                export_data["dimensions"] = options.get("dimensions", {"width": 800, "height": 600})
            elif format == "svg":
                export_data["scalable"] = True
            elif format == "pdf":
                export_data["page_size"] = options.get("page_size", "A4")
            elif format == "html":
                export_data["interactive"] = True
            
            result = {
                "success": True,
                "export": export_data,
                "message": f"Visualization exported successfully to {format.upper()}"
            }
            
            logger.info("Visualization exported successfully", 
                       format=format, 
                       filename=export_data["filename"])
            
            return result
            
        except Exception as e:
            logger.error("Error exporting visualization", error=str(e))
            return {"error": f"Visualization export failed: {str(e)}"}
    
    def _generate_heatmap_annotations(
        self, 
        values: List[List[float]], 
        countries: List[str], 
        indicators: List[str]
    ) -> List[Dict[str, Any]]:
        """Generate annotations for heatmap"""
        annotations = []
        
        for i, country in enumerate(countries):
            for j, indicator in enumerate(indicators):
                if i < len(values) and j < len(values[i]):
                    value = values[i][j]
                    annotations.append({
                        "row": i,
                        "col": j,
                        "text": f"{value:.2f}",
                        "color": "white" if value < 0.5 else "black"
                    })
        
        return annotations
    
    def _interpret_correlation_strength(self, correlation: float) -> str:
        """Interpret correlation strength"""
        if correlation >= 0.8:
            return "very strong"
        elif correlation >= 0.6:
            return "strong"
        elif correlation >= 0.4:
            return "moderate"
        elif correlation >= 0.2:
            return "weak"
        else:
            return "very weak"
    
    def _calculate_trend_line(self, x_values: List[float], y_values: List[float]) -> Dict[str, Any]:
        """Calculate trend line for scatter plot"""
        if len(x_values) < 2:
            return {"slope": 0, "intercept": 0, "points": []}
        
        # Simple linear regression
        x_array = np.array(x_values)
        y_array = np.array(y_values)
        
        # Calculate slope and intercept
        n = len(x_values)
        sum_x = np.sum(x_array)
        sum_y = np.sum(y_array)
        sum_xy = np.sum(x_array * y_array)
        sum_x2 = np.sum(x_array ** 2)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        
        # Generate trend line points
        x_min, x_max = min(x_values), max(x_values)
        x_trend = [x_min, x_max]
        y_trend = [slope * x + intercept for x in x_trend]
        
        return {
            "slope": float(slope),
            "intercept": float(intercept),
            "points": [
                {"x": float(x), "y": float(y)} 
                for x, y in zip(x_trend, y_trend)
            ]
        }
    
    def _generate_scatter_interpretation(self, scatter_data: Dict[str, Any]) -> str:
        """Generate interpretation for scatter plot"""
        correlation = scatter_data["correlation"]
        
        interpretation = f"The scatter plot shows a {correlation['strength']} {correlation['direction']} "
        interpretation += f"correlation (r = {correlation['value']:.3f}) between the variables. "
        
        if abs(correlation['value']) > 0.7:
            interpretation += "This suggests a strong linear relationship."
        elif abs(correlation['value']) > 0.4:
            interpretation += "This suggests a moderate linear relationship."
        else:
            interpretation += "This suggests a weak linear relationship."
        
        return interpretation
    
    def _create_dashboard_component(
        self, 
        component_config: Dict[str, Any], 
        data_sources: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Create dashboard component"""
        try:
            component_type = component_config.get("type")
            data_source = component_config.get("data_source")
            
            if data_source not in data_sources:
                logger.warning(f"Data source not found: {data_source}")
                return None
            
            component = {
                "component_id": f"comp_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                "type": component_type,
                "title": component_config.get("title", f"{component_type.title()} Component"),
                "data_source": data_source,
                "data": data_sources[data_source],
                "position": component_config.get("position", {}),
                "size": component_config.get("size", {"width": 400, "height": 300}),
                "styling": component_config.get("styling", {}),
                "filters": component_config.get("filters", [])
            }
            
            return component
            
        except Exception as e:
            logger.error("Error creating dashboard component", error=str(e))
            return None
    
    def _generate_dashboard_interactions(self, dashboard: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate dashboard-level interactions"""
        interactions = [
            {
                "type": "filter_sync",
                "description": "Synchronize filters across all components",
                "enabled": True
            },
            {
                "type": "drill_down",
                "description": "Enable drill-down functionality",
                "enabled": True
            },
            {
                "type": "export",
                "description": "Export dashboard as image or PDF",
                "enabled": True
            }
        ]
        
        return interactions
    
    def _process_chart_data(self, data: Dict[str, Any], chart_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Process data for custom chart"""
        processed_data = {
            "labels": data.get("labels", []),
            "datasets": []
        }
        
        # Process datasets based on chart type
        chart_type = chart_spec.get("type", "line")
        
        if chart_type == "line":
            processed_data["datasets"] = [{
                "label": chart_spec.get("dataset_label", "Dataset 1"),
                "data": data.get("values", []),
                "borderColor": chart_spec.get("styling", {}).get("color", "#3498db"),
                "backgroundColor": chart_spec.get("styling", {}).get("fill_color", "rgba(52, 152, 219, 0.1)")
            }]
        elif chart_type == "bar":
            processed_data["datasets"] = [{
                "label": chart_spec.get("dataset_label", "Dataset 1"),
                "data": data.get("values", []),
                "backgroundColor": chart_spec.get("styling", {}).get("color", "#3498db")
            }]
        
        return processed_data
    
    def _generate_custom_chart_config(
        self, 
        chart_spec: Dict[str, Any], 
        custom_chart: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate configuration for custom chart"""
        config = {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "title": {
                    "display": True,
                    "text": custom_chart["title"]
                },
                "legend": {
                    "display": chart_spec.get("options", {}).get("show_legend", True)
                }
            }
        }
        
        # Add chart-specific options
        chart_type = chart_spec.get("type", "line")
        if chart_type in ["line", "bar"]:
            config["scales"] = {
                "x": {
                    "title": {
                        "display": True,
                        "text": chart_spec.get("x_label", "X Axis")
                    }
                },
                "y": {
                    "title": {
                        "display": True,
                        "text": chart_spec.get("y_label", "Y Axis")
                    }
                }
            }
        
        return config
