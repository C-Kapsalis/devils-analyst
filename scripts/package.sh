#!/bin/sh
# Build the release assets into dist/ (attach them to a GitHub Release).
#
#   devils-analyst-plugin.zip    Claude plugin: .claude-plugin/plugin.json and
#                                icon.png, skills/, hooks/, house-rules/ at the
#                                zip root.
#                                Upload under Customize > Plugins in Claude
#                                (web or Desktop).
#   skills/devils-analyst-<skill>.zip
#                                one zip per skill, for Customize > Skills in
#                                Claude or the Skills tab in ChatGPT. Exactly
#                                one top-level folder, one SKILL.md, no
#                                manifest, a description under 200 characters.
#   devils-analyst-skills.zip    all of the above in one archive, for download.
#   devils-analyst-chatgpt.zip   ChatGPT plugin: plugin.json + skills/ (no
#                                hooks), for the ChatGPT plugin upload.
#
# POSIX sh; needs only `zip`. Run from anywhere: sh scripts/package.sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
DIST="$ROOT/dist"
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT INT TERM

command -v zip >/dev/null 2>&1 || { echo "package.sh: zip not found" >&2; exit 1; }
rm -rf "$DIST"
mkdir -p "$DIST/skills"

# Short descriptions for the standalone skill zips. Claude's skill upload
# documents a 200-character limit for a description; the plugin and the
# ChatGPT zip keep the long one from SKILL.md. No single quotes in these.
short() {
  case "$1" in
    route-question) echo 'Use first for any marketing data question: list the data you can reach, read house rules, rewrite the question into a precise request, say what can be answered.' ;;
    metric-definitions) echo 'Use before computing any marketing metric (CTR, CPA, CAC, ROAS, users, reach, LTV): the formula, the valid grain and the trap. Reads house rules first.' ;;
    whats-changed) echo 'Use when a marketing number moved between periods: fair comparison, drivers, mix versus rate, contribution, and a noise check before explaining why.' ;;
    diagnose) echo 'Use to find the likely cause of a marketing number that moved and what to do: funnel and brand diagnostics, playbooks, evidence for and against, how to verify.' ;;
    evidence-check) echo 'Use before saying something worked, won or should be scaled or cut: A/B checks, controls, seasonality, Simpson, holdouts, promo pull-forward, attribution.' ;;
    marketing-dashboard) echo 'Use to build a marketing dashboard or report from connected data or exports: definitions first, what changed and why, at most three findings with actions.' ;;
    review) echo 'Use to check a marketing report, deck or dashboard someone else made: recompute the numbers, check claims, leave correct things alone, rank Must, Should, Nice to have.' ;;
    audit) echo 'Use to audit a marketing setup (Google Ads, PMax, Meta, GA4 and UTMs, Search Console, email, CRM, revenue, tests, Power BI): numbered checks, money at stake, fix first.' ;;
    pricing-promotions) echo 'Use for price and discount decisions and promotion read-outs: elasticity, break-even depth, pull-forward, baseline erosion, contribution after discount.' ;;
    brand-health) echo 'Use for brand questions: tracker metrics, share of search, price premium, brand extensions and architecture, judged on the long view rather than one campaign.' ;;
    channel-audit) echo 'Use when asking whether a channel or tactic pays: paid search economics, attribution choice, influencers, SEO visibility, site funnel, judged on margin.' ;;
    product-decisions) echo 'Use to decide what to build, launch, price or kill from concept tests, conjoint, forecasts or a business case: calibration, segments, NPV, scoring weights.' ;;
    marketing-models) echo 'Use when a marketing question needs a model: regression, logit, segmentation, customer value, pricing and forecasting, with the assumptions stated.' ;;
    research-design) echo 'Use to plan or check customer research: survey or interviews, questionnaire wording, sampling and sample size, nonresponse, and what the results can support.' ;;
    hybrid-research) echo 'Use when research puts AI in the loop: synthetic respondents and personas, AI-drafted surveys, interview synthesis, and how to check them against human data.' ;;
    power-bi-definitions) echo 'Use when a Power BI semantic model exists: read its measures and toggles, audit them, and query them live or translate DAX to SQL faithfully.' ;;
    *) echo "package.sh: no short description for $1" >&2; exit 1 ;;
  esac
}

# Copy one skill folder to $2, renaming the skill (folder and `name:`) to $3.
# With $4, replace the frontmatter description with that one line, in YAML
# single quotes (so $4 must not contain a single quote).
copy_skill() {
  mkdir -p "$2"
  cp -R "$ROOT/skills/$1/." "$2/"
  find "$2" \( -name '.DS_Store' -o -name '__pycache__' \) -prune -exec rm -rf {} +
  sed "s/^name: .*/name: $3/" "$ROOT/skills/$1/SKILL.md" > "$2/SKILL.md"
  if [ $# -ge 4 ]; then
    [ ${#4} -lt 200 ] || { echo "package.sh: short description for $3 is ${#4} characters" >&2; exit 1; }
    awk -v d="$4" '
      NR == 1 && /^---$/ { fm = 1; print; next }
      fm && /^---$/ { fm = 0; print; next }
      fm && /^description:/ { print "description: \047" d "\047"; skip = 1; next }
      fm && skip && /^[ \t]/ { next }
      { skip = 0; print }
    ' "$2/SKILL.md" > "$2/SKILL.md.tmp" && mv "$2/SKILL.md.tmp" "$2/SKILL.md"
  fi
}

zip_dir() { # zip the contents of directory $1 into $2
  (cd "$1" && zip -qrX "$2" .)
}

SKILLS=$(cd "$ROOT/skills" && for d in */; do printf '%s\n' "${d%/}"; done)

# 1. Claude plugin
P="$STAGE/plugin"
mkdir -p "$P/.claude-plugin" "$P/hooks"
cp "$ROOT/.claude-plugin/plugin.json" "$ROOT/.claude-plugin/icon.png" "$P/.claude-plugin/"
cp -R "$ROOT/skills" "$ROOT/house-rules" "$P/"
cp "$ROOT/clawhub-package.json" "$P/package.json"
cp "$ROOT/hooks/claude-hooks.json" "$ROOT/hooks/core.md" "$P/hooks/"
cp "$ROOT/LICENSE" "$ROOT/README.md" "$P/"
find "$P" \( -name '.DS_Store' -o -name '__pycache__' \) -prune -exec rm -rf {} +
zip_dir "$P" "$DIST/devils-analyst-plugin.zip"

# 2. Claude or ChatGPT skills, one zip per skill (folder name = skill name)
for s in $SKILLS; do
  d="$(short "$s")"
  copy_skill "$s" "$STAGE/skill-$s/devils-analyst-$s" "devils-analyst-$s" "$d"
  zip_dir "$STAGE/skill-$s" "$DIST/skills/devils-analyst-$s.zip"
done
(cd "$DIST" && zip -qrX "$DIST/devils-analyst-skills.zip" skills)

# 3. ChatGPT plugin: skills only, no hooks
C="$STAGE/chatgpt"
mkdir -p "$C/skills" "$C/assets"
cp "$ROOT/adapters/chatgpt/plugin.json" "$C/"
cp "$ROOT/.claude-plugin/icon.png" "$C/assets/icon.png"
for s in $SKILLS; do
  copy_skill "$s" "$C/skills/devils-analyst-$s" "devils-analyst-$s"
done
cp "$ROOT/LICENSE" "$C/"
zip_dir "$C" "$DIST/devils-analyst-chatgpt.zip"

ls -l "$DIST" "$DIST/skills"
