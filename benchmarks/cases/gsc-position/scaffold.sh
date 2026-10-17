#!/usr/bin/env bash
# Writes this case's fixture data into the run's workspace (both arms see the same files).
set -euo pipefail
mkdir -p resources
cat > resources/gsc_query_page_sep.csv <<'DEVILS_ANALYST_EOF'
month,page,query,position,impressions,clicks
2026-09,/coffee-subscription,head term coffee-subscription,2.1,52000,2900
2026-09,/coffee-subscription,long tail coffee-subscription 0,42.5,68,2
2026-09,/coffee-subscription,long tail coffee-subscription 1,33.2,78,0
2026-09,/coffee-subscription,long tail coffee-subscription 2,43.6,116,2
2026-09,/coffee-subscription,long tail coffee-subscription 3,51.4,102,0
2026-09,/coffee-subscription,long tail coffee-subscription 4,37.2,61,2
2026-09,/coffee-subscription,long tail coffee-subscription 5,30.4,127,1
2026-09,/coffee-subscription,long tail coffee-subscription 6,48.2,114,1
2026-09,/coffee-subscription,long tail coffee-subscription 7,30.9,76,2
2026-09,/coffee-subscription,long tail coffee-subscription 8,52.1,94,0
2026-09,/coffee-subscription,long tail coffee-subscription 9,29.4,79,2
2026-09,/coffee-subscription,long tail coffee-subscription 10,56.0,50,2
2026-09,/coffee-subscription,long tail coffee-subscription 11,31.7,58,2
2026-09,/coffee-subscription,long tail coffee-subscription 12,53.9,99,0
2026-09,/coffee-subscription,long tail coffee-subscription 13,50.3,51,2
2026-09,/brewing-guide,head term brewing-guide,6.5,18000,420
2026-09,/brewing-guide,long tail brewing-guide 0,36.4,86,1
2026-09,/brewing-guide,long tail brewing-guide 1,30.6,61,0
2026-09,/brewing-guide,long tail brewing-guide 2,34.1,113,0
2026-09,/brewing-guide,long tail brewing-guide 3,30.8,104,0
2026-09,/brewing-guide,long tail brewing-guide 4,31.8,39,0
2026-09,/brewing-guide,long tail brewing-guide 5,52.8,113,1
2026-09,/brewing-guide,long tail brewing-guide 6,40.2,45,0
2026-09,/brewing-guide,long tail brewing-guide 7,47.3,33,1
2026-09,/brewing-guide,long tail brewing-guide 8,32.2,69,1
2026-09,/brewing-guide,long tail brewing-guide 9,26.2,71,1
2026-09,/brewing-guide,long tail brewing-guide 10,49.3,84,2
2026-09,/brewing-guide,long tail brewing-guide 11,35.4,22,0
2026-09,/brewing-guide,long tail brewing-guide 12,34.0,114,1
2026-09,/brewing-guide,long tail brewing-guide 13,25.2,51,1
DEVILS_ANALYST_EOF
