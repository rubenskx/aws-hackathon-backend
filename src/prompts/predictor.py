
def create_prompt(financial_statement: str):
    """Generate prompt"""
    prompt = f"""
    You are an expert financial analyst. Below are financial statements for a company in markdown format.

    INPUT: {financial_statement}

    STEPWISE PROCEDURE (must follow in order):
    1. Validate and normalize data (currency, units). Report any missing fields or assumptions used to fill gaps.
    2. Compute aggregates (Total Assets, Total Liabilities, Total Equity, EBIT, Net Income, Cash from Ops).
    3. Compute ratios for each period: Current Ratio, Quick Ratio, Debt/Equity, Interest Coverage, Gross Margin, Operating Margin, Net Margin, ROA, ROE, Asset Turnover, Inventory Turnover, Receivables Turnover, FCF and FCF Margin. Use formulas provided below.
    4. Produce YoY changes and 3-year CAGR where applicable for Revenue, EBIT, Net Income, CFO.
    5. Perform quality-of-earnings checks: compare Net Income to Cash from Ops; flag major discrepancies and nonrecurring items.
    6. Assess liquidity and solvency: flag if Current Ratio <1.2, Quick Ratio <1.0, Interest Coverage <1.5, Debt/Equity >2.0 (use these as guidelines and explain any context).
    7. Analyze profitability and efficiency: summarize whether margins are stable, improving, or deteriorating.
    8. Analyze cash-flow sustainability: is FCF sufficient to cover debt servicing and capex? Note funding sources if FCF negative.
    9. Forecast next 3 years (2025–2027) under three scenarios: Base, Upside, Downside. Use recent CAGR or specify growth rate assumption; list all assumptions. Provide projected Revenue, EBIT, Net Income, CFO, and FCF for each year of each scenario.
    10. List top 5 risks or red flags and their likely impact.
    11. Provide 3–6 actionable recommendations to improve financial health.
    12. Provide a confidence score (0–100) for the forecasts with a short justification.
    
    List these insights in proper bullet points.
    """
    return prompt