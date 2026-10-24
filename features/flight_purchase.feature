Feature: BlazeDemo Flight Purchase with Autonomous AI Modules
  Scenario: Purchase the cheapest flight with AI synthetic test data and AI assertions
    Given I open the BlazeDemo flight search
    When I search for flights from Paris to New York
    And I select the cheapest available flight
    And I complete the purchase with Cohere generated customer details
    Then the purchase confirmation is displayed
    And the order ID is returned
