# Deploy Gate - Deployment Quality Gates

## Overview

Deploy Gate is a policy-based deployment approval system that evaluates deployments against quality gates before they reach your environments. It integrates with CI/CD pipelines to provide automated approve/block/review decisions.

## Key Features

- **Policy Engine**: Define quality rules with severity levels
- **External Signal Fetching**: Real-time metrics from IDI service
- **CI/CD Webhooks**: GitHub, GitLab, Jenkins, ArgoCD
- **Override Workflow**: Request and approve manual exceptions
- **Deployment History**: Audit trail of all evaluations

## Quick Start

### 1. Create a Policy

```bash
curl -X POST http://localhost/api/gate/policies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Production Quality Gate",
    "description": "Strict quality checks for production",
    "environment": "production",
    "rules": [
      {
        "name": "Code Coverage",
        "type": "code_coverage_min",
        "threshold": 80,
        "severity": "CRITICAL"
      },
      {
        "name": "IDI Score",
        "type": "idi_score_max",
        "threshold": 75,
        "severity": "CRITICAL"
      },
      {
        "name": "Critical Vulnerabilities",
        "type": "critical_vulns_max",
        "threshold": 0,
        "severity": "CRITICAL"
      }
    ]
  }'
```

### 2. Evaluate a Deployment

```bash
curl -X POST http://localhost/api/gate/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "project_id": "my-project",
    "cluster_id": "prod-cluster",
    "namespace": "production",
    "release_name": "myapp",
    "chart_name": "myapp",
    "chart_version": "1.2.3",
    "commit_sha": "abc123",
    "environment": "production"
  }'
```

**Response**:
```json
{
  "evaluation_id": "eval-123",
  "decision": "APPROVED",
  "idi_score": 45,
  "policy_results": [
    {
      "policy_name": "Production Quality Gate",
      "decision": "APPROVED",
      "passed": 3,
      "failed": 0
    }
  ]
}
```

## Policy Rules

### Available Rule Types

| Rule Type | Description | Threshold |
|-----------|-------------|-----------|
| `code_coverage_min` | Minimum code coverage % | 0-100 |
| `idi_score_max` | Maximum IDI score | 0-100 |
| `critical_vulns_max` | Max critical vulnerabilities | 0-N |
| `high_vulns_max` | Max high vulnerabilities | 0-N |
| `test_pass_rate_min` | Minimum test pass rate % | 0-100 |
| `deployment_frequency_max` | Max deploys in time window | 0-N |

### Severity Levels

- **CRITICAL**: Blocks deployment
- **HIGH**: Requires manual review
- **MEDIUM**: Warning, allows deployment
- **LOW**: Informational

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy with Gate

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Evaluate Deploy Gate
        run: |
          RESULT=$(curl -X POST http://gate-service/api/gate/evaluate \
            -H "Content-Type: application/json" \
            -d '{
              "project_id": "${{ github.repository }}",
              "commit_sha": "${{ github.sha }}",
              "environment": "production"
            }')
          
          DECISION=$(echo $RESULT | jq -r '.decision')
          if [ "$DECISION" != "APPROVED" ]; then
            echo "Deploy gate blocked deployment"
            exit 1
          fi
```

### GitLab CI

```yaml
deploy:
  stage: deploy
  script:
    - |
      RESULT=$(curl -X POST http://gate-service/api/gate/evaluate \
        -H "Content-Type: application/json" \
        -d "{
          \"project_id\": \"$CI_PROJECT_PATH\",
          \"commit_sha\": \"$CI_COMMIT_SHA\",
          \"environment\": \"production\"
        }")
      
      DECISION=$(echo $RESULT | jq -r '.decision')
      [ "$DECISION" = "APPROVED" ] || exit 1
```

### Webhook Integration

See [Webhook Integration Guide](./webhooks.md) for detailed webhook setup.

## Override Workflow

### Request Override

```bash
curl -X POST http://localhost/api/gate/override \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "evaluation_id": "eval-123",
    "reason": "Hotfix for production issue #456"
  }'
```

### Approve Override

```bash
curl -X POST http://localhost/api/gate/override/approve \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "override_id": "override-789",
    "approved": true
  }'
```

## API Reference

Full API documentation: [Swagger UI](http://localhost/api/gate/swagger/index.html)

### Key Endpoints

- `POST /api/gate/evaluate` - Evaluate deployment
- `GET /api/gate/status/:id` - Get evaluation status
- `GET /api/gate/history` - List evaluations
- `POST /api/gate/policies` - Create policy
- `GET /api/gate/policies` - List policies
- `POST /api/gate/override` - Request override
- `POST /api/gate/override/approve` - Approve/reject override

## Best Practices

1. **Environment-Specific Policies**: Create different policies for dev/staging/prod
2. **Gradual Rollout**: Start with WARNING severity, then increase to CRITICAL
3. **Monitor Trends**: Track evaluation history to identify patterns
4. **Document Overrides**: Always provide clear reasons for overrides
5. **Automate Integration**: Use webhooks for automatic evaluation

## Troubleshooting

### Evaluation Fails with "No Policies Found"

Ensure you have created at least one policy for the target environment:

```bash
curl http://localhost/api/gate/policies | jq '.[] | select(.environment == "production")'
```

### IDI Score Always Returns 0

Check that IDI service is running and `IDI_SERVICE_URL` is configured:

```bash
curl http://localhost/api/idi/score
```

### Webhook Not Triggering

Verify webhook secret and URL configuration in your CI/CD platform. Check gate-service logs:

```bash
docker-compose logs gate-service | grep webhook
```

## Configuration

Environment variables for gate-service:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/netpin
REDIS_URL=redis://localhost:6379
AUTH_SERVICE_URL=http://auth-service:8000
IDI_SERVICE_URL=http://discovery-service:8001
IDI_THRESHOLD=75  # Max IDI score before MANUAL_REVIEW
ENVIRONMENT=production
PORT=8000
```

## Further Reading

- [Webhook Integration Guide](./webhooks.md)
- [Policy Configuration Reference](../api/gate-policies.md)
- [API Documentation](http://localhost/api/gate/swagger/index.html)
