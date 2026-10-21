# Fievel: Open-Source AI Content Systems Architect

## Project brief and implementation plan

**Project name:** Fievel  
**Tagline:** Your AI content systems architect  
**Format:** Open-source GitHub repository  
**Primary audience:** Content designers, UX writers, conversation designers, and AI experience designers  
**Target environments:** OpenAI Codex, Claude Code, and VS Code with compatible AI coding agents  
**Primary goal:** Help content designers learn how to design, build, evaluate, and maintain AI-ready content systems through a guided, hands-on experience.

---

# 1. Instructions for the development agent

You are the lead software architect and engineering partner responsible for designing and implementing Fievel.

Your task is to turn the following product vision into a working open-source repository.

Do not treat this document as an instruction to produce only research or additional specifications. Use it to guide actual implementation.

Begin by researching existing open-source tools, evaluating reusable approaches, and establishing a minimal but extensible architecture.

Then implement a functional vertical slice of the experience.

Follow these principles:

1. Research before reinventing. Identify existing implementations that can be reused, integrated, or adapted.
2. Prioritize working functionality over unnecessary infrastructure.
3. Design for nontechnical content designers.
4. Build around portable files, skills, and open standards wherever practical.
5. Keep the system modular and maintainable.
6. Develop the user experience and technical architecture together.
7. Implement meaningful quality checks and tests.
8. Preserve user ownership and control over generated content systems.
9. Never claim an integration, evaluation, or capability works without verifying it.
10. Document architectural decisions, tradeoffs, limitations, and future opportunities.

You are expected to make reasonable implementation decisions independently, document them, and proceed without requiring approval for every minor choice.

Do not attempt to build the entire product in one pass. Establish a strong foundation, deliver a complete initial workflow, and expand incrementally.

# 2. Product vision

## What is Fievel?

Fievel is an AI-powered guide, educator, and collaborator that helps content designers create the systems that shape AI-generated experiences.

It combines three core capabilities:

**Teach:** Explain content systems, AI concepts, agent architecture, language models, context, tools, and evaluations in language content designers understand.

**Build:** Help users construct real content systems using their organization's existing guidelines, terminology, content patterns, product context, AI requirements, and connected information sources.

**Evaluate:** Help users define what good AI behavior and communication look like, develop realistic test scenarios, run available quality checks, and improve their systems.

Fievel should not function merely as a generic chatbot or collection of prompts. It should guide users through meaningful workflows and produce reusable, maintainable artifacts.

The desired outcome is a content designer who has both a functional content system and a better understanding of how it works.

## Core positioning

Fievel helps content designers move from writing individual pieces of content to designing the systems that influence how AI communicates and behaves.

Its central promise:

**Learn to build AI content systems by building one.**

# 3. Target users and use cases

Fievel should support three primary user profiles.

### Beginner: The curious content designer

Has strong content design skills but limited experience with AI architecture, coding agents, MCP, GitHub, or LLM evaluations.

Needs:
- Clear explanations without unnecessary jargon
- Guided onboarding
- Small, understandable decisions
- Practical examples
- Safe experimentation
- A complete learning experience without company data or paid services

### Intermediate: The practicing AI content designer

Already uses AI tools and has content guidelines, existing prompts, or an emerging agent experience.

Needs:
- Help organizing existing content standards
- Guidance on designing AI behavior
- Knowledge-source integration
- Structured reusable instructions
- Evaluation plans and testing
- Opportunities to improve an existing system

### Advanced: The content systems practitioner

Already works with agents, AI infrastructure, structured content, or automated evaluations.

Needs:
- Fast access to modular workflows
- Extensible content-system schemas
- Integration with existing repositories and services
- Advanced evaluation approaches
- Versioning and governance
- Minimal unnecessary instructional content

Fievel must adapt its explanations and guidance to the user's demonstrated knowledge.

Expert users should not have to complete beginner tutorials.

# 4. The Fievel experience

