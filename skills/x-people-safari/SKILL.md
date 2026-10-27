---
name: x-people-safari
description: >-
  Use when finding source-backed X posts from people already doing a
  particular job, qualifying practitioners, evaluating firsthand work
  episodes, or excluding false matches. Return post links, dates,
  counterexamples and a bounded search audit. Not for follower outreach
  campaigns, private-source search without authorization, or sending DMs.
license: MIT
compatibility: >-
  Live discovery needs a working public X search or read tool, such as
  Grok Bot's built-in X access. Without one, returns a reproducible search
  plan and no candidates.
metadata:
  author: Hiten Shah
---

# X people safari

## Mission

Find **people with credible public self-reports of performing a particular job**, not simply people who resemble the intended user. Make it possible for a human to check every claim.

## Use this skill when

- The founder asks "who already does this?" or "find practitioners for this job on X."
- A specific public X conversation must be checked for actual job evidence.
- A candidate list needs strong and weak examples, disqualifiers or contrary cases.

## Do not use this skill when

- There is no usable job definition and the task is purely eligibility design: start with `job-evidence-map`.
- The task is a substantive comparison of current workarounds: use `workaround-atlas` after source retrieval if needed.
- The task is drafting invitations to an already vetted group: use `cohort-assembly`.

## Required input and output

Input: the job, inclusion criteria, exclusion criteria and permitted search resources. Return **Candidate Review** with dated post receipts and eligibility reasoning, excluded cases, one counterexample or a documented scarcity result, query/time boundaries and a next validation question. Use `assets/CANDIDATE-REVIEW.md`.

## Procedure

1. Inspect whether a real public X search tool is available. Record tool access mode, search time and what can be retrieved. If not, stop with a reproducible search plan and **no invented results**. Review `references/ACCESS.md` and `references/CONTEXT.md`.
2. Search bounded phrases for a *task*, current tools, workarounds, specific previous events, and explicit cases in which the alleged problem is absent. Vary surface and phrasing without claiming exhaustive coverage.
3. Retrieve exact post links and available thread context. Determine whether the candidate author reports their **own** work or merely quotes a colleague, shares a promotion or asks a hypothetical question. If parent posts cannot be retrieved, record that limitation.
4. Extract a Job Episode with author, canonical post URL, post date, retrieval time, quote fragment, described trigger/action, environment, workaround and known/unknown results. Keep the account identity separate from the episode and from the researcher's interpretation. See `references/EVIDENCE.md`.
5. Deduplicate by canonical post ID and account across results; don't turn many posts from one person into several distinct qualified people.
6. Classify each candidate **included / possible / rejected / unknown**, explain why, and name which missing fact would change the decision. Favor behavior over account reach.
7. Deliberately test non-fits and successful incumbent workarounds. For a remote-interactive-Mac tool, an SSH-only workflow can be a disqualifier even if the author owns three Macs.
8. Audit returned examples against the actual job: show the strongest cases and the strongest contradictory case or a documented lack of enough evidence. Do not make claims about the proportion of all users doing the job.
9. Provide one high-value qualifying question or invitation angle but no unsolicited outbound message sending.

## Quality bar and failure cases

Read `references/QUALITY.md`. No forged source/post/date, no incorrect quote attribution, no private X retrieval without authorized capability, no assumption of research consent. A syntactically valid URL **does not mean the post was independently opened and checked**. If the source is unavailable, mark its retrieval status accordingly.

## Handoff

To analyze existing alternatives, pass source episodes to `workaround-atlas`; to invite qualified people, pass candidate review to `cohort-assembly`. Only pass evidence actually retrieved.
