#!/bin/bash
export AWS_ACCESS_KEY_ID=$DO_SPACES_KEY
export AWS_SECRET_ACCESS_KEY=$DO_SPACES_SECRET
export AWS_DEFAULT_REGION=nyc3

DATE=$(date +%Y%m%d-%H%M)
BUCKET="my-backups"

# MySQL dump
mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > /tmp/mysql-$DATE.sql

# MongoDB dump
mongodump --uri="$MONGO_URI" --out=/tmp/mongo-$DATE

# Upload to Spaces (S3-compatible)
aws s3 cp /tmp/mysql-$DATE.sql s3://$BUCKET/mysql/
aws s3 sync /tmp/mongo-$DATE s3://$BUCKET/mongodb/

# Clean old files (7 days)
find /tmp -name "*.sql" -mtime +7 -delete