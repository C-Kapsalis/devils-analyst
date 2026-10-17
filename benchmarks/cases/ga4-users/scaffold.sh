#!/usr/bin/env bash
# Writes this case's fixture data into the run's workspace (both arms see the same files).
set -euo pipefail
mkdir -p resources
cat > resources/ga4_daily_by_channel.csv <<'DEVILS_ANALYST_EOF'
date,session_default_channel_group,total_users,sessions
2026-09-01,Organic Search,803,981
2026-09-01,Paid Search,515,618
2026-09-01,Email,216,259
2026-09-02,Organic Search,952,1164
2026-09-02,Paid Search,624,749
2026-09-02,Email,265,318
2026-09-03,Organic Search,964,1178
2026-09-03,Paid Search,522,626
2026-09-03,Email,257,308
2026-09-04,Organic Search,863,1055
2026-09-04,Paid Search,657,788
2026-09-04,Email,274,329
2026-09-05,Organic Search,1006,1230
2026-09-05,Paid Search,522,626
2026-09-05,Email,278,334
2026-09-06,Organic Search,1012,1237
2026-09-06,Paid Search,680,816
2026-09-06,Email,221,265
2026-09-07,Organic Search,821,1003
2026-09-07,Paid Search,530,636
2026-09-07,Email,215,258
2026-09-08,Organic Search,994,1215
2026-09-08,Paid Search,656,787
2026-09-08,Email,260,312
2026-09-09,Organic Search,988,1208
2026-09-09,Paid Search,624,749
2026-09-09,Email,234,281
2026-09-10,Organic Search,792,968
2026-09-10,Paid Search,528,634
2026-09-10,Email,269,323
2026-09-11,Organic Search,820,1002
2026-09-11,Paid Search,567,680
2026-09-11,Email,244,293
2026-09-12,Organic Search,771,942
2026-09-12,Paid Search,556,667
2026-09-12,Email,234,281
2026-09-13,Organic Search,958,1171
2026-09-13,Paid Search,576,691
2026-09-13,Email,237,284
2026-09-14,Organic Search,1025,1253
2026-09-14,Paid Search,601,721
2026-09-14,Email,276,331
2026-09-15,Organic Search,932,1139
2026-09-15,Paid Search,516,619
2026-09-15,Email,243,292
2026-09-16,Organic Search,883,1079
2026-09-16,Paid Search,649,779
2026-09-16,Email,239,287
2026-09-17,Organic Search,955,1167
2026-09-17,Paid Search,607,728
2026-09-17,Email,229,275
2026-09-18,Organic Search,998,1220
2026-09-18,Paid Search,526,631
2026-09-18,Email,274,329
2026-09-19,Organic Search,811,991
2026-09-19,Paid Search,510,612
2026-09-19,Email,228,274
2026-09-20,Organic Search,971,1187
2026-09-20,Paid Search,686,823
2026-09-20,Email,213,256
2026-09-21,Organic Search,898,1098
2026-09-21,Paid Search,598,718
2026-09-21,Email,272,326
2026-09-22,Organic Search,815,996
2026-09-22,Paid Search,599,719
2026-09-22,Email,239,287
2026-09-23,Organic Search,990,1210
2026-09-23,Paid Search,557,668
2026-09-23,Email,283,340
2026-09-24,Organic Search,842,1029
2026-09-24,Paid Search,549,659
2026-09-24,Email,265,318
2026-09-25,Organic Search,900,1100
2026-09-25,Paid Search,530,636
2026-09-25,Email,260,312
2026-09-26,Organic Search,787,962
2026-09-26,Paid Search,652,782
2026-09-26,Email,265,318
2026-09-27,Organic Search,977,1194
2026-09-27,Paid Search,623,748
2026-09-27,Email,239,287
2026-09-28,Organic Search,873,1067
2026-09-28,Paid Search,581,697
2026-09-28,Email,279,335
2026-09-29,Organic Search,788,963
2026-09-29,Paid Search,670,804
2026-09-29,Email,214,257
2026-09-30,Organic Search,821,1003
2026-09-30,Paid Search,557,668
2026-09-30,Email,280,336
DEVILS_ANALYST_EOF
