## Alexa Skills for Satori Open Data Channels

Included in this repository is everything you need to build an Amazon Echo Skill to interact with streaming data from [Satori Data Channels](https://www.satori.com/channels/).  This tutorial is built using [AWS Lambda](http://aws.amazon.com/lambda) so that final product will have the benefits of high availability, automatic scaling, and zero server administration.

While this example specifically showcases the [Streaming Ether](https://www.satori.com/channels/complete-ethereum-market-data) feed built by [EthVentures](https://ethventures.io), connecting it to different channels should be fairly straightforward.

### Click Below for Video Demo
<p align="center">
<a href="https://goo.gl/Xyqdpu" target="blank">
<img src="http://img.youtube.com/vi/cvMe_i8qPh0/0.jpg"
 width=480 height=360 border=5></a>
</p>

### Setup
To run this example skill you need to do two things. The first is to deploy the example code in lambda, and the second is to configure the Alexa skill to use function we create.


### AWS Lambda
1. Navigate to the [AWS Console](https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions) and select Lambda from services menu. link.
2. Click on the Create a Lambda Function. We will not be using a blueprint and should select blank function on the following screen.
3. After you select blank function, you then need to add a trigger. Select Alexa Skills Kit and press next. (Note: ensure you are in us-east or you won't be able to use Alexa as a trigger for your Lambda Function.)
4. Name the Lambda Function "AlexaSatori".
5. Select the runtime as Python 2.7
6. Zip up lambda_function.py as well as the sitepackages in requirements.txt to upload on this page. (Dont forget to add your appkey to lambda_function.py!)
7. Select Code Entry type as "Upload a .ZIP file" and then select the zip file we just created.
8. Keep the Handler as lambda_function.lambda_handler (this refers to the main python file in the zip).
9. Under role, select create a basic execution role for lambda and click create.
10. Leave the Advanced settings as the defaults.
11. Click "Next" and review the settings then click "Create Function"
12. Click the "Event Sources" tab and select "Add event source"
13. Set the Event Source type as Alexa Skills kit and Enable it now. Click Submit.
14. Copy the ARN from the top right to be used later in the Alexa Skill Setup

### Alexa Skill Setup
1. Now we need to navigate to the [Amazon Developer Console](https://developer.amazon.com/edw/home.html) to configure the Alexa Skills Kit. Click getting started under ASK and then add a new skill.
2. Set "Streaming Ether" for the skill name and "Streaming Ether" as the invocation name, this is what is used to activate your skill. For example you would say: "Alexa, Start Streaming Ether"
3. Copy the Intent Schema from the included IntentSchema.json.
4. Copy the Sample Utterances from the included SampleUtterances.txt. Click Next.
5. Select the Lambda ARN for the skill Endpoint and paste the ARN copied from above. Click Next.
6. You are now able to start testing your Streaming Ether skill! You should be able to go to the [Echo webpage](http://echo.amazon.com/#skills) and see your skill enabled.
7. In order to test it, try to say some of the Sample Utterances from the Examples section below.
8. Your skill is now saved and once you are finished testing you can continue to publish your skill.

## Examples
Example user interactions:

### One-shot model:
  User:  "Alexa, ask Streaming Ether for latest price.""

### Sample Questions/Requests for Streaming Ether:
- What is the price of Ether?
- What exchanges are supported?

### Support
Find us on [Twitter](https://twitter.com/ethventuresio)
