
# Github Actions
엔드포인트를 통해 호출할 수 있는 파이썬 api를 만들어보자
```shell
 mkdir cdk-action && cd cdk-action
cdk init app --language typescript
```

vi cdk-action/lib/cdk-action-stack.ts
```typescript
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';

export class CdkActionStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const lambdaFunction = new lambda.Function(this, 'LambdaFunction', {
      runtime: lambda.Runtime.PYTHON_3_12,
      code: lambda.Code.fromAsset('lambda'),
      handler: 'main.handler'
    });

    const functionUrl = lambdaFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedOrigins: ['*'],
        allowedMethods: [lambda.HttpMethod.ALL],
        allowedHeaders: ['*']
      }
    });

    new cdk.CfnOutput(this, 'Url', {
      value: functionUrl.url
    });
  }
}
```

```shell
mkdir lambda && cd lambda
touch main.py

# main.py
def handler(event, context):
    return {
        "statusCode": 200,
        "body": "Hello World"
    }
```

```shell
cd .. 
cdk deploy
...
CdkActionStack.Url = https://2hjb7n3mbgopfw6377alzhdokm0dqfoy.lambda-url.ap-northeast-2.on.aws/
```

```shell
mkdir -p .github/workflows
touch .github/workflows/deploy_beta.yml
```

```yaml
name: Deploy to AWS (CDK)

on:
  push:
    branches:
      - feature

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: 18

      - name: Install AWS CDK
        run: npm ci

      - name: Deploy CDK
        working-directory: ./
        run: npx cdk deploy --require-approval never
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.BETA_AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.BETA_AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: ${{ secrets.BETA_AWS_REGION }}
```

github secrets 설정 \
https://github.com/codelab-kr/aws-cdk-action/settings/secrets/actions - new repository secret

```shell
BETA_AWS_ACCESS_KEY_ID
BETA_AWS_SECRET_ACCESS_KEY
BETA_AWS_REGION
```

```shell
git add .
git commit -m "Add github actions"
git push origin feature
```

# Auto Increment Version
```shell
cd cdk-action/.git/hooks && cp pre-commit.sample pre-commit
```

```shell
vi pre-commit
#!/bin/bash
# .env 파일에서 VERSION 값을 읽어옵니다.
VERSION=$(sed -n 's/VERSION="\([^"]*\)"/\1/p' .env)

if [[ -n "$VERSION" ]]; then
	# 버전을 증가시킵니다.
	IFS='.' read -ra ADDR <<< "$VERSION"
	last_index=$(( ${#ADDR[@]}-1 ))
	ADDR[last_index]=$((${ADDR[last_index]} + 1))
	NEW_VERSION=$(IFS=.; echo "${ADDR[*]}")

	# .env 파일에서 이전 버전을 새 버전으로 교체합니다.
	perl -pi -e "s/$VERSION/$NEW_VERSION/g" .env
	echo "New version: $NEW_VERSION"

	# 변경된 .env 파일을 git에 추가합니다.
	git add .env
fi
```

```shell
git add .
git commit -m "Add auto increment version"
New version: 1.1
[feature a65ebe9] add version
 7 files changed, 66 insertions(+), 7 deletions(-)
 create mode 100644 .env
 create mode 100755 pre-commit
```
<br>




# Reference
- Youtube @pixegami
https://youtu.be/9uMcN66mfwE?si=IKGoJFjPRCcLLbzj
---





# Welcome to your CDK TypeScript project

This is a blank project for CDK development with TypeScript.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

## Useful commands

* `npm run build`   compile typescript to js
* `npm run watch`   watch for changes and compile
* `npm run test`    perform the jest unit tests
* `npx cdk deploy`  deploy this stack to your default AWS account/region
* `npx cdk diff`    compare deployed stack with current state
* `npx cdk synth`   emits the synthesized CloudFormation template
