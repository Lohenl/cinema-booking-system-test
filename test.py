import sys
import os
from unittest.runner import TextTestRunner
from unittest.loader import TestLoader

def run_tests():
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    loader = TestLoader()
    
    # Discover all tests in directory
    test_dir = os.path.join(project_root, 'tests')
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Configure the test runner
    runner = TextTestRunner(
        verbosity=2,  # Detailed output
        failfast=False,  # Don't stop on first failure
        buffer=False   # Show print statements from tests
    )
    
    # Run Tests
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests())