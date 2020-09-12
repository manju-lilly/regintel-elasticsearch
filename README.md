# Name of your project


## Getting Started

If you haven't already you should create a GitHub repository for this project via [ServiceNow](https://lilly.service-now.com), search for "GitHub Services". You can clone the repository that ServiceNow creates
and copy your project files into that new directory. Once you have copied your files over it is heavily recommended to create an initial commit with the files exactly as they were
created. This provides a point in the git history where you can find what what originally created for you.

In order to deploy your Elasticsearch domain, you will need to create an AWS deployment pipeline.
To create the pipeline, create a new CloudFormation stack using 
[the v2 deployment pipeline template](https://lly-templates.s3.us-east-2.amazonaws.com/shared/cloudformation/deployment_pipelines_v2/cfn-pipeline.yaml).
Once your pipeline has been created you will be able to deploy your template just by pushing code to GitHub.

## Directory Structure

```
.
├── buildspec.yml                     <-- CodeBuild file able to run pre-deployment scripts
├── params.dev.json                   <-- CloudFormation dev environment configuration
├── params.prod.json                  <-- CloudFormation prod environment configuration
├── params.qa.json                    <-- CloudFormation qa environment configuration
├── post-deploy-buildspec.yml         <-- CodeBuild file able to run post-deployment scripts
├── README.MD                         <-- This instructions file
└── template.yml                      <-- CloudFormation template
```
