# Secure SAP AI Agent Platform

## Architecture, Development, Production Deployment, Threat Model, and Operations Guide

**Document status:** Reference architecture and implementation blueprint  
**Version:** 1.0  
**Last updated:** 2026-09-08  
**Intended audience:** SAP architects, ABAP developers, AI engineers, security engineers, platform engineers, production support teams, service managers, and auditors

---

## 1. Executive Summary

This document defines a secure, production-grade architecture for an AI-assisted SAP engineering and operations platform. The platform combines an agent orchestration framework, such as LangChain or an equivalent controlled workflow engine, with TypeScript, Python, JavaScript, SAP APIs, an enterprise large language model, governed knowledge retrieval, identity services, approval workflows, and centralized monitoring.

The platform is intended to improve SAP development and production operations without giving an AI model unrestricted access to production systems. It can assist with:

- SAP incident intake, classification, investigation, and resolution guidance
- Service request validation and fulfillment planning
- Change request preparation, impact analysis, and evidence collection
- ABAP development assistance, code review, and test generation
- Root-cause analysis and problem management
- Knowledge article generation and controlled retrieval
- Transport readiness checks and release evidence
- Operational monitoring and support-team productivity

The central design principle is:

> The model may reason and recommend, but deterministic services authorize and execute.

No model response, prompt, retrieved document, or agent decision is treated as trusted. Every production-impacting operation is subject to identity verification, policy enforcement, least privilege, input validation, human approval, audit logging, and an independently enforced execution boundary.

---

## 2. Scope

### 2.1 In Scope

- Web or conversational user interface
- API gateway and backend-for-frontend services
- Authentication, authorization, and entitlement checks
- AI agent orchestration
- Model gateway and enterprise LLM integration
- Retrieval-augmented generation, or RAG
- SAP integration through approved interfaces
- Incident, problem, service request, and change workflows
- Development assistance and code-quality workflows
- Human-in-the-loop approvals
- Secrets and key management
- Security monitoring, auditability, and operational support
- CI/CD, infrastructure deployment, testing, release, and rollback
- Threat modeling and security control requirements

### 2.2 Out of Scope

Unless explicitly approved through a later design review, the platform must not:

- Perform direct database updates in an SAP production system
- Store SAP passwords in prompts, source code, configuration files, logs, or vector stores
- Allow an LLM to invoke unrestricted RFC, BAPI, OData, SQL, shell, or operating-system commands
- Automatically release production transports
- Automatically approve its own recommendations or changes
- Bypass SAP authorization objects, GRC controls, segregation of duties, or emergency-access procedures
- Use unrestricted public model endpoints for confidential production data
- Train a public or shared model on enterprise incident, customer, employee, or production data
- Treat generated code as production-ready without static analysis, testing, review, and release governance

---

## 3. Assumptions and Design Decisions

This reference design assumes:

1. The organization operates SAP ECC, SAP S/4HANA, or both.
2. Approved SAP interfaces are available, such as OData, REST, SOAP, RFC, BAPI, IDoc, Event Mesh, or an integration platform.
3. A corporate identity provider supports SSO, MFA, conditional access, service identities, and group-based access.
4. An enterprise-approved LLM endpoint provides contractual data protection, tenant isolation, and configurable retention.
5. ITSM and change-management systems expose approved APIs.
6. Production actions require formal authorization outside the model.
7. Sensitive fields can be classified, masked, tokenized, or excluded before model processing.
8. OpenClaw is treated as an optional agent or automation component. Its exact permissions must be constrained by the same policy and execution controls as every other agent framework.
9. The system uses separate development, test, quality, pre-production, and production environments.
10. All production deployments are performed through controlled pipelines, not from a developer workstation.

---

## 4. Goals and Non-Goals

### 4.1 Goals

- Reduce mean time to acknowledge, diagnose, and resolve SAP issues
- Increase development quality through assisted analysis and automated checks
- Standardize incident, change, and release evidence
- Preserve data confidentiality and SAP authorization boundaries
- Provide complete traceability from user request to agent decision and tool execution
- Prevent prompt injection from becoming tool execution
- Ensure production-impacting actions are reviewed and reversible
- Build reusable, governed knowledge from validated operational outcomes
- Support audit, compliance, and incident response requirements

### 4.2 Non-Goals

- Replacing SAP functional, technical, security, or Basis experts
- Permitting autonomous unrestricted production remediation
- Replacing formal CAB, GRC, or transport-management controls
- Allowing generated explanations to serve as the only audit evidence
- Using model confidence as an authorization decision

---

## 5. Guiding Principles

1. **Zero trust:** Authenticate and authorize every user, service, tool call, and data request.
2. **Least privilege:** Give every component only the exact permissions required.
3. **Separation of duties:** Separate request, development, review, approval, deployment, and validation roles.
4. **Deterministic enforcement:** Enforce permissions in code and policy engines, never only in prompts.
5. **Read-only by default:** Start with knowledge retrieval and diagnostic functions before write actions.
6. **Human control:** Require approval for consequential, irreversible, or production-impacting operations.
7. **Data minimization:** Send only necessary and appropriately redacted context to the model.
8. **Defense in depth:** Apply controls at the client, API, orchestration, tool, SAP, data, and network layers.
9. **Fail closed:** Reject actions when identity, policy, approval, validation, or telemetry is unavailable.
10. **Evidence by design:** Generate tamper-resistant records for every significant decision and action.
11. **Reversibility:** Define rollback or compensating actions before production execution.
12. **Progressive autonomy:** Increase automation only after measured safety and reliability gates are met.

---

## 6. Logical Architecture

```text
+-------------------- Enterprise Users and Systems ---------------------+
| SAP developers | Functional teams | Basis | Security | Service desk  |
| Approvers | Release managers | Monitoring tools | ITSM integrations  |
+----------------------------------+------------------------------------+
                                   |
                                   v
+----------------------- Experience and Access Layer -------------------+
| Web portal | Chat interface | IDE extension | ITSM plug-in            |
| SSO | MFA | session controls | user notices | secure file upload     |
+----------------------------------+------------------------------------+
                                   |
                                   v
+----------------------- Edge and API Security Layer -------------------+
| WAF | API gateway | rate limits | schema validation | OAuth/OIDC      |
| request IDs | anti-replay | threat detection | tenant routing         |
+----------------------------------+------------------------------------+
                                   |
                                   v
+---------------------- Application Control Plane ----------------------+
| Backend for frontend | Workflow API | Case service | Approval service |
| Policy decision point | Entitlement service | Audit event service     |
+---------------------+-----------------------------+-------------------+
                      |                             |
                      v                             v
+---------------- AI Orchestration Plane --+   +--- Integration Plane --+
| LangChain/equivalent workflow graph      |   | Tool gateway           |
| Agent state machine                      |   | SAP adapters            |
| Prompt templates and versioning          |   | ITSM/Git/CI adapters    |
| Input/output guardrails                  |   | Command allowlists       |
| Context builder and data redaction       |   | Parameter constraints    |
| Model routing and confidence evaluation  |   | Transaction limits       |
+-------------------+----------------------+   +------------+------------+
                    |                                       |
          +---------+----------+                            v
          |                    |                +-------------------------+
          v                    v                | Enterprise Systems      |
+------------------+   +--------------------+   | SAP ECC/S/4HANA         |
| Model Gateway    |   | Knowledge Platform |   | SAP BTP/integration     |
| Private LLMs     |   | Vector index       |   | ITSM/change management  |
| Content filters  |   | Document store     |   | Git and CI/CD           |
| Token budgets    |   | Metadata/RBAC/ACL  |   | Monitoring/SIEM         |
+------------------+   +--------------------+   +-------------------------+

+---------------- Platform and Security Foundation ---------------------+
| Secrets vault | KMS/HSM | service mesh/mTLS | private networking      |
| container platform | artifact registry | SIEM | backup | DR           |
| vulnerability management | configuration management | FinOps          |
+------------------------------------------------------------------------+
```

