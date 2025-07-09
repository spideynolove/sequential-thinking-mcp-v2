# Generate Enterprise PRP

Generate a comprehensive Product Requirements Prompt (PRP) for enterprise multi-project environments with thorough research and validation gates.

## Feature file: $ARGUMENTS

Research and create enterprise-grade PRP with:
- Cross-project pattern analysis
- Shared knowledge base integration
- Enterprise validation requirements
- Multi-team collaboration patterns

## Enterprise Research Process

1. **Shared Knowledge Analysis**
   - Search materials/shared/patterns/ for similar implementations
   - Identify reusable components from materials/shared/libraries/
   - Check materials/shared/standards/ for compliance requirements
   - Review materials/documentation/best_practices/ for enterprise patterns

2. **Cross-Project Pattern Discovery**
   - Analyze materials/projects/*/patterns/ for proven approaches
   - Identify successful integration patterns across teams
   - Extract validated workflow patterns from materials/PRPs/validated/
   - Check materials/documentation/architecture/ for system constraints

3. **Enterprise Validation Requirements**
   - Include materials/examples/validation_patterns/ in validation gates
   - Reference materials/documentation/troubleshooting/ for common issues
   - Integrate enterprise compliance checks from materials/shared/standards/
   - Add cross-team review requirements for shared component changes

4. **Multi-Team Collaboration Context**
   - Include team access patterns from materials/projects/shared_knowledge/
   - Reference integration guides from materials/documentation/integration_guides/
   - Add version control patterns for materials synchronization
   - Include knowledge transfer requirements for pattern contributions

## Enterprise PRP Generation

Using materials/PRPs/templates/enterprise_base.md as foundation:

### Critical Enterprise Context
- **Shared Patterns**: Reference validated patterns from materials/shared/patterns/
- **Integration Guides**: Include specific integration patterns from materials/documentation/
- **Compliance Requirements**: Enterprise standards from materials/shared/standards/
- **Cross-Project Dependencies**: Impact analysis on other teams and projects

### Enterprise Implementation Blueprint
- **Pattern Reuse First**: Check existing patterns before custom implementation
- **Shared Component Integration**: Use materials/shared/libraries/ components
- **Enterprise Validation Gates**: Include team review and compliance checks
- **Knowledge Contribution**: Plan for pattern contribution to shared repository

### Enterprise Validation Gates
```bash
# Enterprise compliance check
python materials/shared/standards/compliance_check.py

# Cross-project impact analysis
python materials/shared/patterns/impact_analyzer.py

# Team review validation
python materials/documentation/validation_patterns/team_review.py

# Shared pattern validation
python materials/shared/patterns/pattern_validator.py
```

### Enterprise Quality Gates
- [ ] Shared pattern reuse validated
- [ ] Cross-project impact assessed
- [ ] Enterprise compliance verified
- [ ] Team review completed
- [ ] Knowledge contribution planned
- [ ] Integration guide updated

## Output Location

Save as: `materials/PRPs/generated/{feature-name}-enterprise.md`

Copy to team workspace: `materials/projects/{team-name}/context/`

## Enterprise Quality Checklist
- [ ] All shared patterns referenced
- [ ] Cross-project dependencies identified
- [ ] Enterprise validation gates included
- [ ] Team collaboration patterns documented
- [ ] Knowledge contribution workflow defined
- [ ] Compliance requirements verified

Score the Enterprise PRP on confidence level (1-10) for multi-team implementation success.

Remember: Enterprise success requires pattern reuse, cross-team collaboration, and shared knowledge contribution.