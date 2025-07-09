name: "Enterprise PRP Template - Multi-Team Context Engineering"

## Purpose
Enterprise-grade template for AI agents implementing features in multi-project, multi-team environments with shared knowledge bases, pattern reuse requirements, and organizational hierarchy.

## Enterprise Principles
1. **Pattern Reuse First**: Leverage materials/shared/patterns/ before custom implementation
2. **Cross-Team Collaboration**: Consider impact on other teams and shared components
3. **Knowledge Contribution**: Extract and share reusable patterns for organizational benefit
4. **Enterprise Compliance**: Follow materials/shared/standards/ for security and quality
5. **Validation Gates**: Multi-level validation including team review and enterprise compliance

---

## Goal
[Enterprise feature description with business impact and cross-team considerations]

## Why
- [Business value across multiple teams/projects]
- [Integration with enterprise architecture]
- [Problems solved for organization-wide benefit]

## What
[Feature behavior with enterprise context and multi-team implications]

### Success Criteria
- [ ] [Measurable outcomes for primary team]
- [ ] [Cross-team integration requirements]
- [ ] [Enterprise compliance verification]
- [ ] [Knowledge contribution to shared repository]

## All Needed Enterprise Context

### Enterprise Documentation & References
```yaml
# MUST READ - Enterprise context requirements
- path: materials/shared/patterns/
  why: Reusable patterns to leverage before custom implementation
  
- path: materials/shared/standards/
  why: Enterprise compliance and coding standards
  
- path: materials/documentation/architecture/
  why: System constraints and enterprise architecture decisions
  
- path: materials/projects/shared_knowledge/
  why: Cross-project lessons learned and proven approaches
  
- path: materials/PRPs/validated/
  why: Previously validated PRP patterns for similar features
  
- url: [External API docs]
  why: [Required external integrations]
  
- team_contact: [Team lead/architect]
  why: [Cross-team coordination requirements]
```

### Enterprise Codebase Context
```bash
# Current enterprise structure
materials/
├── shared/patterns/           # Organizational pattern library
├── shared/libraries/          # Shared component libraries  
├── shared/standards/          # Enterprise coding standards
├── projects/{team-name}/      # Team-specific context
└── documentation/             # Enterprise guides and architecture
```

### Target Enterprise Structure
```bash
# Files to be added/modified with enterprise considerations
{project}/
├── src/                       # Implementation following enterprise patterns
├── tests/                     # Enterprise testing standards
├── docs/                      # Team documentation updates
└── integration/               # Cross-team integration points

materials/shared/patterns/     # New patterns to contribute
materials/documentation/       # Updated integration guides
```

### Enterprise Gotchas & Compliance Requirements
```python
# CRITICAL: Enterprise security requirements
# Must use materials/shared/standards/security_patterns.py
# Must validate with materials/shared/standards/compliance_check.py

# CRITICAL: Cross-team impact analysis required
# Run materials/shared/patterns/impact_analyzer.py before changes

# CRITICAL: Shared component modification requires team review
# Follow materials/documentation/integration_guides/review_process.md
```

## Enterprise Implementation Blueprint

### Shared Pattern Analysis
```python
# Check existing patterns before implementation
pattern_matches = scan_shared_patterns(feature_requirements)
# Use materials/shared/patterns/{pattern_name}.py if relevance > 0.8

# Validate shared library availability  
shared_components = check_shared_libraries(functionality_needed)
# Integrate materials/shared/libraries/{component}/ if available
```

