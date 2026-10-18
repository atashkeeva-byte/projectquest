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

class SaveError(Exception):
    """Save error"""
class InvalidSaveError(SaveError):
    """Invalid save data"""

class LoadError(Exception):
    """Load error"""
class InvalidLoadError(LoadError):
    """Invalid load data"""
class InvalidNameError(LoadError):
    """Name error"""
class InvalidLoadLocationError(LoadError):
    """Location error"""
class InvalidLoadItemError(LoadError):
    """Item error"""