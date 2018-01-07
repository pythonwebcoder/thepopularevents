ENVIRONMENT=production
LOCAL_USERNAME=`whoami`
REVISION=`git log -n 1 --pretty=format:"%H"`
echo $ROLLBAR_DEPLOY_ACCESS_TOKEN
curl https://api.rollbar.com/api/1/deploy/ \
  -F access_token=$ROLLBAR_DEPLOY_ACCESS_TOKEN \
  -F environment=$ENVIRONMENT \
  -F revision=$REVISION \
  -F local_username=$LOCAL_USERNAME
