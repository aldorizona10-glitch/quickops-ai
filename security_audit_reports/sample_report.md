# AI Security Micro-Audit Report

Client: {{client}}

Workflow: {{workflow}}

Date: {{date}}

Auditor: Aldo Rizona

## Scope

Tested one AI workflow:

- Entry point:
- User role:
- Data available to model:
- Tools/actions available:
- Out of scope:

## Summary

Overall risk: {{Low/Medium/High}}

Main concerns:

- {{concern_1}}
- {{concern_2}}
- {{concern_3}}

## Findings

### Finding 1 - {{title}}

Severity: {{Low/Medium/High}}

Observation:

{{observation}}

Impact:

{{impact}}

Recommended fix:

{{fix}}

Retest:

{{retest}}

## Positive Controls Observed

- {{control_1}}
- {{control_2}}

## Retest Checklist

- [ ] Prompt injection attempts are ignored or safely handled.
- [ ] Sensitive context is not exposed.
- [ ] Tool calls require appropriate confirmation.
- [ ] Logs provide enough detail for investigation.
- [ ] User-facing errors do not reveal internals.

## Notes

This report is limited to the agreed scope and does not guarantee that the system is free of vulnerabilities.
