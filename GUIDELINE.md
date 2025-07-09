# Enhanced Sequential Thinking with Memory Bank MCP - Complete Usage Guide

A comprehensive guide to using the unified MCP system for various programming scenarios, from simple debugging to complex enterprise workflows.

## Quick Start Reference

### Essential Tool Categories

**Session Management**
- `start_thinking_session()` - General problem solving
- `start_coding_session()` - Development with package discovery
- `create_memory_session()` - Memory-focused workflows

**Core Workflow Tools**
- `add_thought()` / `add_coding_thought()` - Build reasoning chains
- `store_memory()` - Persist insights with code integration
- `analyze_thinking()` / `analyze_memories()` - Session analysis

**Coding Integration**
- `explore_packages()` - Discover existing libraries
- `detect_code_reinvention()` - Prevent unnecessary reimplementation
- `record_architecture_decision()` - Document technical choices

---

## Programming Task Workflows

### 1. Problem Solving & Debugging

**Scenario**: Debug performance issue in web application

```python
# Start analytical session
start_thinking_session(
    problem="Web application response time degraded from 200ms to 2000ms after deployment",
    success_criteria="Identify root cause and solution with <500ms response time",
    constraints="Production system, cannot use invasive debugging"
)

# Build systematic analysis
add_thought(
    content="First principle: performance regression suggests new code or configuration change",
    confidence=0.9
)

add_thought(
    content="Check recent deployment changes: database queries, caching, external API calls",
    dependencies="previous_thought_id",
    confidence=0.8
)

# Store findings for future reference
store_memory(
    content="Performance regression analysis: always check DB query N+1 problems first",
    tags=["debugging", "performance", "web_development"],
    importance=0.9,
    pattern_type="debugging_workflow"
)

# Document decision for team
record_architecture_decision(
    decision_title="Performance Monitoring Strategy",
    context="Response time regression incident",
    options_considered="APM tools, database profiling, code review",
    chosen_option="Database query optimization with APM monitoring",
    rationale="Root cause identified in ORM query patterns",
    consequences="Need ongoing query performance monitoring"
)
```

**Advanced Pattern**: Branch exploration for multiple hypotheses

```python
# Create alternative investigation paths
create_branch(
    name="database_hypothesis",
    from_thought="root_analysis_thought_id",
    purpose="Investigate database performance as primary cause"
)

add_thought(
    content="Database connection pool exhaustion could explain 10x slowdown",
    branch_id="database_branch_id",
    confidence=0.7
)

create_branch(
    name="external_api_hypothesis", 
    from_thought="root_analysis_thought_id",
    purpose="Investigate external API latency issues"
)

# Merge findings after investigation
merge_branch(
    branch_id="database_branch_id",
    target_thought="final_solution_thought_id"
)
```

### 2. System Architecture & Design

**Scenario**: Design microservices architecture for e-commerce platform

```python
# Start architecture-focused session
start_coding_session(
    problem="Design scalable microservices architecture for e-commerce platform",
    success_criteria="Handle 100k concurrent users, 99.9% uptime, sub-200ms API response",
    constraints="Kubernetes deployment, existing PostgreSQL, budget considerations",
    codebase_context="Monolithic Django application currently serving 10k users",
    package_exploration_required=True
)

# Explore relevant packages and patterns
explore_packages(
    task_description="microservices architecture patterns python kubernetes",
    language="python"
)

# Document architecture decisions systematically
record_architecture_decision(
    decision_title="Service Decomposition Strategy",
    context="E-commerce platform with user management, catalog, orders, payments",
    options_considered="Domain-driven design, database-per-service, shared database",
    chosen_option="Domain-driven microservices with database-per-service",
    rationale="Clear business domain boundaries, independent scaling, fault isolation",
    consequences="Increased complexity, eventual consistency challenges, distributed transactions",
    package_dependencies="FastAPI, PostgreSQL, Redis, Celery"
)

record_architecture_decision(
    decision_title="Inter-Service Communication",
    context="Microservices need synchronous and asynchronous communication",
    options_considered="REST APIs, GraphQL federation, gRPC, event streaming",
    chosen_option="REST APIs + Apache Kafka for events",
    rationale="REST for synchronous, Kafka for eventual consistency and events",
    consequences="Need event schema management, increased operational complexity"
)

# Store reusable patterns
store_memory(
    content="Microservices decomposition pattern: start with API boundaries, then extract services",
    tags=["architecture", "microservices", "decomposition"],
    code_snippet="""
# Service boundary identification
class ServiceBoundary:
    domain: str
    entities: List[str]
    apis: List[str]
    dependencies: List[str]
""",
    language="python",
    pattern_type="architecture_pattern",
    importance=0.95
)
```