---

## 7. Trust Boundaries

### TB-1: User Device to Enterprise Edge

Requests originate from devices that may be compromised. The edge must enforce authentication, session validation, request-size limits, malware scanning for uploads, and anti-automation protections.

### TB-2: Edge to Application Control Plane

Only authenticated requests with validated schemas and trusted routing headers may pass. End-user identity must be propagated in signed claims without trusting user-supplied identity fields.

### TB-3: Application to AI Orchestration Plane

Agent inputs may contain malicious prompt content. Context must be classified and sanitized. The orchestrator must receive a scoped task identity, not reusable SAP credentials.

### TB-4: Orchestrator to Model Provider

Prompts can contain regulated or confidential information. The model gateway must enforce provider allowlists, data-loss controls, token budgets, logging rules, and retention policy.

### TB-5: Orchestrator to Knowledge Platform

Retrieved documents are untrusted input. Retrieval must enforce document-level authorization, provenance, validity periods, and approved-source filters.

### TB-6: Orchestrator to Tool Gateway

This is the principal safety boundary. The agent may propose a tool call, but the gateway independently validates identity, entitlement, parameters, workflow state, approval evidence, and risk policy.

### TB-7: Tool Gateway to SAP and Enterprise Systems

System-to-system communication must use private channels, mTLS where supported, vaulted credentials, narrow technical roles, transaction limits, and SAP-side authorization checks.

### TB-8: Production and Non-Production

Production must use separate accounts, credentials, networks, data stores, model configurations, indexes, and CI/CD approvals. Production data must not be copied to lower environments unless masked and explicitly approved.

---

## 8. Core Components

### 8.1 User Experience

Supported channels may include a secure web portal, Microsoft Teams or equivalent enterprise chat, an ITSM extension, and an IDE assistant. The UI must:

- Show the authenticated identity and current operating environment
- Clearly distinguish recommendations from executed actions
- Display data-classification warnings
- Present sources, confidence indicators, and limitations
- Require explicit approval for high-risk actions
- Prevent hidden instructions in uploaded files from being treated as trusted commands
- Provide an action history and approval status
- Avoid presenting model-generated output as verified fact

### 8.2 API Gateway and Backend

Recommended implementation:

- TypeScript with a supported Node.js framework for externally facing APIs
- OpenAPI contracts and strict request/response schemas
- Correlation IDs and distributed tracing
- OAuth 2.0 or OIDC for user requests
- Workload identity or short-lived tokens for service-to-service access
- Pagination and output-size limits
- Rate limiting by user, application, route, and organization
- Central handling for validation, error normalization, and audit events

### 8.3 Agent Orchestrator

The orchestrator manages a bounded state machine rather than an unconstrained autonomous loop. Each workflow should contain explicit states, permitted transitions, timeouts, retry limits, and terminal outcomes.

Example states:

```text
RECEIVED
  -> IDENTITY_VERIFIED
  -> REQUEST_CLASSIFIED
  -> DATA_SCOPE_APPROVED
  -> CONTEXT_RETRIEVED
  -> ANALYSIS_GENERATED
  -> OUTPUT_VALIDATED
  -> HUMAN_REVIEW_REQUIRED or SAFE_RESPONSE_READY
  -> ACTION_PROPOSED
  -> POLICY_CHECKED
  -> APPROVED
  -> EXECUTED
  -> VERIFIED
  -> CLOSED
```

Forbidden behavior:

- Infinite reasoning or tool loops
- Dynamic loading of arbitrary tools
- Execution of model-generated code in the orchestrator process
- Passing raw model output directly into an SAP adapter
- Reusing one user's retrieved context for another user
- Escalating permissions based on prompt content

### 8.4 Model Gateway

All LLM traffic should pass through a model gateway that provides:

- Approved provider and model allowlists
- Regional and tenant routing rules
- Prompt and completion filtering
- Sensitive-data detection and redaction
- Request and response size limits
- Model-version pinning
- Timeout, retry, and circuit-breaker controls
- Cost and token quotas
- Abuse detection
- Restricted logging with sensitive-value masking
- Provider health and fallback policy

A fallback model must not silently have weaker privacy or security terms than the primary model.

### 8.5 Knowledge and RAG Platform

The knowledge platform includes a source registry, ingestion pipeline, object store, metadata database, embeddings service, vector index, and retrieval API.

Every document should carry:

- Source system and canonical identifier
- Owner and business domain
- Classification level
- Access-control list or entitlement attributes
- Version and effective date
- Review and expiry dates
- Approval status
- Integrity hash
- Environment, system ID, client, and application scope
- Retention and legal-hold metadata

Retrieval should combine semantic similarity with metadata filters and authorization. A similarity score alone must never grant access.

### 8.6 Tool Gateway

The tool gateway is the only route through which an agent may interact with SAP or other enterprise systems. It should expose small, typed, business-level operations rather than general-purpose access.

Good tool examples:

```text
get_incident_summary(incident_id)
get_transport_status(transport_id)
read_application_log(system_id, object, time_range)
validate_change_window(change_id)
run_approved_health_check(check_id, system_id)
create_draft_change_record(case_id, approved_fields)
attach_evidence(change_id, evidence_reference)
```

Prohibited tools:

```text
execute_arbitrary_rfc(function_name, parameters)
run_sql(query)
run_shell(command)
update_any_table(table, values)
execute_abap_source(source_code)
impersonate_user(user_id)
```

Each tool definition must include:

- Business purpose
- Inputs and strict schema
- Output schema
- Data classification
- Required roles and entitlements
- Permitted systems and clients
- Read or write classification
- Risk tier
- Approval requirements
- Idempotency behavior
- Timeout and retry policy
- Audit fields
- Rollback or compensation method

### 8.7 SAP Integration Layer

Use approved interfaces and avoid direct database connectivity. Controls include:

