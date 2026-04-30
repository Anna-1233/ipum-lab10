# __main__.py

import pulumi
from components import RegionalBucket


regions = [
    ("us-east-1", 30),
    ("us-west-2", 60),
]

# regions = ["us-east-1", "us-west-2"]
buckets = [RegionalBucket(
    name=r_name,
    region=r_name,
    bucket_name_prefix="pulumi-lab",
    lifecycle_days=days
) for r_name, days in regions]

pulumi.export("region_to_bucket_arn", {r[0]: b.bucket.arn for r, b in zip(regions, buckets)})