**Enterprise Pattern**: Multi-team architecture coordination

```python
# Query previous architecture decisions for consistency
similar_decisions = query_architecture_decisions(
    pattern="microservices",
    technology="kubernetes",
    similarity_threshold=0.8
)

# Set external context for cross-team coordination
set_external_context(
    external_context="""
    Platform team constraints:
    - Kubernetes 1.25+ required
    - Istio service mesh mandatory
    - Prometheus/Grafana monitoring stack
    - GitOps deployment with ArgoCD
    """,
    session_id="current_session"
)

# Create collection for architecture decisions
create_collection(
    name="ecommerce_microservices_architecture",
    from_memory="service_decomposition_memory_id",
    purpose="Track all architectural decisions for e-commerce microservices project"
)
```

### 3. Implementation & Development

**Scenario**: Implement user authentication service

```python
# Start development session with package discovery
start_coding_session(
    problem="Implement JWT-based authentication service with refresh tokens",
    success_criteria="Secure authentication, token refresh, rate limiting, audit logging",
    constraints="Must integrate with existing user database, GDPR compliance",
    codebase_context="FastAPI application with PostgreSQL, Redis available",
    package_exploration_required=True
)

# Check for existing solutions before implementing
prevent_reinvention_check("JWT authentication library Python FastAPI")

detect_code_reinvention(
    proposed_code="""
def create_jwt_token(user_id: str, expiry: int):
    payload = {"user_id": user_id, "exp": expiry}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
""",
    existing_packages_checked="python-jose, PyJWT, authlib"
)

# Explore authentication packages
explore_existing_apis("JWT authentication FastAPI")

# Store implementation patterns
store_codebase_pattern(
    pattern_type="authentication",
    code_snippet="""
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

jwt_authentication = JWTAuthentication(
    secret=settings.JWT_SECRET,
    lifetime_seconds=3600,
    tokenUrl="auth/jwt/login"
)
""",
    description="FastAPI Users JWT authentication setup",
    language="python",
    tags="authentication,jwt,fastapi"
)

# Document security decision
record_architecture_decision(
    decision_title="JWT vs Session Authentication",
    context="Authentication service for microservices architecture",
    options_considered="JWT tokens, session cookies, OAuth2 with external provider",
    chosen_option="JWT with refresh tokens",
    rationale="Stateless for microservices, supports mobile clients, scalable",
    consequences="Token management complexity, logout challenges, storage security",
    package_dependencies="python-jose, passlib, python-multipart"
)
```

**Advanced Pattern**: Auto-cycle development workflow

```python
# Enable auto-cycle for systematic development
start_coding_session(
    problem="Implement user authentication service",
    success_criteria="Production-ready authentication with all security measures",
    auto_validation=True  # Enables 5-step automation
)

# Auto-cycle automatically executes:
# 1. Package discovery (finds: fastapi-users, python-jose, passlib)
# 2. Thought generation (security considerations, implementation steps)
# 3. Memory storage (authentication patterns, security practices)
# 4. Architecture decisions (JWT vs sessions, security measures)
# 5. Validation analysis (completeness, security coverage)

# Validate implementation against discovered packages
validate_package_usage("""
def authenticate_user(username: str, password: str):
    # Custom authentication implementation
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return check_user_credentials(username, hashed)
""")
# Returns warning: Consider using passlib for password hashing
```

### 4. Research & Learning

**Scenario**: Research modern frontend state management approaches

```python
# Start research session
start_thinking_session(
    problem="Evaluate modern frontend state management solutions for React application",
    success_criteria="Compare options with pros/cons, recommend solution for team",
    constraints="Team familiar with Redux, performance critical application"
)

# Build research methodology
add_thought(
    content="Research approach: evaluate Redux Toolkit, Zustand, Jotai, Valtio based on bundle size, learning curve, performance",
    confidence=0.8
)

add_thought(
    content="Evaluation criteria: developer experience, bundle size, TypeScript support, devtools, community",
    dependencies="research_methodology_thought_id",
    confidence=0.9
)

# Explore package ecosystem
explore_packages(
    task_description="React state management Redux alternatives",
    language="javascript"
)

# Store research findings
store_memory(
    content="State management comparison: Redux Toolkit (familiar, verbose), Zustand (lightweight, simple), Jotai (atomic, granular)",
    tags=["research", "react", "state_management", "frontend"],
    importance=0.8
)

store_memory(
    content="Bundle size analysis: Zustand 2.2kb, Jotai 3.1kb, Redux Toolkit 11.2kb - significant for performance-critical apps",
    tags=["performance", "bundle_size", "frontend_optimization"],
    code_snippet="""
// Zustand store example
import { create } from 'zustand'

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }))
}))
""",
    language="javascript",
    pattern_type="state_management",
    importance=0.9
)

# Create research collection
create_collection(
    name="frontend_state_management_research",
    from_memory="comparison_memory_id",
    purpose="Compile all research on React state management solutions"
)

# Export research findings
export_memories_to_file(
    filename="state_management_research.md",
    tags="research,react,state_management"
)
```

