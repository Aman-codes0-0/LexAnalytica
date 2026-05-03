class NeuroSymbolicEngine:
    """
    A lightweight forward-chaining logic engine for legal reasoning.
    It evaluates extracted facts (entities) against predefined legal rules.
    """
    def __init__(self):
        # Define a simple ruleset.
        # In a real system, these would be loaded from a database or DSL.
        self.rules = [
            {
                "id": "RULE_1_FRAUD",
                "condition": lambda facts: ("Fraud" in facts.get("law_sections", []) or "420" in facts.get("law_sections", [])) and len(facts.get("persons", [])) > 0,
                "conclusion": "Potential Fraud Charge identified against extracted persons. Requires immediate compliance review.",
                "severity": "HIGH"
            },
            {
                "id": "RULE_2_NDA_BREACH",
                "condition": lambda facts: ("NDA" in facts.get("organizations", []) or "Confidentiality" in facts.get("organizations", [])) and len(facts.get("persons", [])) > 0,
                "conclusion": "Non-Disclosure Agreement (NDA) context detected. Flagging persons for confidentiality clearance.",
                "severity": "MEDIUM"
            },
            {
                "id": "RULE_3_CORPORATE_DISPUTE",
                "condition": lambda facts: len(facts.get("organizations", [])) >= 2 and len(facts.get("law_sections", [])) > 0,
                "conclusion": "Multiple organizations identified alongside legal sections. Likely a corporate dispute or multi-party contract.",
                "severity": "INFO"
            }
        ]

    def evaluate(self, facts: dict) -> list:
        """
        Evaluate a set of facts (extracted entities) against all rules.
        Returns a list of triggered conclusions.
        """
        results = []
        for rule in self.rules:
            try:
                # Safely evaluate condition
                if rule["condition"](facts):
                    results.append({
                        "rule_id": rule["id"],
                        "conclusion": rule["conclusion"],
                        "severity": rule["severity"]
                    })
            except Exception as e:
                print(f"[ERROR] Rule {rule['id']} failed to evaluate: {e}")
                
        return results

# Global singleton
logic_engine = NeuroSymbolicEngine()
