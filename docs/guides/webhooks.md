# CI/CD Webhook Integration Guide

## Overview

Deploy Gate supports webhook integrations with major CI/CD platforms to automatically evaluate deployments when pipelines complete.

## Supported Platforms

- **GitHub** - Check runs and override requests
- **GitLab** - Pipeline completion
- **Jenkins** - Build completion
- **ArgoCD** - PreSync and PostSync hooks

---

## GitHub Integration

### Setup

1. Configure webhook in your GitHub repository:
   - URL: `http://gate-service:8000/api/gate/webhooks/github`
   - Content type: `application/json`
   - Secret: Set in `GITHUB_WEBHOOK_SECRET` env var
   - Events: Select "Check runs"

2. Set environment variable:
```bash
GITHUB_WEBHOOK_SECRET=your-secret-token
```

### Webhook Payload

GitHub sends webhooks for check run events:

```json
{
  "action": "completed",
  "check_run": {
    "name": "deploy-gate",
    "head_sha": "abc123",
    "conclusion": "success",
    "output": {
      "title": "Deploy Gate Evaluation",
      "summary": "..."
    }
  }
}
```

### Override Request (GitHub App Required)

To enable override requests via GitHub action buttons:

1. Create a GitHub App with Check Runs write permission
2. Add action button annotation in check run output
3. Handle `requested_action` webhook events

---

## GitLab Integration

### Setup

1. Navigate to Project → Settings → Webhooks
2. Configure webhook:
   - URL: `http://gate-service:8000/api/gate/webhooks/gitlab`
   - Secret token: `your-secret`
   - Trigger: Pipeline events
   - Enable SSL verification (production only)

### Webhook Payload

GitLab sends pipeline events:

```json
{
  "object_kind": "pipeline",
  "project": {
    "name": "my-app",
    "namespace": "my-org"
  },
  "commit": {
    "sha": "abc123"
  },
  "ref": "refs/heads/main",
  "status": "success"
}
```

### Gate Evaluation

The webhook handler:
1. Checks status is "success"
2. Extracts project, commit, branch
3. Determines environment from branch name (main → production)
4. Creates evaluation request
5. Returns evaluation results

**Example Response**:
```json
{
  "message": "GitLab pipeline evaluated",
  "project": "my-app",
  "commit": "abc123",
  "status": "success",
  "evaluation_id": "eval-456",
  "decision": "APPROVED",
  "idi_score": 42
}
```

### GitLab CI Integration

Add to `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - deploy

deploy_production:
  stage: deploy
  only:
    - main
  script:
    # Webhook is triggered automatically
    # Or trigger manually:
    - |
      EVAL_RESULT=$(curl -X POST http://gate-service/api/gate/evaluate \
        -H "Content-Type: application/json" \
        -d "{
          \"project_id\": \"$CI_PROJECT_PATH\",
          \"commit_sha\": \"$CI_COMMIT_SHA\",
          \"environment\": \"production\"
        }")
      
      DECISION=$(echo $EVAL_RESULT | jq -r '.decision')
      if [ "$DECISION" != "APPROVED" ]; then
        echo "Deploy gate blocked deployment"
        exit 1
      fi
```

---

## Jenkins Integration

### Setup

1. Install "Generic Webhook Trigger" plugin
2. Configure webhook in Jenkinsfile or job configuration:
   - URL: `http://gate-service:8000/api/gate/webhooks/jenkins`
   - Method: POST

### Configure Post-Build Action

Add to Jenkinsfile:

```groovy
pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                // Your build steps
                sh 'make build'
            }
        }
    }
    
    post {
        success {
            script {
                // Trigger gate evaluation
                def payload = """
                {
                    "name": "${env.JOB_NAME}",
                    "build": {
                        "number": ${env.BUILD_NUMBER},
                        "url": "${env.BUILD_URL}",
                        "phase": "COMPLETED",
                        "status": "SUCCESS"
                    },
                    "scm": {
                        "commit": "${env.GIT_COMMIT}",
                        "branch": "${env.GIT_BRANCH}",
                        "url": "${env.GIT_URL}"
                    }
                }
                """
                
                sh """
                    curl -X POST http://gate-service:8000/api/gate/webhooks/jenkins \
                        -H 'Content-Type: application/json' \
                        -d '${payload}'
                """
            }
        }
    }
}
```

### Webhook Payload Example

```json
{
  "name": "myapp-build",
  "build": {
    "number": 42,
    "url": "http://jenkins/job/myapp/42",
    "phase": "COMPLETED",
    "status": "SUCCESS"
  },
  "scm": {
    "commit": "abc123",
    "branch": "main",
    "url": "https://github.com/org/repo"
  }
}
```

