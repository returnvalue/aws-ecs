import boto3

def main():
    autoscaling = boto3.client('application-autoscaling', endpoint_url="http://localhost:4566", region_name="us-east-1")

    # 1. Register the ECS Service as a Scalable Target
    autoscaling.register_scalable_target(
        ServiceNamespace='ecs',
        ResourceId='service/FargateCluster/WebAppService',
        ScalableDimension='ecs:service:DesiredCount',
        MinCapacity=2,
        MaxCapacity=10
    )
    print("Registered scalable target.")

    # 2 & 3. Apply the Scaling Policy
    policy_response = autoscaling.put_scaling_policy(
        ServiceNamespace='ecs',
        ResourceId='service/FargateCluster/WebAppService',
        ScalableDimension='ecs:service:DesiredCount',
        PolicyName='ECSTargetTrackingCPU',
        PolicyType='TargetTrackingScaling',
        TargetTrackingScalingPolicyConfiguration={
            'TargetValue': 70.0,
            'PredefinedMetricSpecification': {
                'PredefinedMetricType': 'ECSServiceAverageCPUUtilization'
            },
            'ScaleOutCooldown': 60,
            'ScaleInCooldown': 60
        }
    )
    print(f"Applied scaling policy: {policy_response['PolicyARN']}")

if __name__ == '__main__':
    main()
