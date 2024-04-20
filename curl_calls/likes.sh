curl "https://api.twitter.com/2/users/$1/liked_tweets" \
    -H "Authorization: Bearer $TWITTER_BEARER_TOKEN"
