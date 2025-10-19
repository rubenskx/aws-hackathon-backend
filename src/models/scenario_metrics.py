from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AuditorAgentResults(BaseModel):
    """Class for structuring the auditor agent results"""
    auditor_agent_report: str = Field(
        description="The brief summaried results from the auditor agent")
    citations: str = Field(
        description="Citations extracted from Knowledge Base")
    errors: list[str] = Field(
        description="The list of errors if any in the audit report")


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


class ReportModel(BaseModel):
    auditor_results: AuditorAgentResults = Field(
        description="Overall auditor agent results")
    analyst_agent_results: AnalystAgentResults = Field(
        description="Overall analyst agent results")
    investor_agent_results: InvestorAgentResults = Field(
        description="Overall investor agent results")