- Dedicated communication users or workload identities
- Separate credentials per environment and integration
- SAP authorization roles restricted to required objects and values
- Trusted RFC only where justified and securely configured
- Network allowlists and encrypted communication
- BAPI transaction handling with commit and rollback controls
- OData scopes and service-level authorization
- Table and field allowlists for read operations
- Explicit client and system validation
- Protection against cross-system routing mistakes
- SAP Security Audit Log and application-change logging where applicable

### 8.8 Policy and Approval Service

The policy service evaluates facts independent of the model. Inputs may include:

- Authenticated user identity
- Business role and team
- SAP entitlements
- Tool and action risk tier
- Target system, client, and environment
- Ticket and change status
- Maintenance window
- Data classification
- Approval chain
- Segregation-of-duties conflicts
- Emergency-access status
- Model confidence and validation results, as non-authoritative signals

Example policy outcome:

```json
{
  "decision": "REQUIRE_APPROVAL",
  "policyVersion": "sap-agent-prod-17",
  "reasons": [
    "Production write operation",
    "Change record is approved but execution window has not started"
  ],
  "requiredApproverRoles": [
    "SAP_RELEASE_MANAGER",
    "APPLICATION_OWNER"
  ],
  "expiresAt": "2026-09-08T18:30:00Z"
}
```

### 8.9 Audit and Evidence Service

Audit records should be append-only and sent to a protected central platform. Each record should contain:

- Event ID, timestamp, and correlation ID
- User and workload identity
- Session and case identifier
- Source channel
- Workflow and prompt-template version
- Model provider, model ID, and configuration version
- Data classifications involved
- Retrieved document identifiers and versions
- Proposed and authorized tool name
- Validated parameters or protected parameter hash
- Policy decision and policy version
- Approvers and approval timestamps
- Execution outcome and SAP transaction reference
- Verification result
- Sanitized error details

Full prompts and completions should not be logged by default. Logging them requires a documented need, restricted access, encryption, masking, retention limits, and legal/privacy approval.

---

## 9. Agent Roles and Boundaries

Prefer several narrow agents or workflow modules over one all-powerful agent.

### 9.1 Intake Agent

- Normalizes the request
- Detects system, client, module, urgency, and business impact
- Classifies data sensitivity
- Links the request to an ITSM case
- Does not access production tools

### 9.2 Diagnostic Agent

- Retrieves approved logs, telemetry, known errors, and runbooks
- Generates hypotheses with supporting evidence
- Can invoke only approved read-only diagnostic tools
- Must state uncertainty and missing evidence

### 9.3 Development Agent

- Explains ABAP or integration code
- Proposes patches in a branch or draft
- Generates unit-test candidates
- Cannot merge code, release transports, or deploy to production

### 9.4 Change Planning Agent

- Creates impact summaries, implementation plans, test plans, and rollback plans
- Validates required fields and dependencies
- Creates only draft records unless an authorized workflow advances them

### 9.5 Knowledge Agent

- Retrieves approved knowledge
- Drafts new knowledge articles from resolved cases
- Cannot publish articles without owner review

### 9.6 Execution Agent or Deterministic Executor

The preferred design is a deterministic execution service rather than a conversational agent. It:

- Accepts only approved, signed action manifests
- Revalidates current approvals and maintenance windows
- Calls only allowlisted tools
- Enforces idempotency and transaction limits
- Records immutable evidence
- Performs post-action verification
- Stops and escalates on unexpected state

---

## 10. End-to-End Production Workflows

## 10.1 Incident Management

### Phase A: Intake

1. User signs in through SSO and MFA.
2. The portal creates a correlation ID and captures the stated issue.
3. The intake service links or creates an ITSM incident.
4. Input is scanned for malicious content, secrets, personal data, and unsupported attachments.
5. The system identifies SAP system, client, module, priority, and affected process.
6. Access policy confirms that the user may view the case and relevant system metadata.

### Phase B: Triage

1. The agent retrieves only authorized incident details and safe telemetry.
2. The classifier assigns a category and recommends priority.
3. Priority remains subject to deterministic business rules or service-desk review.
4. Duplicate and related incidents are searched by authorized metadata.
5. The system assigns the ticket to an appropriate support queue.

### Phase C: Diagnosis

1. The diagnostic agent constructs a minimal context package.
2. The retrieval service filters runbooks by entitlement, environment, module, validity, and approval status.
3. Read-only diagnostics are executed through the tool gateway.
4. The model develops ranked hypotheses.
5. The output validator checks that claims are supported by cited evidence.
6. A specialist reviews high-severity or low-confidence diagnoses.

### Phase D: Remediation Planning

1. The agent proposes one or more remediation options.
2. Each option includes impact, prerequisites, risk, validation, and rollback.
3. The policy service assigns a risk tier.
4. Read-only or advisory responses may be returned directly when policy permits.
5. Any write action creates or links a change record and requires the applicable approval path.

### Phase E: Controlled Execution

1. Approval service confirms named approvers and segregation of duties.
2. The executor rechecks target system, client, maintenance window, and current incident state.
3. Parameters are validated against tool-specific allowlists.
4. The operation runs using a short-lived workload identity.
5. The result is captured with the SAP transaction or job reference.
6. Unexpected output causes an immediate stop and escalation.

### Phase F: Verification and Closure

1. Post-change health checks run independently of the model's recommendation.
2. The user or service owner validates restored business function.
3. The incident is updated with sanitized evidence and resolution details.
4. A draft root-cause record or knowledge article is created.
5. Knowledge publication requires owner approval.
6. Metrics and lessons learned feed a controlled improvement backlog.

## 10.2 Service Request Fulfillment

1. Authenticate the requester and validate request eligibility.
2. Identify the service catalog item and required fields.
3. Apply deterministic entitlement and segregation-of-duties checks.
4. Retrieve approved fulfillment instructions.
5. Create a fulfillment plan and risk tier.
6. Obtain owner, security, or manager approval as required.
7. Execute through an approved API or queue for a human fulfiller.
8. Verify the result and update the service request.
9. Record fulfillment evidence and access expiry where applicable.

Examples include user-role requests, report scheduling, interface onboarding, and master-data workflow initiation. Sensitive access requests must remain governed by SAP GRC or the organization's authoritative access-control process.

## 10.3 Change Request Process

1. Create or link a change record.
2. Capture business justification and affected systems.
3. Generate impact analysis from code, configuration, interfaces, jobs, roles, and dependencies.
4. Classify normal, standard, emergency, or low-risk change according to enterprise policy.
5. Produce implementation, testing, validation, monitoring, and rollback plans.
6. Link requirements, commits, work items, transports, test evidence, and approvals.
7. Run security, quality, and segregation-of-duties checks.
8. Obtain CAB or delegated approval.
9. Enforce release window and transport sequence.
10. Deploy through the standard release pipeline.
11. Run smoke tests and business validation.
12. Close only after evidence is complete.

The agent may prepare artifacts but must not be the sole approver, deployer, and validator.

## 10.4 ABAP Development Process

### Requirements and Design

