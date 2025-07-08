#!/usr/bin/env python3
"""
Example: Running specific Schemathesis test scenarios
"""
import schemathesis

# Load the OpenAPI schema
schema = schemathesis.from_path("zer_search_openapi.yaml")
schema.base_url = "https://zer.bzst.de/api/v1"

# Test specific edge cases
@schema.parametrize()
def test_api_edge_cases(case):
    """Test API with edge cases"""
    # Schemathesis will generate test cases like:
    # - plz="00000" (min valid postal code)
    # - plz="99999" (max valid postal code)  
    # - plz="" (empty string)
    # - zwecke=0 (boundary value)
    # - zwecke=-1 (negative)
    # - kombiniert alle Parameter
    
    response = case.call()
    case.validate_response(response)

# Run focused tests
if __name__ == "__main__":
    # Test with specific examples
    import requests
    
    print("Testing specific edge cases:")
    print("-" * 40)
    
    # Test 1: Empty postal code
    response = requests.get("https://zer.bzst.de/api/v1/search?plz=")
    print(f"Empty postal code: Status {response.status_code}")
    
    # Test 2: Invalid postal code format
    response = requests.get("https://zer.bzst.de/api/v1/search?plz=ABCDE")
    print(f"Invalid postal code: Status {response.status_code}")
    
    # Test 3: Negative zwecke
    response = requests.get("https://zer.bzst.de/api/v1/search?zwecke=-1")
    print(f"Negative zwecke: Status {response.status_code}")
    
    # Test 4: Very large page number
    response = requests.get("https://zer.bzst.de/api/v1/search?page=999999")
    print(f"Large page number: Status {response.status_code}")
    
    # Test 5: Combined parameters
    response = requests.get("https://zer.bzst.de/api/v1/search?plz=10115&bundesland=BE&zwecke=57")
    print(f"Combined parameters: Status {response.status_code}")
    
    print("\nNote: Schemathesis would generate hundreds of such test cases automatically!")