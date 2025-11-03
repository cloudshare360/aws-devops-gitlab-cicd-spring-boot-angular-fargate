# AWS WAF Hands-On Lab

## Lab Overview
**Duration**: 4-6 hours across 2-3 sessions  
**Objective**: Deploy production-ready AWS WAF protecting a web application  
**Prerequisites**: AWS CLI configured, basic web application deployed  

---

## Lab Environment Setup

### Required Resources
- AWS Account with WAF permissions
- Web application deployed (can be simple "Hello World" app)
- CloudFront distribution (or ALB)
- AWS CLI configured with appropriate permissions

### Pre-Lab Checklist
- [ ] AWS CLI installed and configured
- [ ] Test application accessible via HTTP/HTTPS
- [ ] CloudFront distribution or ALB available for WAF association
- [ ] Billing alerts configured (WAF charges per web ACL and requests)

---

## Lab Exercises

### Exercise 1: Basic WAF Deployment (2 hours)

#### Step 1.1: Create Basic Web ACL
```bash
# Create the Web ACL JSON configuration
cat > basic-web-acl.json << EOF
{
  "Name": "DevOpsLab-WAF",
  "Scope": "CLOUDFRONT",
  "DefaultAction": {
    "Allow": {}
  },
  "Rules": [
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
  ],
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "DevOpsLabWAF"
  }
}
EOF

# Create the Web ACL
aws wafv2 create-web-acl \
  --cli-input-json file://basic-web-acl.json \
  --region us-east-1
```

#### Step 1.2: Capture Web ACL Details
```bash
# List Web ACLs to find your newly created one
aws wafv2 list-web-acls --scope CLOUDFRONT --region us-east-1

# Get detailed information (replace <web-acl-id> with actual ID)
aws wafv2 get-web-acl \
  --scope CLOUDFRONT \
  --id <web-acl-id> \
  --region us-east-1 > web-acl-details.json

# Save the ARN for later use
grep '"ARN"' web-acl-details.json | cut -d'"' -f4 > web-acl-arn.txt
```

#### Step 1.3: Associate WAF with CloudFront
```bash
# Get your CloudFront distribution ARN
aws cloudfront list-distributions --query 'DistributionList.Items[0].ARN' --output text > distribution-arn.txt

# Associate WAF with CloudFront
aws wafv2 associate-web-acl \
  --web-acl-arn $(cat web-acl-arn.txt) \
  --resource-arn $(cat distribution-arn.txt) \
  --region us-east-1
```

#### Step 1.4: Verify Association
```bash
# Check if association was successful
aws wafv2 get-web-acl-for-resource \
  --resource-arn $(cat distribution-arn.txt) \
  --region us-east-1
```

**Expected Outcome**: WAF is now protecting your CloudFront distribution with AWS managed core rules.

---

### Exercise 2: Custom Rule Creation (2 hours)

#### Step 2.1: Create Rate Limiting Rule
```bash
# Create rate limiting rule configuration
cat > rate-limit-rule.json << EOF
{
  "Name": "RateLimitRule",
  "Priority": 0,
  "Statement": {
    "RateBasedStatement": {
      "Limit": 2000,
      "AggregateKeyType": "IP"
    }
  },
  "Action": {
    "Block": {}
  },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "RateLimitRule"
  }
}
EOF

# Add the rule to existing Web ACL
# First, get current rules
aws wafv2 get-web-acl \
  --scope CLOUDFRONT \
  --id <web-acl-id> \
  --region us-east-1 | jq '.WebACL.Rules' > current-rules.json

# Create updated rules JSON (manual step - combine current rules with new rate limit rule)
# Then update the Web ACL
aws wafv2 update-web-acl \
  --scope CLOUDFRONT \
  --id <web-acl-id> \
  --lock-token <lock-token> \
  --rules file://updated-rules.json \
  --region us-east-1
```

#### Step 2.2: Create Geographic Blocking Rule
```bash
# Create IP set for blocked countries
aws wafv2 create-ip-set \
  --name "BlockedCountries" \
  --scope CLOUDFRONT \
  --ip-address-version IPV4 \
  --addresses "1.2.3.0/24" \
  --region us-east-1

# Create geo-blocking rule
cat > geo-block-rule.json << EOF
{
  "Name": "GeoBlockRule",
  "Priority": 2,
  "Statement": {
    "GeoMatchStatement": {
      "CountryCodes": ["CN", "RU"]
    }
  },
  "Action": {
    "Block": {}
  },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "GeoBlockRule"
  }
}
EOF
```

