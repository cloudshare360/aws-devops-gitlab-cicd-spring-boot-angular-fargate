# Spring Boot Microservices to AWS Fargate: Complete DevOps Pipeline

## Document Overview
**Target**: Deploy Spring Boot microservices + Angular frontend to AWS Fargate with complete security and CI/CD pipeline  
**Tech Stack**: Spring Boot, Angular, Oracle RDS, GitLab CI/CD, AWS Fargate, CloudFront, WAF, Shield  
**Approach**: Quick Overview → Hands-On Implementation → End-to-End Integration  
**Timeline**: 7-10 days for complete pipeline setup  

---

## 🎯 **Learning Journey Map**

### **Day 1-2: Quick Overview & Foundation**
- GitLab CI/CD concepts and Spring Boot integration
- CloudFront for Angular frontend distribution
- AWS WAF for application security
- AWS Shield for DDoS protection
- Architecture understanding

### **Day 3-5: Hands-On Implementation**
- Set up GitLab CI/CD pipeline for Spring Boot
- Configure CloudFront for Angular distribution
- Deploy AWS WAF with custom rules
- Enable AWS Shield monitoring

### **Day 6-7: End-to-End Integration**
- Complete pipeline from code commit to production
- Security integration testing
- Performance optimization
- Monitoring and alerting setup

---

## 📚 **Quick Overview: Core Technologies**

### **GitLab CI/CD for Spring Boot Microservices**
**What**: Automated pipeline for building, testing, and deploying Spring Boot applications  
**Why**: Ensures consistent, reliable deployments with automated testing  
**Key Concepts**:
- **Multi-module builds**: Handle multiple Spring Boot microservices
- **Docker image creation**: Package Spring Boot apps as containers
- **Environment promotion**: Dev → Staging → Production pipeline
- **Parallel execution**: Build multiple microservices simultaneously

**Architecture Flow**:
```
Git Push → GitLab CI/CD → Build Spring Boot JARs → Create Docker Images → Push to ECR → Deploy to Fargate
```

### **CloudFront for Angular Frontend**
**What**: Global CDN for fast Angular application delivery  
**Why**: Improves user experience with global edge locations and caching  
**Key Concepts**:
- **Static asset distribution**: Serve Angular build files globally
- **Custom domains**: Use your domain with SSL/TLS
- **Cache strategies**: Optimize for Angular single-page application
- **Security integration**: Works with WAF for protection

**Architecture Flow**:
```
Angular Build → S3 Bucket → CloudFront Distribution → Global Edge Locations → Users
```

### **AWS WAF for Application Security**
**What**: Web Application Firewall protecting against common attacks  
**Why**: Shields Spring Boot APIs and Angular frontend from threats  
**Key Concepts**:
- **Layer 7 protection**: Inspects HTTP/HTTPS requests
- **Managed rules**: AWS-provided security rules
- **Custom rules**: Application-specific protection
- **Rate limiting**: Protect against DDoS and abuse

**Protection Areas**:
- Spring Boot REST APIs (SQL injection, XSS)
- Angular frontend (malicious scripts, CSRF)
- Database access patterns (unusual query attempts)

### **AWS Shield for DDoS Protection**
**What**: Managed DDoS protection service  
**Why**: Protects infrastructure from volumetric attacks  
**Key Concepts**:
- **Always-on detection**: Automatic attack detection
- **Shield Standard**: Free protection for all AWS customers
- **Shield Advanced**: Enhanced protection with 24/7 support
- **Integration**: Works with CloudFront, ALB, Route 53

---

## 🏗️ **Complete Architecture Overview**

```
Internet Users
    ↓
[AWS Shield] → [CloudFront + WAF] → [Application Load Balancer]
    ↓                                      ↓
Angular Frontend (S3)              Spring Boot Microservices (Fargate)
    ↓                                      ↓
CloudFront Cache                    [Service 1] [Service 2] [Service N]
                                           ↓
                                    Oracle RDS Database
```

**Security Layers**:
1. **AWS Shield**: DDoS protection at network level
2. **CloudFront + WAF**: Application-level filtering and global distribution
3. **VPC Security Groups**: Network access control for Fargate tasks
4. **RDS Security**: Database encryption and access control

---

## 🚀 **Phase 1: Quick Awareness (Day 1-2)**

### **GitLab CI/CD Quick Start**
**Time**: 3-4 hours

