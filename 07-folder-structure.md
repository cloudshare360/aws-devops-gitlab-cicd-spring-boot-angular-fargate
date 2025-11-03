# 📁 Repository Folder Structure

## 🧭 Navigation
**For detailed navigation guide**: See [`NAVIGATION.md`](./NAVIGATION.md)

## 📂 Complete Hierarchical Organization with Index

```
📁 aws-devops-gitlab-cicd-spring-boot-angular-fargate/
├── 📖 00-README.md                                    # Repository overview
├── 🧭 01-NAVIGATION.md                               # Complete navigation guide ⭐ NEW
├── 📄 07-folder-structure.md                         # This document
├── 📄 08-index.md                                    # GitHub Pages homepage
│
├── 🎯 CORE DOCUMENTS
│   ├── 📖 02-spring-boot-microservices-devops-pipeline.md  # Main learning document ⭐
│   ├──  03-learning-plan.md                        # Lambda→DevOps transition plan
│   ├── 📄 04-requirements.md                         # 14-week comprehensive learning path
│   ├── 📄 05-requirements-based-on-project-priority.md  # Role-specific immediate priorities
│   └── 📄 06-raw-requirements.md                     # Original scattered requirements
│
├── 📁 10-learning-path/                       # Sequential learning modules
│   ├── 📁 11-foundations/
│   │   ├── 📄 11.1-spring-boot-containerization.md
│   │   ├── 📄 11.2-devops-principles-for-microservices.md
│   │   ├── 📄 11.3-aws-services-for-spring-boot.md
│   │   └── 📄 11.4-microservices-architecture-patterns.md
│   │
│   ├── 📁 12-containerization/
│   │   ├── 📄 12.1-spring-boot-docker-optimization.md
│   │   ├── 📄 12.2-multi-stage-builds-spring-boot.md
│   │   ├── 📄 12.3-ecs-fargate-deployment.md
│   │   └── � 12.4-microservices-orchestration.md
│   │
│   ├── 📁 13-aws-security/ 🚨 PRIORITY
│   │   ├── 📄 13.1-aws-waf-deep-dive.md ⭐
│   │   ├── 📄 13.2-aws-shield-protection.md
│   │   ├── 📄 13.3-cloudfront-security.md
│   │   └── 📄 13.4-security-automation.md
│   │
│   ├── 📁 14-cicd-pipelines/ 🚨 PRIORITY
│   │   ├── 📄 14.1-gitlab-cicd-spring-boot-microservices.md
│   │   ├── 📄 14.2-multi-microservice-pipeline-patterns.md
│   │   ├── 📄 14.3-angular-build-deployment.md
│   │   └── 📄 14.4-security-scanning-integration.md
│   │
│   ├── 📁 15-infrastructure-as-code/
│   │   ├── 📄 15.1-terraform-fundamentals.md
│   │   ├── 📄 15.2-aws-terraform-patterns.md
│   │   ├── 📄 15.3-cloudformation-comparison.md
│   │   └── 📄 15.4-state-management.md
│   │
│   └── 📁 16-monitoring-observability/
│       ├── 📄 16.1-cloudwatch-advanced.md
│       ├── 📄 16.2-application-monitoring.md
│       ├── 📄 16.3-alerting-strategies.md
│       └── 📄 16.4-cost-optimization.md
│
├── 📁 20-hands-on-labs/                      # Practical exercises
│   ├── 📁 21-week-01-foundation-setup/
│   │   └── 📄 21.1-README.md
│   ├── 📁 22-week-02-aws-waf-setup/ ⭐ PRIORITY LAB
│   │   ├── 📄 22.1-README.md
│   │   ├── 📄 22.2-waf-basic-deployment.md
│   │   ├── 📄 22.3-custom-rules-creation.md
│   │   └── 📄 22.4-monitoring-tuning.md
│   ├── 📁 23-week-03-containerization-lab/
│   ├── 📁 24-week-04-cicd-pipeline-lab/
│   ├── 📁 25-week-05-infrastructure-lab/
│   └── 📁 26-week-06-monitoring-lab/
│
├── 📁 30-project-tracking/                   # Progress management
│   ├── 📄 30.1-dashboard.md
│   ├── 📄 30.2-weekly-milestones.md
│   ├── 📄 30.3-skill-assessment.md
│   └── 📄 30.4-completion-checklist.md
│
├── 📁 40-resources/                          # Additional materials
│   ├── 📄 40.1-reference-links.md
│   ├── 📄 40.2-troubleshooting-guide.md
│   ├── 📄 40.3-best-practices-checklist.md
│   └── 📄 40.4-certification-paths.md
│
└── 📁 50-agent-memory/                       # AI assistant optimization
    ├── 📄 50.1-conversation-log.md           # Learning progress tracking
    ├── 📄 50.2-user-profile.md               # User background & preferences
    └── 📄 50.3-project-evolution.md          # Repository change history
│   ├── 📄 conversation-log.md                # Session history & patterns
│   └── 📄 optimization-notes.md              # Continuous improvement
│
├── 📁 project-tracking/                      # Progress management
│   ├── 📄 dashboard.md                       # Main progress tracking
│   ├── 📄 milestones.md                      # Detailed milestone tracking
│   ├── 📄 weekly-reviews/                    # Weekly progress reviews
│   └── 📄 risk-issues.md                     # Risk and issue management
│
├── 📁 hands-on-labs/                         # Practical exercises
│   ├── 📁 week-01-docker-basics/
│   ├── 📁 week-02-aws-waf-setup/
│   ├── 📁 week-03-gitlab-pipeline/
│   ├── 📁 week-04-security-integration/
│   └── 📁 final-project/
│
└── 📁 resources/                             # Reference materials
    ├── 📄 cheat-sheets/
    ├── 📄 documentation-links.md
    ├── 📄 troubleshooting-guide.md
    └── 📄 emergency-procedures.md
```

