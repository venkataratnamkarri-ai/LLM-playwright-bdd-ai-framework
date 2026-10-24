"""
AI Assertion Engine.
Performs semantic verification on unstructured page content to confirm business outcomes.
"""

from ai.cohere_helper import CohereHelper

class AssertionEngine:
    def __init__(self):
        self.ai = CohereHelper()

    def verify_purchase_success(self, page_content: str) -> str:
        prompt = f"""
Determine whether the flight booking completed successfully based on the page content below:
{page_content[:3000]}

If successful, return only the primary purchase confirmation message (e.g. 'Thank you for your purchase today!').
Nothing else.
"""
        return self.ai.ask(prompt)
