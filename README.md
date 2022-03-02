```
    $ docker network create cloud-resume
    $ docker run --network cloud-resume --name dynamodb -d -p 8000:8000 amazon/dynamodb-local
    $ aws dynamodb create-table --table-name visitorTable --attribute-definitions AttributeName=siteUrl,AttributeType=S --key-schema AttributeName=siteUrl,KeyType=HASH --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 --endpoint-url http://localhost:8000
```
Build SAM application

```
    $ sam build --use-container
```

Invoke cloud resume function 
```
    $ sam local invoke CloudResumeFunction --parameter-overrides ParameterKey=Environment,  ParameterValue=local ParameterKey=DDBTableName,  ParameterValue=visitorTable --docker-network cloud-resume
```