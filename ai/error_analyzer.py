"""
AI Automated Root-Cause Failure Analyzer.
Upon test failure, parses the Playwright exception and DOM state to diagnose:
1. Root Cause
2. Probable Reason
3. Fix Recommendation
"""

from ai.cohere_helper import CohereHelper

class ErrorAnalyzer:
    def __init__(self):
        self.ai = CohereHelper()

    def analyze(self, error: str, page_content: str) -> str:
        prompt = f"""
Analyze this Playwright automation test failure:

ERROR:
{error}

CURRENT PAGE CONTENT:
{page_content[:2500]}

Provide structured diagnosis:
1. Root Cause
2. Probable Reason
3. Fix Recommendation
"""
        return self.ai.ask(prompt)
