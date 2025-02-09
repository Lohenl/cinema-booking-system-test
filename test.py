import sys
import os
from unittest.runner import TextTestRunner
from unittest.loader import TestLoader

def run_tests():
    # Add the project root directory to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    # Create a test loader
    loader = TestLoader()
    
    # Discover all tests in the 'tests' directory
    test_dir = os.path.join(project_root, 'tests')
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Configure the test runner
    runner = TextTestRunner(
        verbosity=2,  # Detailed output
        failfast=False,  # Don't stop on first failure
        buffer=False   # Show print statements from tests
    )
    
    # Run the tests and get the results
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())