## Initial interaction

When users first activate Fievel, it should introduce itself conversationally.

Suggested introduction:

"Hi! I'm Fievel.

I help content designers build systems that make AI experiences more consistent, useful, and reliable.

We can start from scratch, work with content guidelines you already have, or improve an existing AI experience.

Along the way, I'll explain the concepts, help you make design decisions, and create the actual files you need.

What would you like to work on?"

Present three starting paths:

**I'm new to this.** Teach me how AI content systems work while helping me build a simple example.

**I have existing content guidelines.** Help me turn my content standards into a system that can guide AI behavior and generated content.

**I'm building an AI experience.** Help me design and evaluate the content and behavioral systems for an AI assistant or agent.

## Conversational behavior

Fievel should:

- Ask questions progressively rather than presenting long questionnaires.
- Explain why information is being requested.
- Introduce terminology when relevant, not all at once.
- Provide examples from realistic content design work.
- Clearly distinguish recommendations from established facts.
- Explain important design decisions and tradeoffs.
- Recognize what the user already understands.
- Allow users to skip educational explanations.
- Summarize decisions before making significant changes.
- Remember project decisions through repository files.
- Make progress visible.
- Never invent organizational policies, approved terminology, or source material.
- Request approval for changes that could overwrite user-owned assets.

The personality should be approachable, knowledgeable, practical, and professional.

Avoid excessive enthusiasm, generic encouragement, and unnecessary technical complexity.

# 5. Educational knowledge base

Fievel needs a curated knowledge library specifically designed around the needs of content designers working with AI.

This is a major product differentiator.

## Core knowledge areas

### Content design foundations
- Content strategy and governance
- Content systems and reusable patterns
- Voice, tone, style, and terminology
- Information architecture
- Structured content and content models
- Accessibility and inclusive language
- Localization and internationalization
- User needs and task-oriented communication

### AI and LLM fundamentals
- How large language models work
- Prompts and instructions
- System instructions and behavioral constraints
- Context windows and tokens
- Model capabilities and limitations
- Retrieval and grounding
- Hallucinations and uncertainty
- Structured outputs
- AI agents and autonomy
- Tool calling and MCP
- Human oversight and escalation

### Designing AI experiences
- Conversation design
- AI interaction patterns
- Designing when agents act versus explain
- Proactive versus reactive communication
- Permissions and confirmations
- Error handling and recovery
- Agent handoffs
- Personalization
- Context management
- Dynamic interfaces and generated UI
- Trust, transparency, and user control

### Evaluation and quality
- Defining successful AI behavior
- Developing test scenarios
- Identifying things to check
- Writing evaluation criteria
- Human review
- Automated checking
- LLM-based evaluation
- Multi-turn conversation testing
- Tool-use evaluation
- Regression testing
- Quality thresholds
- Interpreting failures
- Improving instructions through evaluation results

## Knowledge architecture

Knowledge should be organized into small, reusable modules.

Each module should support:

- Plain-language explanation
- Technical terminology
- Practical examples
- Common mistakes
- Relevant exercises
- Related concepts
- Source references
- Publication or review dates where applicable

Use progressive disclosure.

Do not load the entire knowledge library into the agent's context by default.

Instead, design a method for accessing relevant material on demand.

Maintain a source registry distinguishing:

- Core principles
- External reference material
- Tool-specific documentation
- Version-sensitive information
- Unverified or experimental guidance

Prioritize authoritative primary sources and high-quality open-source projects.

Recent information should be verified where live research is available. Do not claim bundled materials are current without checking their review dates.

# 6. The content-system builder

This is Fievel's central functional capability.

It should help users create and maintain a structured content system that informs AI-generated experiences.

A content system is not simply a style guide or a large prompt.

It is a connected set of decisions, standards, knowledge sources, behavioral instructions, reusable patterns, quality criteria, and governance practices.

## Core system components

### A. Product and audience context

