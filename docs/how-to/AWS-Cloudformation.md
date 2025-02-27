## AWS CloudFormation Template Guide

This guide explains the components of the provided AWS CloudFormation template for creating an ECS Cluster with Fargate, an RDS MySQL database with subnets, and an IAM role.

### Why Use These Components Together:
- **ECS Cluster with Fargate**: 
  - **Simplifies container management**: No need to manage servers or clusters of Amazon EC2 instances.
  - **Scalability**: Automatically scales applications to handle varying traffic loads.
  - **Cost Efficiency**: Pay only for the resources you use.

- **RDS MySQL with Subnets**:
  - **Managed Database**: RDS handles database administration tasks such as backups, patch management, and scaling.
  - **Subnets**: Ensure your database is deployed in a secure and isolated network environment, improving security and compliance.
  - **Reliability**: Automatic backups, multi-AZ deployments, and read replicas for high availability and disaster recovery.

- **IAM Role**:
  - **Fine-Grained Access Control**: Define permissions for accessing AWS services and resources.
  - **Security**: Use roles to grant temporary access, minimizing the need for long-term credentials.
  - **Compliance**: Helps meet security and regulatory requirements by controlling who can access your resources and how.

### How to Use Them Together:
1. **Define an ECS Cluster**:
   - Create an ECS Cluster with Fargate as the launch type to run your containerized applications.

2. **Set Up RDS MySQL**:
   - Create an RDS MySQL instance and place it within specified subnets for network isolation.

3. **Configure IAM Roles**:
   - Create and assign IAM roles to your ECS tasks and services, granting them the necessary permissions to interact with other AWS resources securely.



## AWS CloudFormation Template Guide

This guide explains the components of the provided AWS CloudFormation template for creating an ECS Cluster with Fargate, an RDS MySQL database with subnets, and an IAM role.

![image](https://github.com/user-attachments/assets/86bfbbfd-932e-416e-b49a-e5c55c7fb521)


### Template Structure

The template is structured as follows:
- **AWSTemplateFormatVersion**: Specifies the AWS CloudFormation template version.
- **Description**: A brief description of the template.
- **Parameters**: Defines input parameters for the template.
- **Resources**: Defines the AWS resources to be created.
- **Outputs**: Defines the values to be returned after the stack creation.

### Parameters

#### `DBPassword`
- **Description**: The database admin account password.
- **Type**: String.
- **NoEcho**: true (prevents the password from being displayed in the console).

### Resources

#### `MyVPC`
- **Type**: `AWS::EC2::VPC`
- **Properties**:
  - **CidrBlock**: `10.0.0.0/16`
  - **EnableDnsSupport**: true
  - **EnableDnsHostnames**: true
  - **Tags**:
    - **Key**: `Name`
    - **Value**: `MyVPC`

#### `PublicSubnet`
- **Type**: `AWS::EC2::Subnet`
- **Properties**:
  - **VpcId**: Reference to `MyVPC`.
  - **CidrBlock**: `10.0.1.0/24`
  - **MapPublicIpOnLaunch**: true
  - **AvailabilityZone**: `eu-west-1a`
  - **Tags**:
    - **Key**: `Name`
    - **Value**: `PublicSubnet`

#### `PrivateSubnet1`
- **Type**: `AWS::EC2::Subnet`
- **Properties**:
  - **VpcId**: Reference to `MyVPC`.
  - **CidrBlock**: `10.0.2.0/24`
  - **AvailabilityZone**: `eu-west-1a`
  - **Tags**:
    - **Key**: `Name`
    - **Value**: `PrivateSubnet1`

#### `PrivateSubnet2`
- **Type**: `AWS::EC2::Subnet`
- **Properties**:
  - **VpcId**: Reference to `MyVPC`.
  - **CidrBlock**: `10.0.3.0/24`
  - **AvailabilityZone**: `eu-west-1b`
  - **Tags**:
    - **Key**: `Name`
    - **Value**: `PrivateSubnet2`

#### `MyCluster`
- **Type**: `AWS::ECS::Cluster`
- **Properties**:
  - **ClusterName**: `MyECSCluster`

#### `MyECRRepository`
- **Type**: `AWS::ECR::Repository`
- **Properties**:
  - **RepositoryName**: `my-repo`

#### `MyDBSubnetGroup`
- **Type**: `AWS::RDS::DBSubnetGroup`
- **Properties**:
  - **DBSubnetGroupDescription**: `My DB subnet group`
  - **SubnetIds**:
    - Reference to `PrivateSubnet1`
    - Reference to `PrivateSubnet2`

#### `MyRDSInstance`
- **Type**: `AWS::RDS::DBInstance`
- **Properties**:
  - **DBInstanceIdentifier**: `my-rds-instance`
  - **AllocatedStorage**: `20`
  - **DBInstanceClass**: `db.t3.micro`
  - **Engine**: `MySQL`
  - **MasterUsername**: `admin`
  - **MasterUserPassword**: Reference to `DBPassword`
  - **DBSubnetGroupName**: Reference to `MyDBSubnetGroup`
  - **VPCSecurityGroups**:
    - `MyDBSecurityGroup` GroupId

#### `MyDBSecurityGroup`
- **Type**: `AWS::EC2::SecurityGroup`
- **Properties**:
  - **GroupDescription**: `RDS security group`
  - **VpcId**: Reference to `MyVPC`
  - **SecurityGroupIngress**:
    - **IpProtocol**: `tcp`
    - **FromPort**: `3306`
    - **ToPort**: `3306`
    - **CidrIp**: `0.0.0.0/0`

#### `MyTaskExecutionRole`
- **Type**: `AWS::IAM::Role`
- **Properties**:
  - **AssumeRolePolicyDocument**:
    - **Version**: `2012-10-17`
    - **Statement**:
      - **Effect**: `Allow`
      - **Principal**:
        - **Service**: `ecs-tasks.amazonaws.com`
      - **Action**: `sts:AssumeRole`
  - **Policies**:
    - **PolicyName**: `ECRAccessPolicy`
    - **PolicyDocument**:
      - **Version**: `2012-10-17`
      - **Statement**:
        - **Effect**: `Allow`
        - **Action**:
          - `ecr:GetDownloadUrlForLayer`
          - `ecr:BatchGetImage`
          - `ecr:BatchCheckLayerAvailability`
          - `ecr:PutImage`
          - `ecr:InitiateLayerUpload`
          - `ecr:UploadLayerPart`
          - `ecr:CompleteLayerUpload`
          - `ecr:ListImages`
          - `ecr:GetAuthorizationToken`
        - **Resource**: `*`

### Outputs

#### `VPCId`
- **Value**: Reference to `MyVPC`

#### `PublicSubnetId`
- **Value**: Reference to `PublicSubnet`

#### `PrivateSubnet1Id`
- **Value**: Reference to `PrivateSubnet1`

#### `PrivateSubnet2Id`
- **Value**: Reference to `PrivateSubnet2`

#### `ECSClusterName`
- **Value**: Reference to `MyCluster`

#### `ECRRepositoryURI`
- **Value**: Substitution for ECR repository URI with account ID and region.

#### `TaskExecutionRoleArn`
- **Value**: Get attribute `Arn` from `MyTaskExecutionRole`

