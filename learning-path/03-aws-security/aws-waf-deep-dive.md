# AWS WAF Deep Dive

## Prerequisites ✅
- **Required**: AWS CLI experience (you have this from Lambda development)
- **Required**: Basic understanding of web applications (you have this)
- **Required**: JSON/YAML syntax familiarity (you have this)
- **Helpful**: Basic networking concepts (can learn alongside)

## Module Overview
Learn to deploy and configure AWS WAF (Web Application Firewall) to protect web applications from common attacks. This module leverages your existing AWS knowledge while introducing security concepts.

**Time Investment**: 8-10 hours over 3-4 days  
**Practical Outcome**: Production-ready WAF protecting your application

---

## Learning Objectives

By the end of this module, you will:
- [ ] Deploy AWS WAF with managed rule sets
- [ ] Create custom WAF rules for specific threats
- [ ] Integrate WAF with CloudFront and Application Load Balancer
- [ ] Monitor WAF logs and tune rules to reduce false positives
- [ ] Implement emergency response procedures for security events

---

## Conceptual Foundation

### WAF vs Lambda Security
Coming from Lambda development, you're used to:
- **API Gateway**: Basic throttling and authentication
- **Lambda Authorizers**: Custom authentication logic
- **VPC**: Network isolation for Lambda functions

AWS WAF adds:
- **Layer 7 Protection**: Deep packet inspection of HTTP/HTTPS requests
- **Threat Intelligence**: AWS-managed rules updated automatically  
- **Rate Limiting**: Advanced traffic control beyond API Gateway
- **Geographic Filtering**: Block traffic from specific countries/regions

### WAF Architecture in Your Stack
```
Internet → CloudFront → [WAF Rules Applied] → ALB → ECS Fargate → Application
```

**Key Insight**: WAF sits at the edge, filtering malicious traffic before it reaches your application infrastructure.

---

## Core Concepts

### 1. Web ACLs (Access Control Lists)
**What**: Container for WAF rules that defines what traffic to allow/block  
**Lambda Parallel**: Like IAM policies for API Gateway - defines permissions

```json
{
  "Name": "MyWebACL",
  "Scope": "CLOUDFRONT",
  "DefaultAction": {"Allow": {}},
  "Rules": [...]
}
```

### 2. WAF Rules
**What**: Individual conditions that inspect traffic  
**Types**:
- **AWS Managed Rules**: Pre-built rule sets (recommended starting point)
- **Custom Rules**: Application-specific protection
- **Rate-based Rules**: Traffic throttling

### 3. Rule Evaluation
**Order Matters**: Rules evaluated by priority (lowest number first)  
**Actions**: Allow, Block, Count (monitoring mode)

---

## Hands-On Implementation

### Step 1: Basic WAF Setup (Day 1)

#### Create Web ACL with AWS CLI
```bash
# Create basic Web ACL
aws wafv2 create-web-acl \
  --name "MyApp-WAF" \
  --scope CLOUDFRONT \
  --default-action Allow={} \
  --rules file://basic-rules.json \
  --region us-east-1

# Get Web ACL details
aws wafv2 get-web-acl \
  --name "MyApp-WAF" \
  --scope CLOUDFRONT \
  --id <web-acl-id>
```

#### Basic Rules Configuration (basic-rules.json)
```json
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
    "Action": {
      "Block": {}
    },
    "VisibilityConfig": {
      "SampledRequestsEnabled": true,
      "CloudWatchMetricsEnabled": true,
      "MetricName": "CoreRuleSetMetric"
    }
  }
]
```

### Step 2: Advanced Rule Configuration (Day 2)

#### Rate Limiting Rule
```bash
# Create rate-based rule (1000 requests per 5 minutes)
aws wafv2 create-rule-group \
  --name "RateLimitRule" \
  --scope CLOUDFRONT \
  --capacity 100 \
  --rules file://rate-limit-rule.json
```

#### Custom Application Rules
- **SQL Injection Protection**: Block common SQL injection patterns
- **XSS Protection**: Filter cross-site scripting attempts  
- **Known Bad IPs**: Block traffic from malicious IP addresses

### Step 3: Integration & Testing (Day 3)

#### Associate WAF with CloudFront
```bash
# Associate Web ACL with CloudFront distribution
aws wafv2 associate-web-acl \
  --web-acl-arn <web-acl-arn> \
  --resource-arn <cloudfront-distribution-arn>
```

