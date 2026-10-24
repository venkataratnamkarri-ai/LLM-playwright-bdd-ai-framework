"""
AI Test Data Generator using Cohere ClientV2.
Generates realistic, synthetic single-customer checkout records in strict JSON format.
"""

import json
import re
from ai.cohere_helper import CohereHelper

class CustomerDataGenerator:
    def __init__(self):
        self.ai = CohereHelper()

    def generate_customer(self) -> dict:
        prompt = """
        Generate ONLY ONE realistic synthetic customer for test automation checkout.

        Return ONLY valid JSON matching this schema:
        {
         "name": "Full Name",
         "address": "Street Address",
         "city": "City Name",
         "state": "State Name",
         "zip": "12345",
         "card_number": "4111111111111111",
         "month": "11",
         "year": "2027",
         "card_holder": "Full Name"
        }

        Do not return arrays or extra commentary.
        """
        response = self.ai.ask(prompt)
        response = re.sub(r"```json", "", response)
        response = re.sub(r"```", "", response)

        customer = json.loads(response.strip())
        return customer
