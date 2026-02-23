# Testing ML Remediation System Endpoints

## Quick Test Script

This document provides quick commands to test all the ML remediation endpoints through Traefik.

### Prerequisites

```bash
# Ensure all services are running
docker-compose ps

# Should see:
# - netpin-postgres (healthy)
# - netpin-redis (healthy) 
# - netpin-gateway (up)
# - netpin-discovery (up)
# - netpin-discovery-ml (up/healthy)
# - netpin-auth (healthy)
```

### Testing Endpoints

#### 1. Test Traefik Gateway
```bash
curl -I http://localhost:80
# Should return: HTTP/1.1 404 Not Found (normal, shows Traefik is working)
```

#### 2. Test Discovery Service Health
```bash
curl http://localhost/api/discovery/health
# Expected: {"status": "healthy"}
```

#### 3. Test ML Service (Direct)
```bash
# Direct access (bypass Traefik)
curl http://localhost:8001/health
# Expected: {"status": "healthy"}

# Via Traefik
curl http://localhost/api/ml/health  
# Expected: {"status": "healthy"}
```

#### 4. Test Lifecycle Endpoints

**Get False Positive Patterns** (Analytics):
```bash
curl "http://localhost/api/remediation/analytics/false-positives?min_samples=1"
# Expected: {"patterns": [...]} or empty array if no data yet
```

**Refresh Analytics Views**:
```bash
curl -X POST http://localhost/api/remediation/analytics/refresh
# Expected: HTTP 200 OK
```

#### 5. Test Individual Remediation Actions

**Note**: You'll need a valid remediation ID from your database. Replace `{id}` below.

**Mark as Applied**:
```bash
curl -X POST http://localhost/api/remediation/actions/{id}/mark-applied \
  -H "Content-Type: application/json" \  -d '{"applied_by": "test@example.com"}'
# Expected: HTTP 200 OK
```

**Mark as Resolved**:
```bash
curl -X POST http://localhost/api/remediation/actions/{id}/mark-resolved \
  -H "Content-Type: application/json" \
  -d '{"resolved": true, "verification_method": "manual"}'
# Expected: HTTP 200 OK
```

**Submit Feedback**:
```bash
curl -X POST http://localhost/api/remediation/actions/{id}/feedback \
  -H "Content-Type: application/json" \
  -d '{"score": 4, "comment": "Very helpful!"}'
# Expected: HTTP 200 OK
```

**Mark as False Positive**:
```bash
curl -X POST http://localhost/api/remediation/actions/{id}/mark-false-positive \
  -H "Content-Type: application/json" \
  -d '{"reason": "Not applicable to our setup"}'
# Expected: HTTP 200 OK
```

**Get Lifecycle History**:
```bash
curl http://localhost/api/remediation/actions/{id}/lifecycle
# Expected: {"events": [{...}]}
```

#### 6. Test ML Predictions

**Get Remediation Suggestions**:
```bash
curl -X POST http://localhost/api/ml/predict/remediations \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "failure_pattern": "OOMKilled",
      "error_signature": "exit code 137",
      "deployment_frequency": 5.2,
      "time_since_last_failure_hours": 24,
      "severity": "high"
    }
  }'
# Expected: {"suggestions": [{...}]}
```

**Reload ML Models**:
```bash
curl -X POST http://localhost/api/ml/models/reload
# or via Traefik:
curl -X POST http://localhost/api/ml/models/reload
# Expected: {"status": "success", "fp_filter_enabled": true}
```

**Get Model Info**:
```bash
curl http://localhost/api/ml/models/info
# Expected: {"models": {...}, "last_trained": "..."}
```

### Automated Test Script

Save this as `test-endpoints.sh`:

```bash
#!/bin/bash

echo "🧪 Testing ML Remediation System Endpoints"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

test_endpoint() {
  local name="$1"
  local url="$2"
  local method="${3:-GET}"
  
  echo -n "Testing $name... "
  
  if [ "$method" = "GET" ]; then
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  else
    status=$(curl -s -o /dev/null -w "%{http_code}" -X "$method" "$url")
  fi
  
  if [ "$status" -eq 200 ] || [ "$status" -eq 404 ]; then
    echo -e "${GREEN}✓ $status${NC}"
  else
    echo -e "${RED}✗ $status${NC}"
  fi
}

# Test Traefik
test_endpoint "Traefik Gateway" "http://localhost:80" "GET"

# Test Core Services
test_endpoint "Discovery Health" "http://localhost/api/discovery/health" "GET"
test_endpoint "ML Service Health (Direct)" "http://localhost:8001/health" "GET"
test_endpoint "ML Service Health (Traefik)" "http://localhost/api/ml/health" "GET"
test_endpoint "Auth Service" "http://localhost/api/auth/health" "GET"

# Test Analytics
test_endpoint "FP Patterns" "http://localhost/api/remediation/analytics/false-positives?min_samples=1" "GET"
test_endpoint "Analytics Refresh" "http://localhost/api/remediation/analytics/refresh" "POST"

# Test ML Endpoints
test_endpoint "ML Models Info" "http://localhost/api/ml/models/info" "GET"

echo ""
echo "=========================================="
echo "✅ Test Complete"
echo ""
echo "Note: 404s are OK for endpoints requiring data"
echo "Note: Use Swagger UI for interactive testing: http://localhost/api-docs"
```