#### **Core Concepts to Understand**:
```yaml
# .gitlab-ci.yml structure for Spring Boot microservices
stages:
  - build
  - test
  - package
  - security-scan
  - deploy-staging
  - deploy-production

variables:
  SPRING_PROFILES_ACTIVE: "docker"
  MAVEN_OPTS: "-Dmaven.repo.local=.m2/repository"

# Example job for Spring Boot
build-microservice:
  stage: build
  script:
    - ./mvnw clean compile
    - ./mvnw package -DskipTests
  artifacts:
    paths:
      - target/*.jar
    expire_in: 1 hour
```

#### **Key Learning Points**:
- **Multi-stage pipelines**: Build → Test → Package → Deploy
- **Artifacts management**: Pass JARs between pipeline stages
- **Environment variables**: Configure Spring profiles
- **Parallel jobs**: Build multiple microservices simultaneously

### **CloudFront Quick Start**
**Time**: 2-3 hours

#### **Core Concepts**:
- **Origin configuration**: Point to S3 bucket with Angular build
- **Caching behavior**: Configure for SPA (Single Page Application)
- **Custom error pages**: Handle Angular routing
- **SSL/TLS certificates**: Use AWS Certificate Manager

#### **Angular-Specific Configuration**:
```json
{
  "Origins": {
    "S3Origin": "your-angular-app-bucket.s3.amazonaws.com"
  },
  "DefaultRootObject": "index.html",
  "CustomErrorResponses": [
    {
      "ErrorCode": 404,
      "ResponseCode": 200,
      "ResponsePagePath": "/index.html"
    }
  ]
}
```

### **AWS WAF Quick Start**
**Time**: 2-3 hours

#### **Essential Rule Sets for Spring Boot + Angular**:
- **Core Rule Set**: Basic OWASP Top 10 protection
- **Known Bad Inputs**: Block malicious payloads
- **SQL Database**: Protect Spring Boot database queries
- **Rate-based rules**: Limit request frequency

#### **Spring Boot Specific Considerations**:
```json
{
  "Rules": [
    {
      "Name": "SpringBootAPIProtection",
      "Statement": {
        "ByteMatchStatement": {
          "SearchString": "/api/",
          "FieldToMatch": {"UriPath": {}},
          "PositionalConstraint": "STARTS_WITH"
        }
      }
    }
  ]
}
```

### **AWS Shield Quick Start**
**Time**: 1-2 hours

#### **Configuration Steps**:
1. **Enable Shield Standard**: Automatic for CloudFront and ALB
2. **Configure monitoring**: CloudWatch metrics and alarms
3. **Set up notifications**: SNS for attack alerts
4. **Response procedures**: Escalation and mitigation steps

---

## 🛠️ **Phase 2: Hands-On Implementation (Day 3-5)**

### **Day 3: GitLab CI/CD Pipeline Setup**

#### **Prerequisites Setup**:
```bash
# Install GitLab Runner (if self-hosted)
curl -L https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh | sudo bash
sudo apt-get install gitlab-runner

# Register runner for your project
gitlab-runner register \
  --url https://gitlab.com/ \
  --registration-token <your-token> \
  --description "Spring Boot Runner" \
  --tag-list "docker,aws" \
  --executor docker \
  --docker-image "maven:3.8.6-openjdk-17"
```

#### **Create Spring Boot Pipeline**:
```yaml
# .gitlab-ci.yml for Spring Boot microservices
image: maven:3.8.6-openjdk-17

variables:
  DOCKER_DRIVER: overlay2
  SPRING_PROFILES_ACTIVE: "test"

stages:
  - build
  - test
  - package
  - security
  - deploy

cache:
  paths:
    - .m2/repository/

build:
  stage: build
  script:
    - ./mvnw clean compile
  artifacts:
    paths:
      - target/
    expire_in: 1 hour

test:
  stage: test
  script:
    - ./mvnw test
  artifacts:
    reports:
      junit:
        - target/surefire-reports/TEST-*.xml

package:
  stage: package
  script:
    - ./mvnw package -DskipTests
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
    - develop
```

### **Day 4: CloudFront + Angular Setup**

#### **Angular Build Configuration**:
```bash
# Build Angular for production
ng build --configuration production --output-path dist/

# Upload to S3
aws s3 sync dist/ s3://your-angular-bucket/ --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation \
  --distribution-id $CLOUDFRONT_DISTRIBUTION_ID \
  --paths "/*"
```

