# Infrastructure Debt Index (IDI) - Analytics Guide

## Overview

The Infrastructure Debt Index (IDI) is a comprehensive scoring system (0-100) that measures infrastructure health across five key dimensions. A lower score indicates better infrastructure health.

## IDI Dimensions

### 1. Security (25%)
- Vulnerability count and severity
- Exposed secrets and credentials
- RBAC misconfigurations
- Network policy gaps

### 2. Performance (20%)
- Resource over-provisioning
- Resource under-provisioning
- Missing resource limits/requests
- Inefficient architectures

### 3. Compliance (20%)
- CIS Kubernetes Benchmark violations
- CIS AWS Benchmark violations
- HIPAA, SOC2, PCI-DSS violations
- Industry best practices

### 4. Cost (20%)
- Idle resources
- Over-provisioned infrastructure
- Unused volumes and snapshots
- Expensive instance types

### 5. Operational (15%)
- Missing health checks
- No monitoring/logging
- Manual processes
- Documentation gaps

## Quick Start

### Get Current IDI Score

```bash
curl http://localhost/api/idi/score
```

**Response**:
```json
{
  "overall_score": 45.2,
  "grade": "B",
  "timestamp": "2026-02-02T14:00:00Z",
  "dimensions": {
    "security": 38.5,
    "performance": 52.0,
    "compliance": 41.2,
    "cost": 48.9,
    "operational": 45.0
  },
  "total_issues": 127,
  "critical_issues": 3
}
```

### Get Detailed Breakdown

```bash
curl http://localhost/api/idi/breakdown
```

### Get Historical Trend

```bash
curl "http://localhost/api/idi/trend?days=30"
```

**Response**:
```json
{
  "scores": [
    { "timestamp": "2026-01-03T00:00:00Z", "score": 52.1 },
    { "timestamp": "2026-01-10T00:00:00Z", "score": 49.8 },
    { "timestamp": "2026-01-17T00:00:00Z", "score": 47.2 },
    { "timestamp": "2026-01-24T00:00:00Z", "score": 45.2 }
  ],
  "trend": "improving",
  "change_percent": -13.2
}
```

## Understanding Your Score

### Grade Scale

| Score Range | Grade | Status |
|-------------|-------|--------|
| 0-20 | A | Excellent - Minimal debt |
| 21-40 | B | Good - Some room for improvement |
| 41-60 | C | Fair - Action recommended |
| 61-80 | D | Poor - Immediate attention needed |
| 81-100 | F | Critical - Severe issues |

### Priority Actions by Grade

**Grade C or below**: Review critical and high-severity findings immediately

**Grade B**: Schedule remediation for medium-severity findings

**Grade A**: Maintain current practices, monitor for new issues

## Compliance Scanning

### Supported Frameworks

- **CIS Kubernetes Benchmark v1.8**
- **CIS AWS Foundations Benchmark v1.4**
- **HIPAA** (Health Insurance Portability and Accountability Act)
- **SOC 2** (Service Organization Control 2)
- **PCI-DSS** (Payment Card Industry Data Security Standard)

### Run Compliance Scan

```bash
curl -X POST http://localhost/api/compliance/run \
  -H "Content-Type: application/json" \
  -d '{
    "frameworks": ["cis-kubernetes", "cis-aws", "soc2"]
  }'
```

### Get Compliance Results

```bash
curl http://localhost/api/compliance/results
```

**Response**:
```json
{
  "results": [
    {
      "framework": "cis-kubernetes",
      "total_controls": 157,
      "passed": 134,
      "failed": 18,
      "skipped": 5,
      "score": 88.5,
      "status": "PASS"
    },
    {
      "framework": "soc2",
      "total_controls": 42,
      "passed": 35,
      "failed": 7,
      "score": 83.3,
      "status": "FAIL"
    }
  ]
}
```

### Get Detailed Findings

```bash
curl "http://localhost/api/compliance/findings?severity=CRITICAL&status=FAIL"
```

## Remediation

### Get Automated Fix Scripts

```bash
curl -X POST http://localhost/api/remediation/fix \
  -H "Content-Type: application/json" \
  -d '{
    "finding_id": "finding-123"
  }'
```

