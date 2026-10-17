#!/usr/bin/env bash
# Writes this case's fixture data into the run's workspace (both arms see the same files).
set -euo pipefail
mkdir -p resources
cat > resources/google_ads_sep.csv <<'DEVILS_ANALYST_EOF'
month,campaign,cost,conversion_value
2026-09,Brand Search,3100.0,21800.0
2026-09,Generic Search,9400.0,30500.0
2026-09,Performance Max,7200.0,34100.0
DEVILS_ANALYST_EOF
cat > resources/meta_ads_sep.csv <<'DEVILS_ANALYST_EOF'
month,campaign,spend,purchase_value
2026-09,Prospecting,8800.0,19900.0
2026-09,Retargeting,2600.0,17300.0
DEVILS_ANALYST_EOF
cat > resources/shopify_sep.csv <<'DEVILS_ANALYST_EOF'
month,net_sales,orders
2026-09,84600.0,1710
DEVILS_ANALYST_EOF
