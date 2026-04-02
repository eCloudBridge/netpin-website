# ML-Based Remediation System - Complete Guide

## Overview

The NetPin Discovery Service includes a comprehensive ML-powered remediation system that suggests fixes for deployment issues, tracks their effectiveness, and continuously improves through user feedback.

## Table of Contents

1. [Architecture](#architecture)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Using the System](#using-the-system)
5. [API Reference](#api-reference)
6. [ML Pipeline](#ml-pipeline)
7. [Database Schema](#database-schema)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────┐
│                 Frontend (React)                     │
│  - Remediation Feedback Widget                      │
│  - Lifecycle Timeline                                │
│  - Remediation Detail Page                           │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST
┌──────────────────▼──────────────────────────────────┐
│            Traefik API Gateway (Port 80)             │
└──────────┬────────────────────┬─────────────────────┘
           │                    │
    ┌──────▼─────────┐   ┌─────▼──────────────┐
    │  Discovery     │   │  ML Service        │
    │  Service (Go)  │   │  (FastAPI/Python)  │
    │  Port 8000     │   │  Port 8001         │
    └──────┬─────────┘   └─────┬──────────────┘
           │                   │
           │      ┌────────────▼───────────┐
           │      │   ML Training          │
           │      │   (Weekly Scheduler)   │
           │      └────────────┬───────────┘
           │                   │
    ┌──────▼───────────────────▼──────────┐
    │        PostgreSQL Database           │
    │  - Deployment data                   │
    │  - Remediation actions               │
    │  - Lifecycle events                  │
    │  - Training data views               │
    └──────────────────────────────────────┘
```

### Data Flow

1. **Suggestion Generation**
   - Discovery service collects deployment failures
   - Calls ML service with failure features
   - ML service predicts category & ranks suggestions
   - False positive filter applied
   - Top suggestions returned to user

2. **User Feedback Loop**
   - User applies remediation
   - System tracks: applied → resolved/failed
   - User submits rating (1-5 stars)
   - Optionally marks as false positive
   - Events stored in database

3. **Model Improvement**
   - Weekly retraining pipeline runs
   - Fetches lifecycle data (90 days)
   - Trains new ranking model
   - Generates FP filter rules
   - Hot-reloads updated models

---

## Features

### ✨ Key Capabilities

#### 1. **Intelligent Remediation Suggestions**
- Multi-class categorization (configuration, resource, network, security, scaling)
- Confidence scoring (0-100%)
- Expected risk reduction estimates
- Effort estimation (minutes)
- Step-by-step instructions
- Documentation links

#### 2. **Lifecycle Tracking**
- Complete audit trail of suggestions
- Status tracking: suggested → applied → resolved
- User attribution
- Timing metrics (time-to-apply, time-to-resolve)
- Event metadata

#### 3. **User Feedback System**
- 1-5 star ratings
- Free-text comments
- False positive marking with reasons
- Ranking quality metrics (MRR, Top-K, DCG)

#### 4. **Continuous Improvement**
- Automated weekly retraining
- Relevance labeling from user actions
- False positive pattern detection
- Model performance monitoring
- Hot model deployment

#### 5. **False Positive Filtering**
- Pattern-based suppression (≥50% FP rate)
- Confidence penalty for moderate patterns (≥30% FP rate)
- Category + pattern + signature matching
- Automatic rule generation

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- 4GB RAM minimum
- 10GB disk space

### Quick Start

```bash
# Clone repository
cd /path/to/kubeapps

# Start all services
docker-compose up -d

# Verify deployment
docker-compose ps

# Check migrations
docker logs netpin-discovery-migrations

# Test ML service
curl http://localhost:8001/health

# Access UI
open http://localhost:80
```

### Verifying Installation

```bash
# 1. Check database tables
docker exec -it netpin-postgres psql -U netpin -d netpin -c "\dt remediation_*"

# Expected output:
#  remediation_actions
#  remediation_lifecycle_events
#  remediation_ranking_feedback

# 2. Check materialized views
docker exec -it netpin-postgres psql -U netpin -d netpin -c "\dv"

# Expected output:
#  remediation_ranking_training_data
#  false_positive_patterns

# 3. Test ML service
curl -X GET http://localhost:8001/models/info

# 4. Test discovery service
curl -X GET http://localhost/api/remediation/analytics/false-positives?min_samples=5
```

---

## Using the System

### For End Users

#### Viewing Suggestions

1. Navigate to **IDI Analytics** page
2. View deployment issues with risk scores
3. Click on any issue to see remediation suggestions
4. Suggestions are ranked by confidence × expected impact

#### Applying a Remediation

1. Click on a suggestion to open detail page
2. Review step-by-step instructions
3. Click **"Mark as Applied"** button
4. Follow the remediation steps
5. Return to page after resolution

#### Providing Feedback

1. After applying, click **"Mark as Resolved"** (or leave as is if failed)
2. Rate the suggestion (1-5 stars)
3. Add optional comment
4. Click **"Submit Feedback"**

#### Reporting False Positives

1. Click **"Mark as False Positive"** button
2. Provide reason (e.g., "Not applicable to our setup")
3. Click **"Confirm"**
4. Suggestion will be used to improve future filtering

### For Administrators

#### Monitoring System Health

```bash
# Check all services
docker-compose ps

# View ML service logs
docker-compose logs -f discovery-ml-service

# View training logs
docker-compose logs -f discovery-ml-training

# Check database connections
docker exec -it netpin-postgres psql -U netpin -d netpin -c "SELECT count(*) FROM remediation_actions;"
```

#### Triggering Manual Retraining

```bash
# Run retraining manually
docker exec -it netpin-discovery-ml python ml_training/retrain_pipeline.py

# Check if retraining needed
docker exec -it netpin-discovery-ml python -c "
from ml_training.retrain_pipeline import should_retrain
import psycopg2
import os
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
should_run, reason = should_retrain(conn, None)
print(f'Should retrain: {should_run}, Reason: {reason}')
"
```

#### Reloading Models

```bash
# Hot reload models in ML service
curl -X POST http://localhost:8001/models/reload

# Or via Traefik
curl -X POST http://localhost/api/ml/models/reload
```

#### Viewing Analytics

```bash
# Get false positive patterns
curl http://localhost/api/remediation/analytics/false-positives?min_samples=5

# Refresh materialized views
curl -X POST http://localhost/api/remediation/analytics/refresh
```

---

## API Reference

### Lifecycle Tracking Endpoints

#### Mark as Applied
```http
POST /api/remediation/actions/{id}/mark-applied
Content-Type: application/json

{
  "applied_by": "user@example.com"
}
```

**Response**: `200 OK`

#### Mark as Resolved
```http
POST /api/remediation/actions/{id}/mark-resolved
Content-Type: application/json

{
  "resolved": true,
  "verification_method": "manual"
}
```

**Response**: `200 OK`

#### Submit Feedback
```http
POST /api/remediation/actions/{id}/feedback
Content-Type: application/json

{
  "score": 4,
  "comment": "Very helpful, fixed the issue quickly"
}
```

**Response**: `200 OK`

#### Mark as False Positive
```http
POST /api/remediation/actions/{id}/mark-false-positive
Content-Type: application/json

{
  "reason": "Not applicable to our infrastructure setup"
}
```

**Response**: `200 OK`

#### Get Lifecycle History
```http
GET /api/remediation/actions/{id}/lifecycle
```

**Response**:
```json
{
  "events": [
    {
      "id": "uuid",
      "event_type": "suggested",
      "event_timestamp": "2026-02-17T10:00:00Z",
      "user_id": "system",
      "event_source": "ml_service"
    },
    {
      "event_type": "applied",
      "event_timestamp": "2026-02-17T10:15:00Z",
      "user_id": "user@example.com",
      "triggered_by": "user"
    }
  ]
}
```

### Analytics Endpoints

#### Get False Positive Patterns
```http
GET /api/remediation/analytics/false-positives?min_samples=5
```

**Response**:
```json
{
  "patterns": [
    {
      "category": "configuration",
      "failure_pattern": "OOMKilled",
      "false_positive_rate": 0.67,
      "total_samples": 15,
      "avg_confidence": 0.85,
      "common_reasons": ["k8s autoscaling handles this"]
    }
  ]
}
```

#### Refresh Analytics Views
```http
POST /api/remediation/analytics/refresh
```

**Response**: `200 OK`

### ML Service Endpoints

#### Get Remediation Suggestions
```http
POST /api/ml/predict/remediations
Content-Type: application/json

{
  "features": {
    "failure_pattern": "OOMKilled",
    "error_signature": "exit code 137",
    "deployment_frequency": 5.2,
    ...
  }
}
```

**Response**:
```json
{
  "suggestions": [
    {
      "category": "resource_limits",
      "confidence": 0.92,
      "expected_risk_reduction": 0.75,
      "remediation_steps": ["Increase memory limit", "Add resource requests"],
      "estimated_effort_minutes": 15
    }
  ]
}
```

#### Reload Models
```http
POST /api/ml/models/reload
```

**Response**:
```json
{
  "status": "success",
  "message": "Models reloaded successfully",
  "fp_filter_enabled": true
}
```

---

## ML Pipeline

### Training Data Preparation

Materialized view `remediation_ranking_training_data` provides training data:

```sql
SELECT 
    snapshot_id,
    suggested_remediations,  -- Array of UUIDs
    applied_remediation_id,  -- UUID or NULL
    relevance_label         -- 2.0, 1.0, 0.0, or -1.0
FROM remediation_ranking_training_data
WHERE created_at > NOW() - INTERVAL '90 days';
```

**Relevance Labels**:
- `2.0` = Applied + Resolved (highly relevant)
- `1.0` = Applied + Not resolved (somewhat relevant)
- `0.0` = Suggested but not applied (unknown)
- `-1.0` = Marked as false positive (irrelevant)

### Ranking Model

**Algorithm**: LightGBM LambdaRank
**Objective**: Maximize NDCG@3
**Features**: 27 deployment + temporal features

**Training**:
```python
model = lgb.LGBMRanker(
    objective='lambdarank',
    metric='ndcg',
    ndcg_eval_at=[3]
)
model.fit(X_train, y_train, group=train_groups)
```

**Evaluation Metrics**:
- **NDCG@3**: Normalized Discounted Cumulative Gain
- **Top-3 Hit Rate**: % with relevant item in top 3
- **MRR**: Mean Reciprocal Rank

### False Positive Filter

Generated from false_positive_patterns view:

**Suppression Rules** (FP rate ≥ 50%, samples ≥ 10):
```python
{
  "suppressed_patterns": [
    {
      "category": "scaling",
      "failure_pattern": "pod_pending",
      "signature": "insufficient_resources",
      "fp_rate": 0.67
    }
  ]
}
```

**Confidence Adjustments** (FP rate ≥ 30%, samples ≥ 5):
```python
{
  "confidence_adjustments": [
    {
      "pattern": {...},
      "penalty": 0.3  # Reduce confidence by 30%
    }
  ]
}
```

### Retraining Pipeline

**Schedule**: Every 7 days (configurable)

**Triggers**:
1. ≥100 new labeled samples
2. Top-K hit rate drops >5%
3. ≥7 days since last training

**Process**:
1. Check triggers
2. Refresh materialized views
3. Fetch 90-day training data
4. Train new ranking model
5. Generate FP filter rules
6. Save models to shared volume
7. Trigger hot reload

---

## Database Schema

### Tables

#### `remediation_actions`
```sql
CREATE TABLE remediation_actions (
    id UUID PRIMARY KEY,
    deployment_id TEXT,
    snapshot_id UUID,
    category TEXT,
    failure_pattern TEXT,
    error_signature TEXT,
    confidence FLOAT,
    expected_risk_reduction FLOAT,
    remediation_steps JSONB,
    -- Lifecycle fields
    remediation_suggested TIMESTAMP,
    remediation_applied TIMESTAMP,
    issue_resolved TIMESTAMP,
    user_feedback_score INTEGER,
    user_feedback_comment TEXT,
    false_positive BOOLEAN,
    false_positive_reason TEXT,
    time_to_apply_minutes INTEGER,
    time_to_resolve_minutes INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### `remediation_lifecycle_events`
```sql
CREATE TABLE remediation_lifecycle_events (
    id UUID PRIMARY KEY,
    remediation_action_id UUID REFERENCES remediation_actions(id),
    event_type TEXT,  -- suggested, applied, resolved, failed, feedback, dismissed
    event_timestamp TIMESTAMP,
    user_id TEXT,
    event_source TEXT,  -- api, automation, scheduler
    triggered_by TEXT,  -- user, automation
    event_metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### `remediation_ranking_feedback`
```sql
CREATE TABLE remediation_ranking_feedback (
    id UUID PRIMARY KEY,
    snapshot_id UUID,
    suggested_remediations UUID[],
    applied_remediation_id UUID,
    applied_remediation_rank INTEGER,
    top_k_hit BOOLEAN,
    mean_reciprocal_rank FLOAT,
    discounted_cumulative_gain FLOAT,
    ranking_quality_score FLOAT,
    num_false_positives INTEGER,
    false_positive_ids UUID[],
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Materialized Views

#### `remediation_ranking_training_data`
Provides ML training data with relevance labels.

#### `false_positive_patterns`
Aggregates FP patterns for filter generation.

**Refresh**:
```sql
REFRESH MATERIALIZED VIEW CONCURRENTLY remediation_ranking_training_data;
REFRESH MATERIALIZED VIEW CONCURRENTLY false_positive_patterns;
```

Or via API:
```bash
curl -X POST http://localhost/api/remediation/analytics/refresh
```

---

## Configuration

### Environment Variables

#### Discovery Service
```env
DATABASE_URL=postgresql://netpin:password@postgres:5432/netpin
ML_SERVICE_URL=http://discovery-ml-service:8001
REDIS_URL=redis://redis:6379/0
```

#### ML Service
```env
DB_HOST=postgres
DB_PORT=5432
DB_NAME=netpin
DB_USER=netpin
DB_PASSWORD=password
MODEL_DIR=/app/ml_training/models
```

### Retraining Configuration

Edit `ml_training/retrain_pipeline.py`:

```python
# Retraining thresholds
MIN_NEW_SAMPLES = 100              # Minimum new samples to trigger
PERFORMANCE_DROP_THRESHOLD = 0.05  # 5% drop in Top-K
RETRAINING_INTERVAL_DAYS = 7       # Days between scheduled retraining
```

### False Positive Filter Configuration

Edit `ml_training/false_positive_filter.py`:

```python
# FP filter thresholds
FP_RATE_HIGH = 0.5                 # ≥50% = suppress
FP_RATE_MODERATE = 0.3             # ≥30% = reduce confidence
MIN_SAMPLES_FOR_SUPPRESSION = 10   # Minimum samples required
MIN_SAMPLES_FOR_ADJUSTMENT = 5     # Minimum for confidence adjustment
```

---

## Troubleshooting

### Common Issues

#### 1. Migrations Fail with "relation already exists"

**Cause**: Migrations were previously run
**Solution**: This is normal, the container will exit successfully

```bash
# Check migration logs
docker logs netpin-discovery-migrations | grep "✓"

# If all migrations applied successfully, you're good
```

#### 2. ML Service Returns "No models loaded"

**Cause**: Models don't exist yet (first run)
**Solution**: Run initial training

```bash
# Train initial models
docker exec -it netpin-discovery-ml python ml_training/train_model.py

# Reload models
curl -X POST http://localhost:8001/models/reload
```

#### 3. Frontend Shows No Suggestions

**Cause**: No deployment failures in database yet
**Solution**: Test with sample data

```bash
# Create sample deployment failure
# (requires implementing test data script)
docker exec -it netpin-postgres psql -U netpin -d netpin -f /path/to/test_data.sql
```

#### 4. Retraining Never Triggers

**Cause**: Not enough labeled data
**Solution**: Check training data availability

```bash
docker exec -it netpin-postgres psql -U netpin -d netpin -c "
SELECT 
    COUNT(*) as total_samples,
    COUNT(*) FILTER (WHERE relevance_label != 0.0) as labeled_samples
FROM remediation_ranking_training_data;
"

# Needs ≥100 labeled samples for training
```

#### 5. High False Positive Rate

**Cause**: Model needs retraining with feedback
**Solution**: Ensure users are marking FPs

```bash
# Check FP marking rate
docker exec -it netpin-postgres psql -U netpin -d netpin -c "
SELECT 
    COUNT(*) FILTER (WHERE false_positive = true) * 100.0 / COUNT(*) as fp_rate
FROM remediation_actions
WHERE remediation_suggested IS NOT NULL;
"
```

### Getting Help

1. **Check logs**: `docker-compose logs -f [service-name]`
2. **Verify database**: Connect via psql and check tables
3. **Test endpoints**: Use curl to test each API endpoint
4. **Review metrics**: Check ML model performance metrics

### Performance Tuning

#### Database Optimization
```sql
-- Analyze tables for query optimization
ANALYZE remediation_actions;
ANALYZE remediation_lifecycle_events;

-- Vacuum to reclaim space
VACUUM remediation_actions;
```

#### ML Service Scaling
```yaml
# docker-compose.yml
discovery-ml-service:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 1G
```

---

## Best Practices

### For Users

1. **Always provide feedback** - Even negative feedback helps improve the system
2. **Mark false positives** - Include detailed reasons
3. **Apply suggestions quickly** - Timing data improves rankings
4. **Leave comments** - Qualitative feedback is valuable

### For Administrators

1. **Monitor retraining** - Check logs weekly
2. **Review FP patterns** - Investigate high FP rate categories
3. **Track metrics** - Monitor NDCG, MRR, hit rates
4. **Backup models** - Save model versions before retraining
5. **Test before deployment** - Validate new models on held-out data

---

## Security Considerations

### Current Limitations

⚠️ **For Production Use**:

1. **Add JWT Authentication**
   - ML service endpoints are currently unprotected
   - Implement FastAPI JWT dependency

2. **Enable HTTPS/TLS**
   - Configure Traefik with SSL certificates
   - Use Let's Encrypt for automatic renewal

3. **Implement Rate Limiting**
   - Prevent abuse of ML API
   - Use FastAPI middleware

4. **Secure Database**
   - Use strong passwords
   - Restrict network access
   - Enable SSL connections

5. **API Input Validation**
   - Already implemented via Pydantic
   - Review for edge cases

---

## Appendix

### Glossary

- **NDCG**: Normalized Discounted Cumulative Gain - Ranking quality metric
- **MRR**: Mean Reciprocal Rank - Position of first relevant item
- **FP**: False Positive - Incorrect suggestion
- **LambdaRank**: Gradient boosting algorithm for learning to rank
- **Lifecycle Event**: Tracked state change in remediation process

### Further Reading

- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [Learning to Rank](https://en.wikipedia.org/wiki/Learning_to_rank)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Last Updated**: 2026-02-17  
**Version**: 1.1.0 (Lifecycle Tracking Release)
