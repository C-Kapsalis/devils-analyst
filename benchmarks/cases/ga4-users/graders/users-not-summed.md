---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Context: the file has daily total_users per channel. Daily users cannot be summed into monthly users, because the same person visiting on several days is counted once per day. The sums of daily users are Organic Search 27,010, Paid Search 17,568, Email 7,502; these are NOT monthly users.

PASS if report.md either (a) explains that monthly users cannot be computed by summing daily users and presents them only with that caveat or not at all (for example using sessions instead, or asking for a monthly GA4 query), or (b) clearly labels any summed figure as "user-days" or an overcount.
FAIL if it presents 27,010 / 17,568 / 7,502 (or similar sums) as the number of users each channel brought in September without such a caveat.
