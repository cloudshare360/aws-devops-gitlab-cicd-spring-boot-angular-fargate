# Spring Boot Containerization Guide

## Prerequisites ✅
- **Required**: Basic Spring Boot knowledge (REST APIs, Maven/Gradle)
- **Required**: Java development experience
- **Helpful**: Docker basics (can learn alongside)
- **Helpful**: AWS CLI experience

## Module Overview
Learn to containerize Spring Boot microservices for deployment to AWS Fargate. This module focuses on creating production-ready Docker containers optimized for Spring Boot applications.

**Time Investment**: 6-8 hours over 2 days  
**Practical Outcome**: Production-ready Spring Boot containers

---

## Learning Objectives

By the end of this module, you will:
- [ ] Create optimized Dockerfiles for Spring Boot applications
- [ ] Implement multi-stage builds for efficient container images
- [ ] Configure Spring Boot for containerized environments
- [ ] Deploy Spring Boot containers to local Docker environment
- [ ] Understand Spring Boot-specific container optimization techniques

---

## Spring Boot Container Fundamentals

### Key Considerations for Spring Boot Containers
- **JAR vs WAR**: Most Spring Boot apps use embedded Tomcat (JAR)
- **Java Base Images**: Choose appropriate JDK/JRE versions
- **Layer Optimization**: Separate dependencies from application code
- **Configuration**: Externalize configuration for different environments
- **Health Checks**: Implement proper health endpoints

### Container Architecture
```
Base Image (Eclipse Temurin JRE)
├── Dependencies Layer (JAR dependencies)
├── Application Layer (Spring Boot JAR)
├── Configuration Layer (application.yml, etc.)
└── Runtime Configuration (JVM options, profiles)
```

---

## Hands-On Implementation

### Step 1: Basic Spring Boot Dockerfile

#### Standard Dockerfile for Spring Boot
```dockerfile
# Multi-stage build for Spring Boot
FROM maven:3.8.6-openjdk-17 AS build
WORKDIR /app

# Copy dependency files first (for layer caching)
COPY pom.xml .
COPY src ./src

# Build the application
RUN mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:17-jre-alpine
WORKDIR /app

# Create non-root user for security
RUN addgroup -g 1001 -S appuser && adduser -u 1001 -S appuser -G appuser
USER appuser

# Copy the built JAR from build stage
COPY --from=build /app/target/*.jar app.jar

# Configure JVM for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8080/actuator/health || exit 1

# Expose port
EXPOSE 8080

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### Step 2: Optimized Multi-Service Dockerfile

#### For Microservices Architecture
```dockerfile
# Advanced multi-stage build
FROM maven:3.8.6-openjdk-17 AS dependencies
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B

FROM dependencies AS build
COPY src ./src
RUN mvn clean package -DskipTests -o

# Final runtime image
FROM eclipse-temurin:17-jre-alpine AS runtime
WORKDIR /app

# Install necessary packages
RUN apk add --no-cache curl

# Security: non-root user
RUN addgroup -g 1001 -S spring && adduser -u 1001 -S spring -G spring
USER spring

