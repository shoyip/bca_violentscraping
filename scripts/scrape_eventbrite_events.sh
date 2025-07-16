#!/bin/bash

# Set your OAuth token here
OAUTH_TOKEN=""

# Input file with one event ID per line
INPUT_FILE="eventbrite_bari_ids.txt"

# Base URL
BASE_URL="https://www.eventbriteapi.com/v3/events"


# Read IDs into an array
mapfile -t EVENT_IDS < "$INPUT_FILE"
TOTAL_IDS=${#EVENT_IDS[@]}

# Temp file for building the JSON array
TMP_FILE="tmpfile.json"
echo "[" > "$TMP_FILE"

FIRST=true
COUNT=0

# Iterate over event IDs
for EVENT_ID in "${EVENT_IDS[@]}"; do
    [ -z "$EVENT_ID" ] && continue
    ((COUNT++))

    echo "Fetching event $COUNT of $TOTAL_IDS: $EVENT_ID"

    URL="${BASE_URL}/${EVENT_ID}/"
    RESPONSE=$(curl -s -X GET "$URL" \
              -H "Authorization: Bearer $OAUTH_TOKEN")

    # Add comma between JSON objects
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        echo "," >> "$TMP_FILE"
    fi

    echo "$RESPONSE" | jq '.' >> "$TMP_FILE"
done

echo "]" >> "$TMP_FILE"
mv "$TMP_FILE" "$OUTPUT_FILE"

echo "All $TOTAL_IDS events saved to $OUTPUT_FILE"
