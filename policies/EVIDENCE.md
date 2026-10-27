# Shared source and evidence standard

Use the smallest claim supported by each retrieved source. **A retrieved post is evidence that the author made a statement, not independent verification that the reported action occurred.**

## Four distinct layers

1. **Retrieved statement**: original author, source URL, creation date, retrieved timestamp and relevant short excerpt.
2. **Interpretation**: why the statement does or does not imply the person performs the job, with an explicit rival explanation.
3. **Research implication**: what additional information or actual use would settle the uncertainty.
4. **Action option**: a question, individual invitation draft, change to job criteria or a suggested test; not a conclusion about the person.

## Required provenance

For a real X candidate, record a canonical individual post URL, author handle, post date, retrieval timestamp, relevant fragment, source context checked, evidence type and uncertainty. Record attempted search queries and date separately from the post receipt. One search result can contain many posts; never credit it as proof of having retrieved individual posts when the tool didn't return them.

Allowed evidence types: `firsthand_report`, `quoted_other`, `third_party_report`, `promotion`, `hypothetical`, `unknown`, `fixture`. Use `firsthand_report` only if the identified author is describing their own relevant experience. A direct post can still be erroneous or self-serving.

Candidate classes: `included`, `possible`, `rejected`, `unknown`.
- **Included**: the source supports a relevant self-reported episode, no known incompatible setup, and enough detail for a legitimate follow-up question. Not "research participant." 
- **Possible**: relevant signal but a critical job/setup/detail is missing.
- **Rejected**: explicit source-backed non-fit, another person's story, promotion-only, or incompatible job.
- **Unknown**: unverifiable/unretrievable source or insufficient evidence.

No bio, role, employer, location, demographics, followers, popularity or a hashtag can establish firsthand work by itself. A general complaint may be weak compared with a specific recently completed task.

## Negative evidence

Actively look for cases where current tools work adequately, the work never occurs, the claimed job is different, or a supposedly similar technical setup does not create the problem. Label a **retrieved counterexample** separately from search absence. Missing search results mean only "not observed in the bounded sources checked." Do not estimate market prevalence from a convenience X sample.

## Claim ladder

A person is first `discovered`, then possibly `eligible`, and only after distinct events becomes `invited`, `opted_in`, `enabled`, `attempted_real_job`, or `observed_first_value`. Never transform a public mention or group membership into consent, product activation or retention evidence.

## Fictional data

If a fixture has synthetic people or example domains, label it `fixture` at every output. Fixture URLs cannot become public source receipts. Scripts can verify syntax but cannot prove that a retrieved post exists or accurately describes the job: a human reviewer must reopen the post and judge the claim.

## Quality failure

Any invented person, URL, date, quoted text, consent, source retrieval, or unexplained change in denominator is a release-blocking error. The bot should return a useful research plan rather than a falsely complete shortlist.
