# Devil's Analyst installed

Connect your data (a warehouse, or the connectors for your ad platforms,
analytics, CRM or email tool), or attach exports, and ask the way you
normally would:

- "How did paid search do last month, and what should we change?"
- "Our analyst says September was a record month. Is it?"
- "Audit our GA4 setup and tell me what to fix first."
- "Did the new homepage hero win?"

You get the scope it answered (source, account, conversion action, window,
grain), the answer with its number, at most three findings with a likely
cause, an action and how to verify it, and what it checked and could not
check. Audits and reviews end with what to fix first.

House rules: put your team's rules in a `house-rules/` folder in your
project, one per file, from the template in this plugin's
`house-rules/TEMPLATE.md`. They are read first and override the shipped
defaults.

Skills, where the host supports them: `devils-analyst:route-question` loads
first; the others (metric-definitions, whats-changed, diagnose,
evidence-check, marketing-dashboard, review, audit, power-bi-definitions and
seven more) load by the job.

To check it loaded in Claude Code, start a new session and ask "Is Devil's
Analyst active?". The session hook adds the routing table and seven core
rules to every session.

Found an analysis that was wrong? Please open an issue with the export (or a
version with private details removed) and what it got wrong:
https://github.com/C-Kapsalis/devils-analyst/issues