---

## Domain-Specific Use Cases

### Web Development Workflow

```python
# Full-stack web application development
start_coding_session(
    problem="Build job posting platform with user authentication, job listings, and application tracking",
    success_criteria="MVP with user registration, job CRUD, application workflow",
    codebase_context="FastAPI backend, React frontend, PostgreSQL database"
)

# API design workflow
record_architecture_decision(
    decision_title="API Design Patterns",
    context="RESTful API for job posting platform",
    options_considered="REST, GraphQL, RPC-style endpoints",
    chosen_option="RESTful API with OpenAPI documentation",
    rationale="Team familiar with REST, good tooling, clear semantics",
    consequences="Multiple endpoints for complex queries, potential over-fetching"
)

# Database design
store_codebase_pattern(
    pattern_type="database_schema",
    code_snippet="""
class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid4)
    email = Column(String, unique=True, index=True)
    company_id = Column(UUID, ForeignKey("companies.id"), nullable=True)
    
class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(UUID, primary_key=True, default=uuid4)
    title = Column(String, index=True)
    company_id = Column(UUID, ForeignKey("companies.id"))
    created_by = Column(UUID, ForeignKey("users.id"))
""",
    description="SQLAlchemy schema for job platform with relationships",
    language="python"
)
```

### System Integration Project

```python
# Enterprise system integration
start_coding_session(
    problem="Integrate CRM system with marketing automation platform via API synchronization",
    success_criteria="Real-time contact sync, automated campaign triggers, error handling",
    constraints="Legacy CRM with limited API, rate limiting, data privacy compliance"
)

# Integration pattern analysis
explore_existing_apis("enterprise integration patterns ETL data synchronization")

detect_code_reinvention(
    proposed_code="Custom HTTP client for API integration",
    existing_packages_checked="requests, httpx, aiohttp"
)

# Cross-system context sharing
set_external_context(
    external_context="""
    CRM System: Salesforce API with OAuth2
    Marketing Platform: HubSpot API with API keys
    Data Requirements: Contact sync every 15 minutes
    Compliance: GDPR data processing consent required
    """
)

# Document integration architecture
record_architecture_decision(
    decision_title="Data Synchronization Strategy",
    context="CRM to Marketing Platform integration",
    options_considered="Real-time webhooks, scheduled batch sync, event-driven sync",
    chosen_option="Event-driven sync with fallback batch processing",
    rationale="Near real-time without overwhelming APIs, resilient to failures",
    consequences="Requires event queue infrastructure, complex error handling"
)
```

### Trading/Finance Application

```python
# Financial trading algorithm development
start_coding_session(
    problem="Develop cryptocurrency trading algorithm with risk management",
    success_criteria="Backtested strategy with Sharpe ratio >1.5, max drawdown <10%",
    constraints="Real-time data processing, regulatory compliance, risk limits"
)

# Risk analysis workflow
add_thought(
    content="Risk management principle: position sizing based on Kelly criterion with conservative scaling",
    confidence=0.9
)

store_memory(
    content="Trading algorithm pattern: signal generation → risk assessment → position sizing → execution → monitoring",
    tags=["trading", "algorithm", "risk_management", "finance"],
    code_snippet="""
class RiskManager:
    def __init__(self, max_portfolio_risk=0.02):
        self.max_portfolio_risk = max_portfolio_risk
    
    def calculate_position_size(self, signal_strength, volatility, account_balance):
        kelly_fraction = signal_strength / volatility
        conservative_fraction = kelly_fraction * 0.25  # Kelly reduction
        return min(conservative_fraction, self.max_portfolio_risk) * account_balance
""",
    language="python",
    pattern_type="risk_management",
    importance=0.95
)

# Document trading strategy decisions
record_architecture_decision(
    decision_title="Backtesting Framework Selection",
    context="Cryptocurrency trading algorithm development",
    options_considered="Backtrader, Zipline, custom framework",
    chosen_option="Backtrader with custom crypto data feeds",
    rationale="Mature ecosystem, good documentation, flexible strategy implementation",
    consequences="Learning curve for team, dependency on third-party library"
)
```