### Enterprise Implementation Tasks
```yaml
Task 1: Enterprise Pattern Discovery
SCAN materials/shared/patterns/:
  - FIND patterns matching feature requirements
  - EVALUATE reusability score (target >0.8 for direct use)
  - ADAPT patterns for current use case if needed

VALIDATE materials/shared/libraries/:
  - CHECK existing components for required functionality
  - INTEGRATE shared libraries following materials/documentation/integration_guides/
  - AVOID reimplementation of available shared components

Task 2: Cross-Team Impact Analysis  
RUN materials/shared/patterns/impact_analyzer.py:
  - IDENTIFY teams affected by changes
  - DOCUMENT integration touchpoints
  - SCHEDULE coordination meetings if needed

REVIEW materials/projects/*/dependencies:
  - VALIDATE no breaking changes to shared components
  - UPDATE dependency documentation for affected teams

Task 3: Implementation with Enterprise Standards
FOLLOW materials/shared/standards/:
  - CODE according to enterprise coding standards
  - VALIDATE security requirements with compliance_check.py
  - TEST using enterprise testing patterns

CREATE following enterprise patterns:
  - STRUCTURE modules according to materials/shared/standards/architecture.md
  - IMPLEMENT error handling per materials/shared/patterns/error_handling.py
  - DOCUMENT APIs following materials/shared/standards/api_documentation.md

Task 4: Knowledge Contribution Planning
EXTRACT reusable patterns:
  - IDENTIFY components suitable for materials/shared/patterns/
  - DOCUMENT pattern usage and benefits
  - PREPARE contribution to shared repository

UPDATE enterprise documentation:
  - MODIFY materials/documentation/integration_guides/ if needed
  - ADD lessons learned to materials/projects/shared_knowledge/
  - CONTRIBUTE PRP to materials/PRPs/validated/ after validation
```

### Enterprise Integration Points
```yaml
SHARED_COMPONENTS:
  - integrate: materials/shared/libraries/{library_name}
  - validate: Cross-team compatibility
  - document: Integration touchpoints

ENTERPRISE_COMPLIANCE:
  - security: materials/shared/standards/security_validator.py
  - coding: materials/shared/standards/.ruff.toml
  - architecture: materials/documentation/architecture/constraints.md

CROSS_TEAM_COORDINATION:
  - notify: Affected teams of shared component changes
  - review: Team leads for integration approval
  - schedule: Knowledge transfer if new patterns created
```

## Enterprise Validation Loop

### Level 1: Enterprise Compliance
```bash
# Enterprise standards validation
ruff check --config materials/shared/standards/.ruff.toml
python materials/shared/standards/security_validator.py
python materials/shared/standards/compliance_check.py

# Expected: All enterprise compliance checks pass
```

### Level 2: Cross-Team Impact Validation
```bash
# Impact analysis on other teams
python materials/shared/patterns/impact_analyzer.py

# Shared component validation
python materials/shared/libraries/dependency_checker.py

# Integration testing with other team components
python materials/documentation/integration_guides/integration_tester.py

# Expected: No breaking changes to other teams, all integrations pass
```

### Level 3: Pattern Contribution Validation
```bash
# Extract and validate new patterns
python materials/shared/patterns/pattern_extractor.py

# Knowledge base contribution
python materials/projects/shared_knowledge/knowledge_updater.py

# Documentation generation
python materials/documentation/doc_generator.py

# Expected: New patterns extracted, knowledge base updated, documentation current
```

### Level 4: Team Review and Approval
```bash
# Team notification for review
python materials/shared/standards/team_notifier.py

# Automated team review checklist
python materials/documentation/validation_patterns/team_review.py

# Expected: Team review completed, approval received for shared component changes
```

## Enterprise Final Validation Checklist
- [ ] All shared patterns evaluated and reused where applicable
- [ ] Enterprise compliance checks passed
- [ ] Cross-team impact analyzed and approved
- [ ] Shared component integration validated
- [ ] New patterns extracted for organizational benefit
- [ ] Team review completed for shared changes
- [ ] Knowledge contribution documented
- [ ] Integration guides updated
- [ ] Enterprise architecture team notified of decisions

---

## Enterprise Anti-Patterns to Avoid
- ❌ Don't reimplement existing shared patterns
- ❌ Don't modify shared components without team coordination
- ❌ Don't skip enterprise compliance validation
- ❌ Don't ignore cross-team impact analysis
- ❌ Don't forget to contribute reusable patterns back to shared repository
- ❌ Don't implement without checking materials/shared/libraries/ first

## Enterprise Confidence Score: [1-10]

Enterprise confidence factors:
- Shared pattern reuse score
- Cross-team coordination complexity
- Enterprise compliance requirements
- Knowledge contribution potential
- Multi-team integration complexity

Higher confidence when:
- Extensive shared pattern reuse
- Clear cross-team coordination plan
- Well-documented enterprise compliance path
- Valuable pattern contribution identified