"""
Data Provenance Tracking Service
Tracks data sources, processing steps, and maintains audit trails
"""

import json
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog
from dataclasses import dataclass, asdict
from enum import Enum

logger = structlog.get_logger()

class ProcessingStepType(Enum):
    DATA_INGESTION = "data_ingestion"
    DATA_CLEANING = "data_cleaning"
    DATA_TRANSFORMATION = "data_transformation"
    DATA_VALIDATION = "data_validation"
    DATA_AGGREGATION = "data_aggregation"
    MODEL_TRAINING = "model_training"
    SIMULATION_EXECUTION = "simulation_execution"

class DataSourceType(Enum):
    WHO_GLOBAL_HEALTH = "who_global_health"
    INTERNAL_PROCESSING = "internal_processing"

@dataclass
class DataSource:
    name: str
    url: str
    last_updated: datetime
    reliability_score: float
    coverage: List[str]
    source_type: DataSourceType
    version: str = "1.0"
    description: str = ""

@dataclass
class ProcessingStep:
    step_id: str
    description: str
    timestamp: datetime
    input_data: str
    output_data: str
    parameters: Dict[str, Any]
    step_type: ProcessingStepType
    duration_ms: int = 0
    success: bool = True
    error_message: Optional[str] = None

@dataclass
class DataTransformation:
    transformation_id: str
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    transformation_logic: str
    timestamp: datetime
    parameters: Dict[str, Any]

@dataclass
class DatasetVersion:
    version_id: str
    dataset_id: str
    version_number: str
    created_at: datetime
    created_by: str
    changes: List[str]
    data_hash: str
    size_bytes: int
    record_count: int

@dataclass
class AuditEntry:
    entry_id: str
    timestamp: datetime
    action: str
    user_id: Optional[str]
    resource_type: str
    resource_id: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None

@dataclass
class ProvenanceData:
    dataset_id: str
    original_sources: List[DataSource]
    processing_steps: List[ProcessingStep]
    transformations: List[DataTransformation]
    version_history: List[DatasetVersion]
    audit_trail: List[AuditEntry]
    created_at: datetime
    last_updated: datetime