#### Step 2.3: Test Custom Rules
```bash
# Create test script to verify rate limiting
cat > test-rate-limit.sh << 'EOF'
#!/bin/bash
echo "Testing rate limiting..."
for i in {1..10}; do
  curl -s -o /dev/null -w "%{http_code}\n" https://your-domain.com
  sleep 0.1
done
EOF

chmod +x test-rate-limit.sh
./test-rate-limit.sh
```

**Expected Outcome**: Rate limiting triggers after configured threshold, custom rules active.

---

### Exercise 3: Monitoring & Alerting Setup (1-2 hours)

#### Step 3.1: Enable WAF Logging
```bash
# Create S3 bucket for WAF logs
aws s3 mb s3://your-waf-logs-bucket-$(date +%s) --region us-east-1

# Configure WAF logging
aws wafv2 put-logging-configuration \
  --logging-configuration '{
    "ResourceArn": "'$(cat web-acl-arn.txt)'",
    "LogDestinationConfigs": ["arn:aws:s3:::your-waf-logs-bucket"]
  }' --region us-east-1
```

#### Step 3.2: Create CloudWatch Dashboard
```bash
# Create CloudWatch dashboard configuration
cat > waf-dashboard.json << EOF
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/WAFV2", "AllowedRequests", "WebACL", "DevOpsLab-WAF"],
          [".", "BlockedRequests", ".", "."],
          [".", "SampledRequests", ".", "."]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "us-east-1",
        "title": "WAF Request Summary"
      }
    }
  ]
}
EOF

# Create the dashboard
aws cloudwatch put-dashboard \
  --dashboard-name "DevOpsLab-WAF-Dashboard" \
  --dashboard-body file://waf-dashboard.json \
  --region us-east-1
```

#### Step 3.3: Set Up CloudWatch Alarms
```bash
# Create alarm for high blocked requests
aws cloudwatch put-metric-alarm \
  --alarm-name "WAF-HighBlockedRequests" \
  --alarm-description "Alert when WAF blocks many requests" \
  --metric-name BlockedRequests \
  --namespace AWS/WAFV2 \
  --statistic Sum \
  --period 300 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=WebACL,Value=DevOpsLab-WAF \
  --evaluation-periods 2 \
  --region us-east-1
```

**Expected Outcome**: Comprehensive monitoring setup with dashboards and alerting.

---

### Exercise 4: Attack Simulation & Response (1 hour)

#### Step 4.1: Simulate Common Attacks
```bash
# SQL Injection attempt (should be blocked)
curl -X POST "https://your-domain.com/search" \
  -d "query='; DROP TABLE users; --"

# XSS attempt (should be blocked)
curl "https://your-domain.com/page?input=<script>alert('xss')</script>"

# Check if attacks were blocked in WAF logs
aws logs filter-log-events \
  --log-group-name aws-waf-logs-your-cloudfront-distribution \
  --start-time $(date -d '5 minutes ago' +%s)000 \
  --filter-pattern "BLOCK"
```

#### Step 4.2: Test False Positive Handling
```bash
# Create legitimate request that might trigger rules
curl -X POST "https://your-domain.com/api/data" \
  -H "Content-Type: application/json" \
  -d '{"query": "SELECT * FROM products WHERE category = \"electronics\""}'

# If blocked, create exception rule
cat > exception-rule.json << EOF
{
  "Name": "LegitimateAPIException",
  "Priority": 0,
  "Statement": {
    "AndStatement": {
      "Statements": [
        {
          "ByteMatchStatement": {
            "SearchString": "/api/",
            "FieldToMatch": {
              "UriPath": {}
            },
            "TextTransformations": [
              {
                "Priority": 0,
                "Type": "LOWERCASE"
              }
            ],
            "PositionalConstraint": "CONTAINS"
          }
        }
      ]
    }
  },
  "Action": {
    "Allow": {}
  },
  "VisibilityConfig": {
    "SampledRequestsEnabled": true,
    "CloudWatchMetricsEnabled": true,
    "MetricName": "APIException"
  }
}
EOF
```

**Expected Outcome**: Ability to identify and respond to both attacks and false positives.

---

## Lab Validation

### Checklist
- [ ] WAF deployed and associated with CloudFront/ALB
- [ ] AWS managed rules active and blocking test attacks
- [ ] Custom rate limiting rule configured and tested
- [ ] Geographic blocking configured (if required)
- [ ] Logging enabled and log analysis performed
- [ ] CloudWatch dashboard created with key metrics
- [ ] Alerting configured for security events
- [ ] Attack simulation performed with expected results
- [ ] False positive handling demonstrated