**Response**:
```json
{
  "finding_id": "finding-123",
  "title": "Missing resource limits",
  "fix_type": "kubectl_patch",
  "script": "kubectl patch deployment myapp -p '{\"spec\":{\"template\":{\"spec\":{\"containers\":[{\"name\":\"app\",\"resources\":{\"limits\":{\"cpu\":\"500m\",\"memory\":\"512Mi\"}}}]}}}}'",
  "validation": "kubectl get deployment myapp -o json | jq '.spec.template.spec.containers[0].resources.limits'"
}
```

## Findings and Recommendations

### List All Findings

```bash
curl "http://localhost/api/idi/findings?severity=CRITICAL"
```

**Response**:
```json
{
  "findings": [
    {
      "id": "finding-001",
      "category": "security",
      "severity": "CRITICAL",
      "title": "Privileged container detected",
      "description": "Container 'app' in deployment 'myapp' is running with privileged: true",
      "resource": "deployment/myapp",
      "remediation": "Remove privileged flag or use securityContext with specific capabilities",
      "impact": 20
    }
  ],
  "total": 1
}
```

## Integration with Deploy Gate

IDI scores are automatically integrated into Deploy Gate evaluations:

```json
{
  "rules": [
    {
      "name": "IDI Score Threshold",
      "type": "idi_score_max",
      "threshold": 60,
      "severity": "CRITICAL"
    }
  ]
}
```

This blocks deployments when infrastructure debt exceeds acceptable levels.

## Best Practices

### 1. Regular Scanning

Schedule automated scans:
```bash
# Daily compliance scan
0 2 * * * curl -X POST http://localhost/api/compliance/run
```

### 2. Track Trends

Monitor IDI scores over time to ensure continuous improvement:
```bash
curl http://localhost/api/idi/trend?days=90
```

### 3. Prioritize by Impact

Focus on findings with highest impact scores first:
```bash
curl "http://localhost/api/idi/findings?sort=impact_desc&limit=10"
```

### 4. Automate Remediation

Use fix scripts for low-risk changes:
```bash
curl -X POST http://localhost/api/remediation/fix \
  -d '{"finding_id": "finding-123", "auto_apply": true}'
```

### 5. Set Thresholds

Configure Deploy Gate to enforce IDI thresholds:
- **Production**: IDI < 50
- **Staging**: IDI < 70
- **Development**: IDI < 90

## Dashboard Integration

The IDI Analytics page in the UI provides:

1. **Current Score Card** - Overall IDI and grade
2. **Dimension Breakdown** - Chart showing all 5 dimensions
3. **Trend Graph** - 30-day historical view
4. **Top Findings** - Critical and high-severity issues
5. **Remediation Actions** - Quick-fix recommendations

Access: `http://localhost:3000/idi-analytics`

## API Reference

Full API documentation: [Swagger UI](http://localhost/api/discovery/swagger/index.html)

### Key Endpoints

**IDI Metrics**
- `GET /api/idi/score` - Current IDI score
- `GET /api/idi/summary` - Summary with recommendations
- `GET /api/idi/breakdown` - Detailed dimension breakdown
- `GET /api/idi/trend` - Historical trends
- `POST /api/idi/calculate` - Trigger IDI recalculation

**Compliance**
- `GET /api/compliance/frameworks` - List supported frameworks
- `POST /api/compliance/run` - Run compliance scan
- `GET /api/compliance/results` - Get scan results
- `GET /api/compliance/findings` - Get detailed findings

**Remediation**
- `POST /api/remediation/fix` - Get fix script for finding

## Configuration

Environment variables for discovery-service:

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/netpin
REDIS_URL=redis://localhost:6379
AWS_REGION=us-east-1
AZURE_SUBSCRIPTION_ID=xxx
GCP_PROJECT_ID=xxx
PORT=8001
```

## Troubleshooting

### IDI Score Not Updating

Trigger manual recalculation:
```bash
curl -X POST http://localhost/api/idi/calculate
```

### Compliance  Scan Fails

Check discovery-service logs:
```bash
docker-compose logs discovery-service | grep compliance
```

### No Findings Despite High Score

Ensure resource discovery has completed:
```bash
curl http://localhost/api/discovery/jobs | jq '.[] | select(.status == "completed")'
```

## Further Reading

- [Deploy Gate Integration](./deploy-gate.md)
- [Compliance Benchmarking](./compliance.md)
- [API Documentation](http://localhost/api/discovery/swagger/index.html)
