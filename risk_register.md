# Risk Register: Customer Churn Use Case

  -----------------------------------------------------------------------------------------
  ID             Risk               Likelihood /   Mitigation           Monitoring /
                                    impact                              rollback trigger
  -------------- ------------------ -------------- -------------------- -------------------
  R1             Churn label is     High / High    Obtain business      Stop if label
                 undefined or                      definition, event    definition changes
                 inconsistent                      timestamp, and label or cannot be
                                                   QA rules             audited

  R2             Feature leakage    High / High    Establish prediction Roll back if any
                 from post-churn                   timestamp and        feature is shown to
                 activity                          feature lookback     use post-outcome
                                                   windows              data

  R3             Tiny,              Certain / High Collect larger       No deployment until
                 unrepresentative                  time-stamped         validation sample
                 sample                            representative data; and uncertainty are
                                                   use temporal         adequate
                                                   validation           

  R4             Privacy or consent Unknown / High Obtain data-owner    Stop processing if
                 basis is                          approval, purpose    authority or
                 undocumented                      limitation, access   permitted purpose
                                                   controls, retention  is unclear
                                                   rules                

  R5             Proxy              Medium / High  Review feature       Pause if material
                 discrimination via                necessity, assess    unexplained
                 spend or plan type                lawful subgroup      disparities appear
                                                   performance, human   
                                                   oversight            

  R6             False positives    Medium /       Limit contact        Pause if
                 create unwanted    Medium         frequency, make      complaint/opt-out
                 contact or                        outreach optional,   rate exceeds
                 discounts                         cap incentives       approved threshold

  R7             False negatives    Medium /       Measure recall and   Reassess policy if
                 miss preventable   Medium         opportunity cost;    missed-churn cost
                 churn                             allow                exceeds agreed
                                                   customer-initiated   limit
                                                   support              

  R8             Model/data drift   Unknown / High Monitor feature      Revert to baseline
                                                   distributions,       when agreed drift
                                                   calibration, and     or performance
                                                   outcome rates        thresholds breach

  R9             Automation causes  Low / High     No automated adverse Immediate rollback
                 harmful customer                  action; human review on any automated
                 treatment                         for material         restriction or
                                                   decisions            punitive action

  R10            Security exposure  Medium / High  Minimize,            Incident response
                 of customer                       pseudonymize,        and suspend access
                 identifiers                       encrypt, restrict    on suspected breach
                                                   access, log access   
  -----------------------------------------------------------------------------------------

## Required owners and thresholds

The business owner, data owner, privacy/security reviewer, and
operations lead must be named. Numerical alert thresholds must be agreed
before deployment; none can be responsibly inferred from the supplied
12-row dataset.
