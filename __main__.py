# __main__.py

import pulumi
import pulumi_aws as aws

regions = ["us-east-1", "us-west-2"]
# regions = ["us-east-1", "us-west-2", "us-west-1"]
region_to_arn = {}
# buckets = []

for region in regions:
    provider = aws.Provider(f"provider-{region}", region=region)

    bucket = aws.s3.Bucket(f"bucket-{region}",
        tags={"Region": region},
        opts=pulumi.ResourceOptions(provider=provider)
    )

    aws.s3.BucketVersioning(f"versioning-{region}",
        bucket=bucket.id,
        versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
            status="Enabled"
        ),
        opts=pulumi.ResourceOptions(provider=provider)
    )

    aws.s3.BucketLifecycleConfiguration(f"lifecycle-{region}",
        bucket=bucket.id,
        rules=[aws.s3.BucketLifecycleConfigurationRuleArgs(
            id="glacier-transition-rule",
            status="Enabled",
            transitions=[aws.s3.BucketLifecycleConfigurationRuleTransitionArgs(
                days=90,
                storage_class="GLACIER",
            )],
        )],
        opts=pulumi.ResourceOptions(provider=provider)
    )

    region_to_arn[region] = bucket.arn

pulumi.export("region_to_arn", region_to_arn)

# pulumi.export("bucket_names", [b.id for b in buckets])
# pulumi.export("bucket_arns", [b.arn for b in buckets])