#### **CloudFront Configuration**:
```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://cloudfront-config.json

# Sample cloudfront-config.json
{
  "CallerReference": "angular-app-$(date +%s)",
  "Origins": {
    "Quantity": 1,
    "Items": [
      {
        "Id": "S3-angular-bucket",
        "DomainName": "your-angular-bucket.s3.amazonaws.com",
        "S3OriginConfig": {
          "OriginAccessIdentity": ""
        }
      }
    ]
  },
  "DefaultCacheBehavior": {
    "TargetOriginId": "S3-angular-bucket",
    "ViewerProtocolPolicy": "redirect-to-https",
    "Compress": true
  }
}
```

### **Day 5: AWS WAF + Shield Setup**

#### **WAF Configuration for Spring Boot**:
```bash
# Create Web ACL
aws wafv2 create-web-acl \
  --name "SpringBoot-WAF" \
  --scope CLOUDFRONT \
  --default-action Allow={} \
  --rules file://spring-boot-waf-rules.json

# spring-boot-waf-rules.json
[
  {
    "Name": "AWSManagedRulesCoreRuleSet",
    "Priority": 1,
    "Statement": {
      "ManagedRuleGroupStatement": {
        "VendorName": "AWS",
        "Name": "AWSManagedRulesCoreRuleSet"
      }
    },
    "Action": {"Block": {}},
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "CoreRuleSet"
    }
  },
  {
    "Name": "SpringBootAPIRateLimit",
    "Priority": 2,
    "Statement": {
      "RateBasedStatement": {
        "Limit": 1000,
        "AggregateKeyType": "IP",
        "ScopeDownStatement": {
          "ByteMatchStatement": {
            "SearchString": "/api/",
            "FieldToMatch": {"UriPath": {}},
            "PositionalConstraint": "STARTS_WITH"
          }
        }
      }
    },
    "Action": {"Block": {}},
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "APIRateLimit"
    }
  }
]
```

#### **Shield Configuration**:
```bash
# Enable Shield Advanced (optional)
aws shield subscribe-to-proactive-engagement

# Configure DDoS response team
aws shield put-proactive-engagement-details \
  --proactive-engagement-status ENABLED \
  --emergency-contact-list file://emergency-contacts.json

# Set up CloudWatch alarms for DDoS attacks
aws cloudwatch put-metric-alarm \
  --alarm-name "DDoS-Attack-Detected" \
  --alarm-description "Alert on DDoS attack" \
  --metric-name DDoSDetected \
  --namespace AWS/DDoSProtection \
  --statistic Maximum \
  --period 60 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold
```

---

## 🔗 **Phase 3: End-to-End Integration (Day 6-7)**

### **Day 6: Complete Pipeline Integration**

#### **Full GitLab CI/CD Pipeline**:
```yaml
# Complete .gitlab-ci.yml
stages:
  - build
  - test
  - package
  - security
  - deploy-staging
  - deploy-production

variables:
  AWS_DEFAULT_REGION: us-east-1
  ECR_REGISTRY: $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
  SPRING_PROFILES_ACTIVE: "docker"

# Build Spring Boot microservices
build-backend:
  stage: build
  script:
    - ./mvnw clean package -DskipTests
    - docker build -t $ECR_REGISTRY/spring-boot-app:$CI_COMMIT_SHA .
    - aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
    - docker push $ECR_REGISTRY/spring-boot-app:$CI_COMMIT_SHA

# Build Angular frontend
build-frontend:
  stage: build
  image: node:18
  script:
    - cd frontend/
    - npm ci
    - ng build --configuration production
    - aws s3 sync dist/ s3://$ANGULAR_BUCKET/ --delete
    - aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_ID --paths "/*"

# Security scanning
security-scan:
  stage: security
  script:
    - docker run --rm -v $(pwd):/app securecodewarrior/docker-security-scanner /app
    - aws wafv2 test-web-acl --web-acl-arn $WAF_ARN --test-data file://security-tests.json

# Deploy to Fargate
deploy-staging:
  stage: deploy-staging
  script:
    - aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --task-definition $TASK_DEFINITION:$CI_COMMIT_SHA
    - aws ecs wait services-stable --cluster $ECS_CLUSTER --services $ECS_SERVICE
  environment:
    name: staging
    url: https://staging.yourdomain.com

deploy-production:
  stage: deploy-production
  script:
    - aws ecs update-service --cluster $PROD_ECS_CLUSTER --service $PROD_ECS_SERVICE --task-definition $PROD_TASK_DEFINITION:$CI_COMMIT_SHA
    - aws ecs wait services-stable --cluster $PROD_ECS_CLUSTER --services $PROD_ECS_SERVICE
  environment:
    name: production
    url: https://yourdomain.com
  when: manual
  only:
    - main
```

