---
layout: default
title: 13.1 AWS WAF Deep Dive
parent: 3. AWS Security
grand_parent: Learning Path
nav_order: 1
permalink: /learning-path/security/aws-waf-deep-dive/
---

# 13.1 AWS WAF Deep Dive
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## 📋 Module Overview

**Duration**: 4-6 hours  
**Difficulty**: Intermediate  
**Prerequisites**: Basic AWS knowledge, Networking fundamentals

{: .important }
> This is a **priority module** for immediate job requirements.

### What You'll Learn
- AWS WAF architecture and components
- Rule creation and management
- Protection against common web attacks
- Monitoring and troubleshooting

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:

1. ✅ Explain AWS WAF architecture and components
2. ✅ Create and configure WAF Web ACLs
3. ✅ Implement rules for common attack vectors
4. ✅ Monitor WAF metrics in CloudWatch
5. ✅ Troubleshoot WAF issues in production

---

## 📖 Content

### 1. AWS WAF Architecture

AWS WAF (Web Application Firewall) protects web applications from common exploits.

**Key Components**:
- **Web ACL**: Access Control List containing rules
- **Rules**: Conditions that inspect web requests
- **Rule Groups**: Reusable collections of rules
- **IP Sets**: Lists of IP addresses for allow/block rules

#### How WAF Works

```
User Request → CloudFront/ALB → AWS WAF → Web ACL Rules → Allow/Block Decision
```

### 2. Common Attack Protections

#### SQL Injection Protection

```json
{
  "Name": "SQLInjectionRule",
  "Priority": 1,
  "Statement": {
    "SqliMatchStatement": {
      "FieldToMatch": {
        "QueryString": {}
      },
      "TextTransformations": [
        {
          "Priority": 0,
          "Type": "URL_DECODE"
        }
      ]
    }
  },
  "Action": {
    "Block": {}
  }
}
```

#### Cross-Site Scripting (XSS) Protection

```json
{
  "Name": "XSSProtectionRule",
  "Priority": 2,
  "Statement": {
    "XssMatchStatement": {
      "FieldToMatch": {
        "Body": {}
      },
      "TextTransformations": [
        {
          "Priority": 0,
          "Type": "HTML_ENTITY_DECODE"
        }
      ]
    }
  },
  "Action": {
    "Block": {}
  }
}
```

#### Rate Limiting

```json
{
  "Name": "RateLimitRule",
  "Priority": 3,
  "Statement": {
    "RateBasedStatement": {
      "Limit": 2000,
      "AggregateKeyType": "IP"
    }
  },
  "Action": {
    "Block": {}
  }
}
```

### 3. Geographic Blocking

Block or allow traffic from specific countries:

```json
{
  "Name": "GeoBlockRule",
  "Priority": 4,
  "Statement": {
    "GeoMatchStatement": {
      "CountryCodes": ["CN", "RU"]
    }
  },
  "Action": {
    "Block": {}
  }
}
```

### 4. Managed Rule Groups

AWS provides managed rule groups maintained by AWS and AWS Marketplace sellers:

- **Core Rule Set (CRS)**: Protection against OWASP Top 10
- **Known Bad Inputs**: Block patterns of known malicious requests
- **IP Reputation List**: Block IPs with poor reputation
- **Anonymous IP List**: Block proxies, VPNs, Tor exit nodes

### 5. Monitoring and Logging

#### CloudWatch Metrics
- `AllowedRequests`: Requests that passed all rules
- `BlockedRequests`: Requests blocked by rules
- `CountedRequests`: Requests that matched count rules

#### WAF Logs
Configure logging to:
- Amazon S3
- CloudWatch Logs
- Amazon Kinesis Data Firehose

---

## 🔨 Hands-On Exercise

### Exercise 1: Create a Web ACL

1. **Navigate to AWS WAF Console**
   ```bash
   # Or use AWS CLI
   aws wafv2 create-web-acl \
     --name my-web-acl \
     --scope REGIONAL \
     --default-action Allow={} \
     --region us-east-1
   ```

2. **Add SQL Injection Rule**
   - Create a rule to detect SQL injection attempts
   - Set action to Block
   - Test with sample malicious requests

3. **Configure Rate Limiting**
   - Set limit to 2000 requests per 5 minutes
   - Test by sending multiple requests

4. **Associate with ALB**
   - Link Web ACL to your Application Load Balancer
   - Verify traffic is being inspected

### Exercise 2: Test WAF Rules

```bash
# Test SQL injection blocking
curl -X POST "https://your-domain.com/api/users?id=1' OR '1'='1"

# Test XSS blocking  
curl -X POST "https://your-domain.com/api/comment" \
  -d "text=<script>alert('XSS')</script>"

# Test rate limiting
for i in {1..3000}; do
  curl https://your-domain.com/ &
done
```

---

## 🚨 Emergency Procedures

### WAF is Blocking Legitimate Traffic

1. **Check CloudWatch Logs**
   ```bash
   aws logs filter-log-events \
     --log-group-name aws-waf-logs-my-web-acl \
     --filter-pattern "BLOCK"
   ```

2. **Temporarily Disable Rule**
   - Change rule action from Block to Count
   - Monitor for 24 hours
   - Adjust rule conditions

3. **Add IP to Whitelist**
   ```bash
   aws wafv2 update-ip-set \
     --name whitelist-ips \
     --scope REGIONAL \
     --id <ip-set-id> \
     --addresses 203.0.113.0/24
   ```

### Attack in Progress

1. **Enable rate limiting immediately**
2. **Block offending IP ranges**
3. **Enable additional managed rules**
4. **Alert security team**

---

## ✅ Knowledge Check

Test your understanding:

1. What's the difference between a Web ACL and a Rule?
2. How does rate limiting work in AWS WAF?
3. What are the benefits of managed rule groups?
4. How do you troubleshoot false positives?
5. What's the order of rule evaluation?

<details markdown="1">
<summary><strong>View Answers</strong></summary>

1. **Web ACL vs Rule**: A Web ACL is a container that holds multiple rules. Rules are individual conditions that inspect requests.

2. **Rate Limiting**: Tracks requests from each IP address. Blocks IPs exceeding the specified limit within a 5-minute window.

3. **Managed Rule Groups**: Maintained by AWS/partners, automatically updated, cover OWASP Top 10, reduce management overhead.

4. **False Positives**: Review CloudWatch logs, identify blocked legitimate requests, adjust rule conditions, use Count action for testing.

5. **Rule Evaluation**: Rules are evaluated in order of priority (lowest number first). First matching rule determines the action.

</details>

---

## 📚 Additional Resources

- [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/)
- [AWS WAF Security Automations](https://aws.amazon.com/solutions/implementations/aws-waf-security-automations/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [AWS WAF Pricing](https://aws.amazon.com/waf/pricing/)

---

## 🎯 Next Steps

1. ✅ Mark this module complete in your [Progress Dashboard](/project-tracking/dashboard)
2. 🔨 Complete [Week 2 Lab: AWS WAF Setup](/hands-on-labs/week-02-aws-waf-setup/)
3. ➡️ Continue to [13.2 AWS Shield Protection](../aws-shield)

---

{: .note }
> **Pro Tip**: Start with AWS Managed Rules before creating custom rules. They provide excellent baseline protection.

**Questions?** Check the [Troubleshooting Guide](/resources/troubleshooting) or join the discussion forum.