- Convert approved requirements into acceptance criteria.
- Identify affected packages, objects, interfaces, enhancements, jobs, and authorization checks.
- Produce a technical design with performance and security considerations.
- Confirm clean-core and extensibility strategy where applicable.

### Development

- Generate code only in a controlled branch, development system, or isolated workspace.
- Follow naming, package, transport, exception, logging, and documentation standards.
- Avoid hard-coded credentials, system IDs, clients, destinations, and personal data.
- Use released APIs and approved extension points whenever required by enterprise architecture.

### Automated Quality

- Syntax and activation checks
- ABAP Unit tests
- Static analysis and ATC
- Security-focused checks
- Performance checks for database access and large-volume processing
- Dependency and secret scanning for adjacent TypeScript, Python, and JavaScript services
- Software composition analysis
- Infrastructure policy checks

### Review and Testing

- Peer review by an authorized developer
- Functional review by the responsible consultant
- Negative and authorization testing
- Integration and regression tests
- Volume and performance tests where relevant
- QA evidence linked to the change

### Transport and Release

- Validate transport ownership and object list.
- Detect transport collisions and dependency order.
- Ensure no unresolved critical quality findings.
- Obtain release approvals.
- Use controlled import tools and approved schedules.
- Perform post-import validation.
- Preserve rollback or forward-fix procedures.

## 10.5 Knowledge Automation Process

1. Ingest only from registered sources.
2. Scan files for malware and unsafe active content.
3. Parse content in a sandbox.
4. Classify data and detect secrets or personal information.
5. Apply redaction or reject the document.
6. Attach provenance, ownership, ACL, version, and expiry metadata.
7. Require approval for operational runbooks and high-impact procedures.
8. Generate embeddings in an approved environment.
9. Store documents and indexes by environment and classification.
10. Retrieve with entitlement and metadata filters.
11. Cite the exact source version in responses.
12. Revoke deleted, superseded, or expired content from both object storage and indexes.
13. Periodically revalidate owners and access lists.

---

## 11. Action Risk Classification

### Tier 0: Informational

Examples:

- Explain an error message
- Summarize an approved incident
- Retrieve a public or broadly available internal standard

Controls:

- Authentication
- Retrieval authorization
- Input/output filtering
- Audit event

### Tier 1: Read-Only Diagnostic

Examples:

- Read approved application logs
- Check job status
- Read transport status

Controls:

- All Tier 0 controls
- Tool-specific authorization
- System and client allowlists
- Query and time-range limits
- Sensitive-field masking

### Tier 2: Draft or Non-Production Write

Examples:

- Create a draft change
- Commit a code proposal to a feature branch
- Execute a test-environment diagnostic or reversible operation

Controls:

- All Tier 1 controls
- Ticket linkage
- Requestor entitlement
- Independent validation
- Idempotency
- Review before promotion

### Tier 3: Production-Relevant or Privileged

Examples:

- Trigger an approved production job
- Perform a controlled configuration action
- Initiate a tightly bounded remediation

Controls:

- All Tier 2 controls
- Named human approvals
- Segregation-of-duties verification
- Valid change record and window
- Time-bound action token
- Pre-check, post-check, and rollback plan
- Enhanced monitoring

### Tier 4: Prohibited for AI-Initiated Execution

Examples:

- Release or import unrestricted production transports
- Direct production table updates
- Disable security controls
- Create privileged SAP users or roles without the authoritative GRC workflow
- Run arbitrary ABAP, SQL, shell, or RFC commands
- Alter audit evidence
- Export bulk sensitive data

These operations must be handled by established privileged procedures and authorized personnel.

---

## 12. Data Architecture and Classification

### 12.1 Data Categories

- Public
- Internal
- Confidential
- Restricted or regulated
- Security secrets

Examples of restricted data include customer, vendor, employee, financial, payroll, authentication, and production business records. Secrets include passwords, private keys, tokens, certificates, connection strings, and recovery codes.

### 12.2 Data Flow Rules

- Do not send secrets to the LLM.
- Do not embed secrets in vector indexes.
- Redact or tokenize personal and sensitive business fields before model processing.
- Preserve a protected mapping only when the business workflow requires reversible tokenization.
- Keep production and non-production indexes separate.
- Apply document-level access control at retrieval time.
- Enforce regional and residency constraints.
- Define retention for prompts, completions, traces, documents, embeddings, caches, and audit records.
- Delete derived artifacts when their authoritative source is deleted, unless retention law requires preservation.

### 12.3 Context-Minimization Pipeline

```text
Raw authorized source data
  -> field classification
  -> policy-based field selection
  -> secret and PII detection
  -> redaction/tokenization
  -> size and time-range reduction
  -> provenance attachment
  -> model context
```

### 12.4 Logging Rules

Never intentionally log:

- Passwords or private keys
- Full access or refresh tokens
- Unmasked financial or personal identifiers
- Full production payloads without an approved use case
- Hidden system prompts containing security-sensitive configuration

Prefer event metadata, stable identifiers, hashes, and masked values.

---

## 13. Identity, Authorization, and Secrets

### 13.1 Human Identity

- SSO through the enterprise identity provider
- MFA for privileged or production functions
- Conditional access based on device, network, risk, and location policy
- Short session lifetime for privileged operations
- Step-up authentication before Tier 3 actions
- Group and attribute-based authorization
- Periodic access recertification

### 13.2 Workload Identity

- Unique identity per service and environment
- Short-lived federated credentials where possible
- No shared production service accounts across unrelated tools
- Rotation and revocation support
- Mutual authentication for internal services
- Restricted network paths

### 13.3 SAP Authorization

Authorization must be enforced both before the request reaches SAP and within SAP. The external policy layer supplements but never replaces SAP authorization objects, organizational-value restrictions, roles, and change-control processes.

### 13.4 Secrets Management

- Store secrets in an approved vault backed by KMS or HSM controls.
- Retrieve secrets at runtime using workload identity.
- Never place secrets in source code, container images, prompts, vector stores, or pipeline logs.
- Rotate credentials and certificates on a defined schedule and after suspected compromise.
- Log secret access without logging secret values.
- Use break-glass credentials only through PAM with monitoring and expiry.

---

## 14. Guardrails and Safety Controls

### 14.1 Input Guardrails

- Request-schema validation
- Prompt-injection pattern detection
- Secret and personal-data detection
- File malware scanning
- File type, size, and count limits
- OCR and hidden-text inspection where supported
- URL and external-content restrictions
- Unicode normalization and control-character handling
- Conversation length and token-budget limits

### 14.2 Retrieval Guardrails

- Source allowlists
- Document-level authorization
- Approved-status and validity-date filters
- Environment and system filters
- Poisoning and anomaly detection
- Retrieval-count and context-size limits
- Source diversity requirements for high-impact recommendations
- Exact provenance in the response

### 14.3 Output Guardrails

- Structured output schemas
- Fact-to-source consistency checks
- Secret and sensitive-data scanning
- Hallucination or unsupported-claim flags
- Code and command detection
- Environment and system validation
- Risk classification
- User-facing uncertainty and escalation guidance

