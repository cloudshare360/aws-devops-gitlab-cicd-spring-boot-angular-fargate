# 📊 Architecture Diagrams

## 🧭 Navigation
**← Back to**: [40-Resources](../)  
**↑ Repository**: [01-NAVIGATION.md](../../01-NAVIGATION.md)

## 📋 Diagram Collection
This directory contains comprehensive architecture diagrams for the Spring Boot microservices to AWS Fargate DevOps pipeline.

### 🏗️ **Available Diagrams**

#### **01. Complete System Architecture**
- **File**: [`01-complete-system-architecture.drawio`](./01-complete-system-architecture.drawio)
- **Purpose**: End-to-end system overview
- **Components**: All services, security layers, and data flow
- **Use Case**: System design discussions, documentation

#### **02. Security Architecture**  
- **File**: [`02-security-architecture.drawio`](./02-security-architecture.drawio)
- **Purpose**: Security components and data flow
- **Components**: WAF, Shield, CloudFront, VPC security
- **Use Case**: Security reviews, compliance documentation

#### **03. CI/CD Pipeline Flow**
- **File**: [`03-cicd-pipeline-flow.drawio`](./03-cicd-pipeline-flow.drawio)
- **Purpose**: DevOps pipeline visualization
- **Components**: GitLab stages, deployment flow, environments
- **Use Case**: Pipeline optimization, team training

#### **04. Microservices Deployment**
- **File**: [`04-microservices-deployment.drawio`](./04-microservices-deployment.drawio)
- **Purpose**: Container orchestration and service mesh
- **Components**: ECS Fargate, service discovery, load balancing
- **Use Case**: Development planning, infrastructure design

#### **05. Data Flow Architecture**
- **File**: [`05-data-flow-architecture.drawio`](./05-data-flow-architecture.drawio)
- **Purpose**: Data movement and storage patterns
- **Components**: RDS, S3, CloudFront cache, API flows
- **Use Case**: Performance optimization, troubleshooting

## 🎯 **How to Use These Diagrams**

### **For Architecture Reviews**
1. Start with **01-Complete System** for overview
2. Deep dive into **02-Security** for compliance
3. Review **03-CI/CD Pipeline** for DevOps processes

### **For Implementation Planning**
1. Use **04-Microservices Deployment** for infrastructure setup
2. Reference **05-Data Flow** for performance optimization
3. Validate against **02-Security** for security requirements

### **For Team Communication**
- **Developers**: Focus on 04-Microservices and 05-Data Flow
- **DevOps Engineers**: Emphasize 03-CI/CD Pipeline and 01-Complete System
- **Security Team**: Prioritize 02-Security Architecture
- **Management**: Use 01-Complete System for high-level overview

## 🔧 **Editing Instructions**

### **Software Required**
- **draw.io Desktop**: [Download here](https://github.com/jgraph/drawio-desktop/releases)
- **Online Version**: [app.diagrams.net](https://app.diagrams.net)
- **VS Code Extension**: Draw.io Integration

### **File Format**
- All diagrams are in `.drawio` format
- Compatible with draw.io desktop and web versions
- Can be exported to PNG, SVG, PDF for documentation

### **Customization Guidelines**
- **Colors**: Use consistent color scheme across diagrams
- **Labels**: Keep text clear and readable
- **Layers**: Organize components in logical layers
- **Connections**: Use appropriate arrow styles for data flow

## 📚 **Related Documentation**

### **Architecture References**
- [02-spring-boot-microservices-devops-pipeline.md](../../02-spring-boot-microservices-devops-pipeline.md) - Main architecture document
- [13.1-aws-waf-deep-dive.md](../../10-learning-path/13-aws-security/13.1-aws-waf-deep-dive.md) - Security details
- [14.1-gitlab-cicd-spring-boot-microservices.md](../../10-learning-path/14-cicd-pipelines/14.1-gitlab-cicd-spring-boot-microservices.md) - CI/CD implementation

### **Implementation Guides**
- [22.1-README.md](../../20-hands-on-labs/22-week-02-aws-waf-setup/22.1-README.md) - Security implementation
- [30.1-dashboard.md](../../30-project-tracking/30.1-dashboard.md) - Progress tracking

---

*These diagrams provide visual representation of the architecture described in the learning materials. Use them for planning, implementation, and team communication.*

*Last Updated: November 4, 2025*