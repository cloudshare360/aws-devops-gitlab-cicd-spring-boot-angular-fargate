---
layout: default
title: 11.1 Spring Boot Containerization
parent: 1. Foundations
grand_parent: Learning Path
nav_order: 1
permalink: /learning-path/foundations/spring-boot-containerization/
---

# 11.1 Spring Boot Containerization

## 📋 Module Overview

**Duration**: 3-4 hours  
**Difficulty**: Beginner  
**Prerequisites**: Basic Spring Boot knowledge

### What You'll Learn
- How to create optimized Docker images for Spring Boot
- Multi-stage build techniques
- Container best practices
- Local testing strategies

---

## 🎯 Learning Objectives

By the end of this module, you will be able to:
1. Create Dockerfiles for Spring Boot applications
2. Implement multi-stage builds for optimization
3. Configure Spring Boot for containerized environments
4. Test containers locally before deployment

---

## 📖 Content

### 1. Why Containerization?

Containerization provides:
- **Consistency**: Same environment everywhere
- **Portability**: Run anywhere Docker runs  
**Scalability**: Easy horizontal scaling
- **Isolation**: Dependencies don't conflict

### 2. Basic Dockerfile for Spring Boot

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 3. Multi-Stage Build

```dockerfile
# Build stage
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
RUN mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /build/target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

### 4. Optimization Techniques

#### Layer Caching
- Order Dockerfile commands from least to most frequently changing
- Place dependency installation before source code copying

#### Image Size Reduction
- Use alpine base images
- Remove unnecessary dependencies
- Use `.dockerignore` file

#### Security Best Practices
- Run as non-root user
- Scan images for vulnerabilities
- Use specific version tags

---

## 🔨 Hands-On Exercise

### Exercise 1: Basic Containerization

1. Create a simple Spring Boot application
2. Write a Dockerfile
3. Build the image: `docker build -t my-app .`
4. Run the container: `docker run -p 8080:8080 my-app`
5. Test at `http://localhost:8080`

### Exercise 2: Multi-Stage Build

1. Modify Dockerfile to use multi-stage build
2. Compare image sizes
3. Measure build time differences

---

## ✅ Knowledge Check

Answer these questions to verify your understanding:

1. What are the benefits of multi-stage builds?
2. Why use alpine images?
3. How do you optimize Docker layer caching?
4. What security considerations exist for container images?

---

## 📚 Additional Resources

- [Spring Boot Docker Guide](https://spring.io/guides/gs/spring-boot-docker/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)

---

## 🎯 Next Steps

Once you've completed this module:

1. ✅ Mark this module complete in your [Progress Dashboard](/project-tracking/dashboard)
2. 📝 Complete the hands-on lab: [Week 1 Foundation Setup](/hands-on-labs/week-01-foundation)
3. ➡️ Continue to [11.2 DevOps Principles](../devops-principles)

---

**Questions or stuck?** Check the [Troubleshooting Guide](/resources/troubleshooting) or ask in discussions.
