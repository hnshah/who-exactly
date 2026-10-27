---
name: workaround-atlas
description: >-
  Use when studying what people already do instead of using a proposed
  product, the alternative tools or manual workarounds they use, why
  those work, and when they break. Analyze cited job episodes and
  counterexamples into an Alternatives Matrix. Not for finding individual
  early-access contacts or drafting invitations.
license: MIT
metadata:
  author: Hiten Shah
---

# Workaround atlas

## Mission

Describe the **actual competitive alternatives** that people use to finish a job, including doing nothing, keeping their current workflow, manual work, successful substitutes and workarounds. Produce evidence that improves a product decision, not a generic competitor list.

## Use this skill when

- The founder asks "what are people doing now?", "why haven't they switched?" or "what is the current workaround?"
- A cluster of sourced episodes needs to be grouped by method, trigger or environment.
- The team is deciding whether a claimed pain is strong enough to test in a product.

## Do not use this skill when

- The job itself has not been defined: first use `job-evidence-map`.
- The objective is identifying specific public X accounts: first use `x-people-safari`.
- The objective is inviting already qualified contacts: use `cohort-assembly`.

## Required input and output

Input: a defined job and a collection of actually sourced self-reported episodes, or a research plan where sources are not yet available. Output an **Alternatives Matrix**, evidence limitations, strongest viable incumbent method, contradictions, what to test next. See `assets/ALTERNATIVES-MATRIX.md`.

## Method

1. Confirm the actor, trigger, desired result and constraints. The competitor is whatever the person currently uses to finish that job, which may be a process or status quo rather than a named SaaS product.
2. Verify that every claimed current method has an attributable source episode, timestamp and specific stated activity. Keep the original claim apart from our interpretation, following `references/EVIDENCE.md`.
3. Group alternatives into methods: incumbent software, multiple tools chained together, manual workaround, assistance from people, delay/abandonment, or no problem. Preserve multiple independent episodes per method without inflating frequency.
4. For each method, identify when it succeeds, fails, adds cost, or avoids switching anxiety; list environmental conditions and any contradictory accounts.
5. Compare push of existing pain, pull of a better alternative, anxiety about change, and habit of the present **as hypotheses linked to quotes**, not assumed motivations.
6. State a narrower testable hypothesis and what additional real task observation, interview or repeated use would prove or disprove it.
7. Show the limitations: sample size actually reviewed, self-selection, recency, unknown context and whether source coverage is poor.

## Quality and fallback

Read `references/CONTEXT.md`, `references/QUALITY.md` and `references/ACCESS.md`. No fake market percentages or conversion likelihood. Never generalize a few X discussions to all customers. With no sourced episodes, return a grounded research plan and an empty matrix, not invented alternatives presented as user behavior.

## Handoff

If a new group appears worth identifying, use `x-people-safari`. If a qualified group should be invited, use `cohort-assembly`. Do not advise pricing, roadmap priorities or launch commitments as if X self-reports alone establish demand.