### Machine Learning Project

```python
# ML model development and experimentation
start_coding_session(
    problem="Develop customer churn prediction model for SaaS platform",
    success_criteria="Model with >85% accuracy, deployed in production with monitoring",
    codebase_context="Python data science stack, AWS infrastructure, existing user behavior data"
)

# Experiment tracking workflow
store_memory(
    content="ML experiment tracking: version control data + code + config + metrics for reproducibility",
    tags=["ml", "experiment_tracking", "data_science"],
    code_snippet="""
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_param("n_estimators", 100)
    mlflow.sklearn.log_model(model, "model")
""",
    language="python",
    pattern_type="ml_experiment"
)

# Feature engineering patterns
store_codebase_pattern(
    pattern_type="feature_engineering",
    code_snippet="""
def create_behavioral_features(user_activity_df):
    features = pd.DataFrame()
    features['avg_session_duration'] = user_activity_df.groupby('user_id')['session_duration'].mean()
    features['days_since_last_login'] = (datetime.now() - user_activity_df.groupby('user_id')['last_login'].max()).dt.days
    features['feature_usage_diversity'] = user_activity_df.groupby('user_id')['feature_used'].nunique()
    return features
""",
    description="Customer behavior feature engineering for churn prediction",
    language="python",
    tags="feature_engineering,churn_prediction"
)

# Model deployment decision
record_architecture_decision(
    decision_title="Model Deployment Strategy",
    context="Customer churn prediction model for production use",
    options_considered="Real-time API, batch predictions, embedded model",
    chosen_option="Real-time API with FastAPI and model versioning",
    rationale="Business needs immediate churn risk assessment, flexible model updates",
    consequences="Infrastructure complexity, latency requirements, model monitoring needed"
)
```

---

## Enterprise Collaboration Patterns

### Multi-Team Development

```python
# Load enterprise materials context
load_project_context("materials/projects/platform-team")

# Check shared patterns before implementation
explore_existing_apis("user authentication enterprise patterns")

# Use enterprise PRP generation
# /generate-enterprise-prp materials/features/authentication_service.md

# Enterprise validation workflow
start_coding_session(
    problem="Implement shared authentication service for multiple teams",
    success_criteria="Reusable service meeting enterprise security standards",
    constraints="Must follow enterprise architecture patterns, security compliance"
)

# Cross-team impact analysis
set_external_context(
    external_context="""
    Affected Teams: Frontend (React), Mobile (React Native), Analytics (Python)
    Shared Components: materials/shared/libraries/auth-sdk
    Enterprise Standards: materials/shared/standards/security_requirements.md
    """
)

# Document enterprise decision
record_architecture_decision(
    decision_title="Enterprise Authentication Service Architecture",
    context="Shared service for multiple development teams",
    options_considered="Team-specific auth, shared library, centralized service",
    chosen_option="Centralized authentication service with team-specific SDKs",
    rationale="Consistent security, centralized management, team autonomy through SDKs",
    consequences="Service ownership model needed, SDK maintenance, version coordination",
    package_dependencies="FastAPI, PostgreSQL, Redis, enterprise-auth-sdk"
)

# Contribute patterns to shared repository
store_codebase_pattern(
    pattern_type="enterprise_authentication",
    code_snippet="""
from enterprise_auth import AuthService, TokenValidator

class TeamSpecificAuth:
    def __init__(self, team_id: str):
        self.auth_service = AuthService(team_id)
        self.validator = TokenValidator(team_id)
    
    async def authenticate(self, token: str):
        return await self.validator.validate_token(token)
""",
    description="Enterprise authentication pattern for team-specific implementations",
    language="python",
    file_path="materials/shared/patterns/enterprise_auth.py"
)

# Update enterprise documentation
update_project_index(
    section="Authentication Services",
    content="""
## Enterprise Authentication Service

### Teams Using Service
- Platform Team (owner)
- Frontend Team (React SDK)
- Mobile Team (React Native SDK)
- Analytics Team (Python SDK)

### Integration Guide
See materials/documentation/integration_guides/auth_service_integration.md

### Shared Components
- materials/shared/libraries/auth-sdk/
- materials/shared/patterns/enterprise_auth.py
"""
)
```

