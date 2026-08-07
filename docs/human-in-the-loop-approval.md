# GraphOath — Human-in-the-Loop Approval Interceptor Architecture

This document specifies **GraphOath's Human-in-the-Loop (HITL) Interceptor**, which pauses high-risk or destructive AI agent actions until an authorized human operator approves the execution via Slack or the Operator Dashboard.

---

## 1. Risk Classification Matrix

GraphOath categorizes proposed agent actions into two risk tiers:

| Action Risk Tier | Example Action Types | Execution Flow |
|---|---|---|
| **Tier 1: Non-Destructive (Read/Alert)** | `raiseIncident`, `updateIncident`, `postSlackNotification`, `emitAspect` | **Automated Execution**: Citation Gate verifies claim → Executes immediately. |
| **Tier 2: Destructive (Write/Delete)** | `deprecateDataset`, `dropColumn`, `deleteTag`, `grantAccessRole` | **Human Approval Required**: Citation Gate verifies claim → Enters `PENDING_APPROVAL` → Waits for Slack/Dashboard sign-off. |

---

## 2. Interactive Approval Workflow Sequence

```
  AI Agent              GraphOath Gate         Slack Approval        DataHub API
     │                        │                       │                   │
     │ 1. Propose Action      │                       │                   │
     ├───────────────────────►│                       │                   │
     │ (deprecateDataset)     │                       │                   │
     │                        │ 2. Check Risk Tier    │                   │
     │                        │ (Tier 2: Destructive) │                   │
     │                        │                       │                   │
     │                        │ 3. Post Interactive   │                   │
     │                        │    Slack Message      │                   │
     │                        ├──────────────────────►│                   │
     │                        │                       │                   │
     │                        │                       │ 4. Human Clicks   │
     │                        │                       │    "APPROVE"      │
     │                        │ 5. Webhook Callback   │                   │
     │                        │◄──────────────────────┤                   │
     │                        │                       │                   │
     │                        │ 6. Execute Mutation   │                   │
     │                        ├──────────────────────────────────────────►│
     │                        │                       │                   │
     │ 7. Return Signed       │ 7. Record Custody     │                   │
     │    Receipt             │    Receipt Hash       │                   │
     │◄───────────────────────┤                       │                   │
```

---

## 3. Slack Interactive Payload Specification

When a Tier 2 action is paused, GraphOath posts a formatted Slack Block Kit payload:

```json
{
  "channel": "#data-governance-approvals",
  "text": "APPROVAL REQUIRED: Agent proposing dataset deprecation.",
  "blocks": [
    {
      "type": "header",
      "text": { "type": "plain_text", "text": "APPROVAL REQUIRED: Dataset Deprecation" }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Proposed By:* Deposition Agent" },
        { "type": "mrkdwn", "text": "*Risk Tier:* Tier 2 (Destructive)" },
        { "type": "mrkdwn", "text": "*Target URN:* `urn:li:dataset:(snowflake,prod.orders)`" },
        { "type": "mrkdwn", "text": "*Evidence Count:* 4 Verified Citations" }
      ]
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Approve Action" },
          "style": "primary",
          "value": "approve_rcpt_98f4a12b"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Deny Action" },
          "style": "danger",
          "value": "deny_rcpt_98f4a12b"
        }
      ]
    }
  ]
}
```

---

## 4. Cryptographic Binding of Approval

When a human clicks "Approve", the operator's user URN (`urn:li:corpuser:priya_ramaswamy`) and timestamp are permanently appended to the receipt payload before computing the final SHA-256 hash in the Custody ledger. This guarantees that **no destructive action executes without an immutable human sign-off record**.
