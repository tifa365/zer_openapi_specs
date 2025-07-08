#!/bin/bash
# Run Swagger UI to preview OpenAPI documentation

echo "Starting Swagger UI..."
echo "The documentation will be available at http://localhost:8080"
echo ""

# Stop any existing container
docker stop swagger-ui 2>/dev/null
docker rm swagger-ui 2>/dev/null

# Run Swagger UI
docker run -d --name swagger-ui \
  -p 8080:8080 \
  -e SWAGGER_JSON=/api/zer_search_openapi.yaml \
  -v $(pwd)/zer_search_openapi.yaml:/api/zer_search_openapi.yaml \
  swaggerapi/swagger-ui

echo "Swagger UI is running!"
echo "To stop: docker stop swagger-ui"
echo "To view logs: docker logs swagger-ui"