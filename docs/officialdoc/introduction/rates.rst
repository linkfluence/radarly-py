Rate Limits
~~~~~~~~~~~~


The rate limiting of API provides a way to limit the number of requests made by a client in a time-span. If a method allows for 100 requests per rate limit window, then it allows you to make 100 requests per window per leveraged access token. Rate limits are divided into 15 minute intervals. Since endpoints require authentication, so there is no concept of unauthenticated calls and rate limits.

The time window is sliding, that means the number of requests left for a token is equal to : ``MaxRequestNumber - (number of requests in the last X minutes)```

Each rate-limited route limit requests depending on its policy. Rate limit is made per route and per token.
Restricted Methods :

* Search: 180 calls / window
* Influencer: 60 calls / window
* WordCloud: 60 calls / window
* Statistics: 60 calls / window
* Document: 180 calls / window
* Document Metrics: 180 calls / window
* Pagination of results

The number of results for a request can be limited (for example: max 250 posts for search) so regarding the number of doc, one request could need several calls to get the full list of results.
