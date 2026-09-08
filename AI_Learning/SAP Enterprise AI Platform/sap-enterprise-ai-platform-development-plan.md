# SAP Enterprise AI Platform

## Functional Product Development Plan

| Document field | Value |
|---|---|
| Product | SAP Enterprise AI Platform |
| Document type | MVP and production development plan |
| Version | 1.0 |
| Date | 2026-09-08 |
| Deployment model | Private enterprise network |
| Initial production mode | Advisory and read-only |
| Intended audience | Product owners, SAP consultants, ABAP developers, AI engineers, security engineers, platform engineers, SRE teams, auditors, and business stakeholders |

---

## 1. Executive Summary

The SAP Enterprise AI Platform is a secure, privately deployed enterprise application for assisting SAP business users, consultants, developers, support personnel, and operations teams.

The system will provide a simple user experience while keeping identity, authorization, data selection, execution, approval, and audit decisions outside the AI model.

The platform will initially support:

- Secure enterprise login
- AI-assisted SAP knowledge search
- Incident summarization and diagnosis
- ABAP code explanation and review assistance
- Read-only SAP diagnostics
- Evidence-linked answers and recommendations
- Business-configurable data access
- Role-based, attribute-based, row-level, and field-level authorization
- Complete request and access auditing
- Private-network-only deployment

The initial product will not perform unrestricted production actions. Production writes, transport imports, job execution, security administration, and configuration changes will remain disabled until deterministic controls, named approvals, rollback procedures, and production safety tests are completed.

> **Core rule:** AI may analyze, explain, summarize, draft, and propose. Deterministic services authenticate, authorize, retrieve, approve, execute, verify, and audit.

---

## 2. Product Vision

The product should operate as a governed AI workspace for SAP rather than as a chatbot connected directly to SAP.

```text
Business User
    -> asks a question or opens a case
    -> system authenticates the user
    -> system determines the user's permitted data scope
    -> authorized and minimized data is retrieved
    -> AI analyzes the permitted context
    -> system returns an evidence-linked answer
    -> optional action is proposed
    -> policy and approval services evaluate the proposal
    -> deterministic executor performs an approved action
    -> independent verification confirms the outcome
    -> complete audit evidence is retained
```

### 2.1 Product outcomes

The platform should:

- Reduce time spent collecting SAP incident evidence
- Improve troubleshooting consistency
- Make SAP knowledge easier to discover
- Improve ABAP review and test preparation
- Standardize change and remediation plans
- Prevent unauthorized production-data disclosure
- Preserve SAP authorization controls
- Provide traceability for every important operation
- Keep enterprise data within approved network boundaries
- Allow business and security owners to choose what the platform can access

---

## 3. Product Principles

1. **Private by design**  
   The platform runs inside the corporate network or an approved private cloud network.

2. **Read-only by default**  
   Initial production capabilities use narrow, predefined read operations.

3. **AI has no direct SAP access**  
   SAP access is available only through registered tools and deterministic executors.

4. **Business-configurable data scope**  
   Authorized administrators select systems, modules, datasets, fields, purposes, operations, and retention rules.

5. **SAP remains authoritative**  
   SAP authorization objects and organizational restrictions remain final controls.

6. **No prompt-based security**  
   Prompts can guide model behavior, but they cannot grant permission or approve execution.

7. **Minimum necessary context**  
   The model receives only the smallest authorized, relevant, and redacted context.

8. **Evidence before action**  
   Important claims must be connected to approved source evidence or deterministic system checks.

9. **Fail closed**  
   Privileged operations are denied when identity, policy, approval, audit, or target validation is unavailable.

10. **Progressive autonomy**  
    Additional automation is introduced only after measured safety and reliability gates are satisfied.

---

## 4. Initial Product Scope

### 4.1 Release 1 capabilities

#### Secure access

- Enterprise SSO
- MFA according to organizational policy
- Session expiry and revocation
- Conditional access where supported
- User and workload identity separation
- Role and attribute-based permissions

#### Knowledge assistant

- Search approved runbooks, standards, procedures, and knowledge articles
- Entitlement-filtered retrieval
- Source citations and document versions
- Source ownership, expiry, and revocation
- Grounded responses based only on authorized context

#### Incident assistant

- Load authorized ITSM incident information
- Summarize issue, impact, timeline, and existing evidence
- Suggest likely diagnostic paths
- Retrieve related runbooks and resolved cases
- Separate confirmed observations from hypotheses
- Generate a proposed resolution plan for human review

#### ABAP development assistant

- Explain authorized ABAP programs, classes, methods, CDS views, and interfaces
- Suggest code improvements
- Draft ABAP Unit test candidates
- Identify possible performance and authorization concerns
- Prepare review notes
- Never activate, merge, release, import, or deploy code automatically

#### Read-only SAP diagnostics

- Transport status
- Background job status
- Approved application logs
- Interface monitoring summaries
- Short-dump metadata through an approved wrapper
- Health-check results from registered checks

#### Administrative controls

- System and client allowlists
- Data-category selection
- Field masking rules
- Access-profile management
- Tool enablement and disablement
- Risk-tier configuration
- Retention controls
- Emergency kill switches

#### Audit and operations

- Correlation IDs
- User and service identity recording
- Data-source and tool-access records
- Model, prompt, workflow, policy, and tool versions
- Security events and denied requests
- Operational dashboards and alerts

### 4.2 Disabled in Release 1

- Production write operations
- Background-job triggering
- Transport release or import
- User or role creation
- Privileged access assignment
- Configuration updates
- Direct SAP table access
- Arbitrary RFC execution
- Arbitrary OData queries
- Arbitrary SQL, ABAP, shell, or HTTP execution
- Automatic code merges
- Automatic knowledge publication
- System-initiated writes
- Internet-based model or tool calls

---

## 5. Business User Experience

Business users should not need to understand agents, embeddings, vector databases, LangChain, or model orchestration.

### 5.1 Main navigation

```text
Home
Assistant
Incidents
SAP Diagnostics
ABAP Workspace
Knowledge
Approvals
Activity History
Administration
```

### 5.2 Assistant interaction

A user may ask:

```text
Why did monthly-closing job ZFI_CLOSE_01 fail?
```

The platform should:

1. Authenticate the user.
2. Validate the linked incident or approved business purpose.
3. Resolve permitted SAP systems, clients, fields, and time ranges.
4. Retrieve only authorized evidence.
5. Mask controlled fields before model use.
6. Retrieve approved runbooks and knowledge.
7. Produce observations, hypotheses, and recommendations.
8. Display source references and evidence status.
9. Record the operation in the audit service.

### 5.3 Required visual indicators

The interface must clearly display:

- Signed-in identity
- Current environment
- SAP system and client
- Data classification
- Read-only or action-enabled mode
- Evidence status
- AI-generated content label
- Missing or conflicting evidence
- Required approval status
- Request and execution history

---

## 6. Business-Configurable Data Governance

The platform must give approved owners explicit control over what production data can be retrieved, viewed, analyzed, retained, and used by AI.

### 6.1 Governance dimensions

Administrators should configure access by:

- User or group
- Business role
- SAP module
- Business purpose
- Case or change state
- Environment
- SAP system
- SAP client
- Company code
- Plant
- Sales organization
- Purchasing organization
- Data category
- Object or approved API
- Field
- Record scope
- Time range
- Maximum rows
- Operation type
- Risk tier
- Retention class

### 6.2 Data classifications

Recommended classifications:

- Public
- Internal
- Confidential
- Restricted or regulated
- Security secret

Security secrets must never be sent to the model, embedded, placed in agent memory, or written to normal logs.

### 6.3 Example access profiles

#### Support analyst

May access:

- Assigned incidents
- Approved application logs
- Job status
- Transport status
- Internal support knowledge

May not access:

- Payroll values
- Vendor bank details
- Credentials or secrets
- Unrelated business records

#### ABAP developer

May access:

- Authorized source code
- Development objects
- ATC findings
- Transport metadata
- Technical standards

May not access by default:

- Unmasked production transactions
- HR and payroll records
- Customer or employee personal data
- Security-account credentials

#### Functional consultant

May access:

- Authorized module configuration
- Relevant business-document status
- Approved process logs
- Module-specific knowledge

The user's SAP organizational restrictions must still apply.

#### Business process owner

May access:

- Approved business KPIs
- Process status
- Requests requiring approval
- Business-oriented evidence

Technical or secret data should remain excluded unless separately authorized.

### 6.4 Row-level and field-level protection

If a user is authorized only for selected company codes, plants, sales organizations, or geographic scopes, the retrieval service must enforce those restrictions before returning content.

Sensitive fields should be:

- Excluded
- Masked
- Tokenized
- Aggregated
- Returned only with separate authorization

### 6.5 Access decision formula

```text
Effective permission
    = human entitlements
    intersect workload entitlements
    intersect workflow permissions
    intersect tool permissions
    intersect data policy
    intersect SAP authorization
    intersect target environment policy
    intersect current case or change state
```

The AI model cannot add permissions to this intersection.

---

## 7. Target Architecture

```text
+------------------------------------------------------------------+
| Users and Enterprise Channels                                    |
| Web portal | ITSM extension | Teams/chat | IDE integration       |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
| Edge and Access Security                                         |
| WAF | API gateway | SSO | MFA | rate limits | request scanning   |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
| Application Control Plane                                        |
| BFF | Case API | Entitlements | Context Broker | Policy PEP      |
| Approval Service | Audit and Evidence Service                    |
+----------------------+------------------------+------------------+
                       |                        |
                       v                        v
+--------------------------------+  +------------------------------+
| AI Orchestration Plane         |  | Knowledge and Model Plane    |
| Bounded LangGraph workflows    |  | Private Model Gateway        |
| Prompt and workflow versions   |  | DLP and redaction            |
| Claim-evidence validation      |  | Authorized RAG               |
+----------------------+---------+  | Document and vector stores   |
                       |            +------------------------------+
                       | Typed proposal only
                       v
+------------------------------------------------------------------+
| Tool Gateway                                                     |
| Registry | schema validation | policy | target resolution        |
| approval verification | limits | idempotency | evidence          |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
| Deterministic Executors                                          |
| SAP read | SAP write, later | ITSM | Git | CI/CD                 |
| pre-checks | execution | post-checks | compensation              |
+-------------------------------+----------------------------------+
                                |
                                v
+------------------------------------------------------------------+
| Enterprise Systems                                               |
| SAP ECC/S4 | BTP | ITSM | Git | CI/CD | monitoring | SIEM        |
+------------------------------------------------------------------+

Platform foundation:
Private network | mTLS | Vault | KMS/HSM | containers | SIEM
SBOM | artifact signing | backups | disaster recovery
```

### 7.1 Mandatory architecture boundaries

- The UI cannot call SAP directly.
- The AI orchestrator cannot call SAP directly.
- The model cannot receive reusable SAP credentials.
- Every SAP operation passes through the Tool Gateway.
- Every tool has a fixed purpose and strict schema.
- SAP system, client, host, destination, and operation are resolved from trusted registries.
- Production and non-production use separate identities, keys, destinations, indexes, and model deployments.
- Write execution, when introduced, uses a separate deterministic executor.

---

## 8. Recommended Technology Stack

### 8.1 Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- Enterprise SSO integration

### 8.2 Enterprise API and control services

- Node.js
- TypeScript strict mode
- NestJS
- OpenAPI
- JSON Schema or Zod for boundary validation

Recommended TypeScript services:

- Backend for Frontend
- Case Service
- Entitlement Service integration
- Context Broker
- Approval Service
- Tool Gateway
- Audit API
- ITSM, Git, and CI/CD connectors

### 8.3 AI services

- Python
- FastAPI
- LangGraph for bounded, state-machine workflows
- LangChain components only where needed
- Pydantic schemas

Recommended Python responsibilities:

- AI workflow orchestration
- Retrieval and reranking
- Document processing
- Classification support
- Model evaluations
- Claim-evidence validation support

### 8.4 Knowledge and persistence

- PostgreSQL for product records
- pgvector for the initial vector index
- Object storage compatible with the private deployment model
- Redis only for carefully partitioned, short-lived state

Every cache entry must include the environment, user security context, case, workflow, data classification, and entitlement version.

### 8.5 Policy and identity

- Microsoft Entra ID or the approved enterprise identity provider
- Open Policy Agent, Cedar, or an approved corporate policy service
- Vault or approved enterprise secret manager
- KMS or HSM for signing and encryption

### 8.6 SAP integration

- Released OData or REST services where available
- Approved BAPIs or RFC wrappers
- SAP Cloud Connector or approved private connectivity pattern
- Principal propagation when organizational policy requires user identity continuity
- Narrow technical identities only for justified system-managed operations
- ABAP wrapper APIs for fixed read or business operations

### 8.7 Runtime and operations

- Kubernetes or the organization's approved container platform
- Private artifact and container registries
- Prometheus-compatible metrics
- Grafana-compatible dashboards
- OpenTelemetry
- Central SIEM integration
- Git-based CI/CD
- Infrastructure as code

---

## 9. Core Services

### 9.1 Web Portal

Responsibilities:

- Present a simple business experience
- Display identity, environment, evidence, and access state
- Submit canonical requests
- Show recommendations separately from approved actions
- Provide administration and audit views

### 9.2 Backend for Frontend

Responsibilities:

- Validate channel requests
- Preserve signed user identity
- Add correlation and trace IDs
- Enforce request and response limits
- Route requests to internal services

### 9.3 Case Service

Responsibilities:

- Load incidents, requests, problems, and changes
- Validate user access to the case
- Track the approved business purpose
- Associate workflows with authoritative ITSM records

### 9.4 Entitlement Service

Responsibilities:

- Resolve groups, roles, attributes, SAP scope, and organizational restrictions
- Produce a versioned entitlement context
- Support rapid revocation
- Never accept user-supplied role claims as authoritative

### 9.5 Context Broker

Responsibilities:

- Determine minimum necessary context
- Apply field and record selection
- Apply classification and purpose controls
- Redact, tokenize, aggregate, or reject sensitive data
- Attach provenance and authorization metadata

### 9.6 AI Orchestrator

Responsibilities:

- Run bounded workflows
- Limit model calls, retrievals, tool proposals, retries, time, and cost
- Generate structured observations, hypotheses, and recommendations
- Produce typed action proposals only
- Stop on contradictory, unauthorized, or unsupported states

### 9.7 Authorized RAG Service

Responsibilities:

- Search only permitted collections
- Apply ACL and metadata filters before returning chunks
- Revalidate source permissions
- Remove expired or superseded documents
- Attach source identity, version, and integrity metadata
- Support immediate source revocation

### 9.8 Model Gateway

Responsibilities:

- Route to approved privately reachable models
- Enforce model and region allowlists
- Apply DLP and secret detection
- Enforce token, cost, timeout, and retention limits
- Pin and record model versions
- Prevent unapproved internet fallback

### 9.9 Tool Gateway

Responsibilities:

- Register narrow tools
- Validate schemas
- Normalize parameters
- Resolve trusted targets
- Evaluate authorization and policy
- Verify approval when needed
- Enforce system, client, field, row, and transaction limits
- Prevent replay and duplicate execution
- Dispatch only to registered deterministic executors

### 9.10 SAP Read Executor

Responsibilities:

- Accept only signed and valid requests from the Tool Gateway
- Execute one allowlisted read operation
- Apply time, record, and field limits
- Use private SAP connectivity
- Record authoritative results
- Return minimal typed responses

### 9.11 Approval Service

This service is required before any consequential action is introduced.

Responsibilities:

- Display exact target and normalized parameters
- Bind approval to target and parameter hashes
- Enforce approval expiry and single use
- Enforce separation of duties
- Capture named approver identity
- Support revocation

### 9.12 Audit and Evidence Service

Responsibilities:

- Record important access and workflow events
- Preserve identity, versions, targets, hashes, sources, outcomes, and evidence
- Write security events to protected storage and SIEM
- Avoid storing full sensitive payloads by default
- Support audit reconstruction

---

## 10. Initial Registered SAP Tools

Release 1 tools should be read-only and narrowly defined.

```text
get_transport_status(transport_id)
get_job_status(system_id, job_name, time_range)
read_application_log(system_id, object, time_range)
get_interface_status(interface_id, time_range)
get_short_dump_summary(system_id, dump_reference)
run_approved_health_check(check_id, system_id)
```

Every tool registration must define:

- Business purpose
- Owner
- Input and output schema
- Permitted workflow
- Required human and workload entitlements
- Data classification
- Permitted environments, systems, and clients
- Field, row, time, and query limits
- Timeout and retry policy
- Audit fields
- Risk tier
- Kill-switch identifier

The platform must not register generic tools such as:

```text
run_sql(query)
execute_arbitrary_rfc(function_name, parameters)
update_any_table(table, values)
run_shell(command)
execute_abap_source(source_code)
call_any_url(url, body)
```

---

## 11. Private-Network Deployment

### 11.1 Network position

The entire product should run inside the corporate network or an approved private cloud network with private connectivity to SAP and enterprise services.

```text
Corporate user network
        |
        v
Private ingress and WAF
        |
        v
Private application network
        |
        +--> Control services
        +--> AI orchestration
        +--> Private model gateway
        +--> RAG and data services
        +--> Tool Gateway
        |
        v
Private SAP integration network
        |
        v
SAP systems
```

### 11.2 Network controls

- Deny-by-default ingress and egress
- No public administrative endpoints
- Private endpoints for dependent services where available
- mTLS between sensitive services
- Segmentation among edge, application, AI, data, and integration tiers
- Egress proxy with strict domain allowlists
- DNS and certificate controls
- Separate production and non-production networks
- No direct user-device connection to SAP through the product
- No silent model fallback to a public endpoint

### 11.3 Private model options

The platform may use:

- An internally hosted approved model
- A managed model exposed only through approved private endpoints
- An enterprise model gateway with tenant isolation and disabled training on enterprise data

The final choice must be approved by security, privacy, legal, platform, and data-residency owners.

---

## 12. Repository Structure

```text
sap-enterprise-ai-platform/
  apps/
    web-portal/
    api-service/
    admin-console/

  services/
    case-service/
    entitlement-service/
    context-broker/
    agent-orchestrator/
    retrieval-service/
    model-gateway-adapter/
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
    schemas/
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
    retrieval/
    data-handling/
    action-risk/
    segregation-of-duties/
    environment-controls/

  infrastructure/
    modules/
    environments/
      local/
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
    ai-evaluations/
    resilience/
    performance/

  docs/
    architecture/
    decisions/
    threat-model/
    api/
    runbooks/
    tool-catalog/
    data-inventory/
    release/

  .github/
  README.md
```

---

## 13. Development Plan

### Sprint 0: Product and security foundation

Deliverables:

- Confirmed Release 1 use cases
- Prohibited-action register
- Product ownership and RACI
- Data inventory and classification
- Threat model
- Private-network design
- Repository and branching strategy
- CI pipeline baseline
- Development environment
- Architecture decision record templates

Exit criteria:

- Architecture and security owners approve the MVP boundary
- No production connectivity exists
- All initial data sources and owners are identified

### Sprint 1: Portal and identity

Deliverables:

- Next.js portal
- Enterprise SSO
- Session management
- Initial user profile and entitlement view
- Environment banner
- BFF and API skeleton
- Correlation and trace IDs

Exit criteria:

- Unauthorized users are blocked
- Identity is propagated separately from service identity
- Session expiry and revocation are tested

### Sprint 2: Knowledge ingestion

Deliverables:

- Source registry
- Document upload and connector framework
- Malware and active-content scan integration
- Parsing sandbox
- Classification and metadata model
- Redaction pipeline
- PostgreSQL and pgvector storage
- Source approval and revocation

Exit criteria:

- Only approved documents enter the active index
- Secrets are blocked
- Revoked sources are no longer retrievable

### Sprint 3: Authorized RAG assistant

Deliverables:

- Query API
- Entitlement-filtered retrieval
- Metadata and ACL enforcement
- Reranking
- Evidence-linked answer schema
- Private model gateway integration
- Prompt and model version recording
- Chat interface

Exit criteria:

- Cross-user retrieval tests are completely blocked
- Responses contain valid source references
- Unsupported claims are removed or labelled as hypotheses

### Sprint 4: Incident assistant

Deliverables:

- ITSM read connector
- Case-access validation
- Incident summary
- Related-knowledge retrieval
- Diagnostic workflow
- Observation, hypothesis, and recommendation structure
- Human feedback capture

Exit criteria:

- The user can access only authorized cases
- No incident content bypasses data minimization
- All output is advisory

### Sprint 5: Read-only SAP diagnostics

Deliverables:

- Tool Registry
- Tool Gateway
- Initial ABAP wrapper APIs
- SAP Read Executor
- Transport-status tool
- Job-status tool
- Application-log tool
- System, client, field, time, and row limits
- SAP and platform audit events

Exit criteria:

- No direct AI-to-SAP connectivity
- Prompt injection cannot select or execute an unauthorized tool
- Arbitrary system, client, destination, table, RFC, or endpoint selection is impossible
- SAP authorization failures are handled safely

### Sprint 6: ABAP development assistant

Deliverables:

- Authorized source-code ingestion or on-demand retrieval
- Code explanation
- Review suggestions
- ABAP Unit test suggestions
- ATC result integration
- Secure output handling

