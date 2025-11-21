"""
Legal rule checker module.
Validates compliance with 6 key legal document requirements.
"""

from typing import List, Dict, Any
from core.vector_store import VectorStoreManager
from core.rag_pipeline import RAGPipeline
from app.schemas import RuleResult
import logging

logger = logging.getLogger(__name__)


class RuleChecker:
    """Validates legal document compliance with standard rules."""
    
    # Define the 6 legal rules
    RULES = [
        {
            "id": 1,
            "name": "Key Terms Defined",
            "description": "Document contains clear definitions of key terms",
            "query": "definitions, defined terms, interpretation, meaning, glossary"
        },
        {
            "id": 2,
            "name": "Eligibility Criteria Present",
            "description": "Document specifies eligibility criteria or requirements",
            "query": "eligibility, eligible, qualified, requirements, criteria, entitled"
        },
        {
            "id": 3,
            "name": "Authority Responsibilities Specified",
            "description": "Document defines authority or agency responsibilities",
            "query": "authority, agency, minister, department, responsible, administer, powers, duties"
        },
        {
            "id": 4,
            "name": "Penalties/Enforcement Exist",
            "description": "Document includes penalties or enforcement mechanisms",
            "query": "penalty, fine, sanction, enforcement, violation, offense, prosecution, punishment"
        },
        {
            "id": 5,
            "name": "Payment/Entitlement Structure",
            "description": "Document describes payment or entitlement structure",
            "query": "payment, amount, benefit, entitlement, compensation, calculation, rate"
        },
        {
            "id": 6,
            "name": "Reporting/Record-keeping",
            "description": "Document includes reporting or record-keeping requirements",
            "query": "record, report, maintain, documentation, register, keep, filing, submit"
        }
    ]
    
    def __init__(self, vector_store: VectorStoreManager):
        """
        Initialize the rule checker.
        
        Args:
            vector_store: VectorStoreManager instance
        """
        self.vector_store = vector_store
        self.rag_pipeline = RAGPipeline(vector_store)
    
    def check_all_rules(self) -> List[RuleResult]:
        """
        Check all legal rules against the document.
        
        Returns:
            List of RuleResult objects
        """
        logger.info("Checking all legal rules")
        results = []
        
        for rule in self.RULES:
            result = self._check_rule(rule)
            results.append(result)
        
        return results
    
    def _check_rule(self, rule: Dict[str, Any]) -> RuleResult:
        """
        Check a single rule.
        
        Args:
            rule: Rule definition dictionary
            
        Returns:
            RuleResult object
        """
        rule_name = rule["name"]
        logger.info(f"Checking rule: {rule_name}")
        
        # Search for relevant content
        query = rule["query"]
        results = self.vector_store.search(query, k=3)
        
        if not results:
            return RuleResult(
                rule=rule_name,
                status="fail",
                evidence="No relevant content found",
                confidence=0.0
            )
        
        # Extract evidence from top results
        evidence_docs = [doc for doc, score in results]
        evidence_text = self._extract_evidence(evidence_docs)
        
        # Use LLM to validate if rule is satisfied
        validation = self._validate_with_llm(rule, evidence_text)
        
        return RuleResult(
            rule=rule_name,
            status=validation["status"],
            evidence=validation["evidence"],
            confidence=validation["confidence"]
        )
    
    def _extract_evidence(self, documents: List) -> str:
        """
        Extract evidence text from documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            Combined evidence text
        """
        evidence_parts = []
        
        for doc in documents[:3]:  # Limit to top 3
            page = doc.metadata.get('page_number', 'N/A')
            section = doc.metadata.get('section_header', 'N/A')
            content = doc.page_content[:300]  # Limit length
            
            evidence_parts.append(
                f"[Page {page}, Section: {section}] {content}..."
            )
        
        return "\n\n".join(evidence_parts)
    
    def _validate_with_llm(
        self,
        rule: Dict[str, Any],
        evidence: str
    ) -> Dict[str, Any]:
        """
        Use LLM to validate if rule is satisfied.
        
        Args:
            rule: Rule definition
            evidence: Evidence text
            
        Returns:
            Validation result dictionary
        """
        prompt = f"""You are a legal compliance analyst. Evaluate whether the following rule is satisfied based on the evidence provided.

Rule: {rule['name']}
Description: {rule['description']}

Evidence from Document:
{evidence}

Determine:
1. Is this rule SATISFIED (pass) or NOT SATISFIED (fail)?
2. What specific evidence supports your determination?
3. What is your confidence level (0-100)?

Respond in JSON format:
{{
    "status": "pass" or "fail",
    "evidence": "brief quote or reference from the evidence",
    "confidence": <number between 0 and 100>,
    "reasoning": "brief explanation"
}}

Respond ONLY with valid JSON."""
        
        try:
            response = self.rag_pipeline._call_llm(prompt)
            result = self.rag_pipeline._parse_llm_response(response)
            
            return {
                "status": result.get("status", "fail"),
                "evidence": result.get("evidence", "No evidence provided"),
                "confidence": float(result.get("confidence", 0.0))
            }
            
        except Exception as e:
            logger.error(f"Error validating rule: {str(e)}")
            return {
                "status": "fail",
                "evidence": f"Validation error: {str(e)}",
                "confidence": 0.0
            }
    
    def get_compliance_summary(self, rule_results: List[RuleResult]) -> Dict[str, Any]:
        """
        Get summary of compliance check results.
        
        Args:
            rule_results: List of RuleResult objects
            
        Returns:
            Summary dictionary
        """
        total_rules = len(rule_results)
        passed_rules = sum(1 for r in rule_results if r.status == "pass")
        failed_rules = total_rules - passed_rules
        
        avg_confidence = sum(r.confidence for r in rule_results) / total_rules if total_rules > 0 else 0.0
        
        return {
            "total_rules": total_rules,
            "passed": passed_rules,
            "failed": failed_rules,
            "pass_rate": (passed_rules / total_rules * 100) if total_rules > 0 else 0.0,
            "average_confidence": avg_confidence,
            "overall_status": "compliant" if passed_rules >= 4 else "non-compliant"
        }
