```
gcloud projects add-iam-policy-binding sublimity-182017 --member 'serviceAccount:backup@sublimity-182017.iam.gserviceaccount.com' --role 'roles/storage.objectViewer'
gcloud projects add-iam-policy-binding sublimity-182017 --member 'serviceAccount:backup@sublimity-182017.iam.gserviceaccount.com' --role 'roles/storage.objectCreator'
gsutil -o "GSUtil:parallel_process_count=3" -o GSUtil:parallel_thread_count=4 -m rsync -r -d -e /var/vmail gs://sublimity-backup/mailserver
gsutil config
gsutil versioning set on gs://sublimity-backup
```
