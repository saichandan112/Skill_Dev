# Secure SAP AI Agent Platform

## Development, Security, Deployment, Threat Model, and Operations Blueprint

| Document field | Value |
|---|---|
| Status | Development reference architecture |
| Version | 2.0 |
| Last updated | 2026-09-08 |
| Intended audience | SAP architects, ABAP developers, AI engineers, security engineers, platform engineers, SRE teams, service managers, approvers, auditors, and product owners |
| Primary objective | Build a secure AI-assisted platform for SAP engineering, development, incident diagnosis, change planning, governed knowledge retrieval, and bounded automation |

> **Core principle:** The AI model may analyze, explain, draft, and propose. Deterministic services authenticate, authorize, approve, execute, verify, and audit.

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Executive Architecture Position](#2-executive-architecture-position)
3. [Scope](#3-scope)
4. [Goals and Non-Goals](#4-goals-and-non-goals)
5. [Security and Engineering Principles](#5-security-and-engineering-principles)
6. [System Context](#6-system-context)
7. [Target Logical Architecture](#7-target-logical-architecture)
8. [Trust Boundaries](#8-trust-boundaries)
9. [Component Responsibilities](#9-component-responsibilities)
10. [Identity and Delegation Model](#10-identity-and-delegation-model)
11. [Authorization Model](#11-authorization-model)
12. [Agent and Workflow Design](#12-agent-and-workflow-design)
13. [Tool Gateway and Deterministic Execution](#13-tool-gateway-and-deterministic-execution)
14. [SAP Integration Design](#14-sap-integration-design)
15. [Knowledge and RAG Architecture](#15-knowledge-and-rag-architecture)
16. [Data Protection and Privacy](#16-data-protection-and-privacy)
17. [Approval and Action Manifest Design](#17-approval-and-action-manifest-design)
18. [End-to-End Workflows](#18-end-to-end-workflows)
19. [Action Risk Classification](#19-action-risk-classification)
20. [Threat Model](#20-threat-model)
21. [Secure Development Lifecycle](#21-secure-development-lifecycle)
22. [Repository and Code Organization](#22-repository-and-code-organization)
23. [API and Event Contracts](#23-api-and-event-contracts)
24. [Policy-as-Code Design](#24-policy-as-code-design)
25. [Testing and AI Evaluation](#25-testing-and-ai-evaluation)
26. [CI/CD and Supply-Chain Security](#26-cicd-and-supply-chain-security)
27. [Environment and Deployment Architecture](#27-environment-and-deployment-architecture)
28. [Observability, Audit, and SRE](#28-observability-audit-and-sre)
29. [Operational Runbooks](#29-operational-runbooks)
30. [Implementation Roadmap](#30-implementation-roadmap)
31. [Initial Production Scope](#31-initial-production-scope)
32. [Production Readiness and Acceptance Criteria](#32-production-readiness-and-acceptance-criteria)
33. [Team Structure and Responsibilities](#33-team-structure-and-responsibilities)
34. [Architecture Decision Records](#34-architecture-decision-records)
35. [Definition of Done](#35-definition-of-done)
36. [Final Design Rules](#36-final-design-rules)
37. [Reference Sources](#37-reference-sources)

---

## 1. Purpose

This document is a development-ready reference for building a secure enterprise platform that applies AI to SAP engineering and operations without giving a language model uncontrolled authority over SAP systems.

The platform can support:

- SAP incident intake, triage, diagnosis, and resolution guidance
- Root-cause analysis and problem-management assistance
- Service-request validation and fulfillment planning
- Change-request drafting, impact analysis, test planning, and evidence collection
- ABAP development assistance, review, test generation, and remediation proposals
- Transport readiness and release-evidence preparation
- Governed knowledge retrieval and knowledge-article drafting
- Read-only SAP diagnostics
- Selected, approved, tightly bounded automation

This blueprint explains not only what components are required, but also how they interact, where security is enforced, what an AI agent may do, what it must never do, and how the platform can be introduced safely in phases.

---

## 2. Executive Architecture Position

A secure SAP AI platform is not a chatbot connected directly to SAP. It is a governed enterprise application in which AI is one bounded analytical component.

The authoritative execution path is:

```text
User intent
  -> authenticated request
  -> case and purpose validation
  -> authorized and minimized context
  -> bounded AI analysis
  -> evidence-linked recommendation
  -> typed action proposal
  -> deterministic parameter normalization
  -> policy decision
  -> human approval when required
  -> signed, short-lived action manifest
  -> Tool Gateway enforcement
  -> deterministic executor
  -> SAP-side authorization and validation
  -> execution
  -> independent post-action verification
  -> immutable audit evidence
```

The following systems remain authoritative:

- The identity provider for human and workload identity
- The entitlement service for access decisions
- SAP authorization objects and organizational restrictions
- The ITSM platform for case and change status
- The policy engine for action-level decisions
- The approval service for human authorization
- The Tool Gateway for execution enforcement
- The deterministic executor for controlled invocation
- SAP for transaction and business-rule enforcement
- The evidence service and SIEM for audit records

The model is never an authority for identity, permission, approval, policy, business state, execution success, or audit truth.

---

## 3. Scope

### 3.1 In Scope

- Secure web, chat, ITSM, and IDE experiences
- SSO, MFA, conditional access, and session controls
- APIs and backend-for-frontend services
- Case, workflow, approval, policy, and audit services
- Bounded agent orchestration
- Enterprise model gateway and approved LLM integration
- Retrieval-augmented generation
- Document ingestion, classification, provenance, and revocation
- SAP integration through approved OData, REST, SOAP, RFC, BAPI, IDoc, event, or integration-platform interfaces
- ITSM, Git, CI/CD, monitoring, and knowledge integrations
- ABAP development assistance
- Read-only diagnostics
- Draft and non-production automation
- Carefully selected approved production operations
- Secrets, key, certificate, and workload-identity management
- Threat modeling, testing, deployment, monitoring, recovery, and governance

### 3.2 Out of Scope

The initial platform must not:

- Give an LLM unrestricted SAP credentials
- Allow direct production database updates
- Execute arbitrary RFC functions, SQL, ABAP source, shell commands, or operating-system commands
- Permit an agent to choose arbitrary hosts, destinations, clients, or endpoints
- Allow AI-generated text to serve as authorization
- Allow a model to sign an action manifest
- Allow a model to approve its own proposal
- Release or import unrestricted production transports automatically
- Disable security controls or alter audit records
- Bypass SAP GRC, PAM, segregation-of-duties, CAB, or emergency-access procedures
- Store passwords, tokens, private keys, certificates, or secrets in prompts, logs, source code, vector stores, or agent memory
- Train public or shared models on enterprise production data
- Copy unmasked production data into lower environments
- Treat generated code as production-ready without review, static analysis, testing, and controlled release

---

## 4. Goals and Non-Goals

### 4.1 Goals

- Reduce time spent gathering evidence for SAP incidents and changes
- Improve diagnosis quality through grounded, authorized retrieval
- Improve ABAP quality through assisted design, review, and testing
- Standardize change plans, test plans, rollback plans, and release evidence
- Preserve SAP authorization and organizational-value restrictions
- Prevent prompt injection from becoming tool execution
- Minimize production data exposure to models
- Provide full traceability from request to evidence and execution
- Support safe, progressive automation
- Maintain manual operations when the AI platform is unavailable
- Make every enabled action testable, observable, bounded, and reversible where possible

### 4.2 Non-Goals

- Replacing SAP technical, functional, Basis, security, or business experts
- Fully autonomous production administration
- Replacing SAP GRC, ITSM, CAB, release management, or PAM
- Using model confidence as an authorization decision
- Treating AI output as the only evidence for an operational claim
- Supporting every SAP interface or module in the first release
- Building one all-powerful general-purpose agent

---

## 5. Security and Engineering Principles

1. **Zero trust:** Authenticate and authorize every user, service, request, data source, retrieval, tool call, and target.
2. **Least privilege:** Grant only the permissions required for a specific workflow, tool, environment, system, client, object, and operation.
3. **Separation of duties:** Separate requester, developer, reviewer, approver, executor, and validator roles.
4. **Deterministic enforcement:** Enforce security in code, policies, gateways, and SAP. Prompts are not security controls.
5. **Read-only by default:** Begin with retrieval and diagnostics before introducing write operations.
6. **Human accountability:** Require named approval for production-relevant or consequential actions.
7. **Data minimization:** Send only authorized, relevant, redacted context to the model.
8. **Defense in depth:** Apply controls at the edge, API, workflow, retrieval, model, tool, executor, SAP, network, and audit layers.
9. **Fail closed:** Deny actions if identity, policy, approval, validation, SAP authorization, or audit delivery is unavailable.
10. **Evidence by design:** Produce reconstructable, tamper-resistant records for every significant action.
11. **Progressive autonomy:** Increase automation only after measured safety and reliability gates are met.
12. **Explicit blast radius:** Every tool must define limits on systems, clients, objects, records, fields, time ranges, and transactions.
13. **Independent verification:** The service executing an action must not be the sole authority verifying success.
14. **No ambient authority:** Agents receive task-scoped access, never broad reusable credentials.
15. **Treat retrieved content as untrusted:** Tickets, documents, logs, source code, email, and wiki text can contain malicious instructions.

---

## 6. System Context

### 6.1 Primary Actors

- SAP developer
- SAP functional consultant
- SAP Basis engineer
- SAP security engineer
- Service desk analyst
- Problem manager
- Change manager
- Release manager
- Application owner
- Business process owner
- Platform and SRE engineer
- Security operations analyst
- AI platform owner
- Auditor

### 6.2 External Systems

- SAP ECC and SAP S/4HANA
- SAP BTP services
- SAP Integration Suite or another approved integration platform
- Corporate identity provider
- SAP identity and authorization services
- ITSM and change-management platform
- Git and code-review platform
- CI/CD platform
- Artifact and container registries
- Enterprise LLM or model gateway
- Object storage, metadata database, and vector database
- Vault, KMS, HSM, and PAM
- SIEM, observability, alerting, and incident-management systems

### 6.3 Assumptions

- The enterprise has separate development, test, quality, pre-production, and production environments.
- All production deployments use controlled pipelines.
- Approved SAP interfaces are available or can be created.
- The identity provider supports MFA and service identity.
- SAP authorizations remain the final system-level control.
- The enterprise model endpoint provides tenant isolation, retention controls, and contractual data protection.
- Sensitive fields can be redacted, tokenized, aggregated, or excluded.
- Production write automation will be introduced only after successful advisory and read-only phases.

---

## 7. Target Logical Architecture

```text
+-----------------------------------------------------------------------+
| Users and Enterprise Channels                                         |
| Web portal | Teams/chat | ITSM extension | IDE | Optional OpenClaw    |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Edge and Access Security                                              |
| WAF | API gateway | OAuth/OIDC | MFA | anti-replay | rate limits      |
| request validation | upload quarantine | malware and file scanning    |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Application Control Plane                                             |
| BFF | Case API | Workflow API | Entitlement Service | Context Broker  |
| Policy Enforcement Point | Approval API | Audit and Evidence API      |
+----------------------+-----------------------+------------------------+
                       |                       |
                       v                       v
+----------------------------------+  +---------------------------------+
| AI Orchestration Plane           |  | Knowledge and Model Plane       |
| Bounded workflow graph           |  | Model Gateway                   |
| State machine and checkpoints    |  | DLP and redaction               |
| Prompt templates and versions    |  | Authorized RAG service          |
| Claim-evidence validation        |  | Document store and vector index |
+----------------------+-----------+  +---------------------------------+
                       |
                       | Typed proposal only
                       v
+-----------------------------------------------------------------------+
| Tool Gateway                                                          |
| Tool registry | schema validation | parameter normalization           |
| policy check | approval check | SoD | nonce | expiry | idempotency    |
| transaction limits | evidence capture | execution dispatch            |
+-----------------------------------+-----------------------------------+
                                    |
                                    | Signed execution envelope
                                    v
+-----------------------------------------------------------------------+
| Deterministic Executors                                               |
| SAP read executor | SAP write executor | ITSM | Git | CI/CD           |
| pre-checks | transaction management | post-checks | compensation       |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
| Enterprise Systems                                                    |
| SAP ECC/S4 | BTP | ITSM | Git | CI/CD | monitoring | SIEM            |
+-----------------------------------------------------------------------+

+-----------------------------------------------------------------------+
| Platform and Security Foundation                                      |
| Vault | KMS/HSM | private network | mTLS | service mesh | containers  |
| artifact signing | SBOM | backups | DR | vulnerability management    |
+-----------------------------------------------------------------------+
```

### 7.1 Architectural Rule

No channel, including an optional OpenClaw deployment, may call SAP directly. Every client must call the enterprise API Gateway and pass through the same application, policy, Tool Gateway, and execution controls.

### 7.2 OpenClaw Boundary

OpenClaw may be used as:

- A user channel
- An isolated developer assistant
- A sandboxed non-production automation client
- A client of approved enterprise APIs

OpenClaw must not be used as:

- The production Tool Gateway
- The policy engine
- The approval service
- The secrets broker
- The tenant-isolation boundary
- The authoritative audit service
- The deterministic production executor
- A shared gateway for mutually untrusted users

For mixed-trust users, deploy separate instances, credentials, OS boundaries, and preferably separate hosts or namespaces.

---

## 8. Trust Boundaries

### TB-1: User Device to Enterprise Edge

Threats include stolen sessions, compromised devices, malicious uploads, oversized requests, and automated abuse.

Required controls:

- SSO and MFA
- Conditional access
- Secure session cookies or token storage
- Request and upload limits
- Malware and active-content scanning
- Anti-CSRF where applicable
- Rate limiting and bot detection
- Clear environment and identity display

### TB-2: Edge to Application Control Plane

Required controls:

- Audience, issuer, signature, expiry, and nonce validation
- Signed identity claims
- Strict schemas
- Correlation IDs
- Header sanitization
- No trust in user-supplied role, identity, tenant, system, or client fields

### TB-3: Application to Orchestrator

Required controls:

- Task-scoped service identity
- Authorized case and purpose
- Sanitized and classified inputs
- Bounded workflow definition
- Maximum steps, retries, token use, tool proposals, and duration

### TB-4: Orchestrator to Model Gateway

Required controls:

- Approved model and region allowlists
- DLP, secret detection, and redaction
- Prompt and response size limits
- Model-version pinning
- Restricted retention and logging
- Circuit breakers and quotas
- No silent fallback to weaker privacy terms

### TB-5: Orchestrator to Knowledge Platform

Required controls:

- Entitlement-filtered retrieval before content leaves the retrieval service
- Source provenance
- Version, approval, validity, environment, and classification filters
- Source revocation
- Poisoning detection and quarantine

### TB-6: Orchestrator to Tool Gateway

This is the principal agent safety boundary.

Required controls:

- Typed proposals only
- Independent schema validation
- Independent parameter normalization
- Authoritative workflow-state lookup
- Action policy and risk evaluation
- Approval verification
- Anti-replay and idempotency
- No raw model output passed to adapters

### TB-7: Tool Gateway to Executor

Required controls:

- Signed, short-lived execution envelope
- Exact parameter and target hashes
- Single-use nonce
- Executor allowlist
- Mutual authentication
- Pre-check and post-check requirements

### TB-8: Executor to SAP

Required controls:

- Private connectivity
- Narrow technical roles or principal propagation
- SAP-side authorization
- Destination, system, and client allowlists
- Transaction limits
- SAP audit and application logs
- No dynamic RFC or unrestricted query construction

### TB-9: Production to Non-Production

Required controls:

- Separate accounts, networks, credentials, keys, indexes, model deployments, and destinations
- Masked test data
- Deployment policy preventing production endpoints in lower environments
- No production credential reuse
- Continuous configuration monitoring

---

## 9. Component Responsibilities

### 9.1 Experience Layer

The UI must:

- Display authenticated identity and current environment
- Clearly distinguish recommendation, proposal, approval, and execution
- Show sources and evidence status
- Flag uncertainty and missing evidence
- Show exact action preview for risky operations
- Prevent hidden document instructions from being presented as system authority
- Show approval and execution history
- Support cancellation where the workflow permits it

### 9.2 Backend-for-Frontend

Responsibilities:

- Translate channel-specific requests into canonical API calls
- Enforce channel-level schemas and limits
- Preserve signed user identity
- Add correlation and trace identifiers
- Avoid holding reusable SAP credentials
- Avoid storing unrestricted conversation history

### 9.3 Case Service

Responsibilities:

- Link workflows to authoritative incidents, service requests, problems, or changes
- Validate the user may access the case
- Track business purpose
- Cache only non-sensitive case metadata with explicit TTL
- Never accept model-generated ticket state as authoritative

### 9.4 Context Broker

Responsibilities:

- Determine the minimum authorized context
- Apply data classification and field selection
- Redact, tokenize, aggregate, or reject sensitive fields
- Attach provenance and authorization metadata
- Enforce context size and age limits

### 9.5 Agent Orchestrator

Responsibilities:

- Run bounded state-machine workflows
- Apply versioned prompts and workflow graphs
- Request authorized retrieval
- Produce structured observations, hypotheses, recommendations, and proposals
- Stop on invalid or contradictory states
- Never execute arbitrary model-generated code

### 9.6 Model Gateway

Responsibilities:

- Route only to approved providers and models
- Enforce region and retention policy
- Scan inputs and outputs
- Track token and cost budgets
- Pin or explicitly roll model versions
- Apply timeouts and circuit breakers
- Mask sensitive telemetry

### 9.7 Knowledge Platform

Responsibilities:

- Register authoritative sources
- Scan and parse files in a sandbox
- Manage metadata, ACLs, validity, ownership, and hashes
- Generate embeddings in an approved environment
- Revoke deleted, expired, or superseded material
- Return only authorized content

### 9.8 Policy Decision Point

Responsibilities:

- Evaluate deterministic facts
- Return allow, deny, require approval, or manual-only
- Specify constraints and required approver roles
- Version policy decisions
- Never execute actions

### 9.9 Approval Service

Responsibilities:

- Present independently generated action facts
- Capture named human approvals
- Bind approval to exact target and parameter hashes
- Enforce expiry, nonce, session recency, step-up authentication, and SoD
- Support revocation

### 9.10 Tool Gateway

Responsibilities:

- Register narrow tools
- Validate and normalize requests
- Recheck policy and approvals
- Issue signed execution envelopes
- Enforce idempotency, volume, and transaction limits
- Record evidence
- Dispatch only to registered executors

### 9.11 Deterministic Executor

Responsibilities:

- Accept only valid signed envelopes
- Revalidate target and current state
- Run pre-checks
- Invoke one allowlisted business operation
- Handle commit, rollback, or compensation
- Run post-checks
- Record authoritative outcomes
- Stop on unexpected state

---

## 10. Identity and Delegation Model

### 10.1 Human Identity

Use:

- SSO through the corporate identity provider
- MFA for privileged and production functions
- Conditional access based on trusted device, network, risk, and location policy
- Step-up authentication before Tier 3 actions
- Short privileged-session lifetime
- Group and attribute-based authorization
- Recertification and rapid revocation

### 10.2 Workload Identity

Use:

- Unique identity per service and environment
- Short-lived federated credentials where supported
- mTLS or equivalent workload authentication
- No shared credentials across unrelated executors
- Separate production and non-production identities
- Vault-backed rotation and revocation

### 10.3 Delegation Types

Every tool request must identify one of four modes:

1. `USER_DELEGATED_READ`
2. `USER_DELEGATED_WRITE`
3. `SYSTEM_INITIATED_READ`
4. `SYSTEM_INITIATED_WRITE`

System-initiated writes should be disabled initially and require explicit governance approval before introduction.

### 10.4 Canonical Security Context

```json
{
  "tenantId": "enterprise-tenant",
  "subject": {
    "userId": "employee-123",
    "sessionId": "session-456",
    "authenticationMethods": ["SSO", "MFA"],
    "authenticatedAt": "2026-09-08T12:00:00Z"
  },
  "actor": {
    "serviceId": "diagnostic-orchestrator-prod",
    "agentId": "sap-diagnostic-agent",
    "agentVersion": "3.2.1"
  },
  "delegation": {
    "type": "USER_DELEGATED_READ",
    "purpose": "INCIDENT_DIAGNOSIS",
    "caseId": "INC0012345"
  },
  "target": {
    "environment": "PRODUCTION",
    "systemId": "PRD",
    "client": "100"
  }
}
```

### 10.5 Effective Permission

```text
Effective permission =
    human entitlements
  intersect workload entitlements
  intersect workflow permissions
  intersect tool permissions
  intersect target-system policy
  intersect current case/change state
```

A prompt can never add to this intersection.

---

## 11. Authorization Model

### 11.1 Authorization Inputs

- Authenticated user
- Workload identity
- Delegation type and business purpose
- User groups and attributes
- SAP roles and organizational restrictions
- Tool and action risk tier
- Target environment, system, and client
- Case and change status
- Maintenance window
- Data classification
- Required and completed approvals
- Segregation-of-duties conflicts
- Emergency-access state
- Tool-specific constraints

### 11.2 Authorization Outcomes

- `ALLOW`
- `DENY`
- `REQUIRE_APPROVAL`
- `MANUAL_ONLY`

### 11.3 Model Confidence Rule

Model confidence must not authorize or reduce controls. It may only influence routing to a human specialist.

```text
Low evidence          -> specialist review
Conflicting evidence  -> specialist review
High impact           -> specialist review
Insufficient data     -> request more information
Unsupported claim     -> remove or label as hypothesis
```

### 11.4 Fail-Closed Conditions

Deny execution when:

- Identity is missing, expired, or ambiguous
- The authoritative case cannot be loaded
- Policy service is unavailable
- Required approval cannot be verified
- Approval parameters differ from execution parameters
- Maintenance-window validation fails
- Audit delivery is unavailable for a write action
- SAP target cannot be resolved from the approved registry
- System or client differs from the manifest
- Post-check definition is missing for a write tool

---

## 12. Agent and Workflow Design

### 12.1 Agent Roles

#### Intake Module

- Normalize requests
- Identify SAP system, client, module, impact, and urgency
- Detect sensitive data
- Link a case
- No SAP tools

#### Diagnostic Module

- Retrieve authorized logs and runbooks
- Execute approved read-only checks
- Separate observations from hypotheses
- Cite evidence

#### Development Module

- Explain ABAP and integration code
- Suggest controlled patches
- Generate ABAP Unit test candidates
- Create a draft branch only through an approved tool
- Cannot merge, release a transport, or deploy

#### Change Planning Module

- Draft impact, implementation, validation, monitoring, and rollback plans
- Verify required fields
- Create draft records only unless deterministic workflow advances them

#### Knowledge Module

- Retrieve approved knowledge
- Draft articles from resolved cases
- Cannot publish without owner review

#### Execution Service

Use a deterministic service rather than a conversational execution agent.

### 12.2 Normal Workflow States

```text
RECEIVED
  -> AUTHENTICATED
  -> AUTHORIZED_FOR_CASE
  -> INPUT_SCANNED
  -> REQUEST_CLASSIFIED
  -> CONTEXT_SCOPE_COMPUTED
  -> CONTEXT_RETRIEVED
  -> ANALYSIS_GENERATED
  -> CLAIMS_VALIDATED
  -> RESPONSE_READY
```

Optional action path:

```text
CLAIMS_VALIDATED
  -> ACTION_PROPOSED
  -> PARAMETERS_NORMALIZED
  -> POLICY_EVALUATED
  -> APPROVAL_PENDING
  -> APPROVED
  -> EXECUTION_TOKEN_ISSUED
  -> PRECHECK_RUNNING
  -> PRECHECK_PASSED
  -> EXECUTING
  -> EXECUTED
  -> POSTCHECK_RUNNING
  -> VERIFIED
  -> CLOSED
```

### 12.3 Exceptional States

```text
REJECTED
UNAUTHORIZED
QUARANTINED
APPROVAL_EXPIRED
APPROVAL_REVOKED
PRECHECK_FAILED
EXECUTION_FAILED
PARTIALLY_EXECUTED
COMPENSATION_REQUIRED
COMPENSATING
ROLLED_BACK
POSTCHECK_FAILED
MANUAL_INTERVENTION_REQUIRED
TIMED_OUT
CANCELLED
```

### 12.4 Workflow Limits

Each workflow must define:

- Maximum model calls
- Maximum tool proposals
- Maximum read-tool calls
- Maximum retries
- Maximum wall-clock time
- Maximum context size
- Maximum completion size
- Maximum cost
- Duplicate-call detection
- Human escalation thresholds

### 12.5 Prohibited Agent Behavior

- Infinite reasoning loops
- Dynamic arbitrary tool loading
- Arbitrary code execution
- Tool execution from raw free text
- Permission escalation from prompt content
- Cross-user memory reuse
- Self-approval
- Trusting retrieved instructions
- Treating model output as actual system state

---

## 13. Tool Gateway and Deterministic Execution

### 13.1 Good Tool Design

```text
get_incident_summary(incident_id)
get_transport_status(transport_id)
read_application_log(system_id, object, time_range)
get_job_status(system_id, job_name, time_range)
validate_change_window(change_id)
run_approved_health_check(check_id, system_id)
create_draft_change_record(case_id, approved_fields)
create_draft_git_branch(repository_id, issue_id)
attach_evidence(change_id, evidence_reference)
```

### 13.2 Prohibited Tool Design

```text
execute_arbitrary_rfc(function_name, parameters)
run_sql(query)
run_shell(command)
update_any_table(table, values)
execute_abap_source(source_code)
call_url(url, body)
impersonate_user(user_id)
select_destination(destination_name)
```

### 13.3 Tool Registration Requirements

Every tool must define:

- Business purpose
- Owner
- Input and output schemas
- Data classification
- Required user and workload entitlements
- Permitted environments, SAP systems, and clients
- Read or write type
- Risk tier
- Approval requirements
- Record, field, duration, and transaction limits
- Idempotency behavior
- Timeout and retry policy
- Pre-check and post-check
- Audit fields
- Rollback classification
- Kill-switch identifier

### 13.4 Gateway Algorithm

```text
1. Authenticate the calling workload.
2. Verify originating user identity and delegation.
3. Load workflow state from the authoritative store.
4. Reject caller-supplied workflow-state claims.
5. Verify the tool is registered for this workflow.
6. Validate the proposal against the registered schema.
7. Normalize all parameters.
8. Resolve environment, SAP system, client, and endpoint from registry.
9. Reject free-form host, destination, function, table, or endpoint names.
10. Evaluate deterministic policy.
11. Determine the action risk tier.
12. Load and verify required approvals.
13. Verify segregation of duties.
14. Verify ticket, change, and maintenance-window state.
15. Generate a short-lived signed execution envelope.
16. Invoke the registered deterministic executor.
17. Capture before-state evidence.
18. Execute once using an idempotency key.
19. Capture the result and system reference.
20. Run independent post-checks.
21. Close, compensate, roll back, or escalate.
```

### 13.5 Rollback Categories

```text
ATOMIC_ROLLBACK
COMPENSATING_TRANSACTION
RESTORE_FROM_SNAPSHOT
FORWARD_FIX_ONLY
MANUAL_RECOVERY
NOT_REVERSIBLE
```

Recommended rule:

```text
If risk tier is 3 or higher and rollback category is
FORWARD_FIX_ONLY, MANUAL_RECOVERY, or NOT_REVERSIBLE,
automated execution is not allowed.
```

---

## 14. SAP Integration Design

### 14.1 General Rules

- Use approved SAP APIs and services.
- Avoid direct database access.
- Use a separate identity per environment and integration.
- Validate SAP system ID and client at every layer.
- Use private connectivity and encrypted transport.
- Preserve SAP authorization enforcement.
- Use SAP Security Audit Log and application logs where applicable.
- Do not allow caller-selected destinations or function names.

### 14.2 Read Tools

Read tools must enforce:

- Fixed data sources
- Fixed field projections
- Maximum rows
- Maximum date or time range
- Pagination limits
- Sensitive-field masking
- Query timeouts
- System and client allowlists
- No unrestricted OData expansion or filtering
- No arbitrary table reads

### 14.3 Write Tools

Write tools must enforce:

- One defined business operation
- One approved BAPI, OData operation, or service
- Mandatory pre-validation
- Exact transaction boundary
- Idempotency
- Before and after evidence
- Maximum affected-object count
- Explicit commit or rollback behavior
- Independent post-check
- Compensation where supported

### 14.4 Principal Propagation and Technical Accounts

Use principal propagation when the user’s SAP identity and authorization must remain visible and the approved connectivity pattern supports it. Use narrow technical accounts for system-managed operations only when justified.

In every case:

- External authorization supplements SAP authorization.
- SAP remains responsible for final object and organizational-value enforcement.
- A technical account must not gain broad rights merely because an upstream policy exists.

### 14.5 ABAP Wrapper Pattern

Create SAP-side wrappers that:

- Expose one business operation
- Validate the caller and purpose
- Validate system/client assumptions
- Perform authority checks
- Validate all business inputs
- Enforce affected-record limits
- Write SAP application logs
- Return a typed, minimal response
- Support test mode where possible

---

## 15. Knowledge and RAG Architecture

### 15.1 Ingestion Pipeline

```text
Registered source
  -> publisher authorization
  -> malware and active-content scan
  -> sandboxed parsing
  -> hidden-text and metadata inspection
  -> data classification
  -> secret and personal-data detection
  -> redaction, tokenization, or rejection
  -> owner and ACL assignment
  -> version and integrity hash
  -> approval workflow
  -> approved embedding generation
  -> document and index storage
```

### 15.2 Required Document Metadata

```json
{
  "documentId": "KB-431",
  "version": "7",
  "chunkId": "KB-431-v7-c12",
  "sourceSystem": "ENTERPRISE_WIKI",
  "owner": "SAP-FI-SUPPORT",
  "classification": "INTERNAL",
  "environment": "PRODUCTION",
  "systemScope": ["PRD"],
  "module": ["FI"],
  "approved": true,
  "effectiveFrom": "2026-08-01",
  "expiresAt": "2027-08-01",
  "integrityHash": "sha256:example",
  "aclVersion": "19",
  "retentionClass": "OPERATIONS_KNOWLEDGE"
}
```

### 15.3 Retrieval Sequence

```text
Authenticate user
  -> resolve entitlements
  -> determine allowed collections
  -> apply metadata security filters
  -> retrieve candidate chunks
  -> revalidate source ACL
  -> remove expired or superseded versions
  -> rerank
  -> redact
  -> attach provenance
  -> construct minimal context
```

Filtering must occur before unauthorized chunks leave the retrieval service.

### 15.4 Index Isolation

Separate indexes or enforce equivalent hard partitions by:

- Tenant
- Environment
- Classification
- SAP system
- Business domain
- Legal residency
- Operational versus development knowledge

### 15.5 Cache and Memory Isolation

Every stateful object must be partitioned by:

```text
tenant_id
+ environment
+ user_security_context
+ case_id
+ workflow_instance_id
+ data_classification
```

A safe cache key includes an entitlement hash:

```text
sha256(
  tenant_id
  | environment
  | subject_entitlement_hash
  | case_id
  | source_acl_version
  | normalized_query
)
```

Do not key authorized caches only by query text, case number, SAP system, tool, or conversation ID.

### 15.6 Knowledge Revocation

When a source is deleted, expired, revoked, or superseded:

1. Mark it unavailable in the source registry.
2. Prevent new retrieval immediately.
3. Remove or tombstone chunks in the active index.
4. Invalidate caches.
5. Retain only legally required audit references.
6. Identify important outputs or actions influenced by poisoned content.

---

## 16. Data Protection and Privacy

### 16.1 Data Categories

- Public
- Internal
- Confidential
- Restricted or regulated
- Security secret

### 16.2 Context Minimization

```text
Authorized source data
  -> field classification
  -> purpose-based field selection
  -> secret and sensitive-data detection
  -> redaction/tokenization/aggregation
  -> range and size limitation
  -> provenance attachment
  -> model context
```

### 16.3 Data Rules

- Never send secrets to the model.
- Never embed secrets.
- Do not log full production payloads by default.
- Redact personal and sensitive business fields.
- Store reversible token mappings only when required and in a protected service.
- Keep production and lower-environment data separate.
- Define retention for prompts, completions, traces, caches, documents, embeddings, and audit data.
- Delete derived artifacts when the authoritative source is deleted unless legal retention applies.
- Enforce regional and residency requirements.

### 16.4 Prompt and Completion Logging

Full prompts and completions should be disabled by default. If enabled for an approved case:

- Document the purpose
- Mask sensitive values
- Encrypt separately
- Restrict access
- Set a short retention period
- Obtain legal and privacy approval
- Record who accessed the logs

---

## 17. Approval and Action Manifest Design

### 17.1 Approval Experience

The approval screen must show independently generated facts:

- Exact normalized tool
- Exact environment, system, and client
- Read or write type
- Before-state
- Proposed after-state
- Exact changed fields
- Maximum blast radius
- Change record and business justification
- Maintenance window
- Requester and executor identity
- Pre-check, post-check, and rollback method
- Parameter and target hashes
- Approval expiry
- Unresolved warnings
- Whether AI proposed any values

The model-generated summary is supplementary and not authoritative.

### 17.2 Tool Proposal

```json
{
  "proposalId": "prop-123",
  "workflowId": "wf-456",
  "tool": "get_transport_status",
  "target": {
    "systemId": "QAS",
    "client": "100"
  },
  "parameters": {
    "transportId": "QASWK900123"
  },
  "reason": "Validate transport readiness",
  "evidenceIds": ["change-918", "transport-ref-33"]
}
```

The proposal is untrusted, unsigned, and not an execution token.

### 17.3 Policy Decision

```json
{
  "decisionId": "pd-781",
  "decision": "REQUIRE_APPROVAL",
  "riskTier": 3,
  "normalizedTool": "run_approved_health_check",
  "normalizedTarget": {
    "environment": "PRODUCTION",
    "systemId": "PRD",
    "client": "100"
  },
  "constraints": {
    "maximumRecords": 1,
    "allowSensitiveFields": false
  },
  "requiredApproverRoles": [
    "SAP_RELEASE_MANAGER",
    "APPLICATION_OWNER"
  ],
  "policyVersion": "sap-agent-policy-2026.09.08",
  "validUntil": "2026-09-08T12:10:00Z"
}
```

### 17.4 Approval Record

```json
{
  "approvalId": "apr-332",
  "decisionId": "pd-781",
  "approverId": "employee-approver",
  "approverRole": "SAP_RELEASE_MANAGER",
  "parameterHash": "sha256:example",
  "targetHash": "sha256:example",
  "approvedAt": "2026-09-08T12:05:00Z",
  "expiresAt": "2026-09-08T12:10:00Z",
  "nonce": "single-use-value",
  "signatureReference": "kms-signature-991"
}
```

### 17.5 Secure Action Manifest

```json
{
  "manifestVersion": "1.0",
  "actionId": "act-7c8594d1",
  "caseId": "INC0012345",
  "requestedBy": "enterprise-user-id",
  "actorService": "tool-gateway-prod",
  "tool": "run_approved_health_check",
  "target": {
    "environment": "PRODUCTION",
    "sapSystemId": "PRD",
    "client": "100"
  },
  "parameters": {
    "checkId": "Z_APP_HEALTH_04",
    "timeRangeMinutes": 15
  },
  "riskTier": 1,
  "policyDecisionId": "pol-991783",
  "approvalIds": [],
  "parameterHash": "sha256:example",
  "targetHash": "sha256:example",
  "issuedAt": "2026-09-08T12:00:00Z",
  "expiresAt": "2026-09-08T12:05:00Z",
  "nonce": "single-use-value",
  "idempotencyKey": "INC0012345-Z_APP_HEALTH_04-20260908T1200",
  "signature": "detached-signature-reference"
}
```

### 17.6 Execution Result

```json
{
  "actionId": "act-7c8594d1",
  "status": "SUCCEEDED",
  "startedAt": "2026-09-08T12:06:10Z",
  "completedAt": "2026-09-08T12:06:12Z",
  "sapReference": {
    "transactionId": "sap-transaction-reference"
  },
  "verification": {
    "status": "PASSED",
    "checkIds": ["application-health-check"]
  },
  "evidenceIds": ["ev-991", "ev-992"]
}
```

---

## 18. End-to-End Workflows

### 18.1 Incident Diagnosis

1. User authenticates with SSO and MFA where required.
2. The portal creates a correlation ID.
3. The Case Service loads or creates the ITSM incident.
4. Input and attachments are scanned.
5. The Intake Module identifies target system, client, module, impact, and sensitivity.
6. Entitlements are resolved.
7. The Context Broker constructs a minimal authorized context.
8. RAG retrieves approved, valid, authorized runbooks.
9. Read-only diagnostics run through the Tool Gateway.
10. The Diagnostic Module creates observations and ranked hypotheses.
11. A claim-evidence validator checks factual support.
12. High-severity, low-evidence, or conflicting results are escalated.
13. Remediation options include impact, risk, validation, and rollback.
14. Any proposed write follows the change and approval path.
15. Post-resolution, a draft knowledge article may be created.

### 18.2 Service Request

1. Authenticate the requester.
2. Resolve the catalog item.
3. Validate required fields and eligibility.
4. Evaluate entitlement and SoD.
5. Retrieve approved fulfillment instructions.
6. Prepare a fulfillment plan and risk tier.
7. Obtain required manager, owner, security, or GRC approval.
8. Execute through an approved API or route to a human fulfiller.
9. Verify the result.
10. Record expiry for temporary access.
11. Attach evidence to the request.

Privileged access requests remain governed by the authoritative SAP GRC or access-management process.

### 18.3 Change Request

1. Create or link the change record.
2. Capture business justification and target systems.
3. Analyze affected code, configuration, jobs, interfaces, roles, and transports.
4. Classify the change using deterministic enterprise policy.
5. Draft implementation, test, validation, monitoring, and rollback plans.
6. Link requirements, commits, transports, and evidence.
7. Run quality, security, and SoD checks.
8. Obtain required approval.
9. Verify the release window and transport order.
10. Deploy through the official pipeline or SAP release process.
11. Run smoke tests and business validation.
12. Close only when required evidence is complete.

### 18.4 ABAP Development

#### Requirements and Design

- Convert the requirement into acceptance criteria.
- Identify packages, classes, programs, CDS views, enhancements, interfaces, jobs, and authorization checks.
- Document clean-core and extensibility decisions.
- Define performance, volume, security, and data-protection requirements.

#### Development

- Generate code only in a controlled workspace, branch, or development system.
- Apply naming, package, exception, logging, and documentation standards.
- Avoid hard-coded credentials, system IDs, clients, destinations, and personal data.
- Prefer released APIs and approved extension points.

#### Quality

- Syntax and activation checks
- ABAP Unit tests
- ATC and security-focused checks
- Authorization tests
- Performance checks
- Secret and dependency scanning for adjacent services
- Peer and functional review
- Integration, regression, negative, volume, and performance testing

#### Release

- Validate transport ownership and object list.
- Detect collisions and dependency order.
- Resolve critical findings.
- Obtain approval.
- Import through controlled tools and schedules.
- Perform post-import verification.
- Preserve rollback or forward-fix procedures.

### 18.5 Knowledge Automation

1. Accept content only from registered sources and publishers.
2. Scan and sandbox the content.
3. Detect secrets, personal data, and hidden instructions.
4. Attach classification, provenance, ACL, owner, version, and expiry.
5. Require approval for operational runbooks.
6. Generate embeddings in an approved environment.
7. Retrieve using entitlement and metadata filters.
8. Cite exact source versions.
9. Draft new content from validated outcomes.
10. Publish only after owner review.
11. Revoke expired or poisoned content from stores, indexes, and caches.

---

## 19. Action Risk Classification

### Tier 0: Informational

Examples:

- Explain an error message
- Summarize an authorized incident
- Retrieve a broadly available internal standard

Controls:

- Authentication
- Retrieval authorization
- Input and output scanning
- Audit event

### Tier 1: Read-Only Diagnostic

Examples:

- Read approved application logs
- Check job status
- Check transport status

Additional controls:

- Tool-specific authorization
- System and client allowlists
- Field, row, query, and time limits
- Sensitive-field masking

### Tier 2: Draft or Non-Production Write

Examples:

- Create a draft change
- Create a proposal branch
- Execute a reversible lower-environment operation

Additional controls:

- Ticket linkage
- Idempotency
- Independent validation
- Review before promotion

### Tier 3: Production-Relevant and Privileged

Examples:

- Trigger one approved production job
- Run a tightly bounded remediation
- Perform a controlled configuration action

Additional controls:

- Named approvals
- SoD verification
- Valid change and maintenance window
- Step-up authentication
- Signed single-use action token
- Pre-check, post-check, rollback, and enhanced monitoring

### Tier 4: Prohibited for AI-Initiated Execution

Examples:

- Unrestricted transport release or import
- Direct table update
- Security-control disablement
- Privileged user or role creation outside GRC
- Arbitrary ABAP, SQL, RFC, shell, or endpoint invocation
- Audit alteration
- Bulk sensitive-data export

Tier 4 actions must use established privileged procedures and authorized personnel.

---

## 20. Threat Model

### 20.1 Assets

- SAP business and configuration data
- Customer, employee, vendor, payroll, and financial data
- Credentials, tokens, certificates, and destinations
- Source code, packages, transports, and pipelines
- Incident, problem, request, and change records
- Prompts, policies, agent graphs, evaluators, and tool schemas
- Model inputs, outputs, traces, and memory
- Vector indexes and documents
- Approval and audit evidence
- SAP availability and integrity

### 20.2 Threat Actors

- External attacker
- Malicious or careless insider
- Compromised user device
- Compromised support or developer account
- Malicious document publisher
- Abused service identity
- Compromised dependency or container
- Misconfigured cloud or model service
- Over-privileged administrator

### 20.3 STRIDE Summary

#### Spoofing

Threats:

- Stolen session or token
- Forged service identity
- Impersonated approver
- Cross-environment token misuse

Controls:

- MFA, conditional access, signed short-lived tokens, audience validation, workload identity, mTLS, step-up authentication, revocation, anomaly detection

#### Tampering

Threats:

- Modified tool parameters
- Poisoned knowledge
- Altered prompts or policy
- Modified approval evidence
- Manipulated code or transport

Controls:

- TLS, request signing, strict schemas, hashes, protected sources, version control, CODEOWNERS, append-only evidence, signed artifacts

#### Repudiation

Threats:

- User denies request or approval
- Service action lacks traceability
- Model, prompt, or policy version cannot be reconstructed

Controls:

- Correlation IDs, signed events, synchronized time, version telemetry, immutable retention, execution references

#### Information Disclosure

Threats:

- Production data in prompts or logs
- Unauthorized retrieval
- Cross-user memory leakage
- Read-tool enumeration
- Provider retention exposure

Controls:

- Data minimization, redaction, ACL retrieval, hard isolation, quotas, DLP, encryption, retention controls

#### Denial of Service

Threats:

- API flooding
- Agent loops
- Expensive retrieval
- SAP connection exhaustion
- Parser failure

Controls:

- WAF, quotas, step and cost budgets, circuit breakers, bulkheads, sandboxed parsing, graceful manual fallback

#### Elevation of Privilege

Threats:

- Prompt requests administrator behavior
- Generic tools accept arbitrary functions
- Technical accounts have broad rights
- Agent bypasses approval
- Lower-environment credentials work in production

Controls:

- Deterministic authorization, narrow tools, least-privilege SAP roles, SoD, GRC integration, separate identities, entitlement review

### 20.4 AI-Specific Abuse Cases

#### Direct Prompt Injection

Mitigations:

- Treat user content as data.
- Never grant capability from prompt text.
- Independently authorize retrieval and tools.
- Enforce output DLP and limits.

#### Indirect Prompt Injection

Mitigations:

- Treat tickets, documents, logs, code, and wiki pages as untrusted.
- Separate instructions from retrieved content.
- Scan and classify documents.
- Block tool execution when suspicious content influences the workflow.

#### Tool Abuse and Goal Hijacking

Mitigations:

- Workflow-specific tool allowlists
- Exact parameter binding
- Independent policy and approval
- Blast-radius limits
- Previews and post-checks

#### Memory Poisoning

Mitigations:

- No unrestricted long-term conversational memory
- Per-user and per-case partitioning
- Provenance and expiry
- Controlled writes to memory
- Review and revocation of persistent knowledge

#### RAG Poisoning

Mitigations:

- Registered publishers
- Approval workflow
- Integrity hashes
- Trusted collections
- Source citations
- Quarantine and revocation

#### Slow Data Exfiltration

Mitigations:

- Aggregate quotas across sessions
- Field and record limits
- Enumeration detection
- Purpose-bound access
- DLP and egress monitoring

#### Hallucinated Operational Claims

Mitigations:

- Structured observations and hypotheses
- Exact citations
- Claim-evidence verification
- Deterministic system checks
- No execution based on unsupported claims

#### Approval Manipulation

Mitigations:

- Independent approval facts
- Exact before and after values
- Parameter hashes
- Approval rate limits
- SoD and second approval for higher-risk actions
- Clear warnings for AI-proposed values

#### Supply-Chain Compromise

Mitigations:

- Locked dependencies
- Trusted registries
- SBOM
- Signatures and provenance
- Scanning
- Minimal images
- Runtime restrictions
- Rapid revocation and rebuild

#### Cross-Environment Contamination

Mitigations:

- Separate accounts, networks, identities, vaults, models, and indexes
- Mandatory environment tags
- Masked test data
- Deployment prevention policies
- Continuous drift detection

---

## 21. Secure Development Lifecycle

### 21.1 Planning

- Define use cases and prohibited actions.
- Name business, SAP, data, model, security, and platform owners.
- Complete architecture, privacy, data, and threat reviews.
- Classify tools and data.
- Define measurable safety and reliability objectives.

### 21.2 Design

- Create context, container, trust-boundary, and data-flow diagrams.
- Define API and event contracts.
- Define identity propagation.
- Define authorization and SoD rules.
- Define error, retry, rollback, and idempotency behavior.
- Create abuse cases before implementation.

### 21.3 Implementation

- TypeScript strict mode for TypeScript services
- Strong schemas at every trust boundary
- Secure defaults
- No unsafe dynamic evaluation
- Centralized error handling
- Structured redacted logs
- Dependency pinning
- Mandatory peer review
- Security review for adapters, policies, tool definitions, and prompts

### 21.4 Review

- Protected branches
- Required reviewers
- CODEOWNERS for security-sensitive modules
- Verified commits where required
- No direct production changes
- Separation between author, approver, and production executor

---

## 22. Repository and Code Organization

```text
sap-ai-agent-platform/
  apps/
    web-portal/
    api-service/
    agent-orchestrator/
    context-broker/
    retrieval-service/
    tool-gateway/
    approval-service/
    audit-service/
  executors/
    sap-read-executor/
    sap-write-executor/
    itsm-executor/
    git-executor/
    cicd-executor/
  packages/
    contracts/
    identity/
    policy-client/
    telemetry/
    redaction/
    evidence/
    sap-adapters/
    tool-registry/
  prompts/
    templates/
    schemas/
    evaluations/
  policies/
    authorization/
    data-handling/
    action-risk/
    segregation-of-duties/
  infrastructure/
    modules/
    environments/
      development/
      test/
      quality/
      preproduction/
      production/
  tests/
    unit/
    integration/
    contract/
    authorization/
    adversarial/
    evaluations/
    resilience/
    performance/
  docs/
    architecture/
    decisions/
    threat-model/
    runbooks/
    tool-catalog/
    data-inventory/
    release/
```

### 22.1 Suggested Technology Allocation

Use TypeScript for:

- Web portal
- API and BFF services
- Case and approval APIs
- Tool Gateway
- ITSM, Git, and CI/CD integrations

Use Python for:

- Bounded AI workflow orchestration
- Retrieval reranking
- Document processing
- Evaluation pipelines
- Data classification support

Use ABAP and SAP-native services for:

- SAP-side authorization
- Business validation
- Safe wrapper APIs
- Transaction control
- Application logging
- Domain-specific pre-checks and post-checks

Use a deterministic policy engine such as OPA, Cedar, a corporate entitlement service, or an approved equivalent. The chosen engine must support versioning, testing, explainable decisions, and fail-closed behavior.

---

## 23. API and Event Contracts

### 23.1 General API Requirements

- OpenAPI specifications
- Versioned endpoints
- Strict request and response schemas
- Correlation and trace IDs
- Idempotency keys for writes
- Stable error codes
- No sensitive data in error messages
- Explicit pagination and size limits
- Content type enforcement

### 23.2 Claim-Evidence Response

```json
{
  "observations": [
    {
      "claim": "Batch job ZFI_CLOSE_01 failed at 12:14 UTC",
      "evidenceIds": ["ev-1298"],
      "verificationStatus": "VERIFIED"
    }
  ],
  "hypotheses": [
    {
      "claim": "The failure may be related to a locked posting period",
      "evidenceIds": ["ev-1298", "kb-431-v7"],
      "verificationStatus": "HYPOTHESIS"
    }
  ],
  "recommendations": [
    {
      "description": "Validate posting-period configuration",
      "executionAllowed": false,
      "requiredTool": "get_posting_period_status"
    }
  ]
}
```

### 23.3 Audit Event

```json
{
  "eventId": "evt-123",
  "eventType": "TOOL_EXECUTION_COMPLETED",
  "timestamp": "2026-09-08T12:06:12Z",
  "correlationId": "corr-456",
  "workflowId": "wf-789",
  "caseId": "INC0012345",
  "subjectId": "employee-123",
  "actorServiceId": "sap-read-executor-prod",
  "tool": "run_approved_health_check",
  "toolVersion": "2.1.0",
  "policyVersion": "sap-agent-policy-2026.09.08",
  "promptVersion": "diagnostic-v18",
  "modelId": "approved-model-deployment",
  "targetHash": "sha256:example",
  "parameterHash": "sha256:example",
  "outcome": "SUCCEEDED",
  "evidenceIds": ["ev-991", "ev-992"]
}
```

---

## 24. Policy-as-Code Design

### 24.1 Policy Domains

- User and workload authorization
- Data handling
- Retrieval access
- Tool eligibility
- Risk classification
- Approval requirements
- Segregation of duties
- Environment separation
- Maintenance window
- Emergency access
- Retention and logging

### 24.2 Example Policy Logic

```text
Deny when target environment is production and tool is not production-approved.
Deny when the user may access the case but not the SAP system.
Deny when a write proposal lacks an authoritative change record.
Deny when requester and sole approver are the same person.
Require approval for every Tier 3 action.
Require step-up authentication for Tier 3.
Deny if approval hash differs from normalized parameter hash.
Deny when the execution time is outside the approved window.
Deny when the action nonce was already used.
Deny when post-check or rollback metadata is missing.
```

### 24.3 Policy Engineering Rules

- Policies are version-controlled production artifacts.
- Every policy change requires tests.
- Privileged policy changes require security review.
- Policy decisions must include reason codes.
- Rollback to a previous policy version must be supported.
- The runtime must record the exact policy version used.

---

## 25. Testing and AI Evaluation

### 25.1 Unit Tests

Test:

- Schemas
- Redaction
- Classification
- Policy decisions
- Tool constraints
- State transitions
- Output structure
- Retry and timeout behavior
- Idempotency
- Hash and signature verification

### 25.2 Integration Tests

Test:

- Identity and token exchange
- SAP authorization failures
- OData, RFC, BAPI, and network errors
- Transaction rollback
- ITSM and approval integration
- RAG ACL filters
- Audit propagation
- Key rotation

### 25.3 AI Evaluation Sets

Maintain versioned tests for:

- Intent classification
- SAP error diagnosis
- Grounded answering
- Correct refusal
- Prompt injection resistance
- Sensitive-data handling
- Tool selection
- Parameter correctness
- Unsupported claims
- Multilingual behavior

Track separately:

- Unauthorized-action rate
- Sensitive-data leakage rate
- Cross-user retrieval rate
- Unsupported operational claim rate
- Incorrect tool-selection rate
- Incorrect parameter rate
- Correct refusal rate
- Human override rate

### 25.4 Adversarial Tests

Include:

- Direct and indirect prompt injection
- Encoded and obfuscated instructions
- Hidden document text
- Malicious file formats
- Cross-user and cross-tenant access
- Approval replay
- Parameter substitution
- Slow enumeration
- Tool-loop exhaustion
- Knowledge poisoning
- Model fallback
- Compromised credential scenarios
- Memory poisoning
- Goal hijacking

### 25.5 Resilience and Performance

Test:

- Peak concurrent users
- SAP latency and pool exhaustion
- Model outage
- Vector-store degradation
- Queue backlog
- Regional failure
- Vault or KMS outage
- Audit-service outage
- Partial execution
- Backup restoration

### 25.6 Release Blockers

Fail a release when:

- Critical or prohibited vulnerabilities remain
- Unauthorized-access tests fail
- Prompt injection enables a prohibited action
- Cross-user or cross-environment retrieval occurs
- Approval replay succeeds
- Audit events are incomplete
- Rollback is untested
- Required evaluation thresholds are not met
- Required owners have not approved release

---

## 26. CI/CD and Supply-Chain Security

### 26.1 Pipeline

```text
Commit
  -> formatting and linting
  -> unit and contract tests
  -> secret scanning
  -> SAST
  -> dependency and license scanning
  -> build
  -> SBOM generation
  -> artifact signing
  -> container and IaC scanning
  -> deploy to development
  -> integration and AI evaluations
  -> deploy to test and quality
  -> adversarial, security, and resilience tests
  -> release approval
  -> staged production deployment
  -> post-deployment verification
```

### 26.2 Artifact Rules

- Immutable versioned artifacts
- Trusted private registries
- Provenance and signatures
- SBOM per release
- No build in production
- Promote the same artifact across environments
- Emergency patch process with retrospective review

### 26.3 Prompt and Policy Delivery

Prompts, workflow graphs, tool schemas, evaluators, model configuration, and policy are production artifacts. They require:

- Version control
- Review
- Automated regression evaluation
- Controlled promotion
- Runtime version telemetry
- Rollback

---

## 27. Environment and Deployment Architecture

### 27.1 Environments

- Local isolated development
- Shared development
- Test
- Quality or UAT
- Pre-production
- Production

Separate per environment:

- Account or subscription where practical
- Network
- Service identities
- Vault and encryption keys
- Model deployments
- Vector indexes and document storage
- SAP destinations
- ITSM credentials
- Logging, monitoring, and retention

### 27.2 Network Controls

- Private endpoints where available
- Deny-by-default ingress and egress
- Egress proxy and domain allowlists
- WAF
- Segmentation among edge, application, AI, data, and integration tiers
- No public administrative access
- Approved privileged access paths

### 27.3 Runtime Controls

- Minimal non-root containers
- Read-only filesystems where possible
- Dropped Linux capabilities
- Resource limits
- Network policies
- Runtime monitoring
- Image signing and admission control
- Regular base-image rebuilds
- No long-lived secrets in container images or plain environment variables

### 27.4 Rollout Modes

1. **Shadow:** Recommendations are evaluated but not shown or executed.
2. **Advisory:** Authorized users receive grounded answers, no write tools.
3. **Read-only diagnostics:** Narrow production reads are enabled.
4. **Draft automation:** Draft ITSM records and code branches are enabled.
5. **Bounded non-production execution:** Reversible test operations are enabled.
6. **Approved production execution:** Selected Tier 3 operations are enabled.

---

## 28. Observability, Audit, and SRE

### 28.1 Technical Metrics

- Request rate, errors, and latency
- Model latency and token use
- Retrieval latency and result count
- Tool success, failure, and timeout
- SAP connection-pool use
- Queue depth
- Cache behavior
- Cost by use case and team

### 28.2 AI Safety Metrics

- Grounded-answer rate
- Unsupported-claim rate
- Correct refusal rate
- Sensitive-data leak rate
- Prompt-injection block rate
- Tool-validation failure rate
- Human override and escalation rate
- Post-action verification failure rate

### 28.3 Business Metrics

- Mean time to acknowledge
- Mean time to diagnose
- Mean time to resolve
- Reopen rate
- Change failure rate
- Knowledge reuse
- Development lead time
- Defect escape rate
- Manual effort reduced

### 28.4 Alerts

Alert on:

- Spikes in denied tool calls
- Repeated injection attempts
- Bulk retrieval or enumeration
- Cross-environment access
- Unapproved model fallback
- Missing audit events
- Policy-service failure or bypass
- SAP authorization anomalies
- Unexpected production-write volume
- Secret detection
- Unusual cost or token consumption
- Approval bursts or approver fatigue patterns

### 28.5 Audit Requirements

Audit records should include:

- Event, correlation, workflow, case, and session identifiers
- Human and workload identity
- Channel
- Prompt, workflow, model, policy, and tool versions
- Data classifications
- Retrieved source IDs and versions
- Parameter and target hashes
- Approval evidence
- SAP references
- Verification and compensation outcomes

---

## 29. Operational Runbooks

### 29.1 Model Provider Outage

1. Stop privileged workflows.
2. Use fallback only if privacy and security are equivalent.
3. Preserve queued state without exposing prompts.
4. Notify users.
5. Resume with state and idempotency validation.
6. Review provider and gateway telemetry.

### 29.2 SAP Connectivity Failure

1. Open the circuit breaker.
2. Stop retries at the configured threshold.
3. Preserve workflow state.
4. Verify SAP, network, destination, and certificate health.
5. Prevent duplicated writes.
6. Resume only after authorization and connectivity checks.

### 29.3 Suspected Prompt Injection

1. Block tool execution.
2. Preserve sanitized evidence and source IDs.
3. Quarantine suspicious content.
4. Notify security review.
5. Search related retrieval and action attempts.
6. Add the case to adversarial tests.

### 29.4 Suspected Secret Leakage

1. Stop affected workflows.
2. Revoke and rotate exposed secrets.
3. Locate affected prompts, logs, caches, indexes, and backups.
4. Restrict access and notify security/privacy teams.
5. Remove or isolate exposed material where permitted.
6. Complete root-cause and prevention work.

### 29.5 Incorrect Production Action

1. Disable the affected tool and workflow.
2. Open a production incident.
3. Run the approved rollback or compensation.
4. Validate technical and business recovery.
5. Preserve evidence.
6. Disable the affected prompt, policy, model, or tool version.
7. Complete a problem review before re-enablement.

### 29.6 Knowledge Poisoning

1. Quarantine the source and chunks.
2. Remove them from active retrieval.
3. Invalidate caches.
4. Identify influenced responses and actions.
5. Review publisher identity and ingestion path.
6. Restore the last trusted version.
7. Improve source and approval controls.

### 29.7 Policy Service Outage

1. Deny all writes.
2. Stop new privileged workflows.
3. Allow only explicitly approved low-risk UI functions.
4. Preserve pending state.
5. Restore and validate policy service integrity.
6. Re-evaluate pending actions rather than resuming blindly.

### 29.8 Audit Service Outage

1. Deny new write actions.
2. Buffer eligible low-risk read events in protected storage.
3. Alert SRE and security.
4. Restore audit delivery.
5. Reconcile buffered event sequence and integrity.

---

## 30. Implementation Roadmap

### Phase 0: Foundations

Deliver:

- Approved use cases and prohibited actions
- Owners and governance
- Architecture and threat model
- Identity, network, vault, repository, pipeline, logging, and baseline policy
- Data classification and model-provider approval

Exit criteria:

- Security and architecture approval
- Development environments available
- No production connectivity

### Phase 1: Knowledge Assistant

Deliver:

- Registered non-sensitive sources
- Secure ingestion
- ACL-filtered retrieval
- Citations and claim-evidence response
- Prompt-injection evaluations

Exit criteria:

- No SAP tools
- Cross-user retrieval tests pass
- Source revocation tested

### Phase 2: Incident Assistance

Deliver:

- ITSM read integration
- Case summarization
- Triage recommendations
- Evidence-backed diagnosis drafts
- Human feedback

Exit criteria:

- No production writes
- Quality and safety dashboards active

### Phase 3: Read-Only SAP Diagnostics

Deliver:

- Narrow SAP read tools
- Tool registry and Tool Gateway
- System/client/field/range limits
- SAP-side roles and logging

Exit criteria:

- Authorization, enumeration, and injection tests pass
- Pilot group approval

### Phase 4: Development Assistance

Deliver:

- Code analysis and test generation
- Draft branch creation
- ATC and quality integration
- Review evidence

Exit criteria:

- No automatic merge or transport release
- Required quality gates enforced

### Phase 5: Draft Workflow Automation

Deliver:

- Draft incidents, problems, changes, plans, and knowledge
- Policy-as-code
- Approval service
- Signed parameter binding

Exit criteria:

- Correction and rejection rates measured
- Approval replay tests pass

### Phase 6: Bounded Execution

Deliver:

- A small set of reversible operations
- Deterministic executor
- Pre-check, post-check, compensation, and kill switches
- Canary release

Exit criteria:

- Rollback exercise successful
- Zero authorization bypass in release suite
- Named risk acceptance and production approval

---

## 31. Initial Production Scope

### 31.1 Enable in Release 1

- Authorized knowledge retrieval
- Incident summarization
- Incident categorization recommendation
- Change-draft generation
- ABAP explanation
- Unit-test suggestions
- Read-only transport status
- Read-only job status
- Read-only application-log summaries
- Evidence-linked recommendations

### 31.2 Disable in Release 1

- Production writes
- Job triggering
- Role or user creation
- Transport release or import
- Configuration changes
- Arbitrary RFC, SQL, ABAP, shell, or HTTP tools
- Cross-zone tool chaining
- OpenClaw production execution
- Automatic knowledge publication
- Automatic code merge
- System-initiated writes

### 31.3 Candidate Release 2 Features

- Draft Git branches
- Draft change records
- Test-environment health checks
- Reversible non-production operations
- Signed approvals and manifests

### 31.4 Candidate Release 3 Features

Consider a very small number of Tier 3 actions only after:

- No known cross-user data leaks
- Reliable idempotency
- Complete audit delivery
- Successful rollback exercises
- Tested kill switches
- Stable post-action verification
- Named business, SAP, security, and platform ownership

---

## 32. Production Readiness and Acceptance Criteria

### 32.1 Architecture Checklist

- [ ] Approved context, container, data-flow, and trust-boundary diagrams
- [ ] Production and non-production isolation
- [ ] Tool Gateway is the only agent execution path
- [ ] Deterministic executor is separate from orchestration
- [ ] No direct production database access
- [ ] High availability and disaster recovery tested

### 32.2 Identity and Access Checklist

- [ ] SSO, MFA, and conditional access active
- [ ] User and workload identities propagated separately
- [ ] Production identities are unique and short-lived
- [ ] SAP roles are least privilege
- [ ] SoD enforced
- [ ] Break-glass access uses PAM

### 32.3 Data Checklist

- [ ] Data inventory and classifications approved
- [ ] Secrets blocked before model use
- [ ] Sensitive fields redacted or tokenized
- [ ] Retrieval applies document ACL before return
- [ ] Production and lower-environment indexes separated
- [ ] Retention, deletion, and source revocation tested

### 32.4 Agent Safety Checklist

- [ ] Workflows are bounded
- [ ] All tools use strict schemas
- [ ] No generic RFC, SQL, shell, or endpoint tools
- [ ] Approval binds exact parameters and target
- [ ] Retry, token, time, step, and cost limits configured
- [ ] Injection, memory poisoning, goal hijacking, and RAG poisoning tests pass
- [ ] Kill switches tested

### 32.5 Software Delivery Checklist

- [ ] Protected branches and required reviewers
- [ ] SAST, dependency, secret, container, and IaC scans pass
- [ ] SBOM and signatures generated
- [ ] Prompt, policy, model, and tool changes use controlled promotion
- [ ] Rollback tested

### 32.6 Operations Checklist

- [ ] Dashboards and alerts active
- [ ] Audit events reach protected storage
- [ ] On-call and escalation defined
- [ ] Runbooks exercised
- [ ] Manual support fallback available
- [ ] Recovery objectives approved

### 32.7 Example Go-Live Gates

These targets must be finalized by the organization:

```text
Unauthorized tool execution tests:       100% blocked
Cross-user retrieval tests:              100% blocked
Cross-environment access tests:          100% blocked
Approval replay tests:                   100% blocked
Parameter substitution tests:            100% blocked
Tier 4 agent-initiated actions:           100% blocked
Post-action verification coverage:       100% for write tools
Rollback test coverage:                  100% for enabled Tier 3 tools
Secret detection test set:               100% blocked or redacted
Required audit-event delivery:           99.99% or approved equivalent
```

Authorization bypass and cross-user data leakage are zero-tolerance release blockers.

### 32.8 Initial Release Acceptance Criteria

The first production release is acceptable only if:

1. It is advisory or approved read-only.
2. Every user and service request is authenticated and authorized.
3. Retrieval is filtered by entitlement.
4. Sensitive fields are minimized before model use.
5. No model holds reusable SAP credentials.
6. All SAP calls use narrow schema-validated tools.
7. Prompt injection cannot grant permission or execute a tool.
8. Every request has a correlation ID and reconstructable evidence.
9. Safety, quality, security, and resilience gates pass.
10. The AI platform can be disabled without disrupting SAP.
11. Manual support remains available.
12. Named business, SAP, security, platform, and AI owners approve go-live.

---

## 33. Team Structure and Responsibilities

### Requester

- Provides accurate business intent
- Reviews recommendations
- Validates restored function where appropriate

### SAP Developer or Consultant

- Designs and reviews SAP changes
- Validates functional and technical hypotheses
- Reviews AI-generated code and tests

### Security Team

- Owns threat modeling, policy requirements, adversarial testing, and privileged-access review

### Application Owner

- Owns business risk and application approval
- Accepts residual risk

### Release Manager or CAB

- Owns release authorization, windows, and sequencing

### Platform and SRE

- Operates the platform
- Owns availability, deployment, monitoring, response, and recovery

### AI Owner

- Owns model, prompt, workflow, evaluation, and known limitations

### Knowledge Owner

- Approves authoritative operational knowledge
- Reviews access and expiry

No person or agent should request, approve, execute, and validate the same high-risk production action.

---

## 34. Architecture Decision Records

Create ADRs for:

- Agent orchestration framework
- OpenClaw role and isolation
- Model provider and routing
- Prompt and completion retention
- Embedding model and vector store
- SAP integration pattern per use case
- Principal propagation versus technical identity
- Policy engine
- Approval-token and action-manifest design
- Data masking and reversible tokenization
- Environment isolation
- Audit schema and retention
- Tool risk classification
- Human approval thresholds
- Rollback classification
- Deployment strategy
- Business continuity and manual fallback

Each ADR should include:

- Context
- Decision
- Alternatives considered
- Security consequences
- Operational consequences
- Data implications
- Owner
- Review date

---

## 35. Definition of Done

A feature is not complete until:

- Business purpose and owner are documented.
- Data classification is known.
- Threats and abuse cases are reviewed.
- Identity and authorization behavior is defined.
- Schemas and limits are implemented.
- Unit, integration, authorization, and adversarial tests pass.
- Metrics, logs, audit events, and alerts are available.
- Failure, retry, timeout, rollback, and kill-switch behavior is tested.
- Documentation and runbooks are updated.
- Required security, SAP, business, and platform reviews are complete.
- Production deployment uses a signed immutable artifact.

For a tool, Definition of Done additionally requires:

- Registered owner and risk tier
- Environment and target allowlists
- Exact user and workload entitlements
- Pre-check and post-check
- Idempotency
- Blast-radius limits
- Rollback category
- Audit schema
- Tested denial paths

---

## 36. Final Design Rules

### The AI may

- Classify
- Retrieve authorized information
- Summarize
- Explain
- Generate hypotheses
- Draft documents, code, and tests
- Propose typed actions

### The AI may not

- Grant itself permission
- Select arbitrary integrations
- Construct unrestricted endpoints
- Retrieve secrets
- Sign manifests
- Approve actions
- Bypass case or change state
- Bypass SAP authorization
- Execute arbitrary code
- Decide that execution succeeded
- Alter evidence

### Deterministic services control

- Identity
- Authorization
- Entitlements
- Context scope
- Retrieval filtering
- Tool registration
- Parameter normalization
- Risk classification
- Approval requirements
- Approval verification
- Action signing
- Execution
- Transaction management
- Verification
- Audit evidence
- Rollback and compensation
- Kill switches

### Final Architecture Statement

The platform is safe only when AI remains a bounded analytical and drafting component inside a larger deterministic control system. The security of the platform must not depend on a prompt instructing the model to behave. It must depend on identities, typed interfaces, policy, narrow tools, SAP authorizations, approvals, transaction boundaries, independent verification, and tamper-resistant evidence.

---

## 37. Reference Sources

The following references should be reviewed during detailed design and kept current as products and guidance evolve:

1. NIST, **Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile**, NIST AI 600-1.  
   <https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence>

2. NIST, **AI Risk Management Framework**.  
   <https://www.nist.gov/itl/ai-risk-management-framework>

3. OWASP, **AI Agent Security Cheat Sheet**.  
   <https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html>

4. OWASP GenAI Security Project, **Top 10 for Agentic Applications 2026**.  
   <https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/>

5. LangChain, **Security Policy**.  
   <https://docs.langchain.com/oss/python/security-policy>

6. SAP Help Portal, **SAP AI Core Authentication and Administration**.  
   <https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/user-authentication-and-administration>

7. SAP Cloud SDK, **On-Premise Connectivity and Principal Propagation**.  
   <https://sap.github.io/cloud-sdk/docs/java/features/connectivity/on-premise>

8. OpenClaw, **Gateway Security and Trust Model**.  
   <https://docs.openclaw.ai/gateway/security>

> Validate product-specific behavior, supported versions, licensing, regional availability, and security configuration against current official documentation before implementation.
