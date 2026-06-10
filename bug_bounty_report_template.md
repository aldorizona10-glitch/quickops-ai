# Bug Bounty Report Template

Program:
Asset:
Scope URL:
Submitted at:
Researcher: Aldo Rizona / aldorizona10-glitch / aldorizona10@gmail.com

## Title

[Vulnerability type] in [asset/feature] allows [impact]

## Summary

Short explanation of what is vulnerable, where it happens, and why it matters.

## Scope Confirmation

- Program URL:
- In-scope asset:
- Rule checked date:
- Account used for testing:

## Impact

Explain the concrete security impact. Avoid theory. State what an attacker could do and what prerequisite access is needed.

## Steps To Reproduce

1. Log in as test account A.
2. Navigate to:
3. Send this request or perform this action:
4. Observe:

## Expected Result

Describe the secure behavior.

## Actual Result

Describe the vulnerable behavior.

## Evidence

Attach screenshots, screen recording, or sanitized HTTP request/response.

## Safety Statement

Testing was performed only against in-scope assets, using accounts controlled by the researcher. No third-party data was accessed, modified, retained, or disclosed.

## Suggested Fix

Describe the likely remediation, such as server-side authorization checks, stricter token scope validation, CSRF/state validation, output encoding, or webhook signature verification.

## Timeline

- Discovery:
- Report submission:
- Follow-up:
