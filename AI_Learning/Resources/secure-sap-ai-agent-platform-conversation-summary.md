# Secure SAP AI Agent Platform

## Conversation Summary, Architecture Evolution, and Development Progress

| Document field | Value |
|---|---|
| Document purpose | Summarize the conversation and explain how the SAP AI-agent concept was advanced, clarified, secured, and converted into a development reference |
| Status | Project discovery and architecture progress summary |
| Version | 1.0 |
| Date | 2026-09-08 |
| Primary initiative | Secure AI-assisted SAP engineering, support, change management, knowledge automation, and bounded execution platform |

---

## 1. Executive Summary

This conversation developed an initial idea for an AI-enabled SAP platform into a more structured, secure, and implementation-oriented architecture.

The original objective was broader than building a chatbot or support assistant. The intention was to create an enterprise platform capable of helping SAP teams with development, production support, incidents, service requests, change requests, knowledge automation, diagnostics, release preparation, and selected controlled actions.

The most important advancement made during the conversation was the separation of **AI reasoning** from **enterprise authorization and execution**.

The final architectural principle became:

> The AI model may analyze, explain, retrieve, draft, and propose. Deterministic enterprise services must authenticate, authorize, approve, execute, verify, and audit.

This principle transformed the idea from a potentially over-privileged SAP agent into a governed enterprise architecture with:

- Strong identity and authorization boundaries
- A bounded AI orchestration layer
- Entitlement-filtered knowledge retrieval
- Narrow, typed tools
- A dedicated Tool Gateway
- Deterministic execution services
- Human approval for consequential operations
- SAP-side authorization and validation
- Independent post-action verification
- Tamper-resistant audit evidence
- Progressive production rollout

The conversation also produced a complete Markdown development blueprint containing the architecture, threat model, workflows, security controls, API examples, repository structure, testing strategy, deployment approach, operational runbooks, implementation roadmap, and production-readiness criteria.

---

## 2. Original Vision

The project vision was to combine SAP expertise with modern AI and application-development technologies, including:

- SAP ECC or SAP S/4HANA
- ABAP
- OpenClaw
- LangChain or a similar orchestration framework
- TypeScript
- Python
- JavaScript
- Enterprise large language models
- Retrieval-augmented generation
- SAP APIs
- ITSM and change-management systems
- Git and CI/CD platforms
- Identity, policy, approval, and monitoring services

The intended business and technical capabilities included:

- SAP incident intake and triage
- Production-support assistance
- Root-cause analysis
- Service-request planning
- Change-request preparation
- ABAP development assistance
- Code review and test generation
- SAP diagnostic checks
- Knowledge retrieval and article generation
- Transport-readiness analysis
- Release-evidence preparation
- Selected controlled actions in SAP and connected systems

The key challenge was to support these capabilities without exposing SAP production systems, confidential business data, credentials, or privileged functions to uncontrolled model behavior.

---

## 3. Initial Architecture Supplied for Review

A detailed reference architecture was provided for evaluation. It already contained many strong enterprise design elements, including:

- Zero-trust principles
- Least privilege
- Separation of duties
- Human approval
- A read-only-first strategy
- Data minimization
- Defense in depth
- Environment separation
- A model gateway
- A governed RAG platform
- A Tool Gateway
- Narrow SAP interfaces
- Policy and approval services
- Immutable audit evidence
- Action-risk tiers
- A STRIDE threat model
- AI-specific attack scenarios
- Secure development and CI/CD controls
- Observability and operational runbooks
- A phased production rollout

The document correctly rejected dangerous patterns such as:

- Direct production database updates
- Arbitrary RFC execution
- Arbitrary SQL or shell commands
- Model access to reusable SAP credentials
- Automatic production transport release
- Self-approval by an agent
- Unrestricted public model use for confidential data
- Treating generated code as immediately production-ready

The initial document was therefore assessed as a strong reference architecture, but not yet a fully implementation-ready system specification.

---

## 4. Main Architectural Assessment

The architecture was evaluated from two perspectives:

### 4.1 As a Reference Architecture

It was considered strong because it clearly established:

- AI as a bounded component
- Deterministic authorization
- Independent execution controls
- Human accountability
- SAP authorization preservation
- Secure retrieval
- Auditability
- Progressive autonomy

### 4.2 As an Implementation Specification

It still required more concrete definitions for:

- Runtime component boundaries
- User and workload identity propagation
- Delegated versus system-initiated actions
- Agent memory and cache isolation
- Service-to-service contracts
- Action proposal, policy, approval, and execution schemas
- Workflow failure states
- Approval protection
- Rollback enforcement
- Tool registration
- SAP interface restrictions
- Exact release gates
- Initial production scope

This distinction helped clarify that a good architecture document does not automatically provide all of the contracts, algorithms, schemas, controls, and development sequencing needed to build the system.

---

## 5. Important Gaps Identified

### 5.1 OpenClaw Trust Boundary

The initial design treated OpenClaw as an optional automation or agent component, but its enterprise role needed tighter definition.

The improved position was:

- OpenClaw may act as a user channel or isolated developer assistant.
- OpenClaw may call approved enterprise APIs.
- OpenClaw must not be the production policy engine.
- OpenClaw must not be the Tool Gateway.
- OpenClaw must not hold unrestricted SAP or vault credentials.
- OpenClaw must not be the approval authority.
- OpenClaw must not be the production executor.
- OpenClaw must not be relied on as a hostile multi-user isolation boundary.

The safe pattern became:

```text
OpenClaw or another user channel
  -> Enterprise API Gateway
  -> Application Control Plane
  -> Policy and Approval Services
  -> Tool Gateway
  -> Deterministic Executor
  -> SAP
```

This prevented the optional agent framework from becoming a privileged security boundary.

### 5.2 Identity and Delegation Ambiguity

The architecture discussed human identity and service identity but initially did not fully distinguish the following action types:

1. User-delegated read
2. User-delegated write
3. System-initiated read
4. System-initiated write

This was improved by requiring every request to preserve both:

- The human subject whose purpose and entitlements apply
- The workload or service actor making the technical request

The effective permission was defined as an intersection:

```text
Effective permission =
    user entitlements
  intersect workload entitlements
  intersect workflow permissions
  intersect tool permissions
  intersect target-system policy
  intersect current case or change state
```

This prevents an agent or service identity from gaining more authority than the user, workflow, tool, or target permits.

### 5.3 Cross-User State and Cache Leakage

The original architecture rejected cross-user context reuse but did not fully define isolation for:

- Agent checkpoints
- Conversation state
- Retrieval caches
- Embeddings
- Tool results
- Traces
- Long-term memory

A compound partitioning model was introduced using:

- Tenant
- Environment
- User security context
- Case identifier
- Workflow instance
- Data classification
- Source ACL version

This improvement reduced the risk of one user receiving another user's authorized context through shared caches or memory.

### 5.4 Approval Manipulation and Fatigue

Human approval alone was recognized as insufficient if an AI-generated summary could mislead the approver.

The approval experience was strengthened so that the approval service, rather than the model, must show:

- Exact tool
- Exact target system and client
- Before-state
- Proposed after-state
- Changed fields
- Maximum blast radius
- Change record
- Maintenance window
- Requester and executor
- Rollback method
- Parameter hash
- Approval expiry
- Unresolved warnings
- Whether AI proposed the values

This changed approval from a generic confirmation step into a verifiable security control.

### 5.5 Rollback Enforcement

The initial document required rollback plans, but a textual rollback plan did not guarantee technical reversibility.

Rollback categories were introduced:

```text
ATOMIC_ROLLBACK
COMPENSATING_TRANSACTION
RESTORE_FROM_SNAPSHOT
FORWARD_FIX_ONLY
MANUAL_RECOVERY
NOT_REVERSIBLE
```

A recommended rule was added that Tier 3 automation should not be allowed when recovery is only a forward fix, manual recovery, or non-reversible operation.

### 5.6 Model Confidence in Authorization

The architecture described confidence as non-authoritative, but confidence still appeared among possible policy inputs.

This was clarified:

- Model confidence must not authorize an action.
- It must not reduce approval requirements.
- It may only route a result to human review.
- Low evidence, conflicting evidence, or high impact should increase scrutiny.

This removed the risk of implementing unsafe rules such as automatic approval above a confidence threshold.

### 5.7 General Hallucination Detection

The phrase “hallucination detection” was replaced with the more implementable concept of **claim-evidence validation**.

Responses were structured into:

- Verified observations
- Unverified hypotheses
- Recommendations
- Evidence identifiers
- Verification status

This made it possible to reject unsupported operational claims rather than assuming a general detector could reliably identify every hallucination.

---

## 6. Refined Target Architecture

The revised platform was structured into the following layers.

### 6.1 Experience and Channel Layer

Possible channels include:

- Secure web portal
- Enterprise chat
- ITSM extension
- IDE extension
- Optional OpenClaw client

These channels present the user experience but hold no direct SAP authority.

### 6.2 Edge and Access Security

Responsibilities include:

- WAF
- API Gateway
- OAuth or OIDC
- MFA and conditional access
- Rate limiting
- Anti-replay protection
- Request-schema validation
- Secure upload quarantine
- Malware and hidden-content inspection

### 6.3 Application Control Plane

The control plane includes:

- Backend-for-frontend
- Case Service
- Workflow API
- Entitlement Service
- Context Broker
- Policy Enforcement Point
- Approval Service
- Audit and Evidence Service

This layer controls business context, identity, workflow state, entitlement, and evidence.

### 6.4 AI Orchestration Plane

The orchestrator is a bounded workflow graph rather than an unconstrained autonomous loop.

It may:

- Classify requests
- Request authorized retrieval
- Generate observations and hypotheses
- Produce recommendations
- Draft artifacts
- Propose typed actions

It may not:

- Execute arbitrary code
- Grant permissions
- Approve actions
- Sign manifests
- Pass raw output directly to SAP
- Treat retrieved content as trusted instructions

### 6.5 Model and Knowledge Plane

The model and knowledge plane contains:

- Model Gateway
- Approved LLM deployments
- Data-loss prevention
- Redaction
- Token and cost controls
- Authorized retrieval service
- Document store
- Metadata store
- Vector index
- Provenance and ACL enforcement

### 6.6 Tool Gateway

The Tool Gateway became the principal agent safety boundary.

It performs:

- Tool registration
- Schema validation
- Parameter normalization
- Target resolution
- Policy evaluation
- Approval verification
- Segregation-of-duties checks
- Nonce and expiry validation
- Idempotency enforcement
- Evidence capture
- Dispatch to deterministic executors

### 6.7 Deterministic Executors

Separate executors handle:

- SAP reads
- SAP writes
- ITSM operations
- Git operations
- CI/CD operations

They accept only signed, short-lived execution envelopes and perform pre-checks, execution, transaction handling, post-checks, rollback, or compensation.

### 6.8 SAP and Enterprise Systems

SAP remains responsible for:

- SAP authorization objects
- Organizational restrictions
- Business-rule validation
- Transaction control
- System and client enforcement
- Application logging
- Final data integrity

---

## 7. Improved Workflow Model

The workflow was expanded from a normal success path into a complete operational state machine.

### 7.1 Normal Analysis Path

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

### 7.2 Optional Action Path

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

### 7.3 Exceptional States

The architecture was strengthened with states for:

- Rejection
- Unauthorized access
- Quarantine
- Approval expiry
- Approval revocation
- Failed pre-check
- Failed execution
- Partial execution
- Required compensation
- Rollback
- Failed post-check
- Manual intervention
- Timeout
- Cancellation

This made the workflow suitable for real operational failure handling rather than only ideal success scenarios.

---

## 8. Tool Design Improvements

The conversation clarified the difference between safe business-level tools and dangerous general-purpose tools.

### 8.1 Approved Tool Style

Examples include:

```text
get_incident_summary(incident_id)
get_transport_status(transport_id)
read_application_log(system_id, object, time_range)
get_job_status(system_id, job_name, time_range)
validate_change_window(change_id)
run_approved_health_check(check_id, system_id)
create_draft_change_record(case_id, approved_fields)
attach_evidence(change_id, evidence_reference)
```

### 8.2 Prohibited Tool Style

Examples include:

```text
execute_arbitrary_rfc(function_name, parameters)
run_sql(query)
run_shell(command)
update_any_table(table, values)
execute_abap_source(source_code)
call_url(url, body)
impersonate_user(user_id)
```

### 8.3 Tool Registration Requirements

Every tool was required to define:

- Business purpose
- Owner
- Input and output schema
- Data classification
- User and workload permissions
- Permitted environments, systems, and clients
- Risk tier
- Approval requirements
- Field, row, time, and transaction limits
- Idempotency behavior
- Timeout and retry policy
- Pre-check and post-check
- Rollback category
- Audit fields
- Kill switch

This turned the tool catalog into a governed control surface rather than a collection of agent plug-ins.

---

## 9. SAP Integration Improvements

The SAP integration design was made more concrete.

### 9.1 Read Operations

Read tools must use:

- Fixed data sources
- Fixed field projections
- Maximum row counts
- Maximum date and time ranges
- Pagination limits
- Sensitive-field masking
- Query timeouts
- Client and system allowlists

They must not support arbitrary table reads or unrestricted query construction.

### 9.2 Write Operations

Write tools must use:

- One approved business operation
- One approved BAPI, OData operation, or service
- Pre-validation
- Explicit commit and rollback rules
- Idempotency
- Before and after evidence
- Maximum affected-object count
- Independent post-checks
- Compensation where supported

### 9.3 ABAP Wrapper Pattern

SAP-side wrappers should:

- Expose one business operation
- Perform authority checks
- Validate system and client
- Validate business inputs
- Enforce blast-radius limits
- Write application logs
- Return a typed minimal response
- Support test mode where possible

This keeps critical SAP validation close to the SAP business logic rather than relying entirely on an external AI platform.

---

## 10. Knowledge and RAG Improvements

The knowledge architecture was advanced from general RAG guidance into a controlled data pipeline.

### 10.1 Secure Ingestion

The ingestion process includes:

- Registered publisher validation
- Malware scanning
- Sandboxed parsing
- Hidden-text inspection
- Data classification
- Secret and personal-data detection
- Redaction or rejection
- Owner and ACL assignment
- Versioning and integrity hashes
- Approval workflow
- Approved embedding generation

### 10.2 Authorized Retrieval

Retrieval follows this order:

```text
Authenticate user
  -> resolve entitlements
  -> determine allowed collections
  -> apply security metadata filters
  -> retrieve candidates
  -> revalidate source ACLs
  -> remove expired or superseded content
  -> rerank
  -> redact
  -> attach provenance
  -> construct minimal model context
```

A key improvement was requiring authorization filters before unauthorized content leaves the retrieval service.

### 10.3 Source Revocation

The design also covered deletion, expiry, supersession, and poisoning by requiring:

- Immediate retrieval blocking
- Chunk removal or tombstoning
- Cache invalidation
- Restoration of trusted versions
- Review of affected outputs and actions

---

## 11. Concrete Contracts Introduced

The conversation introduced structured contracts for:

- Security context
- Tool proposal
- Policy decision
- Approval record
- Signed action manifest
- Execution result
- Claim-evidence response
- Audit event

These contracts clarified that an AI proposal is not the same as authorization.

The model may produce a typed proposal, but only deterministic services can:

- Normalize its parameters
- Evaluate policy
- Obtain approval
- Bind approval to exact hashes
- Create a signed execution envelope
- Dispatch an executor
- Verify the outcome

This was one of the most important steps toward making the architecture developable.

---

## 12. Threat Model Advancement

The original STRIDE analysis was retained and expanded through more explicit agent-related abuse cases.

The conversation addressed:

- Direct prompt injection
- Indirect prompt injection
- Tool abuse
- Excessive agency
- Goal hijacking
- Memory poisoning
- RAG poisoning
- Sensitive-data exfiltration
- Slow enumeration
- Hallucinated operational claims
- Approval manipulation
- Supply-chain compromise
- Cross-user leakage
- Cross-environment contamination
- Agent-loop cost exhaustion

The mitigations were connected directly to architectural controls such as:

- Narrow tool schemas
- Independent policy enforcement
- Entitlement-filtered retrieval
- State partitioning
- Approval parameter binding
- Signed nonces
- Idempotency
- Transaction limits
- Model and dependency versioning
- SBOM and artifact signing
- Kill switches
- Independent verification

This improved the threat model by connecting each threat to implementable technical controls.

---

## 13. Development and Repository Planning

A development-oriented repository structure was prepared, separating:

- User-facing applications
- Control-plane services
- Agent orchestration
- Retrieval and context services
- Tool Gateway
- Approval and audit services
- Deterministic executors
- Shared contracts and security packages
- Prompts and evaluations
- Policy-as-code
- Infrastructure
- Tests
- Architecture and operational documentation

Technology responsibilities were also clarified:

### TypeScript

Recommended for:

- Web portal
- Backend APIs
- Case and approval services
- Tool Gateway
- ITSM, Git, and CI/CD integration

### Python

Recommended for:

- Bounded LangChain or LangGraph workflows
- Document processing
- Retrieval reranking
- AI evaluation pipelines
- Classification support

### ABAP and SAP-Native Services

Recommended for:

- SAP-side authorization
- Business validation
- Safe wrapper APIs
- Transaction handling
- Application logging
- Domain-specific pre-checks and post-checks

The policy engine was explicitly kept deterministic and separate from model-generated output.

---

## 14. Testing and Release Improvements

The project was advanced with a complete testing model covering:

- Unit tests
- Contract tests
- Integration tests
- Authorization tests
- AI evaluation sets
- Adversarial tests
- Performance tests
- Resilience tests
- Recovery tests

Important release blockers were defined for:

- Unauthorized access
- Prompt injection enabling prohibited actions
- Cross-user retrieval
- Cross-environment access
- Approval replay
- Parameter substitution
- Incomplete audit events
- Untested rollback
- Missing owner approval

Example go-live goals included:

```text
Unauthorized tool execution:       100% blocked
Cross-user retrieval:              100% blocked
Cross-environment access:          100% blocked
Approval replay:                   100% blocked
Parameter substitution:            100% blocked
Tier 4 AI-initiated actions:        100% blocked
Post-action verification:          100% coverage for write tools
Rollback testing:                  100% coverage for enabled Tier 3 tools
```

These gates changed production readiness from a general review into a measurable engineering decision.

---

## 15. Progressive Implementation Roadmap

A six-phase implementation roadmap was created.

### Phase 0: Governance and Foundations

- Approve use cases and prohibited actions
- Name owners
- Establish architecture, identity, networking, vault, repositories, CI/CD, logging, and policy

### Phase 1: Knowledge Assistant

- Ingest approved non-sensitive knowledge
- Implement ACL-filtered RAG
- Add citations and injection testing
- Keep SAP tools disabled

### Phase 2: Incident Assistance

- Integrate ITSM read access
- Add summarization, triage, and evidence-grounded recommendations
- Introduce human feedback and quality metrics

### Phase 3: Read-Only SAP Diagnostics

- Add narrow read tools
- Enforce SAP system, client, field, row, and time limits
- Pilot with a restricted support group

### Phase 4: Development Assistance

- Add ABAP analysis and test generation
- Create draft branches through controlled workflows
- Integrate ATC and quality gates

### Phase 5: Draft Workflow Automation

- Create draft incidents, problems, changes, plans, and articles
- Introduce policy-as-code and approval services
- Measure rejection and correction rates

### Phase 6: Bounded Execution

- Enable only selected reversible, low-blast-radius actions
- Require signed approvals, pre-checks, post-checks, and kill switches
- Roll out through canary users

This roadmap supplied a practical order of implementation and prevented the project from beginning with unsafe production automation.

---

## 16. Recommended Initial Production Scope

The first production release was deliberately limited.

### Enabled

- Authorized knowledge retrieval
- Incident summarization
- Incident classification recommendations
- Change-draft generation
- ABAP explanations
- Unit-test suggestions
- Read-only transport status
- Read-only job status
- Read-only application-log summaries
- Evidence-linked recommendations

### Disabled

- Production writes
- Job triggering
- User or role creation
- Transport release or import
- Configuration changes
- Arbitrary RFC, SQL, ABAP, shell, or HTTP tools
- Automatic knowledge publication
- Automatic code merge
- System-initiated writes
- OpenClaw-based production execution

This made the initial release useful while preserving a low-risk operating profile.

---

## 17. Deliverable Created

A clean and comprehensive Markdown blueprint was created:

**File name:** `secure-sap-ai-agent-platform-development-blueprint.md`

The blueprint contains:

- Executive architecture position
- Scope, goals, and non-goals
- Security and engineering principles
- System context
- Logical architecture
- Trust boundaries
- Component responsibilities
- Identity and delegation model
- Authorization model
- Agent and workflow design
- Tool Gateway algorithm
- SAP integration requirements
- Secure RAG architecture
- Data protection rules
- Approval and action-manifest schemas
- Incident, service request, change, ABAP, and knowledge workflows
- Action-risk classification
- STRIDE and AI-specific threat model
- Secure development lifecycle
- Repository structure
- API and audit contracts
- Policy-as-code design
- Testing and AI evaluation
- CI/CD and supply-chain security
- Environment and deployment guidance
- Observability and SRE guidance
- Operational runbooks
- Implementation roadmap
- Initial production scope
- Production-readiness checklist
- Acceptance criteria
- Roles and responsibilities
- Architecture decision records
- Definition of Done
- Reference sources

The file was also programmatically checked for:

- Presence and readability
- Correct title
- Table of contents
- Architecture section
- Threat-model section
- Roadmap section
- Acceptance-criteria section
- Balanced Markdown code fences
- Sufficient document size and completeness

---

## 18. How the Conversation Improved Understanding

### 18.1 It Clarified the Product

The idea evolved from an “SAP AI agent” into a platform composed of several governed services.

This is important because an enterprise SAP solution cannot depend on one conversational agent to handle identity, policy, retrieval, execution, and audit safely.

### 18.2 It Separated Intelligence from Authority

The conversation clearly distinguished:

- What an AI model is good at
- What deterministic systems must control

AI is suitable for:

- Interpretation
- Summarization
- Classification
- Retrieval assistance
- Hypothesis generation
- Drafting
- Code and test suggestions

AI is not suitable as the authority for:

- Authentication
- Authorization
- Approval
- SAP transaction control
- Execution success
- Audit evidence

### 18.3 It Converted Security Principles into Engineering Controls

High-level principles such as least privilege and human approval were converted into concrete mechanisms:

- Typed schemas
- Parameter hashes
- Signed manifests
- Single-use nonces
- Short expiry
- Idempotency keys
- Target allowlists
- Tool registries
- SoD checks
- Pre-checks and post-checks
- Kill switches

### 18.4 It Clarified a Safe Role for OpenClaw

OpenClaw can contribute to usability and developer productivity, but it should not become the trusted production enforcement layer.

This distinction protects the platform while preserving the ability to use OpenClaw as a controlled client or isolated assistant.

### 18.5 It Made RAG a Security-Critical Subsystem

Retrieval was recognized as more than semantic search. It requires:

- Source governance
- ACLs
- Provenance
- Versioning
- Data classification
- Poisoning controls
- Revocation
- Cache isolation

This avoids exposing unauthorized content simply because it is semantically relevant.

### 18.6 It Established a Realistic Delivery Sequence

The project no longer needs to begin with production automation. It can deliver value through:

1. Knowledge assistance
2. Incident assistance
3. Read-only SAP diagnostics
4. Development assistance
5. Draft workflow automation
6. Bounded execution

This reduces risk and provides measurable learning at every phase.

---

## 19. Current Project Position

At the end of this conversation, the project has advanced from a broad vision to a structured reference design.

The following are now available conceptually:

- Clear platform purpose
- Clear security principles
- Defined AI authority boundaries
- Target component architecture
- Trust-boundary model
- Agent workflow model
- Tool Gateway pattern
- Deterministic execution model
- Identity and delegation model
- Secure RAG model
- Approval and signed-manifest pattern
- SAP integration constraints
- Threat and abuse cases
- Phased implementation roadmap
- Production-readiness criteria
- A complete Markdown reference blueprint

The project is ready to move into system-specific design, proof-of-concept planning, and repository initialization.

It is not yet production-ready because organization-specific information remains to be supplied and implemented.

---

## 20. Information Still Required

Before detailed implementation, the following must be confirmed:

- SAP systems, versions, system IDs, and clients
- SAP modules and priority use cases
- On-premises, cloud, or hybrid hosting model
- SAP BTP services available
- Identity provider and principal-propagation architecture
- ITSM product
- Git and CI/CD platforms
- Model provider and approved deployment region
- Prompt and completion retention requirements
- Vector database and document sources
- Enterprise data classifications
- Applicable legal and regulatory obligations
- GRC, PAM, SIEM, DLP, KMS, and vault products
- Required service levels and recovery objectives
- Approval matrix
- Segregation-of-duties rules
- Initial read-only SAP tools
- Candidate reversible non-production actions
- OpenClaw hosting and user-isolation model

---

## 21. Recommended Next Steps

### Step 1: Select One Initial Use Case

Recommended first use case:

> Evidence-grounded SAP incident assistant with ITSM integration, approved knowledge retrieval, and narrow read-only diagnostics.

This provides useful operational value without requiring production write authority.

### Step 2: Create System-Specific Diagrams

Prepare:

- Context diagram
- Container diagram
- Level 0 data-flow diagram
- Level 1 data-flow diagram
- Trust-boundary diagram
- Deployment diagram
- Sequence diagram for incident diagnosis

### Step 3: Define the First Tool Catalog

Start with three to five read-only tools, for example:

- Transport status
- Background job status
- Approved application-log retrieval
- System health check
- Incident summary retrieval

### Step 4: Define Contracts

Create versioned schemas for:

- Security context
- Retrieval request and response
- Tool proposal
- Policy decision
- Approval record
- Execution manifest
- Execution result
- Evidence record
- Audit event

### Step 5: Initialize the Repository

Create the application, executor, package, prompt, policy, infrastructure, test, and documentation directories defined in the blueprint.

### Step 6: Build a Non-Production Vertical Slice

The first working slice should demonstrate:

```text
Authenticated user
  -> authorized incident
  -> secure knowledge retrieval
  -> one read-only SAP diagnostic
  -> grounded response
  -> evidence and audit record
```

### Step 7: Build the Security Test Suite Early

Before adding more tools, test:

- Cross-user retrieval
- Prompt injection
- Indirect prompt injection
- Tool parameter manipulation
- Unauthorized system or client access
- Enumeration
- Missing policy service
- Missing audit service
- Model outage

### Step 8: Introduce Draft Automation

After the read-only slice is stable, add:

- Draft change records
- Draft Git branches
- Draft test plans
- Draft knowledge articles

### Step 9: Consider Bounded Execution Last

Only after successful operational measurement should the team consider reversible, low-blast-radius Tier 3 actions.

---

## 22. Final Outcome

The conversation helped transform the project in four major ways:

1. **From an agent idea to an enterprise platform architecture**
2. **From prompt-level safety to deterministic enforcement**
3. **From general controls to concrete contracts and workflows**
4. **From a broad target state to a phased development roadmap**

The resulting design preserves the value of AI while recognizing that enterprise SAP operations require stronger guarantees than a language model can provide.

The final project direction can be summarized as:

```text
AI provides intelligence.
Enterprise services provide authority.
SAP provides business enforcement.
Humans retain accountability.
Evidence provides traceability.
```

This is the foundation for developing a secure, useful, and progressively deployable SAP AI Agent Platform.
