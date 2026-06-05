# components.py

import pulumi
import pulumi_aws as aws

class RegionalBucket(pulumi.ComponentResource):
    def __init__(self, name: str, region: str, lifecycle_days: int = 90, bucket_name_prefix: str = "", opts=None):
        super().__init__("lab:index:RegionalBucket", name, {}, opts)

        child_opts = pulumi.ResourceOptions(parent=self)

        provider = aws.Provider(f"{name}-provider",
            region=region,
            opts=child_opts
        )

        resource_opts = pulumi.ResourceOptions(parent=self, provider=provider)

        bucket_name = f"{bucket_name_prefix}{name}-bucket"

        self.bucket = aws.s3.Bucket(bucket_name,
            tags={"Region": region},
            opts=resource_opts
        )

        aws.s3.BucketVersioning(f"{name}-versioning",
            bucket=self.bucket.id,
            versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
                status="Enabled"
            ),
            opts=resource_opts
        )

        aws.s3.BucketLifecycleConfiguration(f"{name}-lifecycle",
            bucket=self.bucket.id,
            rules=[aws.s3.BucketLifecycleConfigurationRuleArgs(
                id="glacier-transition",
                status="Enabled",
                transitions=[aws.s3.BucketLifecycleConfigurationRuleTransitionArgs(
                    days=lifecycle_days,
                    storage_class="GLACIER"
                )]
            )],
            opts=resource_opts
        )

        self.register_outputs({
            "bucket_id": self.bucket.id,
            "bucket_arn": self.bucket.arn
        })