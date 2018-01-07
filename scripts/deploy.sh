git add .
git commit -a -m "$1"
git push origin master
nanobox deploy
sh scripts/rollbar_deploy_alert.sh
