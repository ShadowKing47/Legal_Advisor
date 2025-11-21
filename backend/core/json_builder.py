"""
JSON report builder module.
Assembles final analysis reports from all processing components.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from app.schemas import RuleResult
import logging

logger = logging.getLogger(__name__)


class JSONBuilder:
    """Builds structured JSON reports from analysis results."""
    
    def __init__(self, output_dir: str):
        """
        Initialize the JSON builder.
        
        Args:
            output_dir: Directory to save JSON reports
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def build_summary_json(
        self,
        summary_data: Dict[str, Any],
        document_name: str
    ) -> str:
        """
        Build summary JSON file.
        
        Args:
            summary_data: Summary information
            document_name: Name of the document
            
        Returns:
            Path to saved JSON file
        """
        output = {
            "document_name": document_name,
            "generated_at": datetime.now().isoformat(),
            "summary": summary_data
        }
        
        file_path = self.output_dir / f"{document_name}_summary.json"
        self._save_json(output, file_path)
        
        logger.info(f"Saved summary JSON: {file_path}")
        return str(file_path)
    
    def build_sections_json(
        self,
        sections_data: Dict[str, Any],
        document_name: str
    ) -> str:
        """
        Build sections JSON file.
        
        Args:
            sections_data: Extracted sections by category
            document_name: Name of the document
            
        Returns:
            Path to saved JSON file
        """
        output = {
            "document_name": document_name,
            "generated_at": datetime.now().isoformat(),
            "sections": sections_data
        }
        
        file_path = self.output_dir / f"{document_name}_sections.json"
        self._save_json(output, file_path)
        
        logger.info(f"Saved sections JSON: {file_path}")
        return str(file_path)
    
    def build_rule_checks_json(
        self,
        rule_results: List[RuleResult],
        document_name: str
    ) -> str:
        """
        Build rule checks JSON file.
        
        Args:
            rule_results: List of rule check results
            document_name: Name of the document
            
        Returns:
            Path to saved JSON file
        """
        # Convert RuleResult objects to dictionaries
        rules_data = [
            {
                "rule": r.rule,
                "status": r.status,
                "evidence": r.evidence,
                "confidence": r.confidence
            }
            for r in rule_results
        ]
        
        # Calculate summary statistics
        total = len(rule_results)
        passed = sum(1 for r in rule_results if r.status == "pass")
        
        output = {
            "document_name": document_name,
            "generated_at": datetime.now().isoformat(),
            "rule_checks": rules_data,
            "summary": {
                "total_rules": total,
                "passed": passed,
                "failed": total - passed,
                "pass_rate": (passed / total * 100) if total > 0 else 0.0
            }
        }
        
        file_path = self.output_dir / f"{document_name}_rule_checks.json"
        self._save_json(output, file_path)
        
        logger.info(f"Saved rule checks JSON: {file_path}")
        return str(file_path)
    
    def build_final_report(
        self,
        document_name: str,
        summary_data: Dict[str, Any],
        sections_data: Dict[str, Any],
        rule_results: List[RuleResult],
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Build comprehensive final report JSON.
        
        Args:
            document_name: Name of the document
            summary_data: Document summary
            sections_data: Extracted sections
            rule_results: Rule check results
            metadata: Optional additional metadata
            
        Returns:
            Path to saved JSON file
        """
        # Convert rule results to dictionaries
        rules_data = [
            {
                "rule": r.rule,
                "status": r.status,
                "evidence": r.evidence,
                "confidence": r.confidence
            }
            for r in rule_results
        ]
        
        # Calculate compliance summary
        total_rules = len(rule_results)
        passed_rules = sum(1 for r in rule_results if r.status == "pass")
        
        # Build comprehensive report
        report = {
            "document_name": document_name,
            "generated_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            
            "summary": summary_data,
            
            "sections": sections_data,
            
            "rule_checks": {
                "results": rules_data,
                "summary": {
                    "total_rules": total_rules,
                    "passed": passed_rules,
                    "failed": total_rules - passed_rules,
                    "pass_rate": (passed_rules / total_rules * 100) if total_rules > 0 else 0.0,
                    "compliance_status": "compliant" if passed_rules >= 4 else "non-compliant"
                }
            },
            
            "analysis_metadata": {
                "categories_analyzed": list(sections_data.keys()) if sections_data else [],
                "total_categories": len(sections_data) if sections_data else 0,
                "report_version": "1.0"
            }
        }
        
        file_path = self.output_dir / f"{document_name}_final_report.json"
        self._save_json(report, file_path)
        
        logger.info(f"Saved final report JSON: {file_path}")
        return str(file_path)
    
    def _save_json(self, data: Dict[str, Any], file_path: Path) -> None:
        """
        Save data as JSON file.
        
        Args:
            data: Data to save
            file_path: Path to save to
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_report(self, file_path: str) -> Dict[str, Any]:
        """
        Load a JSON report.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Loaded data
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


# Convenience function
def create_final_report(
    document_name: str,
    summary_data: Dict[str, Any],
    sections_data: Dict[str, Any],
    rule_results: List[RuleResult],
    output_dir: str,
    metadata: Dict[str, Any] = None
) -> str:
    """
    Create a final report JSON file.
    
    Args:
        document_name: Name of the document
        summary_data: Document summary
        sections_data: Extracted sections
        rule_results: Rule check results
        output_dir: Output directory
        metadata: Optional metadata
        
    Returns:
        Path to saved report
    """
    builder = JSONBuilder(output_dir)
    return builder.build_final_report(
        document_name,
        summary_data,
        sections_data,
        rule_results,
        metadata
    )