Exit criteria:

- No automatic activation, merge, release, import, or deployment
- Generated code is clearly marked for human review
- Sensitive production data is not included in code-related prompts

### Sprint 7: Administration and governance

Deliverables:

- Data Governance Console
- AI Governance Console
- Role and access-profile management
- Tool enablement management
- Model, prompt, workflow, and policy version views
- Retention configuration
- Kill-switch controls

Exit criteria:

- All privileged changes are authorized and audited
- Administrators cannot bypass SAP authorization
- Policy changes require review and automated tests

### Sprint 8: Production hardening and pilot

Deliverables:

- Security testing
- Adversarial AI testing
- Penetration testing
- Load and resilience testing
- Monitoring and SIEM integration
- Backup and recovery tests
- Operational runbooks
- User acceptance testing
- Pilot deployment

Exit criteria:

- Zero known authorization bypasses
- Zero cross-user or cross-environment retrieval
- Required audit delivery meets the approved target
- Manual support remains available
- Kill switches and recovery procedures are tested

---

## 14. CI/CD and Software Supply-Chain Controls

```text
Commit
  -> formatting and linting
  -> unit and contract tests
  -> secret scanning
  -> static application security testing
  -> dependency and license scanning
  -> build
  -> software bill of materials
  -> artifact signing
  -> container and infrastructure scanning
  -> development deployment
  -> integration and AI evaluations
  -> test and quality promotion
  -> authorization and adversarial tests
  -> release approval
  -> staged production deployment
  -> post-deployment verification
```

Required rules:

- Protected branches
- Required peer review
- Security-sensitive CODEOWNERS
- Immutable versioned artifacts
- Private trusted registries
- No build in production
- Same artifact promoted across environments
- Signed images and admission controls
- Versioned prompts, workflows, policies, tool schemas, and evaluation sets
- Production rollback support

---

## 15. Testing Strategy

### 15.1 Functional tests

- Authentication and logout
- Role and entitlement behavior
- Case access
- Knowledge retrieval
- SAP diagnostic tools
- Citation and evidence display
- Administration workflows

### 15.2 Authorization tests

- Unauthorized system access
- Unauthorized client access
- Company-code and plant restrictions
- Field masking
- Cross-user access
- Cross-environment access
- Expired or revoked access
- Tool-specific permission checks

### 15.3 AI safety tests

- Direct prompt injection
- Indirect prompt injection from tickets and documents
- Hidden document instructions
- RAG poisoning
- Memory poisoning
- Goal hijacking
- Unsupported operational claims
- Sensitive-data leakage
- Incorrect tool selection
- Incorrect parameter generation
- Excessive retrieval and slow enumeration

### 15.4 Resilience tests

- Model outage
- SAP connectivity failure
- Vector-store degradation
- Policy-service outage
- Audit-service outage
- Vault or KMS failure
- Queue backlog
- Connection-pool exhaustion
- Regional or infrastructure failure
- Backup restoration

### 15.5 Zero-tolerance release blockers

- Authorization bypass
- Cross-user data disclosure
- Cross-environment access
- Secret leakage
- Approval replay when approvals are introduced
- Parameter substitution
- Tier 4 AI-initiated action
- Missing audit evidence for privileged operation
- Untested rollback for an enabled write tool

---

## 16. Production Rollout

### Stage 1: Shadow mode

- System evaluates requests internally
- Recommendations are not used operationally
- Quality and safety metrics are collected

### Stage 2: Advisory mode

- Authorized users receive grounded answers
- No SAP tools are enabled

### Stage 3: Read-only diagnostics

- Narrow SAP read tools are enabled for a pilot group
- System, client, field, record, and time limits are enforced

### Stage 4: Draft automation

- Draft ITSM records and Git branches may be created
- No automatic approval, merge, release, or deployment

### Stage 5: Bounded non-production execution

- Reversible operations are introduced in lower environments
- Pre-check, post-check, idempotency, and rollback are mandatory

### Stage 6: Approved production execution

Only a small number of production actions may be considered after:

- No known cross-user data leakage
- Stable read-only operation
- Complete audit delivery
- Reliable idempotency
- Tested kill switches
- Successful rollback exercises
- Signed, short-lived approvals and action manifests
- Named business, SAP, security, and platform ownership

---

## 17. Production Go-Live Checklist

### Architecture