### 14.4 Tool Guardrails

- No tool selection based solely on free-text model output
- Typed tool calls only
- Independent authorization
- Allowlists for tool, system, client, object, field, and operation
- Parameter range and format validation
- Approval tokens bound to exact action parameters
- Nonce, expiry, and anti-replay controls
- Idempotency keys for writes
- Transaction and volume limits
- Timeout, retry, and circuit breakers
- Post-execution verification

### 14.5 Loop and Resource Guardrails

- Maximum reasoning steps
- Maximum tool calls per workflow
- Maximum retries per tool
- Wall-clock timeout
- Token and cost budget
- Duplicate-call detection
- Stop on contradictory or repeated failures
- Human escalation after threshold breach

---

## 15. Threat Model

### 15.1 Assets

- SAP business and configuration data
- Customer, employee, vendor, and financial data
- SAP credentials, certificates, tokens, and destinations
- Source code and transports
- Incident, change, and knowledge records
- Prompt templates and agent policies
- Model inputs, outputs, and conversation state
- Vector indexes and document stores
- Audit trails and approval evidence
- CI/CD credentials and artifacts
- Availability and integrity of SAP systems

### 15.2 Threat Actors

- External attacker
- Malicious or careless insider
- Compromised end-user device
- Compromised developer or support account
- Compromised third-party dependency
- Malicious document publisher
- Abused service identity
- Misconfigured model or cloud service
- Over-privileged administrator

### 15.3 STRIDE Analysis

#### Spoofing

Threats:

- Stolen user session or OAuth token
- Forged service identity
- Impersonated approver
- Cross-tenant or cross-environment token misuse

Controls:

- MFA and conditional access
- Short-lived signed tokens with audience validation
- Workload identity and mTLS
- Step-up authentication
- Approval signatures bound to action and expiry
- Session revocation and anomaly detection

#### Tampering

Threats:

- Modified requests or tool parameters
- Poisoned runbooks or embeddings
- Altered model routing or prompt templates
- Modified approval evidence
- Transport or code manipulation

Controls:

- TLS, request signing, schema validation, and integrity hashes
- Controlled ingestion and content approval
- Version-controlled prompts and policy-as-code
- Append-only audit records
- Signed artifacts and protected branches
- Transport and dependency validation

#### Repudiation

Threats:

- A user denies requesting or approving an action
- A service action lacks traceability
- Model or policy version cannot be reconstructed

Controls:

- Correlation IDs and signed audit events
- Recorded identities, timestamps, version IDs, and action hashes
- Central time synchronization
- Immutable retention
- Approval and execution evidence

#### Information Disclosure

Threats:

- Production data in prompts or logs
- Unauthorized RAG retrieval
- Cross-user conversation leakage
- Bulk SAP extraction through read tools
- Model provider retention or training exposure

Controls:

- Data minimization, tokenization, and DLP
- Document-level ACLs
- Session isolation
- Query, field, time, and volume limits
- Enterprise model contracts and retention controls
- Encryption at rest and in transit

#### Denial of Service

Threats:

- API flooding
- Agent-loop exhaustion
- Expensive retrieval or model requests
- SAP connection-pool depletion
- Poisoned inputs causing parser failure

Controls:

- WAF, quotas, and rate limits
- Step, token, and cost budgets
- Circuit breakers and bounded retries
- Bulkheads and separate connection pools
- Sandboxed parsing
- Graceful degradation to manual operation

#### Elevation of Privilege

Threats:

- Prompt asks the agent to act as an administrator
- Tool accepts arbitrary system or function names
- Technical user has broad SAP rights
- Agent bypasses GRC or change approval
- Non-production credentials work in production

Controls:

- Deterministic authorization outside the model
- Narrow typed tools and allowlists
- Least-privilege SAP roles
- GRC and approval integration
- Separate environment identities
- Regular entitlement reviews and penetration tests

### 15.4 AI-Specific Attack Scenarios

#### Scenario A: Direct Prompt Injection

An attacker enters instructions to ignore policy and extract production data.

Mitigations:

- Treat user content as data, not authority.
- Prevent prompts from granting capabilities.
- Apply retrieval and tool authorization independently.
- Filter sensitive output and enforce response limits.

#### Scenario B: Indirect Prompt Injection

A malicious instruction is hidden in a ticket, PDF, wiki page, code comment, or log entry retrieved by the agent.

Mitigations:

- Label retrieved content as untrusted.
- Separate system instructions from retrieved data.
- Sanitize and classify documents during ingestion.
- Require tool authorization regardless of retrieved instructions.
- Display suspicious-source warnings and block high-risk automation.

#### Scenario C: Tool Confusion or Excessive Agency

The model selects a tool or parameters that exceed the user's intent.

Mitigations:

- Use workflow-specific tool allowlists.
- Present an action preview.
- Bind approval to exact normalized parameters.
- Revalidate at execution time.
- Apply transaction and blast-radius limits.

#### Scenario D: RAG Poisoning

An attacker uploads a false runbook that recommends a dangerous production action.

Mitigations:

- Registered publishers and approval workflows
- Cryptographic integrity checks
- Version and expiry metadata
- Retrieval from trusted collections for operational decisions
- Source citations and human review

#### Scenario E: Sensitive Data Exfiltration

An attacker slowly extracts records through repeated, apparently legitimate queries.

Mitigations:

- Aggregate query quotas
- Field and record limits
- Behavioral analytics
- DLP and egress monitoring
- Purpose-bound access
- Alerts for enumeration patterns

#### Scenario F: Model Hallucination

The model invents an SAP note, configuration value, incident cause, or remediation.

Mitigations:

- Require exact source references for factual operational claims.
- Separate observations, hypotheses, and verified facts.
- Use deterministic checks.
- Escalate below confidence or evidence thresholds.
- Never permit unsupported claims to trigger execution.

#### Scenario G: Compromised Agent Dependency

A package, container, plug-in, or CI dependency is compromised.

Mitigations:

- Locked dependencies and trusted registries
- Software bills of materials
- Signature and provenance verification
- Vulnerability and malware scanning
- Minimal images and runtime privileges
- Rapid revocation and rebuild procedures

#### Scenario H: Cross-Environment Contamination

Production data, credentials, or vector content becomes accessible in development.

Mitigations:

- Separate accounts, networks, vaults, indexes, and identities
- Environment tags validated at every layer
- Masked test data
- Deployment policies preventing production endpoints in lower environments
- Continuous configuration monitoring

### 15.5 Example Risk Register

