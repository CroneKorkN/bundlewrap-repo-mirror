JSON=$(cat bundles/build-server/example.json)
curl -X POST 'https://build.sublimity.de/crystal?file=procio.cr' -H "Content-Type: application/json" --data-binary @- <<< $JSON
