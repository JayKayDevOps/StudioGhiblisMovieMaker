# ECS Task Definition and Service

This guide explains how to set up an ECS Task Definition and Service using a CloudFormation YAML template.

## Introduction

An ECS Task Definition is a blueprint for your application, specifying various parameters including the Docker image, CPU and memory requirements, networking mode, logging configuration, and environment variables.


## Parameters

| Parameter Name           | Description                       | Type    |
|--------------------------|-----------------------------------|---------|
| VPCID                    | VPC ID                            | String  |
| PublicSubnetId           | Public Subnet ID                  | String  |
| PrivateSubnet1Id         | Private Subnet 1 ID               | String  |
| PrivateSubnet2Id         | Private Subnet 2 ID               | String  |
| ECSClusterName           | ECS Cluster Name                  | String  |
| ECRRepositoryURI         | ECR Repository URI                | String  |
| TaskExecutionRoleArn     | Task Execution Role ARN           | String  |
| RDSInstanceEndpoint      | RDS Instance Endpoint             | String  |
| DBPassword               | The database admin account password | String  |

## Resources

### MyLogGroup
A CloudWatch Logs log group for ECS service logs.

```yaml
MyLogGroup:
  Type: 'AWS::Logs::LogGroup'
  Properties:
    LogGroupName: '/ecs/my-service'
    RetentionInDays: 30
```

### Task Definition

The `MyTaskDefinition` resource defines the properties of the ECS task.

```yaml
MyTaskDefinition:
  Type: 'AWS::ECS::TaskDefinition'
  Properties:
    Family: 'my-task-family'
    NetworkMode: 'awsvpc'
    RequiresCompatibilities:
      - 'FARGATE'
    Cpu: '1024'
    Memory: '2048'
    ExecutionRoleArn: !Ref TaskExecutionRoleArn
    ContainerDefinitions:
      - Name: 'my-container'
        Image: !Ref ECRRepositoryURI
        PortMappings:
          - ContainerPort: 80
            Protocol: 'tcp'
        LogConfiguration:
          LogDriver: 'awslogs'
          Options:
            awslogs-group: '/ecs/my-service'
            awslogs-region: !Ref 'AWS::Region'
            awslogs-stream-prefix: 'ecs'
        Environment:
          - Name: 'DB_HOST'
            Value: !Ref RDSInstanceEndpoint
          - Name: 'DB_PORT'
            Value: '3306'
          - Name: 'DB_USER'
            Value: 'admin'
          - Name: 'DB_PASS'
            Value: !Ref DBPassword
          - Name: 'DB_NAME'
            Value: 'mydatabase'
```

### Properties Breakdown

* Type: 'AWS::ECS::TaskDefinition': Specifies that this resource is an ECS Task Definition.

* Family: A name for the task family, used to group related task definitions.

* NetworkMode: 'awsvpc': Specifies the network mode as awsvpc, which is required for Fargate tasks.

* RequiresCompatibilities: Indicates that the task requires the Fargate launch type.

* Cpu: Allocates 1024 CPU units to the task (equivalent to 1 vCPU).

* Memory: Allocates 2048 MiB (2 GiB) of memory to the task.

* ExecutionRoleArn: The ARN of the task execution role that grants permissions for AWS API calls.

* ContainerDefinitions: Defines the configuration for the container(s) within the task.

# How to Define an ECS Service in AWS CloudFormation

An ECS Service is responsible for running and maintaining a specified number of instances of a task definition simultaneously in an ECS cluster. It ensures that the desired number of tasks are running and replaces tasks if they fail.

## YAML Explanation

Here is the detailed breakdown of the provided YAML for the ECS Service:

### Service Definition

The `MyService` resource defines the properties of the ECS Service.

```yaml
MyService:
  Type: 'AWS::ECS::Service'
  DependsOn: MyTaskDefinition
  Properties:
    Cluster: !Ref ECSClusterName
    TaskDefinition: !Ref MyTaskDefinition
    DesiredCount: 2
    LaunchType: 'FARGATE'
    NetworkConfiguration:
      AwsvpcConfiguration:
        Subnets:
          - !Ref PublicSubnetId
        SecurityGroups:
          - !Ref MySecurityGroup
        AssignPublicIp: 'ENABLED'
```