Collect:
- Product description and purpose
- User audiences and needs
- Important user tasks
- Business objectives
- Experience constraints
- Accessibility and localization requirements

### B. Content standards

Collect or develop:
- Content principles
- Voice and tone guidance
- Preferred and prohibited terminology
- Writing conventions
- Reusable language patterns
- Accessibility requirements
- Localization considerations

### C. AI behavior guidelines

Help define:
- What the AI is responsible for
- What the AI may and may not do
- When it should explain rather than act
- When it should request clarification
- When it should confirm an action
- How it should communicate uncertainty
- How it should handle errors
- When it should escalate or hand off
- How it should use personalization and context

### D. Context and knowledge sources

Identify and document:
- Existing guidelines
- Design-system documentation
- Product documentation
- Local files and repositories
- Approved APIs and MCP services
- Knowledge bases
- Existing agent instructions
- Relevant examples and reference material

For every source, record its purpose, owner when known, authority, freshness, permissions, and permitted use.

Do not assume that every source is trustworthy or appropriate for AI consumption.

### E. Evaluation criteria

Define how the system's quality will be measured.

Connect each important design requirement to one or more quality checks or test scenarios.

### F. Governance

Help establish:
- Ownership
- Versioning
- Review and approval processes
- Maintenance responsibilities
- Change history
- Evaluation coverage
- Documentation and provenance

## Important architectural requirement

The output should be structured, versionable, and reusable across tools.

Use readable Markdown where helpful, with JSON or YAML and schemas where machine-readable structure provides value.

Avoid storing the entire system in one massive Markdown file or prompt.

The system should have clear relationships between its components.

# 7. LLM evaluations for content designers

Fievel should make evaluation accessible to people who have never written automated tests.

This experience must translate technical concepts into familiar content design language.

## Progressive terminology

| Technical term | User-facing language |
|---|---|
| Evaluation | Checking AI quality |
| Test case | A situation to test |
| Test dataset | Example situations |
| Assertion | Something to check |
| Evaluation criteria | What makes a good response |
| Ground truth | The correct or expected answer |
| Rubric | Guidelines for judging quality |
| Pass/fail | Did it meet expectations? |
| Regression test | Check that improvements didn't break something else |
| LLM as judge | Using AI to review an AI response |
| Multi-turn evaluation | Checking an entire conversation |
| Tool-call evaluation | Checking whether AI used the right tools |
| Trajectory evaluation | Checking the steps AI took |

Introduce the technical equivalents gradually so users build working knowledge, rather than permanently hiding industry terminology.

## Evaluation workflow

Fievel should guide users through the following process:

**Step 1: Identify the experience.**

What is the AI supposed to help people accomplish?

**Step 2: Define what good looks like.**

Which qualities and behaviors matter?

Examples:
- Accuracy
- Clarity
- Helpful next steps
- Appropriate tone
- Terminology compliance
- Accessibility
- Safe and authorized actions
- Appropriate use of source information

**Step 3: Create realistic situations.**

Generate representative user requests, difficult situations, and potential failure cases.

**Step 4: Define things to check.**

Translate user-defined expectations into evaluation criteria.

**Step 5: Choose how to check.**

Select between:
- Deterministic checks
- Human review
- LLM-based review
- Tool and agent behavior checks

**Step 6: Run available evaluations.**

Use the available evaluation engine only when an actual testable target is configured.

**Step 7: Interpret the results.**

Explain what succeeded, what failed, and why the results matter.

**Step 8: Improve the system.**

Help users make informed changes and run checks again.

## Evaluation example

User says:

"I want my AI to explain payment failures clearly without inventing reasons."

Fievel helps translate this into:

Situation:
A customer asks why their payment was declined.

Things to check:
- Did the AI distinguish known facts from unknown causes?
- Did it avoid inventing a reason?
- Did it communicate clearly?
- Did it provide an appropriate next step?

Fievel then creates the corresponding reusable test definition.

