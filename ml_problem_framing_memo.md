# ML Problem-Framing Memo: Customer Churn

## Status

Pre-training assessment. No predictive model is trained or approved for
deployment.

## Dataset inspected

-   File: `customer-churn-training.csv`
-   Rows: 12
-   Columns: 7
-   Target: `churned` (0/1)
-   Target counts: 7 retained (0), 5 churned (1)
-   Missing values: 0 in the supplied file

## Decision to support

Prioritize customers for a voluntary retention intervention (for
example, a support check-in or service review). The model must not
automatically cancel, restrict, penalize, or change a customer's
service.

## Prediction target

The supplied target column is `churned`. Its operational definition is
not present in the supplied data. Before modeling, the data owner must
define the event precisely (for example, account closure or
non-renewal), the event date, and how reactivations are handled.

## Unit of observation

One customer row. `customer_id` is an identifier, not a predictive
feature.

## Action window and prediction horizon

Unknown. The dataset does not document when predictors were measured
relative to churn. The business owner must specify a fixed prediction
horizon and ensure all features are available before the intervention
decision. Do not infer a horizon from the column names.

## Candidate predictors

-   `tenure_months`
-   `support_tickets`
-   `monthly_spend_inr`
-   `last_login_days`
-   `plan_type`

These are candidate fields only. Their definitions, collection
timestamps, permitted uses, and relationship to the churn label require
verification.

## Non-ML baseline

Use a majority-class classifier that predicts the most common label in
the training data. In this sample it predicts retained (0) for every
customer. This is a benchmark, not a useful intervention strategy.
Compare any future model against it using a temporally valid holdout and
business-weighted metrics.

## ML justification

Not established. Twelve rows are far too few to estimate reliable
generalization, calibrate risk, assess subgroup performance, or support
operational deployment. First collect a larger, representative,
time-stamped dataset and test whether a transparent rules-based approach
is adequate.

## Costs and metrics

False positive: a retained customer is flagged as likely to churn,
potentially causing unnecessary contact, discount cost, or annoyance.
False negative: a customer who churns is not flagged, potentially losing
a preventable retention opportunity. The business owner must quantify
intervention cost, contact capacity, customer-harm risks, and the value
of a successfully retained customer before choosing thresholds. Report
confusion matrix, precision, recall, F1, PR-AUC, calibration, and
expected business cost. Accuracy alone is insufficient.

## Safeguards

-   Abstain when required fields are missing, stale, out of
    distribution, or outside the validated population.
-   Route uncertain or high-impact cases to trained human review.
-   Make outreach optional and non-coercive; provide a clear opt-out.
-   Monitor data quality, drift, intervention outcomes, complaints, and
    subgroup error rates.
-   Roll back to the approved non-ML process if monitoring thresholds
    are breached or data lineage changes.

## Go/no-go

NO-GO for model training claims or deployment using this 12-row sample.
GO for data-definition work, data-card completion, baseline
demonstration, and planning a larger prospective/temporal data
collection.