# Copy application
COPY --from=build --chown=spring:spring /app/target/*.jar app.jar

# JVM optimization for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
               -XX:MaxRAMPercentage=75.0 \
               -XX:+UseG1GC \
               -XX:+UnlockExperimentalVMOptions \
               -XX:+UseCGroupMemoryLimitForHeap"

# Spring Boot configuration
ENV SPRING_PROFILES_ACTIVE=docker
ENV SERVER_PORT=8080

EXPOSE ${SERVER_PORT}

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${SERVER_PORT}/actuator/health/readiness || exit 1

ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar app.jar"]
```

### Step 3: Spring Boot Configuration for Containers

#### application-docker.yml
```yaml
spring:
  profiles:
    active: docker
  
  # Database configuration for RDS
  datasource:
    url: ${DATABASE_URL:jdbc:oracle:thin:@//localhost:1521/xe}
    username: ${DATABASE_USERNAME:spring}
    password: ${DATABASE_PASSWORD:password}
    driver-class-name: oracle.jdbc.OracleDriver
    
  # JPA configuration
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.Oracle12cDialect

# Server configuration
server:
  port: ${SERVER_PORT:8080}
  shutdown: graceful
  
# Management endpoints for monitoring
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always
      probes:
        enabled: true
  health:
    readiness-state:
      enabled: true
    liveness-state:
      enabled: true

# Logging configuration
logging:
  level:
    com.yourcompany: INFO
    org.springframework.security: DEBUG
  pattern:
    console: "%d{ISO8601} [%thread] %-5level %logger{36} - %msg%n"
```

### Step 4: Build and Test Locally

#### Build Commands
```bash
# Build the Spring Boot container
docker build -t spring-boot-microservice:latest .

# Run with environment variables
docker run -d \
  --name spring-boot-app \
  -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=docker \
  -e DATABASE_URL=jdbc:oracle:thin:@//host.docker.internal:1521/xe \
  -e DATABASE_USERNAME=your_username \
  -e DATABASE_PASSWORD=your_password \
  spring-boot-microservice:latest

# Check health
curl http://localhost:8080/actuator/health

# View logs
docker logs spring-boot-app

# Test the application
curl http://localhost:8080/api/your-endpoint
```

### Step 5: Docker Compose for Development

#### docker-compose.yml
```yaml
version: '3.8'
services:
  spring-boot-app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - DATABASE_URL=jdbc:oracle:thin:@//oracle-db:1521/xe
      - DATABASE_USERNAME=spring
      - DATABASE_PASSWORD=password
    depends_on:
      - oracle-db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  oracle-db:
    image: container-registry.oracle.com/database/express:latest
    environment:
      - ORACLE_PWD=password
    ports:
      - "1521:1521"
    volumes:
      - oracle_data:/opt/oracle/oradata

volumes:
  oracle_data:
```

---

## Container Optimization Techniques

### Image Size Optimization
```dockerfile
# Use specific base image versions
FROM eclipse-temurin:17-jre-alpine AS runtime

# Multi-stage build to exclude build tools
FROM maven:3.8.6-openjdk-17 AS build
# ... build stage ...

FROM runtime
# Only copy necessary artifacts
COPY --from=build /app/target/*.jar app.jar
```

### Security Best Practices
```dockerfile
# Run as non-root user
RUN addgroup -g 1001 -S spring && adduser -u 1001 -S spring -G spring
USER spring

# Update base image packages
RUN apk upgrade --no-cache

# Use specific image tags, not 'latest'
FROM eclipse-temurin:17-jre-alpine@sha256:specific-hash
```

### Performance Optimization
```dockerfile
# JVM tuning for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
               -XX:MaxRAMPercentage=75.0 \
               -XX:+UseG1GC \
               -Djava.security.egd=file:/dev/./urandom"
```

---

## Integration with AWS Fargate

### Task Definition Considerations
```json
{
  "family": "spring-boot-microservice",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "spring-boot-app",
      "image": "your-ecr-repo/spring-boot-microservice:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SPRING_PROFILES_ACTIVE",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_PASSWORD",
          "valueFrom": "arn:aws:secretsmanager:region:account:secret:db-password"
        }
      ],
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8080/actuator/health/readiness || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      },
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/spring-boot-microservice",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

---

## Testing and Validation

### Container Testing Checklist
- [ ] Application starts successfully in container
- [ ] Health checks respond correctly
- [ ] Database connectivity works
- [ ] Environment variables are properly configured
- [ ] Logs are accessible and properly formatted
- [ ] Performance is acceptable (startup time, memory usage)
- [ ] Security scanning passes

### Common Issues and Solutions

#### Issue 1: Slow Startup Times
**Solution**: Optimize Spring Boot configuration
```yaml
spring:
  jpa:
    hibernate:
      ddl-auto: none  # Don't validate schema on startup
  main:
    lazy-initialization: true  # Enable lazy initialization
```

#### Issue 2: High Memory Usage
**Solution**: JVM tuning
```dockerfile
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75.0 -XX:+UseG1GC -XX:+UseStringDeduplication"
```

#### Issue 3: Database Connection Issues
**Solution**: Connection pool configuration
```yaml
spring:
  datasource:
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 20000
      idle-timeout: 300000
```

---

## Next Steps

### Prepare for Next Module
**Next**: GitLab CI/CD Pipeline Setup (`gitlab-cicd-spring-boot-microservices.md`)  
**Prerequisites**: Container knowledge ✅, Spring Boot containerization ✅

### Production Considerations
1. **Security scanning**: Integrate container security scans
2. **Registry setup**: Push to AWS ECR
3. **Monitoring**: Add application metrics
4. **Scaling**: Configure auto-scaling policies

**Time to Complete**: 2 days with hands-on practice  
**Next Review**: After successfully running Spring Boot container locally