A test that has merely been defined must not be represented as a test that has actually run.

## Evaluation engine

Investigate using Promptfoo as an optional evaluation backend.

Separate the content designer-facing experience from the underlying technical implementation.

Consider deterministic content checks using Vale or lightweight custom validators.

Support manual review when no executable AI target is available.

LLM-based judges should be treated as fallible and their scoring criteria should be inspectable.

Ensure the system can distinguish:
- Test definitions
- Test execution results
- Human judgments
- AI-generated judgments
- Suggested improvements

Store results and changes in a format suitable for review and version control.

# 8. Source discovery and MCP integration

Fievel should help users understand the value of connecting context and data sources without requiring them to understand MCP architecture beforehand.

It should ask questions such as:

"Where does your team keep its writing guidelines?"

"Do you have an existing design system?"

"Are there product documents or examples you'd like me to use?"

"Does your AI already have access to tools or knowledge sources?"

## Integration principles

- Begin with local files and repository content.
- Support external connectors incrementally.
- Use existing, trusted MCP implementations where appropriate.
- Never request users to place credentials in tracked files.
- Require explicit permission for external access and consequential actions.
- Distinguish source discovery from source ingestion.
- Avoid copying confidential documents into public repositories.
- Identify missing, stale, contradictory, or low-quality sources.
- Document integration limitations clearly.

Potential future integrations include GitHub, documentation platforms, design systems, and organizational knowledge bases.

Don't build unnecessary custom MCP servers when maintained solutions already exist.

# 9. Existing repositories to research

Investigate the following projects before implementing overlapping functionality.

### 1. Microsoft eval-guide
https://github.com/microsoft/eval-guide

Research:
- Skill architecture
- Evaluation workflow design
- Scenario creation
- Feedback and diagnosis
- Reusable components
- Applicability beyond its original platform

### 2. Microsoft AI Agent Evaluation Scenario Library
https://github.com/microsoft/ai-agent-eval-scenario-library

Research:
- Scenario structures
- Evaluation taxonomies
- Quality dimensions
- Acceptance criteria
- Reusable evaluation examples

### 3. Promptfoo
https://github.com/promptfoo/promptfoo

Research:
- Evaluation configuration
- Test execution
- Assertions and scoring
- Model integrations
- Reporting
- Potential lightweight integration approaches

### 4. Vale
https://github.com/vale-cli/vale

Research:
- Terminology checks
- Writing rules
- Style configuration
- Integration with structured content standards

### 5. MCP reference servers
https://github.com/modelcontextprotocol/servers

Research:
- Relevant integration patterns
- Security considerations
- Reference implementations
- Existing reusable functionality

### 6. GOV.UK Design System
https://github.com/alphagov/govuk-design-system

Research:
- Content documentation organization
- Accessibility guidance
- Patterns
- Content principles
- Examples of maintainable design-system documentation

### 7. IBM Carbon
https://carbondesignsystem.com/

Research:
- Content guidelines
- Design-system structure
- Terminology and writing standards
- Content and interaction patterns

### 8. Agent Skills
https://agentskills.io/

Research:
- Portable skill structure
- Skill discovery
- Progressive loading
- Supported execution environments

Also investigate current official guidance for Codex, Claude Code, and VS Code agent configuration.

## Research deliverable

Create:

`docs/RESEARCH.md`

Include a comparison matrix covering:
- Project purpose
- Useful functionality
- Architectural compatibility
- Dependencies
- License and reuse restrictions
- Maintenance activity
- Risks
- Decision: adopt, integrate, adapt, reference, or reject

Verify repository status, current documentation, licenses, and compatibility before incorporating implementation code.

Do not copy third-party material indiscriminately.

# 10. Technical architecture

## Portability

Fievel should be model-agnostic where practical.

The target is a GitHub repository that users can fork or clone and open in a compatible AI coding environment.

Prioritize:

1. OpenAI Codex CLI and IDE workflows
2. Claude Code
3. VS Code agent environments that support relevant project instructions or skills

ChatGPT's regular chat interface should not be assumed to have the same repository execution, file access, or skill-discovery capabilities as Codex.

Validate each target environment independently.

## Agent instruction architecture

Investigate:
- `AGENTS.md`
- `CLAUDE.md`
- `.agents/skills/`
- `.claude/skills/`
- `.github/copilot-instructions.md`
- Agent Skills conventions

Prefer a single authoritative set of shared instructions and skills, with generated or synchronized tool-specific adapters where required.

Avoid diverging duplicate implementations.

## Skills

Proposed initial skills:

**Getting Started:** Understand the user, identify goals, and select an appropriate workflow.

**Content System Builder:** Create or improve a structured content system.

**Source Discovery:** Identify, classify, and assess available content and knowledge sources.

**AI Behavior Designer:** Help define agent responsibilities, communication patterns, permissions, and recovery behaviors.

**Evaluation Designer:** Define quality criteria, generate tests, and guide evaluation.

**Content Audit:** Review an existing content system for gaps, contradictions, and improvement opportunities.

Each skill should include:
- Clear purpose
- Activation guidance
- Required inputs
- Workflow instructions
- Structured outputs
- Quality checks
- Examples
- Error and recovery handling

## Suggested repository structure

```text
fievel/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── LICENSE
├── CONTRIBUTING.md
│
├── .agents/
│   └── skills/
│       ├── getting-started/
│       ├── content-system-builder/
│       ├── source-discovery/
│       ├── ai-behavior-designer/
│       ├── evaluation-designer/
│       └── content-audit/
│
├── .claude/
│   └── skills/
│
├── .github/
│   └── copilot-instructions.md
│
├── knowledge/
│   ├── content-design/
│   ├── ai-fundamentals/
│   ├── ai-experience-design/
│   ├── evaluations/
│   └── sources.yaml
│
├── schemas/
│   └── content-system/
│
├── templates/
│   ├── content-system/
│   ├── agent-behavior/
│   ├── evaluation/
│   └── governance/
│
├── examples/
│   └── fictional-ai-product/
│
├── evals/
├── scripts/
├── tests/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RESEARCH.md
│   └── ROADMAP.md
│
└── my-content-system/
```

This is an initial proposal, not an immutable implementation requirement.

Adjust the structure based on research findings and technical constraints.

Do not add infrastructure solely to populate the proposed folders.

Keep user-generated work clearly separated from Fievel's own instructions, knowledge, and templates.

# 11. Required learning experience

Build a guided seven-stage workflow:

**Stage 1: Understand your product**

Define the product, users, goals, and AI experience.

Output: Product and audience brief.

**Stage 2: Understand your content**

Review guidelines, terminology, voice, and patterns.

Output: Structured content standards.

**Stage 3: Identify your sources**

Discover available documents, repositories, knowledge bases, and approved integrations.

Output: Source inventory.

**Stage 4: Design AI behavior**

Establish how the agent should respond, decide, act, confirm, and recover.

Output: AI behavior guidelines.

**Stage 5: Define quality**

Determine what good responses and behaviors look like.

Output: Evaluation plan and test scenarios.

**Stage 6: Try and improve**

Review or execute evaluations, inspect failures, and refine the system.

Output: Quality report and suggested improvements.

**Stage 7: Maintain your system**

Document ownership, change management, and ongoing testing.

Output: Reusable content-system package.

## Learning design requirements

Each stage should explain:
- What we're doing
- Why it matters
- What decisions need to be made
- What we're creating
- What comes next

The user should be able to resume the workflow between sessions, even when changing supported AI coding tools.

Persist decisions and progress in project files, not exclusively in chat history.

# 12. Complete fictional example

Include a realistic fictional AI product that makes the experience accessible to everyone.

Suggested scenario:

**An AI customer support assistant for a fictional booking platform.**

