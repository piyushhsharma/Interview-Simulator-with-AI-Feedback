# Deployment Guide

## GitHub Actions CI/CD

This project uses GitHub Actions to automatically build and deploy Docker images to Amazon ECR (Elastic Container Registry).

### Required GitHub Secrets

Configure the following secrets in your GitHub repository settings:

1. **AWS_ACCESS_KEY_ID**
   - AWS IAM user access key ID
   - Must have ECR permissions

2. **AWS_SECRET_ACCESS_KEY**
   - AWS IAM user secret access key
   - Must have ECR permissions

3. **AWS_REGION**
   - AWS region where ECR is hosted
   - Example: `us-east-1`

4. **AWS_ACCOUNT_ID**
   - Your AWS account ID (12-digit number)
   - Example: `123456789012`

### AWS IAM Policy Requirements

The IAM user needs the following permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:InitiateLayerUpload",
                "ecr:UploadLayerPart",
                "ecr:CompleteLayerUpload",
                "ecr:PutImage",
                "ecr:CreateRepository",
                "ecr:DescribeRepositories"
            ],
            "Resource": "*"
        }
    ]
}
```

### Workflow Triggers

The workflow triggers on:
- Push to `main` or `master` branch
- Pull requests to `main` or `master` branch

### Built Images

The workflow builds and pushes two images:

1. **Backend**: `${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-backend`
2. **Frontend**: `${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-frontend`

Both images are tagged with:
- `latest` (for latest deployment)
- `{commit-sha}` (for versioning)

### Manual Deployment

To deploy the images:

#### Backend
```bash
# Pull the image
docker pull ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-backend:latest

# Run the container
docker run -d \
  --name interview-backend \
  -p 8000:8000 \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-backend:latest
```

#### Frontend
```bash
# Pull the image
docker pull ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-frontend:latest

# Run the container
docker run -d \
  --name interview-frontend \
  -p 3000:80 \
  ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-frontend:latest
```

### Docker Compose (Optional)

Create a `docker-compose.yml` for local development:

```yaml
version: '3.8'

services:
  backend:
    image: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-backend:latest
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/interview-simulator-frontend:latest
    ports:
      - "3000:80"
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Troubleshooting

#### ECR Login Issues
- Verify AWS credentials are correct
- Check IAM permissions
- Ensure AWS region is correct

#### Build Failures
- Check Dockerfile syntax
- Verify all dependencies are included
- Check for syntax errors in code

#### Push Failures
- Verify ECR repository exists
- Check image tag format
- Ensure proper authentication

### Security Considerations

- Images are scanned for vulnerabilities on push
- Non-root users are used in containers
- Health checks are configured
- Security headers are included in nginx configuration

### Monitoring

- Container health checks are configured
- Logs are captured in CloudWatch (if using AWS)
- Image scanning is enabled in ECR
