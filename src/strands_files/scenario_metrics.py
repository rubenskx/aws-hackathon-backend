from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AuditErrors(BaseModel):
    errors :str = Field(
        description="Errors/ non compliance with the guidelines or accounting standards.")
    citations : str = Field(
        description="The source/citation pertaining to the found error from the knowledge base/compliance document.")


class AuditResponse(BaseModel):
    compliance_status :int = Field(
        description="Overall percentage of compliance status with the guidelines")
    audit_errors : list[AuditErrors] = Field(
        description="List of all errors found in the financial statements")
    summaried_results : str = Field(
        description="Brief summarised results from the agent summarizing all the findings.")



class AnalystAgentResults(BaseModel):
    """Class for structuring analyst agent results"""
    analyst_agent_report: str = Field(
        description="The brief summarised results from the analyst agent")
    errors: list[str] = Field(description="List of errors in any found")


class InvestorAgentResults(BaseModel):
    """Class for structing investor agent results"""
    investor_agent_report: str = Field(
        description="The brief summarised results from the analyst agent"
    )
    financial_health: str = Field(
        description="The overall financial health of the company. Should be either of GOOD, BAD, EXCELLENT, SATISFACTORY, UNSATISFACTORY."
    )
    positive_indicators: list[str] = Field(
        description="Positive indicators of financial health based on financial statements and latest news."
    )
    areas_of_concerns: list[str] = Field(
        description="Areas of concern of financial health based on financial statements and latest news."
    )


class ReportModel(BaseModel):
    auditor_results: AuditErrors = Field(
        description="Overall auditor agent results")
    analyst_agent_results: AnalystAgentResults = Field(
        description="Overall analyst agent results")
    investor_agent_results: InvestorAgentResults = Field(
        description="Overall investor agent results")