#### Testing Strategy
1. **Legitimate Traffic Test**: Ensure normal application usage works
2. **Attack Simulation**: Test with known attack patterns
3. **False Positive Check**: Monitor for blocked legitimate requests

---

## Monitoring & Tuning

### CloudWatch Integration
```bash
# Get WAF metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/WAFV2 \
  --metric-name AllowedRequests \
  --dimensions Name=WebACL,Value=MyApp-WAF \
  --start-time 2025-11-03T00:00:00Z \
  --end-time 2025-11-03T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

### Log Analysis
**Enable WAF Logging**:
```bash
# Configure WAF logging to S3
aws wafv2 put-logging-configuration \
  --logging-configuration \
  ResourceArn=<web-acl-arn>,LogDestinationConfigs=<s3-bucket-arn>
```

**Key Metrics to Monitor**:
- **Blocked Requests**: High numbers might indicate attack or false positives
- **Allowed Requests**: Baseline for normal traffic patterns
- **Rule Match Counts**: Which rules are triggering most often

---

## Common Pitfalls & Solutions

### Pitfall 1: Over-blocking Legitimate Traffic
**Symptoms**: Users reporting access issues, high blocked request count  
**Solution**: Use "Count" mode initially, analyze logs before switching to "Block"

### Pitfall 2: Under-protection
**Symptoms**: Still seeing attacks reach application logs  
**Solution**: Enable additional managed rule sets, create custom rules for app-specific threats

### Pitfall 3: Performance Impact
**Symptoms**: Increased response times  
**Solution**: Optimize rule order, use most specific rules first

---

## Integration with Your Development Workflow

### CI/CD Integration
Add WAF rule testing to your GitLab pipeline:
```yaml
waf_test:
  stage: security-test
  script:
    - aws wafv2 test-web-acl --web-acl-arn $WAF_ARN --test-cases file://test-cases.json
    - python validate_waf_rules.py
```

### Infrastructure as Code
**Terraform WAF Configuration**:
```hcl
resource "aws_wafv2_web_acl" "main" {
  name  = "myapp-waf"
  scope = "CLOUDFRONT"
  
  default_action {
    allow {}
  }
  
  rule {
    name     = "AWSManagedRulesCore"
    priority = 1
    
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCoreRuleSet"
        vendor_name = "AWS"
      }
    }
    
    action {
      block {}
    }
  }
}
```

---

## Emergency Procedures

### Immediate Response to False Positives
```bash
# Emergency: Temporarily disable problematic rule
aws wafv2 update-web-acl \
  --id <web-acl-id> \
  --scope CLOUDFRONT \
  --rules file://emergency-rules.json

# Quick IP whitelist for urgent access
aws wafv2 create-ip-set \
  --name "EmergencyAllowList" \
  --scope CLOUDFRONT \
  --ip-address-version IPV4 \
  --addresses "x.x.x.x/32"
```

### Attack Response Procedures
1. **Identify Attack Pattern**: Check WAF logs for commonalities
2. **Create Temporary Rule**: Block specific pattern immediately
3. **Analyze Impact**: Ensure rule doesn't affect legitimate users
4. **Permanent Rule**: Convert temporary fix to permanent solution

---

## Assessment & Next Steps

### Knowledge Check
- [ ] Can explain difference between AWS Managed Rules and Custom Rules
- [ ] Successfully deployed WAF with basic protection
- [ ] Configured monitoring and alerting for WAF events
- [ ] Integrated WAF testing into CI/CD pipeline
- [ ] Responded to simulated security event

### Next Module Preparation
**Next**: AWS Shield Protection (`aws-shield-protection.md`)  
**Prerequisites for Next Module**: WAF knowledge ✅, CloudWatch basics, incident response concepts

### Real-World Application
Apply this knowledge immediately:
1. Deploy WAF for your current application
2. Start with "Count" mode to baseline traffic
3. Gradually enable blocking rules based on analysis
4. Document your specific rule configurations

---

## Additional Resources

### AWS Documentation
- [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/)
- [WAF Rule Statement Reference](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type.html)

### Hands-On Practice
- [AWS WAF Workshop](https://waf.aws-management.tools/)
- [Security Learning Labs](https://aws.amazon.com/training/learning-paths/security/)

### Community Resources
- [AWS Security Blog - WAF Articles](https://aws.amazon.com/blogs/security/tag/aws-waf/)
- [GitHub: WAF Rule Examples](https://github.com/aws-samples/aws-waf-security-automations)

**Time to Complete Module**: 3-4 days with hands-on practice  
**Next Review Date**: After completing hands-on lab and assessment