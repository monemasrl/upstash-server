# Simple Upstash Server Implementation

This is a simple implementation of the [Upstash](https://upstash.com "Serverless Data Platform") service running inside a docker container. Implemented Methods are those needed by the  Upstash APL implementation and a few more, for  development on [Saleor](https://saleor.io ).

### Implemented methods:

* get
* set
* delete
* keys (not required by APL)
* info (not required by APL)

## Docker image build

```bash
docker build -t upstash-server .
```

## Docker run

To run the image you can set the following environment variables:


|Name|Required |Default |
|----------|----|----|
|REDIS_PORT|No | localhost |
|REDIS_PORT | No | 6379|
|REDIS_DB | No | 0 |
|BEARER_TOKEN| No | Self Generated |

```bash
docker run -d upstash-server
```


