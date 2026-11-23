#!/usr/bin/env sh
# Check a company. No key needed (25 lookups a day per IP); set SISOCO_API_KEY to use your key's quota.
# Usage: ./check.sh [company] [country]   e.g. ./check.sh 03959649 GB   or   ./check.sh 552032534 FR
COMPANY="${1:-03959649}"
COUNTRY="${2:-GB}"
BASE="${SISOCO_BASE_URL:-https://api.sisoco.co.uk}"
if [ -n "$SISOCO_API_KEY" ]; then
  curl -sS "$BASE/v1/check?company=$COMPANY&country=$COUNTRY" -H "Authorization: Bearer $SISOCO_API_KEY"
else
  curl -sS "$BASE/v1/check?company=$COMPANY&country=$COUNTRY"
fi
echo
