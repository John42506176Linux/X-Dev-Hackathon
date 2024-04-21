curl --request GET "https://api.twitter.com/2/users/by/username/$1" \
    --header "Authorization: Bearer $TWITTER_BEARER_TOKEN" \
    | jq -r '.data.id'