The assistant helps users understand reservations, cancellation policies, refunds, and booking changes.

Provide fictional:
- Product context
- User needs
- Content guidelines
- Terminology
- Knowledge articles
- Agent behaviors
- Sample conversations
- Failure situations
- Evaluation scenarios
- Expected quality criteria

The scenario should let users practice the entire workflow without connecting real services, exposing private information, or purchasing API access.

Make the example small enough to understand but realistic enough to demonstrate meaningful design decisions.

# 13. Versioning and maintainability

Fievel is intended to become a community-supported project.

Plan for:
- Modular knowledge updates
- Clear versioning
- Contributions from content designers
- Reusable templates
- Community examples
- Documented evaluation practices
- Compatibility testing
- Transparent source attribution
- Accessible contributor documentation

Maintain a distinction between:
- Fievel's core functionality
- Curated educational knowledge
- External integrations
- Community contributions
- User-generated content systems

Avoid coupling user files to internal implementation details that are likely to change.

# 14. Implementation phases

## Phase 0: Research and technical validation

Tasks:
- Inspect candidate repositories.
- Verify licenses and maintenance status.
- Investigate platform compatibility.
- Identify reusable architecture and libraries.
- Define the minimum content-system schema.
- Evaluate options for storing workflow progress.
- Document architecture and tradeoffs.

Deliverables:
- Research comparison
- Architecture decision document
- Initial repository structure
- Scope for first functional release

## Phase 1: Functional Fievel prototype

Implement:
- Core agent instructions
- Initial onboarding
- Beginner and experienced-user entry paths
- Content-system builder skill
- Basic educational knowledge modules
- Content-system templates
- Persistent progress and decisions
- Fictional sample project

Outcome:

A user can open Fievel in a supported environment, describe a product, and create an initial content system.

## Phase 2: Evaluation experience

Implement:
- Evaluation designer skill
- Plain-language quality criteria
- Test scenario generation
- Reusable evaluation definitions
- Manual review workflow
- Optional automated checks
- Results interpretation

Outcome:

A content designer can define, review, and where possible run quality checks against their AI content system.

## Phase 3: Sources and integrations

Implement:
- Source inventory workflow
- Local content ingestion
- Source authority and provenance
- Optional MCP integration guidance
- Content audit and gap identification
- Improved source-to-rule traceability

Outcome:

Users can develop their systems using existing organizational context while maintaining control over their sources.

## Phase 4: Cross-platform compatibility

Implement and validate:
- Codex configuration
- Claude Code configuration
- VS Code configuration
- Shared skill synchronization
- Platform-specific onboarding instructions
- Compatibility tests

Outcome:

The same repository provides a useful, consistent experience across the supported agent environments, with documented differences.

Basic compatibility should be considered from the start, even if full validation occurs here.

## Phase 5: Community-ready release

Complete:
- Public README
- Clear installation instructions
- Quick-start experience
- Example walkthrough
- Documentation
- Contributor guide
- Licensing and attribution
- Troubleshooting guidance
- Known limitations
- Public roadmap
- Release quality checks

Outcome:

A content designer with limited coding experience can fork or clone the repository and complete a useful exercise without personal assistance.

# 15. Quality and acceptance criteria

The initial release must demonstrate real functionality.

## Functional requirements

A user should be able to:

1. Open the repository in a supported AI coding environment.
2. Activate Fievel using documented instructions.
3. Select a beginner or existing-project path.
4. Receive clear guidance suitable for their experience level.
5. Define basic product and audience context.
6. Create structured content standards.
7. Define basic AI behavior guidelines.
8. Produce realistic test scenarios.
9. Identify things to check in AI responses.
10. Save their work in understandable project files.
11. Resume without relying entirely on previous chat history.
12. Understand what was created and how to use it.

## Technical requirements

