#!/bin/bash
# Preview OpenAPI documentation with Redocly

echo "Starting Redocly API documentation preview..."
echo "The documentation will be available at http://127.0.0.1:8080"
echo "Press Ctrl+C to stop the server"
echo ""

npx @redocly/cli@latest preview-docs zer_search_openapi.yaml