### Performance Metrics
- **Request Processing**: <5ms added latency from WAF
- **Block Rate**: >95% of simulated attacks blocked
- **False Positive Rate**: <1% of legitimate traffic blocked
- **Alert Response**: Notifications received within 5 minutes

---

## Troubleshooting Common Issues

### Issue 1: WAF Not Blocking Expected Traffic
**Symptoms**: Attack patterns getting through  
**Debug Steps**:
```bash
# Check rule order and actions
aws wafv2 get-web-acl --scope CLOUDFRONT --id <web-acl-id> | jq '.WebACL.Rules'

# Verify rule statements
aws wafv2 get-web-acl --scope CLOUDFRONT --id <web-acl-id> | jq '.WebACL.Rules[].Statement'

# Check sampled requests
aws wafv2 get-sampled-requests \
  --web-acl-arn $(cat web-acl-arn.txt) \
  --rule-metric-name CoreRuleSetMetric \
  --scope CLOUDFRONT \
  --time-window StartTime=$(date -d '1 hour ago' --iso-8601),EndTime=$(date --iso-8601) \
  --max-items 100
```

### Issue 2: High False Positive Rate
**Symptoms**: Legitimate users being blocked  
**Debug Steps**:
```bash
# Analyze blocked requests
aws logs filter-log-events \
  --log-group-name aws-waf-logs-your-distribution \
  --filter-pattern "BLOCK" \
  --start-time $(date -d '1 hour ago' +%s)000

# Check specific rule triggers
aws wafv2 get-sampled-requests \
  --web-acl-arn $(cat web-acl-arn.txt) \
  --rule-metric-name <rule-metric-name> \
  --scope CLOUDFRONT \
  --time-window StartTime=$(date -d '1 hour ago' --iso-8601),EndTime=$(date --iso-8601) \
  --max-items 100
```

### Issue 3: CloudWatch Metrics Not Appearing
**Symptoms**: Dashboard shows no data  
**Debug Steps**:
```bash
# Verify WAF metrics are being published
aws cloudwatch list-metrics \
  --namespace AWS/WAFV2 \
  --dimensions Name=WebACL,Value=DevOpsLab-WAF

# Check metric data availability
aws cloudwatch get-metric-statistics \
  --namespace AWS/WAFV2 \
  --metric-name AllowedRequests \
  --dimensions Name=WebACL,Value=DevOpsLab-WAF \
  --start-time $(date -d '1 hour ago' --iso-8601) \
  --end-time $(date --iso-8601) \
  --period 300 \
  --statistics Sum
```

---

## Lab Cleanup (IMPORTANT)

### Remove Resources to Avoid Charges
```bash
# Disassociate WAF from CloudFront
aws wafv2 disassociate-web-acl \
  --resource-arn $(cat distribution-arn.txt) \
  --region us-east-1

# Delete Web ACL
aws wafv2 delete-web-acl \
  --scope CLOUDFRONT \
  --id <web-acl-id> \
  --lock-token <lock-token> \
  --region us-east-1

# Delete IP sets
aws wafv2 delete-ip-set \
  --scope CLOUDFRONT \
  --id <ip-set-id> \
  --lock-token <lock-token> \
  --region us-east-1

# Delete S3 bucket (after emptying)
aws s3 rm s3://your-waf-logs-bucket --recursive
aws s3 rb s3://your-waf-logs-bucket

# Delete CloudWatch dashboard
aws cloudwatch delete-dashboards \
  --dashboard-names "DevOpsLab-WAF-Dashboard"

# Delete CloudWatch alarms
aws cloudwatch delete-alarms \
  --alarm-names "WAF-HighBlockedRequests"
```

---

## Lab Report Template

### Summary
- **Duration**: [Actual time spent]
- **Completion**: [Percentage completed]
- **Challenges**: [Major issues encountered]

### Technical Achievements
- [ ] Successfully deployed WAF with managed rules
- [ ] Created and tested custom rules
- [ ] Configured comprehensive monitoring
- [ ] Demonstrated attack mitigation
- [ ] Handled false positive scenarios

### Learning Outcomes
- **New Skills Acquired**: [List key competencies gained]
- **Concepts Clarified**: [What clicked during hands-on practice]
- **Areas for Improvement**: [Topics needing more study]

### Next Steps
- **Immediate Application**: How to apply this in real project
- **Advanced Topics**: What to learn next
- **Integration Planning**: How to incorporate into CI/CD pipeline

**Lab Completion Date**: [Date]  
**Ready for Production**: [Yes/No with rationale]