| ID | Risk | Likelihood | Impact | Initial Rating | Primary Treatment | Residual Target |
|---|---|---:|---:|---:|---|---:|
| R-01 | Prompt injection triggers unauthorized SAP action | High | Critical | Critical | Tool gateway, deterministic policy, approval binding | Medium |
| R-02 | Sensitive production data reaches an unapproved model | Medium | Critical | High | Model gateway, DLP, provider allowlist, private routing | Low |
| R-03 | Poisoned knowledge causes unsafe remediation | Medium | High | High | Trusted ingestion, approval, provenance, expiry | Medium |
| R-04 | Over-privileged SAP communication user is compromised | Medium | Critical | High | Least privilege, vault, rotation, network restriction | Medium |
| R-05 | Hallucinated fix causes outage | High | High | High | Evidence checks, human review, bounded execution | Medium |
| R-06 | Audit records expose secrets | Medium | High | High | Masking, restricted logging, retention controls | Low |
| R-07 | Agent loop causes cost or availability incident | Medium | Medium | Medium | Step, token, retry, and cost limits | Low |
| R-08 | Approval is replayed for different parameters | Medium | Critical | High | Signed parameter hash, nonce, expiry, revalidation | Low |
| R-09 | Cross-user RAG leakage | Medium | Critical | High | ACL-filtered retrieval, session isolation, tests | Low |
| R-10 | Supply-chain compromise in agent service | Medium | Critical | High | SBOM, signatures, scanning, provenance, isolation | Medium |

Risk acceptance must name an owner, rationale, compensating control, expiry, and review date.

---

## 16. Secure Development Lifecycle

### 16.1 Planning

- Define use cases, excluded actions, and measurable outcomes.
- Complete architecture, privacy, data, and threat-model reviews.
- Assign system, data, model, and risk owners.
- Establish action risk tiers and approval paths.
- Define reliability, security, and model-quality objectives.

### 16.2 Repository Structure

```text
sap-agent-platform/
  apps/
    web-portal/
    api-service/
    agent-orchestrator/
    tool-gateway/
    approval-service/
  packages/
    contracts/
    policy-client/
    telemetry/
    redaction/
    sap-adapters/
  prompts/
    templates/
    evaluations/
  policies/
    authorization/
    data-handling/
    action-risk/
  infrastructure/
    modules/
    environments/
  tests/
    unit/
    integration/
    security/
    evaluations/
    resilience/
  docs/
    architecture/
    runbooks/
    decisions/
    threat-model/
```

### 16.3 Coding Standards

- TypeScript strict mode for TypeScript services
- Strong validation at trust boundaries
- Secure defaults and explicit environment configuration
- No unsafe dynamic evaluation
- Parameterized queries and requests
- Centralized error handling
- Structured logs with redaction
- Dependency pinning
- Mandatory peer review
- Security-focused review for adapters, policies, and tool definitions

### 16.4 Branch and Review Controls

- Protected main and release branches
- Pull requests with required reviewers
- CODEOWNERS for policies, SAP adapters, infrastructure, and prompts
- Signed or verified commits where required
- No direct production changes
- Automated status checks before merge
- Separation between code author and production approver

---

## 17. Testing Strategy

### 17.1 Unit Testing

Test:

- Input schemas
- Redaction and classification
- Policy decisions
- Tool parameter constraints
- State-machine transitions
- Output validation
- Retry, timeout, and idempotency logic

### 17.2 Integration Testing

Use lower-environment SAP systems or controlled simulators to test:

- Authentication and token exchange
- SAP authorization failures
- OData, RFC, BAPI, and integration errors
- Transaction rollback
- ITSM and approval workflows
- Knowledge entitlement filters
- Trace and audit propagation

### 17.3 AI Evaluation

Maintain versioned evaluation sets for:

- Intent classification
- SAP error diagnosis
- Source-grounded question answering
- Correct refusal of unauthorized requests
- Prompt-injection resistance
- Sensitive-data handling
- Tool selection and parameter correctness
- Hallucination and unsupported claims
- Multilingual support where required

Do not use only average accuracy. Track false authorization, unsafe-action, data-leakage, and unsupported-claim rates separately.

### 17.4 Adversarial Testing

Include:

- Direct and indirect prompt injection
- Encoded and obfuscated instructions
- Malicious files and hidden text
- Cross-user and cross-tenant access attempts
- Approval replay and parameter substitution
- Bulk extraction and enumeration
- Tool-loop and cost-exhaustion attempts
- Knowledge poisoning
- Model fallback and outage behavior
- Compromised credential scenarios

### 17.5 Performance and Resilience Testing

- Peak concurrent users
- Large but permitted case histories
- SAP latency and connection-pool stress
- Model and vector-store degradation
- Queue backlogs
- Regional failure
- Backup restoration
- Partial dependency failure

### 17.6 Release Gates

A production release must fail if:

- Critical or high vulnerabilities exceed policy
- Required evaluation thresholds are not met
- Unauthorized-access tests fail
- Prompt-injection tests enable a prohibited action
- Rollback is untested
- Audit events are incomplete
- Required owners have not approved the release

---

## 18. CI/CD and Supply-Chain Security

### 18.1 Pipeline Stages

```text
Commit
  -> formatting and linting
  -> unit tests
  -> secret scanning
  -> static security analysis
  -> dependency and license scanning
  -> build
  -> SBOM generation
  -> artifact signing
  -> container and IaC scanning
  -> deploy to development
  -> integration and AI evaluations
  -> deploy to test/quality
  -> security and resilience tests
  -> release approval
  -> canary or staged production deployment
  -> post-deployment verification
```

### 18.2 Artifact Controls

- Immutable versioned artifacts
- Trusted private registries
- Provenance and signatures
- SBOM for each release
- No build in the production environment
- Same promoted artifact across environments
- Emergency patch process with retrospective review

### 18.3 Prompt and Policy Deployment

Prompts, agent graphs, tool schemas, evaluators, and policies are production artifacts. They require:

- Version control
- Code review
- Security review for privileged changes
- Automated regression evaluation
- Environment promotion
- Rollback capability
- Runtime version telemetry

---

## 19. Environment and Deployment Architecture

### 19.1 Environment Separation

At minimum:

- Local isolated development
- Shared development
- Test
- Quality or user acceptance
- Pre-production
- Production

Each environment should have separate:

- Cloud subscription or account where practical
- Network boundaries
- Service identities
- Vault secrets and encryption keys
- Model deployments
- Vector indexes and storage
- SAP destinations
- ITSM integration credentials
- Logging and monitoring configuration

### 19.2 Network Controls

- Private endpoints for model, data, and SAP integration where available
- Deny-by-default ingress and egress
- Egress proxy and domain allowlists
- Web application firewall
- Network segmentation between edge, application, AI, data, and integration tiers
- No inbound administrative access from the public internet
- Privileged administration through approved secure access paths

### 19.3 Container and Runtime Security

- Minimal non-root images
- Read-only filesystems where possible
- Dropped Linux capabilities
- Resource limits
- Runtime security monitoring
- Network policies
- Image signing and admission control
- Regular base-image rebuilds
- No long-lived secrets in environment variables when a mounted or federated alternative is available

### 19.4 Production Rollout

Recommended phases:

1. **Shadow mode:** Agent observes and produces recommendations without user-visible execution.
2. **Advisory mode:** Approved users receive answers and evidence, with no write tools.
3. **Read-only diagnostics:** Narrow production read tools are enabled.
4. **Draft automation:** Agent creates drafts in ITSM or code branches.
5. **Bounded non-production execution:** Reversible lower-environment tools are enabled.
6. **Approved production execution:** Selected Tier 3 operations are enabled with named approvals.

Each phase requires measured safety, quality, adoption, and reliability criteria before progression.

---

## 20. Observability and SRE

### 20.1 Technical Metrics

- Request rate, error rate, and latency
- Model latency and token usage
- Retrieval latency and result count
- Tool call success, failure, and timeout
- SAP connection-pool usage
- Queue depth
- Cache behavior
- Cost by use case and team

### 20.2 AI Quality and Safety Metrics

- Grounded-answer rate
- Unsupported-claim rate
- Correct refusal rate
- Sensitive-data detection and leak rate
- Prompt-injection detection rate
- Tool-call validation failure rate
- Human override rate
- Escalation rate
- Recommendation acceptance rate
- Post-action verification failure rate

### 20.3 Business Metrics

- Mean time to acknowledge
- Mean time to diagnose
- Mean time to resolve
- Incident reopen rate
- Change failure rate
- Knowledge reuse rate
- Developer lead time
- Defect escape rate
- Hours of manual effort reduced

### 20.4 Service Objectives

Define service-level objectives for:

- Portal and API availability
- Diagnostic response latency
- Audit-event delivery
- Policy-service availability
- Maximum recovery time and recovery point
- Maximum safe degradation period

The system must fail closed for authorization and write execution. It may fail open only for low-risk user-interface functions explicitly designated as non-sensitive.

### 20.5 Alerting

Alert on:

- Spikes in denied tool calls
- Repeated prompt-injection attempts
- Bulk retrieval or enumeration
- Cross-environment access attempts
- Model fallback to an unapproved route
- Missing audit events
- Policy-service bypass or outage
- SAP authorization anomalies
- Unexpected production write volume
- Secret detection in prompts, outputs, or logs
- Unusual cost or token consumption

---

## 21. Operational Runbooks

### 21.1 Model Provider Outage

1. Stop privileged workflows.
2. Apply the approved fallback only if equivalent privacy and security controls exist.
3. Preserve queued work without sensitive prompt exposure.
4. Notify affected users.
5. Resume with idempotency and state validation.
6. Review provider and gateway telemetry.

### 21.2 SAP Connectivity Failure

1. Open the circuit breaker.
2. Stop automatic retries after the defined threshold.
3. Preserve the case and action state.
4. Verify SAP, network, certificate, and destination health.
5. Prevent duplicate writes on recovery.
6. Resume only after connection and authorization checks pass.

### 21.3 Suspected Prompt Injection

1. Block the workflow from tool execution.
2. Preserve sanitized evidence and source identifiers.
3. Flag the content and case for security review.
4. Quarantine the source document if indirect injection is suspected.
5. Search for related retrieval or execution attempts.
6. Update detection tests and controls after review.

### 21.4 Suspected Secret Leakage

1. Stop affected workflows and revoke exposed credentials.
2. Rotate tokens, keys, passwords, or certificates.
3. Locate and restrict logs, prompts, caches, indexes, and backups containing the secret.
4. Notify security and privacy teams according to incident policy.
5. Remove or cryptographically isolate exposed content where permitted.
6. Complete root-cause analysis and prevention actions.

### 21.5 Incorrect Production Action

1. Halt additional actions for the workflow and tool.
2. Engage the service owner and production incident process.
3. Execute the pre-approved rollback or compensating action.
4. Validate business and technical recovery.
5. Preserve evidence.
6. Disable the affected policy, prompt, model, or tool version.
7. Complete problem review before re-enablement.

### 21.6 Knowledge Poisoning

1. Quarantine the document and derived chunks.
2. Remove it from active retrieval indexes.
3. Identify all responses and actions influenced by the content.
4. Review publisher identity and ingestion path.
5. Restore the last trusted version.
6. Strengthen publisher, approval, and integrity controls.

---

## 22. Backup, Recovery, and Business Continuity

Back up:

- Workflow and case state
- Approved knowledge source documents and metadata
- Policy and prompt versions
- Configuration and infrastructure state
- Audit references according to compliance policy

Do not assume vector indexes are the authoritative backup. Rebuild them from approved source documents and metadata.

Recovery testing should cover:

- Regional service loss
- Database corruption
- Vector-index loss
- Vault or key outage
- Model-provider unavailability
- SAP destination failure
- Accidental policy or prompt deployment

A manual support path must remain available when the agent platform is unavailable.

---

## 23. Governance and Operating Model

### 23.1 Required Owners

- Executive sponsor
- Product owner
- SAP application owner
- AI/model owner
- Data owner
- Security owner
- Privacy or legal representative
- Platform/SRE owner
- Service-management owner
- Knowledge owner

### 23.2 Governance Forums

- Architecture review board
- AI risk and model governance review
- Security and privacy review
- Change advisory board
- Operational service review
- Knowledge governance review

### 23.3 Periodic Reviews

- Monthly privileged-tool review
- Quarterly access recertification
- Quarterly model and prompt evaluation
- Periodic penetration and adversarial testing
- Annual or material-change threat-model review
- Retention and data-source review
- Disaster-recovery exercise

### 23.4 Model and Agent Inventory

Maintain an inventory containing:

- Use case and owner
- Model provider and version
- Data classification
- Prompt and workflow versions
- Enabled tools and risk tiers
- Evaluation results
- Known limitations
- Approval history
- Deployment environments
- Retirement date and procedure

---

## 24. Roles and Responsibilities

| Activity | Requester | SAP Developer/Consultant | Security | Application Owner | Release Manager/CAB | Platform/SRE | AI Owner |
|---|---|---|---|---|---|---|---|
| Submit case | R | C | I | I | I | I | I |
| Diagnose issue | C | R | C | A | I | C | C |
| Propose code/change | I | R | C | A | C | I | C |
| Approve privileged access | I | C | R | A | I | I | I |
| Approve production change | I | C | C | A | R | I | I |
| Deploy platform release | I | C | C | I | A | R | C |
| Approve model/prompt release | I | C | C | A | I | C | R |
| Operate production platform | I | C | C | I | I | R/A | C |
| Review AI safety metrics | I | C | R | A | I | C | R |

**R:** Responsible, **A:** Accountable, **C:** Consulted, **I:** Informed.

No one person or agent should be responsible for requesting, approving, executing, and validating the same high-risk production action.

---

## 25. Implementation Roadmap

### Phase 0: Governance and Foundations

- Approve use cases and prohibited actions.
- Confirm data classification and model-provider requirements.
- Complete architecture, privacy, and threat reviews.
- Establish repositories, CI/CD, environment separation, identity, vault, and logging.

### Phase 1: Knowledge Assistant

- Ingest approved non-sensitive documents.
- Implement entitlement-filtered retrieval and citations.
- Add evaluation sets and prompt-injection testing.
- Operate with no SAP tools.

