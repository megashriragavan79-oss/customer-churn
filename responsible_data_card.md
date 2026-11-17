# Responsible Data Card: Customer Churn Dataset

## 1. Dataset summary

-   Dataset file: `customer-churn-training.csv`
-   Observed size: 12 rows × 7 columns
-   Intended task: exploratory framing of customer churn prediction
-   Target: `churned` (binary values 0 and 1)
-   Observed label distribution: 7 zeros and 5 ones
-   Missingness: no missing cells detected in this file

## 2. Provenance and collection

  Field                              Status
  ---------------------------------- --------------
  Data owner / source system         Not provided
  Collection method                  Not provided
  Collection period                  Not provided
  Update frequency                   Not provided
  Label-generation process           Not provided
  Data dictionary                    Not provided
  Consent / lawful basis             Not provided
  Retention and deletion policy      Not provided
  Geographic / population coverage   Not provided

Do not assume consent, legal basis, or representativeness from the CSV
alone. Obtain documentation from the data controller before operational
use.

## 3. Fields and intended use

  -----------------------------------------------------------------------
  Field                   Type                    Initial handling
  ----------------------- ----------------------- -----------------------
  customer_id             Identifier              Exclude from model
                                                  features; restrict
                                                  access

  tenure_months           Numeric                 Candidate feature;
                                                  verify timestamp and
                                                  definition

  support_tickets         Numeric                 Candidate feature;
                                                  verify time window and
                                                  meaning

  monthly_spend_inr       Numeric                 Candidate feature;
                                                  verify currency,
                                                  billing period and
                                                  timing

  last_login_days         Numeric                 Candidate feature;
                                                  verify reference date
                                                  and freshness

  plan_type               Categorical             Candidate feature;
                                                  assess proxy/fairness
                                                  implications

  churned                 Binary target           Verify exact event
                                                  definition and label
                                                  timestamp
  -----------------------------------------------------------------------

## 4. Sensitive attributes and proxies

No explicit sensitive attributes are present in the listed columns. This
does not establish that the dataset is non-sensitive or fair. Customer
identifiers can be linkable to personal records. Plan type, spend,
tenure, and usage may act as proxies for socioeconomic circumstances or
other customer characteristics. Conduct a lawful, privacy-reviewed
fairness assessment using appropriately governed data; do not infer
sensitive traits.

## 5. Missingness and quality

-   Missing values: none observed in the 12 rows.
-   Uniqueness: 12 distinct customer IDs.
-   Small sample: severe limitation for statistical inference and model
    validation.
-   Check duplicates, impossible values, inconsistent units, stale
    values, and label correctness when the source system and data
    dictionary become available.

## 6. Leakage risks

-   `customer_id` may encode ordering or source-system artifacts;
    exclude it.
-   `last_login_days` may have been measured after the churn event;
    verify the as-of date.
-   `support_tickets` may include tickets created after churn or during
    a retention intervention; define a pre-prediction lookback window.
-   `monthly_spend_inr` may reflect post-churn billing or cancellation
    adjustments; verify timing.
-   `plan_type` must be captured as of the prediction timestamp.
-   Ensure `churned` is assigned only after the target horizon and is
    not used to construct predictors.

## 7. Allowed and prohibited uses

Potentially acceptable after governance approval: research and
evaluation of a voluntary retention-support workflow. Not approved:
automated cancellation, price discrimination, service restriction,
credit/eligibility decisions, or punitive treatment.

## 8. Evaluation and fairness

Use time-based splits after enough longitudinal data exists. Report
precision, recall, F1, PR-AUC, calibration, confusion matrix, and
business-weighted cost. Examine error rates and intervention outcomes
across relevant, lawfully collected groups where sample sizes permit. Do
not publish subgroup conclusions from this 12-row sample.

## 9. Human oversight and recourse

Use human review for uncertain cases and any action with meaningful
customer impact. Provide clear explanations for outreach, an opt-out, a
complaint route, and a way to correct inaccurate source data.

## 10. Limitations

This file alone does not document provenance, consent, target semantics,
prediction horizon, collection timestamps, or representativeness. It is
too small for a reliable predictive model. The accompanying HTML file
was inspected and appears to be a RabTech Academy webpage rather than a
data-card template.
