# Escalation JSON Schema

Shared state file: `/tmp/escalation-{timestamp}.json`

```json
{
  "id": "escalation-1734372000",
  "created_at": "2024-12-16T12:00:00Z",
  "status": "in_progress|completed|blocked",

  "input": {
    "raw": "original user input or HubSpot URL",
    "source": "hubspot|description|linear",
    "hubspot_url": null
  },

  "extracted": {
    "company_id": null,
    "user_id": null,
    "record_id": null,
    "priority": null,
    "datetime": null,
    "feature_area": null,
    "description": null,
    "steps_to_replicate": [],
    "expected_result": null,
    "actual_result": null,
    "is_mobile": false,
    "mobile_platform": null,
    "ios_version": null,
    "ios_app_version": null,
    "android_version": null,
    "android_app_version": null,
    "replicable_in_customer_account": null,
    "prerequisites": null,
    "steps_to_view": [],
    "recording_url": null,
    "troubleshooting_steps": null,
    "additional_info": null
  },

  "p1_quick_checks": {
    "status": "pending|running|complete",
    "duplicate": {
      "found": false,
      "issue_id": null,
      "title": null,
      "url": null,
      "match_confidence": null
    },
    "documented": {
      "found": false,
      "url": null,
      "summary": null
    },
    "recent_releases": []
  },

  "p2_reproduction": {
    "status": "pending|running|complete|skipped|PASS|FAIL|BLOCKED",
    "reproduced": null,
    "environment": "dev",
    "steps_executed": [],
    "screenshot_paths": [],
    "console_errors": [],
    "network_errors": [],
    "notes": null,
    "findings": null
  },

  "p3_code_investigation": {
    "status": "pending|running|complete|skipped",
    "repo": null,
    "repos_searched": [],
    "root_cause": null,
    "location": null,
    "confidence": null,
    "related_commits": [],
    "regression_risk": null,
    "code_fix": {
      "approach": null,
      "language": null,
      "full_code": null,
      "files": [],
      "risks": null,
      "tests_needed": null
    }
  },

  "finding": {
    "type": "duplicate|documented|new|cannot_reproduce",
    "summary": null,
    "recommendation": null
  },

  "ticket": {
    "created": false,
    "id": null,
    "url": null,
    "team": null,
    "branch": null
  }
}
```

## Status Transitions

```
input → P1 (parallel checks)
         ↓
      duplicate? → STOP (output duplicate)
      documented? → STOP (output doc link)
         ↓
        P2 (reproduction)
         ↓
      reproduced? → P3 (code investigation)
      not reproduced? → finding: cannot_reproduce
         ↓
        P4 (compile finding)
         ↓
        P5 (user confirmation)
         ↓
        P6 (ticket creation)
```
