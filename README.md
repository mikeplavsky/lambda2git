# lambda2git
Syncing Aws Lambda versions to github

Assumptions (which maybe wrong):

- commits are returned by Git from new to old
- Aws Lambda versions are returned from old to new 

Warning:

$LATEST version is not synced, you need explicitly publish Aws Lambda version 

How To:

- docker-compose build
- docker-compose run lambda2git bash
- ./deploy.sh will generate zip
- create AWS Lambda with zip and sync.lambda_handler entry point
- call it from another AWS Lambda like [Example](example.js)