---

## Folder Purpose & Usage

### 📁 learning-path/
**Purpose**: Sequential learning modules organized by complexity and priority  
**Usage**: Follow in order, each folder builds on previous knowledge  
**Priority**: Phases 3 & 4 (AWS Security + CI/CD) are immediate job requirements  

### 📁 agent-memory/
**Purpose**: AI assistant optimization for better future interactions  
**Usage**: Updated after each conversation to improve context and recommendations  
**Benefit**: Personalized assistance that gets better over time  

### 📁 project-tracking/
**Purpose**: Monitor progress, manage milestones, track issues  
**Usage**: Weekly updates, milestone completion tracking, risk management  
**Benefit**: Stay on track for 3-month DevOps competency goal  

### 📁 hands-on-labs/
**Purpose**: Practical exercises to reinforce learning  
**Usage**: Complete labs after studying each module  
**Benefit**: Learn by doing, build portfolio of working examples  

### 📁 resources/
**Purpose**: Quick reference materials and emergency procedures  
**Usage**: Bookmark for quick lookup during actual work  
**Benefit**: Reduce time searching for solutions during production issues  

---

## Navigation Guide

### For Immediate Job Needs (Next 2 Weeks)
1. **Start Here**: `learning-path/03-aws-security/aws-waf-deep-dive.md`
2. **Then**: `learning-path/04-cicd-pipelines/gitlab-cicd-fundamentals.md`
3. **Practice**: `hands-on-labs/week-02-aws-waf-setup/`
4. **Track**: `project-tracking/dashboard.md`

### For Foundational Knowledge (Week 3+)
1. **Start Here**: `learning-path/01-foundations/`
2. **Progress Through**: Each numbered folder in sequence
3. **Practice**: Corresponding hands-on labs
4. **Track**: Weekly reviews in project tracking

### For Quick Reference
- **Commands**: `resources/cheat-sheets/`
- **Troubleshooting**: `resources/troubleshooting-guide.md`
- **Emergency**: `resources/emergency-procedures.md`

---

## Document Relationships

### Core Planning Documents
- `requirements.md` ↔ `learning-plan.md` (comprehensive vs targeted)
- `requirements-based-on-project-priority.md` ↔ `project-tracking/dashboard.md` (planning vs execution)

### Learning Materials Flow
- `learning-plan.md` → `learning-path/[phase]/` → `hands-on-labs/[week]/`
- Prerequisites clearly marked in each learning module

### Tracking & Optimization
- `project-tracking/dashboard.md` ← Weekly progress updates
- `agent-memory/conversation-log.md` ← Each conversation logged
- `agent-memory/user-profile.md` ← Continuously updated preferences

---

## Maintenance Schedule

### Daily Updates
- Progress on current learning module
- Notes in hands-on lab folders
- Issues encountered and solutions

### Weekly Updates  
- `project-tracking/dashboard.md` progress review
- `project-tracking/weekly-reviews/` new entry
- Milestone completion status

### After Each Conversation
- `agent-memory/conversation-log.md` new session entry
- `agent-memory/user-profile.md` preference updates
- `agent-memory/optimization-notes.md` improvement ideas

---

## Quick Start Guide

### Week 1 Action Plan
1. **Navigation First**: Review [`NAVIGATION.md`](./NAVIGATION.md) for complete learning guide
2. **Priority Learning**: AWS WAF basics (`learning-path/03-aws-security/`)
3. **Hands-On Practice**: WAF setup lab (`hands-on-labs/week-02-aws-waf-setup/`)
4. **Progress Tracking**: Update dashboard daily (`project-tracking/dashboard.md`)
5. **Foundation Building**: Docker basics (`learning-path/01-foundations/containerization-basics.md`)

---

**📖 For comprehensive navigation and learning paths, see [`NAVIGATION.md`](./NAVIGATION.md)**

### Success Indicators
- [ ] Folder structure understood and navigated easily
- [ ] First learning module completed with hands-on lab
- [ ] Progress tracking updated and milestones clear
- [ ] Agent memory system providing personalized assistance

This hierarchical structure ensures organized learning, progress tracking, and continuous optimization of the AI assistant to support your DevOps role transition effectively.