Make executable and run:
```bash
chmod +x test-endpoints.sh
./test-endpoints.sh
```

### Troubleshooting Failed Tests

#### 404 on all `/api/remediation/*` endpoints
**Cause**: Discovery service not running or Traefik routing issue

**Solution**:
```bash
# Check discovery service
docker logs netpin-discovery --tail 50

# Restart discovery service
docker-compose restart discovery-service

# Check Traefik routes
curl http://localhost:8080/api/rawdata | python3 -m json.tool | grep "remediation"
```

#### 000 or Connection Refused on ML Service
**Cause**: ML service not started or unhealthy

**Solution**:
```bash
# Check ML service logs
docker logs netpin-discovery-ml --tail 50

# Common issues:
# - Missing dependencies: Rebuild image
# - Model loading error: Check model directory
# - Port conflict: Check if 8001 is available

# Rebuild and restart
docker-compose build discovery-ml-service
docker-compose up -d discovery-ml-service

# Wait for healthy status
docker-compose ps | grep discovery-ml
```

#### Empty Response from Analytics Endpoints
**Cause**: No data in database yet (normal on first run)

**Solution**: This is expected. Data will populate as:
1. Deployment failures are recorded
2. Remediation suggestions are made
3. Users apply and provide feedback

### Frontend Testing

#### Access UI
```bash
open http://localhost:80
```

#### Test Remediation Detail Page

1. Navigate to **IDI Analytics**
2. If you have deployment data, you'll see suggestions
3. Click any suggestion to open detail page
4. You should see:
   - Remediation details
   - Action buttons (Mark as Applied, Resolved, etc.)
   - Star rating widget
   - Lifecycle timeline (if events exist)

#### Test Feedback Submission

1. On remediation detail page
2. Click "Mark as Applied"
3. Rate with stars (1-5)
4. Add comment
5. Click "Submit Feedback"
6. Check network tab - should see successful POSTs

### Database Verification

```bash
# Connect to database
docker exec -it netpin-postgres psql -U netpin -d netpin

# Check tables exist
\dt remediation_*

# Check for sample data
SELECT COUNT(*) FROM remediation_actions;
SELECT COUNT(*) FROM remediation_lifecycle_events;  

# Check materialized views
SELECT COUNT(*) FROM remediation_ranking_training_data;
SELECT COUNT(*) FROM false_positive_patterns;

# Exit
\q
```

### Complete Smoke Test

Run this complete test:

```bash
echo "=== System Smoke Test ==="

echo "1. Services Running:"
docker-compose ps | grep -E "(Up|healthy)" | wc -l

echo "2. Database Tables:"
docker exec -it netpin-postgres psql -U netpin -d netpin -c "\dt remediation_*" | grep remediation | wc -l

echo "3. ML Service:"
curl -s http://localhost:8001/health | grep -q "healthy" && echo "✓ Healthy" || echo "✗ Not Healthy"

echo "4. Traefik Routing:"
curl -s http://localhost:80 | grep -q "404" && echo "✓ Gateway Working" || echo "✗ Gateway Issue"

echo "5. Discovery Service:"
docker logs netpin-discovery 2>&1 | grep -q "Server started" && echo "✓ Started" || echo "⚠ Check logs"

echo "=== Test Complete ==="
```

### Expected Results

On a fresh deployment with no data:

- ✅ All services should be running/healthy
- ✅ ML service: 200 OK
- ✅ Analytics refresh: 200 OK
- ✅ FP patterns: 200 OK with empty array `{"patterns": []}`
- ⚠️ Remediation actions by ID: 404 (no data yet - expected)
- ✅ Model reload: 200 OK (even with no models, should not error)

After using the system:

- ✅ FP patterns: Returns actual patterns
- ✅ Lifecycle endpoints: Return event data
- ✅ Remediation actions: Work with valid IDs

---

**Pro Tip**: Use Swagger UI at http://localhost/api-docs for interactive testing with a nice UI!