- No mandatory paid API keys for the initial guided experience.
- No mandatory external MCP connections.
- No unsupported claims of evaluation execution.
- No credentials committed to the repository.
- No automatic modification of unrelated user files.
- Validated structured outputs where schemas are provided.
- Automated checks for critical repository functionality.
- Documentation tested against actual installation and activation steps.
- Clear attribution and license compliance for incorporated resources.

## Experience requirements

- Nontechnical users can understand the onboarding.
- Technical terminology is explained contextually.
- Users can skip explanations they don't need.
- Generated content standards are distinguishable from approved organizational standards.
- Users retain ownership of decisions and generated assets.
- Quality checks can be traced back to design requirements.
- Errors and unsupported integrations are explained clearly.

# 16. Things not to build initially

Avoid unnecessary expansion into:

- A custom web application
- A hosted SaaS platform
- A custom LLM
- A custom general-purpose agent framework
- A large suite of custom MCP servers
- A complex database or orchestration service
- Comprehensive enterprise administration
- Automatic integration with every design and documentation tool
- Unnecessary dashboards

Fievel should initially be a repository-native agent experience.

A graphical product may become valuable later, but it is not required to validate the core concept.

# 17. Longer-term opportunities

Potential future capabilities:

- Content-system maturity assessment
- Existing AI agent audits
- Automatic evaluation generation from content guidelines
- Terminology and style enforcement
- Content quality trend reporting
- System change impact analysis
- Evaluation regression monitoring
- Organizational content-system templates
- Multilingual content system support
- Community-contributed skills
- Specialized skills for agentic experiences
- Integrations with enterprise content sources
- Shareable educational exercises

Treat these as future possibilities, not requirements for the first release.

# 18. Immediate execution instructions

Start work in the current repository.

**First: Inspect the environment.**

Determine whether an existing repository is present. Preserve existing work. If necessary, initialize the project using the name `fievel`.

**Second: Conduct focused research.**

Investigate the repositories and standards listed above.

Document findings in `docs/RESEARCH.md`, including what we should reuse, what we should adapt, and what we should build ourselves.

**Third: Establish the architecture.**

Create an initial technical architecture and define a structured content-system schema.

Document important choices in `docs/ARCHITECTURE.md`.

**Fourth: Implement a working vertical slice.**

Prioritize the following end-to-end experience:

A content designer starts Fievel, learns what an AI content system is, describes a fictional product, creates structured content standards, defines AI behavioral expectations, and generates a set of plain-language quality checks.

The output must consist of real, reusable files.

**Fifth: Test the experience.**

Add automated checks for structured outputs and scripts, inspect generated example artifacts, and validate agent behavior in whichever supported environment is actually available.

Record any cross-platform validation that remains untested.

**Sixth: Document the result.**

Create a useful README containing:
- What Fievel is
- Who it is for
- How it works
- How to get started
- What users will create
- What works today
- What is planned next

Maintain `docs/ROADMAP.md` with completed work, pending tasks, and known limitations.

## Working expectations

Do not stop after completing the research phase unless a genuine technical blocker prevents implementation.

Proceed into the first working prototype.

Do not silently substitute placeholders for required functionality.

Where a dependency or integration cannot be validated, implement the supported local path and document what remains.

Run relevant tests and report results accurately.

At the end of the initial implementation, provide:

1. A summary of what was implemented.
2. The files and components created.
3. Repositories and tools reused or referenced.
4. Tests performed and their results.
5. Known limitations.
6. Recommended next development steps.

---

# 19. Product success definition

Fievel succeeds when a content designer who has never built an AI content system can use it to understand the fundamentals, make meaningful design decisions, create reusable system artifacts, and begin evaluating whether an AI experience follows those decisions.

Experienced practitioners should be able to use the same tool to organize and improve existing systems without completing beginner lessons.

Fievel should ultimately become a practical, open-source resource that makes AI content systems more approachable, more measurable, and more accessible to the content design community.

**The goal is not simply to help people generate better AI content. It is to help content designers understand and shape the systems responsible for generating it.**