### Knowledge Sharing Workflow

```python
# Create shared knowledge collection
create_collection(
    name="microservices_best_practices",
    from_memory="service_decomposition_memory_id",
    purpose="Share microservices knowledge across platform teams"
)

# Export validated patterns for teams
export_memories_to_file(
    filename="materials/shared/patterns/microservices_patterns.md",
    tags="architecture,microservices,best_practices"
)

# Cross-project context sharing
get_cross_system_context(session_id="architecture_session")

# Update enterprise knowledge base
store_memory(
    content="Enterprise pattern: API-first design with OpenAPI specs enables parallel team development",
    tags=["enterprise", "api_design", "team_collaboration"],
    importance=0.9,
    pattern_type="collaboration_pattern"
)
```

---

## Advanced Tool Combinations

### Context Engineering Auto-Cycle

```python
# Auto-cycle with enterprise validation
start_coding_session(
    problem="Implement distributed caching layer for microservices",
    success_criteria="Redis cluster with automatic failover, monitoring, team SDKs",
    auto_validation=True,
    constraints="Enterprise compliance, multi-team usage, 99.9% availability"
)

# Auto-cycle executes:
# 1. Package discovery → finds Redis, Redis Cluster, Sentinel options
# 2. Thought generation → caching strategies, cluster topology, failover
# 3. Memory storage → caching patterns, Redis best practices
# 4. Architecture decisions → cluster vs sentinel, data partitioning
# 5. Validation analysis → completeness, reliability, team impact

# Validate with enterprise standards
validate_package_usage("""
import redis
import redis.sentinel

# Custom Redis connection manager
class CacheManager:
    def __init__(self, hosts):
        self.redis_client = redis.Redis(host=hosts[0])
""")
# Returns: Warning - Consider using Redis Sentinel for high availability
```

### Complex Debugging Workflow

```python
# Multi-branch debugging investigation
start_thinking_session(
    problem="Distributed system experiencing intermittent 500 errors across services",
    success_criteria="Root cause identified, solution implemented, monitoring improved"
)

# Create investigation branches
create_branch(
    name="service_dependency_analysis",
    from_thought="initial_analysis_thought",
    purpose="Investigate service-to-service communication failures"
)

create_branch(
    name="infrastructure_investigation", 
    from_thought="initial_analysis_thought",
    purpose="Investigate underlying infrastructure issues"
)

create_branch(
    name="data_consistency_check",
    from_thought="initial_analysis_thought", 
    purpose="Investigate distributed data consistency problems"
)

# Document investigation in each branch
add_thought(
    content="Service mesh metrics show 5% increase in circuit breaker activations",
    branch_id="service_dependency_branch",
    confidence=0.8
)

add_thought(
    content="Kubernetes nodes showing memory pressure, possible OOM kills",
    branch_id="infrastructure_branch", 
    confidence=0.7
)

# Merge findings
merge_branch(
    branch_id="service_dependency_branch",
    target_thought="final_analysis_thought"
)

# Store debugging methodology
store_memory(
    content="Distributed debugging approach: parallel investigation of service, infrastructure, and data layers",
    tags=["debugging", "distributed_systems", "methodology"],
    pattern_type="debugging_workflow",
    importance=0.9
)
```

### Research and Implementation Pipeline

```python
# Research phase
start_thinking_session(
    problem="Evaluate event streaming platforms for real-time analytics",
    success_criteria="Platform recommendation with implementation plan"
)

explore_packages("event streaming Kafka Pulsar Kinesis", language="python")

store_memory(
    content="Event streaming comparison: Kafka (mature, complex), Pulsar (multi-tenant, newer), Kinesis (AWS-native, managed)",
    tags=["research", "event_streaming", "real_time_analytics"]
)

# Transition to implementation
start_coding_session(
    problem="Implement event streaming pipeline with chosen platform",
    success_criteria="Production-ready pipeline with monitoring and error handling",
    codebase_context="Python microservices, Kubernetes, existing Kafka experience"
)

# Reference research in implementation
query_architecture_decisions(
    pattern="event streaming",
    technology="kafka",
    similarity_threshold=0.7
)

# Implement with validation
validate_package_usage("""
# Custom event producer
class EventProducer:
    def __init__(self, broker_urls):
        self.producer = KafkaProducer(bootstrap_servers=broker_urls)
""")
# Suggests: Use confluent-kafka-python for better performance
```

