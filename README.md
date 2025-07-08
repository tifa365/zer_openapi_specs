# ZER OpenAPI Specification

OpenAPI 3.0 specification for the **Zuwendungsempfängerregister** (ZER) search endpoint provided by the German Federal Central Tax Office (BZSt).

[![Open in Swagger UI](https://img.shields.io/badge/Open%20in-Swagger%20UI-85EA2D?logo=swagger)](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/tifa365/zer_openapi_specs/main/zer_search_openapi.yaml)

## Overview

The ZER API allows you to search for organizations that are eligible to issue tax-deductible donation receipts in Germany.

**Base URL**: `https://zer.bzst.de/api/v1`

## Quick Start

### View Documentation Online

🌐 **[Open in Swagger UI](https://petstore.swagger.io/?url=https://raw.githubusercontent.com/tifa365/zer_openapi_specs/main/zer_search_openapi.yaml)** - View and test the API directly in your browser

### View Documentation Locally

```bash
# Using Swagger UI (Docker)
docker run -p 8080:8080 \
  -e SWAGGER_JSON=/api/zer_search_openapi.yaml \
  -v $(pwd)/zer_search_openapi.yaml:/api/zer_search_openapi.yaml \
  swaggerapi/swagger-ui

# Using Redocly
npx @redocly/cli@latest preview-docs zer_search_openapi.yaml
```

Then open http://localhost:8080 in your browser.

### Test the API

```bash
# Search for organizations in Berlin
curl "https://zer.bzst.de/api/v1/search?bundesland=BE"

# Search by postal code
curl "https://zer.bzst.de/api/v1/search?plz=10115"

# Search by charity purpose (e.g., 57 = international aid)
curl "https://zer.bzst.de/api/v1/search?zwecke=57"
```

## API Testing

### Property-based Testing with Schemathesis

```bash
# Install
pip install schemathesis

# Run tests
schemathesis run zer_search_openapi.yaml \
  --url https://zer.bzst.de/api/v1 \
  --checks all
```

### Contract Testing with Dredd

```bash
# Install
npm install -g dredd

# Run tests
dredd zer_search_openapi.yaml https://zer.bzst.de/api/v1
```

## Parameters

- `label` - Filter by organization name (partial match)
- `zwecke` - Charity purpose code (e.g., 57, 901)
- `plz` - German postal code (5 digits)
- `ort` - City name
- `bundesland` - Federal state code (e.g., BE for Berlin)
- `page` - Page number (default: 1)
- `pageSize` - Results per page (default: 10, max: 100)
- `sortBy` - Sort field (default: label)
- `sortOrder` - Sort direction: asc/desc (default: asc)

## Response Format

```json
{
  "page": 1,
  "pageSize": 10,
  "totalCount": 123,
  "totalPages": 13,
  "sortBy": "label",
  "sortOrder": "asc",
  "results": [
    {
      "wid": "DE123456789",
      "label": "Organization Name",
      "url": "",
      "plz": "10115",
      "ort": "Berlin",
      "bundesland": "BE",
      "strasse": "Example Street",
      "hausnummer": "42",
      "staat": "Deutschland",
      "zwecke": [57, 901],
      "zustaendigesFinanzamt": "Berlin",
      "freistellungbescheidErteilungAm": "2023-01-01",
      "uuid": 12345
    }
  ]
}
```

## License

This OpenAPI specification is provided as-is for integration with the public ZER API.