- [ ] Approved context, container, data-flow, and trust-boundary diagrams
- [ ] Production and non-production isolation
- [ ] Tool Gateway is the only execution path
- [ ] AI has no direct SAP connectivity
- [ ] No direct production database access
- [ ] High availability and disaster recovery tested

### Identity and access

- [ ] SSO and MFA active
- [ ] User and workload identities separated
- [ ] Production identities are unique and short-lived
- [ ] Least-privilege SAP roles configured
- [ ] Segregation of duties defined
- [ ] Break-glass access uses the approved privileged process

### Data protection

- [ ] Data inventory approved
- [ ] Data classifications assigned
- [ ] Secrets blocked before model use
- [ ] Sensitive fields redacted, tokenized, aggregated, or excluded
- [ ] Retrieval ACLs enforced before data leaves the service
- [ ] Production and non-production indexes separated
- [ ] Retention, deletion, and revocation tested

### Agent safety

- [ ] Workflows have step, time, retry, token, and cost limits
- [ ] All tools use strict schemas
- [ ] Generic RFC, SQL, shell, ABAP, and endpoint tools are prohibited
- [ ] Prompt injection cannot grant permission
- [ ] Cross-user and cross-environment tests pass
- [ ] Kill switches tested

### Software delivery

- [ ] Required reviewers and protected branches configured
- [ ] SAST, dependency, secret, container, and infrastructure scans pass
- [ ] SBOM and artifact signatures generated
- [ ] Prompt, policy, model, workflow, and tool changes use controlled promotion
- [ ] Production rollback tested

### Operations

- [ ] Dashboards and alerts active
- [ ] Audit events reach protected storage
- [ ] On-call and escalation procedures defined
- [ ] Model, SAP, secret-leakage, injection, and audit-outage runbooks exercised
- [ ] Manual support fallback available
- [ ] Business, SAP, security, platform, and AI owners approve go-live

---

## 18. MVP Definition of Done

The MVP is complete when:

- Users authenticate through enterprise SSO.
- The platform runs through private network paths.
- Business owners can select approved knowledge sources and SAP read capabilities.
- Authorized RAG prevents cross-user retrieval.
- Sensitive fields are minimized before reaching the model.
- Knowledge responses contain sources and evidence status.
- Authorized incidents can be summarized and analyzed.
- Initial SAP read tools operate through the Tool Gateway.
- The AI does not possess reusable SAP credentials.
- Every important request has a correlation ID and audit trail.
- Prompt injection cannot grant access or trigger unauthorized tools.
- Production and non-production identities, indexes, keys, and targets are separated.
- Security, authorization, resilience, and AI evaluation gates pass.
- The AI platform can be disabled without disrupting SAP.
- Manual support remains available.

---

## 19. Immediate Next Actions

1. Create the monorepo using the proposed repository structure.
2. Nominate product, SAP, security, data, platform, AI, and knowledge owners.
3. Finalize three Release 1 use cases:
   - Authorized knowledge assistant
   - Incident assistant
   - Read-only SAP diagnostic assistant
4. Choose the enterprise identity provider and private model deployment pattern.
5. Create the data inventory and select the first approved knowledge sources.
6. Select one non-production SAP system for initial integration.
7. Define the first three narrow SAP read tools.
8. Create ABAP wrapper designs for those tools.
9. Implement the portal, BFF, identity propagation, audit skeleton, and policy baseline.
10. Build authorized RAG without production data.
11. Add ITSM read integration.
12. Add the Tool Gateway and SAP Read Executor.
13. Complete adversarial, authorization, resilience, and load testing.
14. Run a limited pilot in advisory mode.
15. Introduce read-only production diagnostics only after formal approval.

---

## 20. Final Product Position

The SAP Enterprise AI Platform can become a practical production product, but its safety must come from architecture and deterministic controls rather than from asking an AI model to behave safely.

The correct first release is an effortless business-facing experience backed by strict identity, data governance, authorized RAG, narrow read-only SAP tools, private networking, and complete auditing.

Production write automation should be treated as a later product capability, not as an MVP requirement. Each future action must be individually designed, authorized, bounded, tested, reversible where possible, independently verified, and protected by a kill switch.

---

## Source Basis

This development plan was prepared from the uploaded **Secure SAP AI Agent Platform: Development, Security, Deployment, Threat Model, and Operations Blueprint, Version 2.0**, dated 2026-09-08.
