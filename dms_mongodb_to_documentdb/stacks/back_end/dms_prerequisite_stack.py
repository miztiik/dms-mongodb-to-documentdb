from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_iam as _iam

from custom_resources.ssh_key_generator.ssh_key_generator_stack import SshKeyGeneratorStack


class GlobalArgs:
    """
    Helper to define global statics
    """

    OWNER = "MystiqueAutomation"
    ENVIRONMENT = "production"
    REPO_NAME = "dms-mongodb-to-documentdb"

    SOURCE_INFO = f"https://github.com/miztiik/{REPO_NAME}"
    VERSION = "2020_10_01"
    MIZTIIK_SUPPORT_EMAIL = ["mystique@example.com", ]


class DmsPrerequisiteStack(core.Stack):

    def __init__(
        self,
        scope: core.Construct,
        id: str,
        vpc,
        stack_log_level,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Create DMS VPC Role

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # THIS STACK WILL FAIL, IF ROLE WITH SIMILAR NAME EXISTS #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        dms_vpc_role = _iam.Role(
            self,
            "dmsVpcRole",
            assumed_by=_iam.ServicePrincipal("dms.amazonaws.com"),
            description="Miztiik Automation: DMS VPC Role",
            role_name="dms-vpc-role"
        )

        # https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Security.html
        # aws iam get-policy --policy-arn arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole

        dms_vpc_role.add_managed_policy(
            # _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDMSVPCManagementRole")
            _iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "dmsRolePolicyArn",
                managed_policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole"
            )
        )

        # Create DMS VPC Role
        dms_cloudwatch_logs_role = _iam.Role(
            self,
            "dmsCloudwatchRole",
            assumed_by=_iam.ServicePrincipal("dms.amazonaws.com"),
            description="Miztiik Automation: DMS VPC Role",
            role_name="dms-cloudwatch-logs-role"
        )

        dms_cloudwatch_logs_role.add_managed_policy(
            _iam.ManagedPolicy.from_managed_policy_arn(
                self,
                "dmsCloudWatchRolePolicyArn",
                managed_policy_arn="arn:aws:iam::aws:policy/service-role/AmazonDMSCloudWatchLogsRole"
            )
        )

        # Retrieve Cognito App Client Secret and Add to Secrets Manager
        ssh_key_generator = SshKeyGeneratorStack(
            self,
            "ssh-key-generator",
            ssh_key_name="mystique-automation-ssh-key"
        )

        # Export Value
        self.ssh_key_gen_status = ssh_key_generator.response

        # Create Security Group for DMS Replication Instance
        dms_sg = _ec2.SecurityGroup(
            self,
            id="dmsSecurityGroup",
            vpc=vpc,
            security_group_name=f"dms_sg_{id}",
            description="Security Group for DMS replication instance to interact with source and target databases"
        )

        dms_sg.add_ingress_rule(
            peer=_ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=_ec2.Port.tcp(27017),
            description="Allow MongoDB inbound connetions"
        )

        # Create Security Group for DocsDB Replication Instance
        docsdb_sg = _ec2.SecurityGroup(
            self,
            id="docsDbSecurityGroup",
            vpc=vpc,
            security_group_name=f"docsdb_sg_{id}",
            description="Security Group for DocsDB"
        )

        docsdb_sg.add_ingress_rule(
            peer=_ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection=_ec2.Port.tcp(27017),
            description="Allow DocsDB inbound connetions"
        )

        # Outputs
        output_0 = core.CfnOutput(
            self,
            "AutomationFrom",
            value=f"{GlobalArgs.SOURCE_INFO}",
            description="To know more about this automation stack, check out our github page."
        )
        output_1 = core.CfnOutput(
            self,
            "SshKeyGenerationStatus",
            value=f"{self.ssh_key_gen_status}",
            description="Ssh Key Generation Status. Check SSM Parameter 'mystique-automation-ssh-key' for key material(private key)"
        )