**Response**:
```json
{
  "message": "Jenkins build evaluated",
  "job": "myapp-build",
  "build": 42,
  "phase": "COMPLETED",
  "evaluation_id": "eval-789",
  "decision": "APPROVED",
  "idi_score": 38
}
```

---

## ArgoCD Integration

### PreSync Hook (Gate Evaluation)

Add annotation to your ArgoCD Application:

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: myapp
  annotations:
    argocd.argoproj.io/hook: PreSync
    argocd.argoproj.io/hook-delete-policy: BeforeHookCreation
spec:
  # ...
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

Configure webhook:
- URL: `http://gate-service:8000/api/gate/webhooks/argocd/presync`

### PostSync Hook (Validation)

For post-deployment validation:

- URL: `http://gate-service:8000/api/gate/webhooks/argocd/postsync`

### Webhook Payload

```json
{
  "application": "myapp",
  "project": "default",
  "revision": "v1.2.3",
  "source": {
    "repoURL": "https://github.com/org/repo",
    "path": "charts/myapp",
    "chart": "myapp"
  },
  "destination": {
    "server": "https://kubernetes.default.svc",
    "namespace": "production"
  },
  "operation": "sync",
  "phase": "PreSync"
}
```

**Response**:
```json
{
  "allowed": true,
  "message": "Deploy Gate approved. IDI Score: 42",
  "phase": "Succeeded"
}
```

If blocked:
```json
{
  "allowed": false,
  "message": "Deploy Gate blocked: IDI score 78 exceeds threshold 75",
  "phase": "Failed"
}
```

---

## Environment Detection

The webhook handler automatically determines the environment from branch/ref names:

| Branch Pattern | Environment |
|----------------|-------------|
| main, master, prod | production |
| staging, stage | staging |
| dev, develop | development  |
| feature/*, bug/* | development (default) |

Override this by including `environment` in evaluation payload.

---

## Security

### Webhook Signature Verification

GitHub webhooks are verified using HMAC-SHA256:

```go
func verifyGitHubSignature(payload []byte, signature string, secret string) bool {
    mac := hmac.New(sha256.New, []byte(secret))
    mac.Write(payload)
    expected := "sha256=" + hex.EncodeToString(mac.Sum(nil))
    return hmac.Equal([]byte(signature), []byte(expected))
}
```

Set `GITHUB_WEBHOOK_SECRET` environment variable.

### Network Security

For production:
1. Use HTTPS endpoints
2. Configure firewall rules
3. Use VPN or private networks
4. Rotate webhook secrets regularly

---

## Testing Webhooks

### Manual Test

```bash
# GitLab webhook test
curl -X POST http://localhost/api/gate/webhooks/gitlab \
  -H "Content-Type: application/json" \
  -d '{
    "object_kind": "pipeline",
    "project": {"name": "test-app", "namespace": "test"},
    "commit": {"sha": "abc123"},
    "ref": "refs/heads/main",
    "status": "success"
  }'

# Jenkins webhook test
curl -X POST http://localhost/api/gate/webhooks/jenkins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test-build",
    "build": {"number": 1, "status": "SUCCESS", "phase": "COMPLETED"},
    "scm": {"commit": "abc123", "branch": "main"}
  }'
```

### View Webhook Logs

```bash
docker-compose logs -f gate-service | grep webhook
```

---

## Troubleshooting

### Webhook Returns 401 Unauthorized

- GitHub: Check `X-Hub-Signature-256` header and `GITHUB_WEBHOOK_SECRET`
- Others: Verify authentication token in request

### Evaluation Not Created

Check gate-service logs:
```bash
docker-compose logs gate-service | grep -A 5 "webhook"
```

Verify policy exists for environment:
```bash
curl http://localhost/api/gate/policies | jq '.[] | select(.environment == "production")'
```

### "No matching policy" Error

Create a policy for the target environment or create a catch-all policy with `environment: "*"`

---

## Best Practices

1. **Use Webhook Secrets**: Always configure secrets for production
2. **Monitor Webhook Failures**: Set up alerts for failed webhooks
3. **Test in Staging First**: Validate webhook configuration in non-prod
4. **Log All Evaluations**: Enable detailed logging for audit trails
5. **Handle Retries**: Implement retry logic in CI/CD for transient failures

---

## Further Reading

- [Deploy Gate Guide](./deploy-gate.md)
- [Policy Configuration](../api/gate-policies.md)
- [API Reference](http://localhost/api/gate/swagger/index.html)
