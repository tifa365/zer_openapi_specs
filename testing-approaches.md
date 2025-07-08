# OpenAPI Testing Approaches: Schemathesis vs Dredd

## Overview

Both Schemathesis and Dredd are tools for testing APIs against their OpenAPI specifications, but they use fundamentally different approaches.

## Schemathesis - Property-Based Testing

### How it works:
Schemathesis uses **property-based testing** and **fuzzing** to automatically generate test cases from your OpenAPI specification.

### Testing approach:
1. **Schema Analysis**: Reads your OpenAPI spec and understands the structure of each endpoint
2. **Test Generation**: Automatically generates test inputs based on the schema, including:
   - Valid values within specified constraints
   - Edge cases (empty strings, maximum/minimum values)
   - Invalid inputs to test error handling
   - Combinations of optional/required parameters
3. **Hypothesis Integration**: Uses the Hypothesis library to generate hundreds of test cases
4. **Negative Testing**: Specifically tries to break your API by sending:
   - Malformed data
   - Boundary values
   - Unexpected data types
   - Missing required fields

### Example test scenarios for ZER API:
- `plz` parameter: Tests with "00000", "99999", "1234", "123456" (too long), "abcde" (letters)
- `zwecke` parameter: Tests with 0, -1, 999999, null, string values
- Combined parameters: Tests all possible combinations of parameters

### Strengths:
- Finds edge cases humans might miss
- Tests error handling thoroughly
- No need to write individual test cases
- Great for security testing (fuzzing)

### Command example:
```bash
uv run schemathesis run zer_search_openapi.yaml --base-url=https://zer.bzst.de/api/v1 --checks all
```

## Dredd - Contract Testing

### How it works:
Dredd performs **contract testing** by validating that the actual API responses match the OpenAPI specification exactly.

### Testing approach:
1. **Example Extraction**: Reads example requests/responses from your OpenAPI spec
2. **Request Execution**: Sends the example requests to your API
3. **Response Validation**: Compares actual responses against the spec:
   - Correct status codes
   - Required fields present
   - Data types match specification
   - Response structure matches schema
4. **Contract Verification**: Ensures the implementation matches the documentation

### Example validations for ZER API:
- Verifies response contains `data` array with organization objects
- Checks each organization has required fields (name, address, etc.)
- Validates pagination metadata structure
- Ensures error responses match documented formats

### Strengths:
- Ensures API implementation matches documentation
- Great for regression testing
- Validates the "happy path" thoroughly
- Good for API versioning and backwards compatibility

### Command example:
```bash
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1
```

## Key Differences

| Aspect | Schemathesis | Dredd |
|--------|--------------|-------|
| **Focus** | Breaking the API | Validating conformance |
| **Test Cases** | Generated automatically | Based on examples in spec |
| **Coverage** | Edge cases & errors | Happy path & examples |
| **Best For** | Finding bugs & security issues | Ensuring spec compliance |
| **Input Data** | Randomly generated | Predefined examples |

## Complementary Usage

These tools are most powerful when used together:

1. **Schemathesis** finds unexpected bugs and edge cases
2. **Dredd** ensures your API matches its documentation

Together, they provide comprehensive API testing coverage from both offensive (trying to break) and defensive (ensuring correctness) perspectives.

## Example Test Workflow

```bash
# 1. Run Schemathesis to find edge cases
uv run schemathesis run zer_search_openapi.yaml \
  --base-url=https://zer.bzst.de/api/v1 \
  --checks all \
  --hypothesis-max-examples=1000

# 2. Run Dredd to validate contract compliance  
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1 \
  --reporter junit \
  --output test-results.xml

# 3. Run specific property tests
uv run python -m pytest test_api_properties.py
```

## Summary

- **Schemathesis**: "What happens if I send unexpected data?"
- **Dredd**: "Does the API behave exactly as documented?"

Both tools automate different aspects of API testing, reducing manual effort while increasing test coverage and reliability.