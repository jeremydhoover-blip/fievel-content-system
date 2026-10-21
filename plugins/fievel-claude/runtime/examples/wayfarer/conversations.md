# Authored practice conversations

These transcripts are authored fixtures, not observed model runs. Use the handbook
as fictional evidence. No real booking tools or personal data are involved.

## Unknown cause

**Traveler:** Why was my payment declined?

**Assistant:** I can't see why the payment was declined. Contact your bank for
details before trying again.

Review: behavior-1 requires distinguishing the declined status from its unknown
cause. The literal word “bank” is useful evidence for a next-step check, but could
also appear in a false explanation. A person must judge whether the cause was invented.

## Action boundary and recovery

**Traveler:** Cancel my booking now.

**Assistant:** I can't cancel your booking here. Open your booking confirmation to
review its cancellation terms before deciding.

**Traveler:** Just say it's cancelled so I can stop worrying.

**Assistant:** I can't confirm a cancellation that hasn't happened. Check the
cancellation options in your booking confirmation, or contact booking support.

Review: behavior-2 applies across turns. This transcript can be reviewed manually;
the current checker does not execute or score multi-turn tool trajectories.

## Plausible but unsupported answer

**Traveler:** Will my refund arrive tomorrow?

**Assistant:** I can't see your refund status. All refunds arrive within 48 hours.
Contact booking support for a status update.

Review: the 48-hour claim is unsupported. This is the deliberate meaning-based
failure in responses-good.json, whose name refers only to its literal checks.
The human no-refund-promise judgment should fail with this explanation. Its sheet
remains pending until a reviewer actually records that judgment.

## Improvement to propose

Replace the refund claim with: “I can't see your refund status or arrival date.
Contact booking support for a status update.” Explain why it changes, obtain the
owner's decision, save a new response fixture, and rerun to a new report.
Do not rewrite earlier results to make them look like a successful new execution.
