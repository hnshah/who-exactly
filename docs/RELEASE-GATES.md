# Release gates and scope

## Where v0.2.1 stands

v0.2.1 is a **developer alpha**: the source is public so the method and skills can be inspected, reused and improved. It is **not** a launched Grok Bot. The gates below separate "the source is public" from "the Bot works for real people".

### In the public repository

README; four independently installable skill folders with their references and assets; the Grok Bot profile and install guide; JSON schemas; synthetic fixtures; offline tests and validators; the quality rubric; example output clearly labeled hypothetical or synthetic; changelog; MIT license.

### Never in the public repository

Real participants' private details, DM contents, private X research, credentials, research adjudication notes, restricted source corpora, unreleased partner or product evidence, and hidden evaluation answer keys. Public post links used in any future demonstration need source, attribution and privacy review first.

## Gates

Source release (v0.2.1):

- [x] License chosen: MIT.
- [x] Privacy and licensing review of every file ([`PUBLIC-RELEASE-REVIEW.md`](PUBLIC-RELEASE-REVIEW.md)).
- [x] Offline validator, `skills-ref` and test suite pass in CI, and the packaged ZIP re-verifies after extraction.
- [x] Public copy separates verified behavior from roadmap.

Bot launch (all still open; tracked as GitHub issues):

- [ ] Final name confirmed, with legal and domain collision screening.
- [ ] Grok Bot accepts and renders the name and label.
- [ ] Four complete skills enabled on a real Bot, with scope checked.
- [ ] One positive and one negative public X example with checked post URLs, dates, original authors and job reasoning.
- [ ] Three different research jobs tested (technical, design, confidential/non-public).
- [ ] No invented citations or author attributions in inspected cases.
- [ ] Account-specific X connection prompt tested in a clean authorized account, plus the capability fallback.
- [ ] All external communication stays draft-only unless a specific write tool and explicit approval are proven.
- [ ] Fresh-account template import verifies instructions, skills and privacy boundaries.
- [ ] Side-by-side comparison against an ordinary Grok Bot on the same task.

**Do not describe Who Exactly? as a running public Bot until the launch gates pass.** A source ZIP is not a Grok Bot install, and script tests are not live X results.
