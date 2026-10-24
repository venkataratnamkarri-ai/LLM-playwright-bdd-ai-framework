"""
Self-Healing Locator using Cohere AI.
When a Playwright locator fails due to UI drift, analyzes current DOM HTML and suggests a healed locator.
"""

from ai.cohere_helper import CohereHelper

class LocatorHealer:
    def __init__(self):
        self.ai = CohereHelper()

    def suggest_locator(self, failed_locator: str, html: str) -> str:
        # Keep HTML snippet concise for fast processing
        html_snippet = html[:4000] if len(html) > 4000 else html
        prompt = f"""
The following Playwright locator failed to find an element:
{failed_locator}

Analyze the DOM HTML and suggest the most resilient replacement Playwright locator (CSS or text selector):
HTML:
{html_snippet}

Return ONLY the locator string, without explanation or backticks.
"""
        healed = self.ai.ask(prompt).strip().strip("`'\"")
        return healed
