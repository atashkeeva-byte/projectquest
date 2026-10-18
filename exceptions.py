class ScenarioError(Exception):
    """Scenario errors"""

class MissingStartError(ScenarioError):
    """No starting location"""
class InvalidLocationError(ScenarioError):
    """Invalid location"""
class InvalidExitError(ScenarioError):
    """Invalid exit"""
class InvalidItemError(ScenarioError):
    """Invalid item"""
