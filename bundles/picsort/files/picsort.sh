#!/bin/bash

#exit 0
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

function log {
  logger -st nc-picsort "${*:-$(</dev/stdin)}"
}

SOURCEPATH="/var/lib/nextcloud/ckn/files/SofortUpload/AutoSort/"
DESTINATIONPATH="/var/lib/nextcloud/ckn/files/Bilder/Chronologie/"
USER="ckn"

log "STARTING..."

if ps aux | grep cron | grep nc-picsort | grep -v $$; then log "EXIT: still running"; exit 0; fi

SCAN="FALSE"
IFS=$'\n'
for f in `find "$SOURCEPATH" -iname *.PNG -o -iname *.JPG -o -iname *.CR2 -o -iname *.CR3 -o -iname *.MP4 -o -iname *.MOV`; do
  log "PROCESSING: $f"
  DATE=`exiftool "$f" | grep -m 1 "Create Date"`
  if ! echo "$DATE" | grep "Create Date" >/dev/null
  then
    log "SKIP: no 'Create Date' in exif ($f)"
    continue
  fi
  SCAN="TRUE"
  YEAR=`echo $DATE | cut -d':' -f2 | cut -c 2-`
  MONTH=`echo $DATE | cut -d':' -f3`
  DAY=`echo $DATE | cut -d':' -f4 | cut -d' ' -f1`
  HOUR=`echo $DATE | cut -d':' -f4 | cut -d' ' -f2`
  MINUTE=`echo $DATE | cut -d':' -f5`
  SECOND=`echo $DATE | cut -d':' -f6`
  HASH=`sha256sum "$f" | xxd -r -p | base64 | head -c 3 | tr '/+' '_-'`
  EXT=`echo "${f##*.}" | tr '[:upper:]' '[:lower:]'`
  if [[ "$EXT" = "cr2" ]] ||  [[ "$EXT" = "cr3" ]]
  then
    RAW="raw/"
  else
    RAW=""
  fi
  FILE="$DESTINATIONPATH$YEAR-$MONTH/$RAW$YEAR$MONTH$DAY"-"$HOUR$MINUTE$SECOND"_"$HASH"."$EXT"
  log "DESTINATION: $FILE"
  mkdir -p "$(dirname "$FILE")"
  mv -v "$f" "$FILE"
done

if [ "$SCAN" == "TRUE" ]; then
  log "SCANNING..."
  # find "$SOURCEPATH/"* -type d -empty -delete >> /var/log/nc-picsort.log # nextcloud app bug when deleting folders
  chown -R www-data:www-data "$DESTINATIONPATH"
  chmod -R 777 "$DESTINATIONPATH"
  sudo -u www-data php /var/www/nextcloud/occ files:scan $USER | log
  sudo -u www-data php /var/www/nextcloud/occ preview:generate-all $USER | log
fi

log "FINISH."
