<br />
<div align="center">
  <h3 align="center">Cloud Resume Backend</h3>
  <p align="center">
  Backend source code for the cloud resume challenge.
    <br />
    <a href="https://cloudresumechallenge.dev/docs/the-challenge/aws/"><strong>See the challenge »</strong></a>
    <br />
    <br />
    <a href="https://resume.kudzaim.codes">View Demo</a>
    |
    <a href="#">Read Blog</a>
  </p>
</div>

### Built With

* Python3
* AWS Lambda
* AWS ApiGateway
* AWS DynamoDB
* Docker

<!-- GETTING STARTED -->
## Getting Started Local Development

This is an optional step to test the AWS Serverless services locally before deploying to AWS saving costs and improving code quality.

### Prerequisites
* Docker
* aws-cli
* aws sam

### Setup & Usage

1. Create the docker network
   ```sh
   docker network create cloud-resume
   ```
3. Deploy DynamoDB in docker
   ```sh
   docker run --network cloud-resume --name dynamodb -d -p 8000:8000   amazon/dynamodb-local
   ```
3. Create the dynamoDB table
   ```sh
   aws dynamodb create-table --table-name visitorTable --attribute-definitions AttributeName=siteUrl,AttributeType=S --key-schema AttributeName=siteUrl,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:8000
   ```
4. Build the SAM application
    ```sh
    sam build --use-container
    ```
5. Invoke the function
    ```sh
    sam local invoke CloudResumeFunction --parameter-overrides ParameterKey=Environment,  ParameterValue=local ParameterKey=DDBTableName,  ParameterValue=visitorTable --docker-network cloud-resume
    ```
6. Start the local API
    ```sh
    sam local start-api --parameter-overrides ParameterKey=Environment,ParameterValue=local ParameterKey=DDBTableName,ParameterValue=visitorTable --docker-network cloud-resume
    ```
7. Test with curl
    ```sh
        curl "http://127.0.0.1:3000/counter"
    ```

### SAM Package & Deploy

1. Package the SAM App
    ```sh

    ```

<!-- ROADMAP -->
## Roadmap

- [x] Setup AWS Serverless for local development
- [x] Write lambda function code
- [x] Deploy SAM Application to AWS.
- [X] CI/CD