### **Day 7: Monitoring & Optimization**

#### **CloudWatch Dashboard Setup**:
```bash
# Create comprehensive monitoring dashboard
aws cloudwatch put-dashboard \
  --dashboard-name "SpringBoot-Production-Dashboard" \
  --dashboard-body file://dashboard-config.json

# dashboard-config.json includes:
# - WAF blocked/allowed requests
# - CloudFront cache hit ratio
# - Fargate CPU/Memory utilization
# - RDS connection counts
# - Application response times
```

#### **Alerting Configuration**:
```bash
# High error rate alert
aws cloudwatch put-metric-alarm \
  --alarm-name "SpringBoot-HighErrorRate" \
  --alarm-description "High error rate in Spring Boot APIs" \
  --metric-name ErrorRate \
  --namespace AWS/ApplicationELB \
  --statistic Average \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold

# WAF blocked requests alert
aws cloudwatch put-metric-alarm \
  --alarm-name "WAF-HighBlockedRequests" \
  --alarm-description "High number of blocked requests" \
  --metric-name BlockedRequests \
  --namespace AWS/WAFV2 \
  --statistic Sum \
  --period 300 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold
```

---

## 📋 **Daily Progress Checklist**

### **Day 1: Architecture Understanding**
- [ ] Understand GitLab CI/CD for Spring Boot
- [ ] Learn CloudFront for Angular distribution
- [ ] Grasp AWS WAF protection concepts
- [ ] Review AWS Shield DDoS protection

### **Day 2: Quick Overview Completion**
- [ ] Review complete architecture diagram
- [ ] Understand security layers
- [ ] Plan hands-on implementation approach

### **Day 3: GitLab CI/CD Implementation**
- [ ] Set up GitLab Runner
- [ ] Create basic Spring Boot pipeline
- [ ] Test build and deployment process

### **Day 4: CloudFront + Angular Setup**
- [ ] Configure S3 bucket for Angular
- [ ] Create CloudFront distribution
- [ ] Test Angular deployment and caching

### **Day 5: Security Implementation**
- [ ] Deploy AWS WAF with Spring Boot rules
- [ ] Enable AWS Shield monitoring
- [ ] Test security configurations

### **Day 6: End-to-End Integration**
- [ ] Complete pipeline from commit to production
- [ ] Test all components working together
- [ ] Verify security integration

### **Day 7: Monitoring & Optimization**
- [ ] Set up comprehensive monitoring
- [ ] Configure alerting and notifications
- [ ] Optimize performance and costs
- [ ] Document the complete solution

---

## 🎯 **Success Criteria**

### **Technical Achievements**
- [ ] Automated CI/CD pipeline for Spring Boot microservices
- [ ] Angular frontend distributed via CloudFront
- [ ] AWS WAF protecting all application endpoints
- [ ] AWS Shield monitoring DDoS attacks
- [ ] Complete observability with monitoring and alerting

### **Learning Outcomes**
- [ ] Understand GitLab CI/CD for Java applications
- [ ] Master CloudFront configuration for SPAs
- [ ] Deploy production-ready AWS WAF
- [ ] Configure comprehensive AWS Shield protection
- [ ] Implement end-to-end DevOps pipeline

### **Production Readiness**
- [ ] Zero-downtime deployments
- [ ] Comprehensive security coverage
- [ ] Proactive monitoring and alerting
- [ ] Disaster recovery procedures documented

---

## 📚 **Next Steps After Completion**

### **Advanced Topics**
- Infrastructure as Code with Terraform
- Advanced Spring Boot monitoring with Micrometer
- Database security and performance optimization
- Blue-green and canary deployment strategies

### **Continuous Improvement**
- Pipeline optimization and parallelization
- Cost optimization strategies
- Advanced security automation
- Performance tuning and scaling

**Start Date**: November 3, 2025  
**Target Completion**: November 13, 2025  
**Focus**: Practical implementation with immediate job applicability