class DataProvenanceTracker:
    """Tracks data provenance, processing history, and maintains audit trails"""
    
    def __init__(self):
        self.provenance_records = {}
        self.audit_trail = []
        
        # Initialize with known data sources
        self._initialize_data_sources()
    
    def _initialize_data_sources(self):
        """Initialize known data sources"""
        self.known_sources = {
            "who_global_health": DataSource(
                name="WHO Global Health Observatory",
                url="https://www.who.int/data/gho",
                last_updated=datetime.now(),
                reliability_score=0.95,
                coverage=["life_expectancy", "mortality", "health_workforce", "health_expenditure"],
                source_type=DataSourceType.WHO_GLOBAL_HEALTH,
                version="2024.1",
                description="WHO's comprehensive health statistics database"
            ),
        }
    
    def create_provenance_record(self, dataset_id: str, initial_sources: List[str]) -> ProvenanceData:
        """Create a new provenance record for a dataset"""
        logger.info("Creating provenance record", dataset_id=dataset_id)
        
        # Get original sources
        original_sources = [self.known_sources[source_id] for source_id in initial_sources if source_id in self.known_sources]
        
        provenance_data = ProvenanceData(
            dataset_id=dataset_id,
            original_sources=original_sources,
            processing_steps=[],
            transformations=[],
            version_history=[],
            audit_trail=[],
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        self.provenance_records[dataset_id] = provenance_data
        
        # Add audit entry
        self._add_audit_entry(
            action="provenance_record_created",
            resource_type="dataset",
            resource_id=dataset_id,
            details={"sources": initial_sources}
        )
        
        logger.info("Provenance record created", dataset_id=dataset_id, sources_count=len(original_sources))
        return provenance_data
    
    def add_processing_step(
        self, 
        dataset_id: str, 
        step_type: ProcessingStepType,
        description: str,
        input_data: str,
        output_data: str,
        parameters: Dict[str, Any],
        duration_ms: int = 0,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> ProcessingStep:
        """Add a processing step to the provenance record"""
        if dataset_id not in self.provenance_records:
            raise ValueError(f"Provenance record not found for dataset: {dataset_id}")
        
        step_id = f"{dataset_id}_{step_type.value}_{datetime.now().isoformat()}"
        
        processing_step = ProcessingStep(
            step_id=step_id,
            description=description,
            timestamp=datetime.now(),
            input_data=input_data,
            output_data=output_data,
            parameters=parameters,
            step_type=step_type,
            duration_ms=duration_ms,
            success=success,
            error_message=error_message
        )
        
        self.provenance_records[dataset_id].processing_steps.append(processing_step)
        self.provenance_records[dataset_id].last_updated = datetime.now()
        
        # Add audit entry
        self._add_audit_entry(
            action="processing_step_added",
            resource_type="dataset",
            resource_id=dataset_id,
            details={
                "step_type": step_type.value,
                "step_id": step_id,
                "success": success
            }
        )
        
        logger.info(
            "Processing step added",
            dataset_id=dataset_id,
            step_type=step_type.value,
            step_id=step_id,
            success=success
        )
        
        return processing_step
    
    def add_data_transformation(
        self,
        dataset_id: str,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        transformation_logic: str,
        parameters: Dict[str, Any]
    ) -> DataTransformation:
        """Add a data transformation to the provenance record"""
        if dataset_id not in self.provenance_records:
            raise ValueError(f"Provenance record not found for dataset: {dataset_id}")
        
        transformation_id = f"{dataset_id}_transform_{datetime.now().isoformat()}"
        
        transformation = DataTransformation(
            transformation_id=transformation_id,
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            transformation_logic=transformation_logic,
            timestamp=datetime.now(),
            parameters=parameters
        )
        
        self.provenance_records[dataset_id].transformations.append(transformation)
        self.provenance_records[dataset_id].last_updated = datetime.now()
        
        # Add audit entry
        self._add_audit_entry(
            action="transformation_added",
            resource_type="dataset",
            resource_id=dataset_id,
            details={
                "transformation_id": transformation_id,
                "name": name
            }
        )
        
        logger.info("Data transformation added", dataset_id=dataset_id, transformation_id=transformation_id)
        return transformation
    
    def create_dataset_version(
        self,
        dataset_id: str,
        version_number: str,
        created_by: str,
        changes: List[str],
        data_hash: str,
        size_bytes: int,
        record_count: int
    ) -> DatasetVersion:
        """Create a new version of a dataset"""
        if dataset_id not in self.provenance_records:
            raise ValueError(f"Provenance record not found for dataset: {dataset_id}")
        
        version_id = f"{dataset_id}_v{version_number}_{datetime.now().isoformat()}"
        
        dataset_version = DatasetVersion(
            version_id=version_id,
            dataset_id=dataset_id,
            version_number=version_number,
            created_at=datetime.now(),
            created_by=created_by,
            changes=changes,
            data_hash=data_hash,
            size_bytes=size_bytes,
            record_count=record_count
        )
        
        self.provenance_records[dataset_id].version_history.append(dataset_version)
        self.provenance_records[dataset_id].last_updated = datetime.now()
        
        # Add audit entry
        self._add_audit_entry(
            action="dataset_version_created",
            resource_type="dataset",
            resource_id=dataset_id,
            details={
                "version_id": version_id,
                "version_number": version_number,
                "created_by": created_by,
                "changes": changes
            }
        )
        
        logger.info("Dataset version created", dataset_id=dataset_id, version_id=version_id)
        return dataset_version
    
    def get_provenance_data(self, dataset_id: str) -> Optional[ProvenanceData]:
        """Get provenance data for a dataset"""
        return self.provenance_records.get(dataset_id)
    
    def get_processing_history(self, dataset_id: str) -> List[ProcessingStep]:
        """Get processing history for a dataset"""
        if dataset_id not in self.provenance_records:
            return []
        
        return self.provenance_records[dataset_id].processing_steps
    
    def get_data_lineage(self, dataset_id: str) -> Dict[str, Any]:
        """Get data lineage information for a dataset"""
        if dataset_id not in self.provenance_records:
            return {}
        
        provenance = self.provenance_records[dataset_id]
        
        lineage = {
            "dataset_id": dataset_id,
            "original_sources": [asdict(source) for source in provenance.original_sources],
            "processing_pipeline": [],
            "transformations": [asdict(transform) for transform in provenance.transformations],
            "versions": [asdict(version) for version in provenance.version_history],
            "created_at": provenance.created_at.isoformat(),
            "last_updated": provenance.last_updated.isoformat()
        }
        
        # Build processing pipeline
        for step in provenance.processing_steps:
            lineage["processing_pipeline"].append({
                "step_id": step.step_id,
                "type": step.step_type.value,
                "description": step.description,
                "timestamp": step.timestamp.isoformat(),
                "duration_ms": step.duration_ms,
                "success": step.success,
                "parameters": step.parameters
            })
        
        return lineage
    
    def export_provenance_data(self, dataset_id: str, format: str = "json") -> str:
        """Export provenance data in specified format"""
        if dataset_id not in self.provenance_records:
            raise ValueError(f"Provenance record not found for dataset: {dataset_id}")
        
        provenance = self.provenance_records[dataset_id]
        
        if format == "json":
            # Convert to JSON-serializable format
            export_data = {
                "dataset_id": provenance.dataset_id,
                "original_sources": [asdict(source) for source in provenance.original_sources],
                "processing_steps": [asdict(step) for step in provenance.processing_steps],
                "transformations": [asdict(transform) for transform in provenance.transformations],
                "version_history": [asdict(version) for version in provenance.version_history],
                "audit_trail": [asdict(entry) for entry in provenance.audit_trail],
                "created_at": provenance.created_at.isoformat(),
                "last_updated": provenance.last_updated.isoformat()
            }
            
            return json.dumps(export_data, indent=2, default=str)
        
        elif format == "csv":
            # Export as CSV (simplified version)
            lines = [f"Dataset ID,{provenance.dataset_id}"]
            lines.append(f"Created At,{provenance.created_at.isoformat()}")
            lines.append(f"Last Updated,{provenance.last_updated.isoformat()}")
            lines.append("")
            lines.append("Original Sources:")
            for source in provenance.original_sources:
                lines.append(f"{source.name},{source.url},{source.reliability_score}")
            
            lines.append("")
            lines.append("Processing Steps:")
            for step in provenance.processing_steps:
                lines.append(f"{step.step_type.value},{step.description},{step.timestamp.isoformat()},{step.success}")
            
            return "\n".join(lines)
        
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _add_audit_entry(
        self,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Dict[str, Any],
        user_id: Optional[str] = None,
        ip_address: Optional[str] = None
    ):
        """Add an entry to the audit trail"""
        entry_id = f"audit_{datetime.now().isoformat()}_{hashlib.md5(f'{action}_{resource_id}'.encode()).hexdigest()[:8]}"
        
        audit_entry = AuditEntry(
            entry_id=entry_id,
            timestamp=datetime.now(),
            action=action,
            user_id=user_id,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address
        )
        
        self.audit_trail.append(audit_entry)
        
        # Also add to dataset-specific audit trail
        if resource_type == "dataset" and resource_id in self.provenance_records:
            self.provenance_records[resource_id].audit_trail.append(audit_entry)
    
    def get_audit_trail(self, resource_type: Optional[str] = None, resource_id: Optional[str] = None) -> List[AuditEntry]:
        """Get audit trail entries"""
        if resource_type and resource_id:
            # Get dataset-specific audit trail
            if resource_id in self.provenance_records:
                return self.provenance_records[resource_id].audit_trail
            else:
                return []
        elif resource_type:
            # Filter by resource type
            return [entry for entry in self.audit_trail if entry.resource_type == resource_type]
        else:
            # Return all audit entries
            return self.audit_trail
    
    def calculate_data_hash(self, data: Any) -> str:
        """Calculate hash for data integrity verification"""
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        else:
            data_bytes = str(data).encode('utf-8')
        
        return hashlib.sha256(data_bytes).hexdigest()
    
    def verify_data_integrity(self, dataset_id: str, current_data: Any) -> bool:
        """Verify data integrity against stored hash"""
        if dataset_id not in self.provenance_records:
            return False
        
        provenance = self.provenance_records[dataset_id]
        if not provenance.version_history:
            return True  # No previous version to compare against
        
        # Get the latest version
        latest_version = provenance.version_history[-1]
        current_hash = self.calculate_data_hash(current_data)
        
        return current_hash == latest_version.data_hash
    
    def get_data_sources_summary(self) -> Dict[str, Any]:
        """Get summary of all data sources"""
        summary = {
            "total_sources": len(self.known_sources),
            "sources_by_type": {},
            "reliability_scores": [],
            "coverage_by_source": {}
        }
        
        for source_id, source in self.known_sources.items():
            source_type = source.source_type.value
            if source_type not in summary["sources_by_type"]:
                summary["sources_by_type"][source_type] = 0
            summary["sources_by_type"][source_type] += 1
            
            summary["reliability_scores"].append(source.reliability_score)
            summary["coverage_by_source"][source.name] = source.coverage
        
        if summary["reliability_scores"]:
            summary["average_reliability"] = sum(summary["reliability_scores"]) / len(summary["reliability_scores"])
        
        return summary
