# versioned_private_service
This example shows how to deploy multiple versions of a private service and attach a Route53 domain to that private service that is only accessible within a VPC. It uses the mono-repo framework, that is, multiple folders are used with their own specifications.

To use:

1. Either create a VPC or use the default one, and add a interface VPC endpoint for API Gateway to your VPC (https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-private-apis.html#apigateway-private-api-create-interface-vpc-endpoint). Copy the VPC ID for use in step 5
2. If you don't have this already, create a private Route53 hosted zone that points to the VPC from step 1. Copy its hosted zone ID for use in step 5
3. Copy the subnet IDs and security group IDs that you wish to place the private service in for use in step 5
4. Create three projects in CloudKommand, lets call them Router, APIV1, and APIV2. Place them all in the same area for easy access.
5. Add the router folder of this example to the Router project. Then, override the load_balancer component with your desired subnet IDs and security group IDs, override the target_group's VPC ID with yours, the apigw_domain's name, and the domain's domain and Route53 Hosted Zone ID
6. Deploy the router project
7. After it is deployed add the api folder of this repo to the APIV1 project, and set the SHA to be
