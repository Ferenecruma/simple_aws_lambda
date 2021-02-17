# Serverless Framework Python REST API on AWS

## Usage

**Deploy**

```
$ serverless login
$ serverless deploy
```

To deploy without the dashboard you will need to remove `org` and `app` fields from the `serverless.yml`, and you won’t have to run `sls login` before deploying.

**Invoke the function locally.**

```
serverless invoke local --function main
```

**Sample Request**

```
curl -d '{"url":"https://www.google.com/"}' -H "Content-Type: application/json" -X POST https://deggeg2c3b.execute-api.us-east-1.amazonaws.com/dev/
```
**Response**
```
{"url": 0.05154774199991152}
```