### Phase 2: Incident Assistance

- Integrate ITSM read access.
- Add case summarization, triage, and evidence-backed recommendations.
- Introduce human feedback and quality monitoring.

### Phase 3: Read-Only SAP Diagnostics

- Add narrow diagnostic tools.
- Enforce system, client, field, and time-range constraints.
- Validate SAP-side permissions and logging.
- Pilot with a limited support group.

### Phase 4: Development Assistance

- Add code analysis, test generation, and draft branch creation.
- Integrate static analysis and quality gates.
- Keep merge and transport release under human control.

### Phase 5: Draft Workflow Automation

- Create draft incidents, problems, changes, test plans, and knowledge articles.
- Integrate approval service and policy-as-code.
- Measure correction and rejection rates.

### Phase 6: Bounded Execution

- Select reversible, low-blast-radius operations.
- Require signed approvals and pre/post checks.
- Deploy progressively with canary users and kill switches.
- Expand only after safety objectives are sustained.

---

## 26. Production Readiness Checklist

### Architecture

- [ ] Data-flow and trust-boundary diagrams are approved.
- [ ] Production and non-production are isolated.
- [ ] Tool gateway is the sole agent execution path.
- [ ] No direct production database access exists.
- [ ] High availability and disaster recovery are documented and tested.

### Identity and Access

- [ ] SSO, MFA, and conditional access are active.
- [ ] Workload identities are unique and short-lived.
- [ ] SAP roles are least privilege.
- [ ] Segregation-of-duties checks are enforced.
- [ ] Break-glass access uses PAM and monitoring.

### Data Protection

- [ ] Data classifications and flows are documented.
- [ ] Secrets and personal data are blocked or redacted before model use.
- [ ] Storage, indexes, backups, and logs are encrypted.
- [ ] Retention and deletion processes are tested.
- [ ] Model-provider data handling is approved.

### Agent Safety

- [ ] Workflows are bounded state machines.
- [ ] Tool schemas and allowlists are reviewed.
- [ ] Approval is bound to exact action parameters.
- [ ] Step, retry, token, time, and cost limits are configured.
- [ ] Prompt-injection and RAG-poisoning tests pass.
- [ ] Kill switches are tested.

### Software Delivery

- [ ] Protected branches and required reviews are configured.
- [ ] SAST, dependency, secret, container, and IaC scanning pass.
- [ ] SBOM and artifact signatures are produced.
- [ ] Prompt, policy, and model changes use controlled promotion.
- [ ] Rollback is tested.

### Operations

- [ ] Dashboards and alerts are active.
- [ ] Audit events reach a protected central store.
- [ ] Incident and recovery runbooks are exercised.
- [ ] On-call ownership and escalation are defined.
- [ ] Manual fallback processes exist.

### Governance

- [ ] System, data, model, security, and business owners are named.
- [ ] Risk register and residual-risk acceptance are approved.
- [ ] Access and model reviews are scheduled.
- [ ] User notices and operating procedures are published.

---

## 27. Acceptance Criteria for Initial Production Release

The initial release is acceptable only if:

1. It operates in advisory or approved read-only mode.
2. Every user and service request is authenticated and authorized.
3. Retrieved knowledge is filtered by user entitlement.
4. Sensitive fields are redacted before model processing.
5. No model has reusable SAP credentials.
6. All SAP access passes through narrow, schema-validated tools.
7. Prompt injection cannot independently change permissions or execute a tool.
8. Every response and tool call has a correlation ID and reconstructable evidence.
9. Safety, quality, security, and resilience test thresholds are met.
10. The platform can be disabled without disrupting normal SAP operations.
11. Manual production-support processes remain available.
12. Named business, SAP, security, platform, and AI owners approve go-live.

---

## 28. Example Secure Action Manifest

An action manifest is created by deterministic application logic after validation. The model may propose values, but it cannot sign or authorize the manifest.

```json
{
  "manifestVersion": "1.0",
  "actionId": "act-7c8594d1",
  "caseId": "INC0012345",
  "requestedBy": "enterprise-user-id",
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
  "issuedAt": "2026-09-08T12:00:00Z",
  "expiresAt": "2026-09-08T12:05:00Z",
  "nonce": "single-use-value",
  "idempotencyKey": "INC0012345-Z_APP_HEALTH_04-20260908T1200",
  "signature": "detached-signature-reference"
}
```

The executor must verify signature, expiry, nonce, identity, target, policy decision, parameter hash, current case state, and tool entitlement before execution.

---

## 29. Architecture Decision Records to Create

The implementation team should maintain architecture decision records for:

- Choice of agent orchestration framework
- Model provider and model-routing strategy
- Prompt and completion retention
- Embedding model and vector store
- SAP integration pattern per use case
- Policy engine and approval-token design
- Identity propagation and service authentication
- Data masking and reversible tokenization
- Environment isolation
- Audit-event schema and retention
- Tool risk classification
- Human approval thresholds
- Deployment and rollback strategy
- Business continuity and manual fallback

---

## 30. Final Architecture Position

A safe SAP AI agent platform is not a chatbot connected directly to SAP. It is a governed enterprise application in which AI is one bounded analytical component. Identity, policy, approvals, typed tools, SAP authorizations, release controls, and audit services remain authoritative.

The production design should therefore preserve these boundaries:

```text
User intent
  -> authenticated request
  -> classified and minimized context
  -> bounded AI analysis
  -> validated recommendation
  -> deterministic policy decision
  -> human approval when required
  -> signed, narrow action manifest
  -> tool gateway enforcement
  -> SAP-side authorization
  -> execution
  -> independent verification
  -> immutable evidence
```

This structure provides useful automation while limiting data exposure, preventing untrusted content from becoming authority, maintaining SAP governance, and retaining human accountability for consequential business operations.

---

## Appendix A: Information Required to Tailor This Reference Design

To convert this guide into a system-specific implementation, document:

- SAP landscape, system IDs, clients, modules, and versions
- Hosting model and network topology
- SAP BTP and integration services in use
- Identity provider and SAP identity architecture
- ITSM, change, source-control, and CI/CD products
- Model provider, deployment region, retention settings, and contractual controls
- OpenClaw role, hosting, plug-ins, and required capabilities
- LangChain or alternative orchestration version and deployment model
- Data classifications and applicable regulatory obligations
- Required use cases and prohibited operations
- Existing SAP GRC, PAM, SIEM, DLP, KMS, and secrets platforms
- Recovery objectives and service-level targets
- Approval matrix and segregation-of-duties rules

## Appendix B: Recommended Deliverables

- Context and container architecture diagrams
- Level 0 and Level 1 data-flow diagrams
- Trust-boundary diagram
- Tool catalog and action risk register
- STRIDE worksheet per data flow
- Data inventory and retention schedule
- Model and agent inventory
- Abuse-case and adversarial test suite
- SAP authorization design
- Policy-as-code repository
- CI/CD control design
- Production support handbook
- Disaster recovery plan
- Go-live and rollback plan
