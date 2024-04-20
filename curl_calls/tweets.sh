curl --request GET "https://api.twitter.com/2/users/$1/tweets" \
    --header "Authorization: Bearer $TWITTER_BEARER_TOKEN"