---

## Tool Reference Matrix

### Session Management Tools

| Tool | Purpose | Best Used For | Combines Well With |
|------|---------|---------------|-------------------|
| `start_thinking_session()` | General problem solving | Analysis, research, debugging | `add_thought()`, `create_branch()` |
| `start_coding_session()` | Development with package discovery | Implementation, architecture | `explore_packages()`, `detect_code_reinvention()` |
| `create_memory_session()` | Memory-focused workflows | Knowledge building, documentation | `store_memory()`, `create_collection()` |

### Thinking & Reasoning Tools

| Tool | Purpose | Example Use Case | Advanced Patterns |
|------|---------|------------------|-------------------|
| `add_thought()` | Build reasoning chains | "First principle: caching improves performance" | Dependency chains, confidence tracking |
| `add_coding_thought()` | Development-specific reasoning | "Need async framework for high performance" | Package exploration, suggestion integration |
| `revise_thought()` | Update existing reasoning | Refine analysis based on new data | Iterative refinement, confidence adjustment |
| `create_branch()` | Alternative investigation paths | Multiple debugging hypotheses | Parallel exploration, hypothesis testing |
| `merge_branch()` | Combine insights | Integrate findings from branches | Knowledge synthesis, decision making |

### Memory & Storage Tools

| Tool | Purpose | Code Integration | Enterprise Usage |
|------|---------|------------------|------------------|
| `store_memory()` | Persist insights | Code snippets, patterns | Shared knowledge base |
| `revise_memory()` | Update stored knowledge | Pattern improvements | Version control |
| `create_collection()` | Group related knowledge | Project patterns | Team collections |
| `merge_collection()` | Combine knowledge sets | Cross-project insights | Knowledge consolidation |

### Coding Integration Tools

| Tool | Primary Function | Prevents | Enables |
|------|------------------|----------|---------|
| `explore_packages()` | Discover existing libraries | Reinvention | Informed decisions |
| `detect_code_reinvention()` | Validate implementation approach | Unnecessary custom code | Library adoption |
| `record_architecture_decision()` | Document technical choices | Decision amnesia | Team alignment |
| `query_architecture_decisions()` | Find similar past decisions | Inconsistency | Pattern reuse |
| `validate_package_usage()` | Check code quality | Poor practices | Best practices |

---

## Best Practices and Anti-Patterns

### Effective Tool Combinations

**✅ Good Patterns:**
```python
# Research → Decision → Implementation flow
start_thinking_session() → explore_packages() → record_architecture_decision() → start_coding_session()

# Problem analysis with branching
add_thought() → create_branch() → add_thought(branch_id) → merge_branch()

# Knowledge building pipeline
store_memory() → create_collection() → export_memories_to_file()

# Enterprise workflow
load_project_context() → query_architecture_decisions() → record_architecture_decision()
```

**❌ Anti-Patterns:**
```python
# Don't start coding without exploration
start_coding_session() # Missing: explore_packages() first

# Don't store memories without context
store_memory(content="Use Redis") # Missing: why, when, how context

# Don't make decisions without documentation
# Implementation without record_architecture_decision()

# Don't ignore enterprise patterns
# Custom implementation without checking materials/shared/patterns/
```

### Tool Selection Guide

**For Research & Learning:**
1. `start_thinking_session()` - Problem analysis
2. `explore_packages()` - Technology landscape
3. `add_thought()` - Build understanding
4. `store_memory()` - Capture insights
5. `export_memories_to_file()` - Share knowledge

**For Development:**
1. `start_coding_session()` - Development context
2. `prevent_reinvention_check()` - Avoid duplication
3. `record_architecture_decision()` - Document choices
4. `validate_package_usage()` - Quality check
5. `store_codebase_pattern()` - Share patterns

**For Debugging:**
1. `start_thinking_session()` - Problem analysis
2. `create_branch()` - Multiple hypotheses
3. `add_thought()` - Investigation steps
4. `merge_branch()` - Combine findings
5. `store_memory()` - Capture solution

**For Enterprise Collaboration:**
1. `load_project_context()` - Team context
2. `query_architecture_decisions()` - Check precedent
3. `set_external_context()` - Cross-team coordination
4. `record_architecture_decision()` - Document choices
5. `update_project_index()` - Share with teams

This comprehensive guide provides the foundation for effective use of the Enhanced Sequential Thinking with Memory Bank MCP system across various programming scenarios and team environments.