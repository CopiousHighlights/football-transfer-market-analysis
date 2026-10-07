# Positional transfer-value ratings

Editorial scouting estimates calibrated to the owner’s references. Weights describe the agreed future rubric; these scores are not weighted statistical model outputs. No subscore or estimated market worth is fabricated. Original source fees, dates and age fields are retained, including known uncertainties.

The original cohort contains 32 historical and 79 summer CDM/deep-midfield records, plus the separate Gross reference. The striker extension adds 55 historical deals, including explicitly labelled mixed-role forwards, and a review queue of all 282 summer Forward records. The winger extension adds 45 historical deals (40 scored, five awaiting evidence) and all 217 summer Winger records as an evidence queue. Summer records in these queues remain unscored because comparable buyer-specific production and cost evidence are incomplete. Broad source labels do not certify exhaustive positional coverage.

Scale: 0.1–10.0, one decimal. Owner scores are retained exactly for the specific deal discussed, never copied to all moves by that player. Historical Rodri→City and summer Casemiro→Inter Miami have separate assistant drafts. Missing fees and loan terms stay unscored. Explicit free transfers may receive a draft but wages and signing costs are unknown. Source fee currencies are kept separate, without unsupported currency conversions. Historical ages come from the source and may contain errors; summer ages are unavailable. Historical outcomes and current scouting judgments are mixed in these discussion drafts, so these are neither pre-transfer predictions nor consistent outcome-model scores. Production, potential and role judgments are provisional.

Weights agreed with owner: production 40%, fee versus worth 30%, potential 15%, age 10%, competition 5%. Subscores are unavailable and have not been reverse-engineered to fit reference ratings. A future statistical model must obtain role-specific per-90 production, valid ages, competition context and independent worth estimates before using this weighted formula.

Draft inference: proposed ratings are qualitative editorial judgments, considering source fee magnitude and available age, role and youth/experience assumptions. A higher number is a proposed better deal, not a verified player ranking. No precision or accuracy validation is claimed.

Review priorities: fee discrepancies (including Rodri 2026), transfer authenticity, ages at signing, role eligibility, performance period, injuries and total acquisition costs. Pascal Groß remains a separate owner reference: Brighton confirms his January 2026 return, but no fee is added to the dataset.


## Excel position framework

Transfer_Ratings is the editable editorial ledger. Position_Rubric contains the agreed CDM weights and proposed production splits for CM, CAM, CB, FB, WB, winger, striker and goalkeeper. Proposed rules are design choices, not validated findings. Rating_Calculator accepts five scores from 0.1 to 10.0 and returns a weighted one-decimal score only when all inputs are numeric, in range and position weights sum to 100%. Existing editorial scores remain separate. Fee basis and evaluation date must be consistent before entering components. Source conflicts remain visible rather than being silently corrected.

Update workflow: edit the ledger / calculator, run the Python pipeline, then rebuild website exports. The original workbook is archived under excel/original. Original charts, formulas and worksheet XML are preserved. Ratings have not yet been added to native Power BI visuals; import the new CSV for a later report page.


## Remaining position extension (7 October 2026)

65 additional historical deals are reviewed: 59 assistant drafts and six entries awaiting transfer/fee-basis evidence. Existing owner scores and previous drafts are unchanged. All 1,493 summer source transfers are now represented, with 915 new midfield/defender/goalkeeper entries left unscored pending role-specific evidence. Broad labels are not guessed into CM, CAM, LB, RB or CB. CM entries already covered in the deep-midfield review are reclassified for filtering without changing their score or original role note. Three Neymar records labelled Midfield in the source are outside the requested roles and remain outside this extension.

The site supports separate CM, CAM, LB, RB, CB and goalkeeper filters and a combined full-back filter. Hybrid classifications are review choices rather than source corrections. Nunes at Wolves is CM; his City review uses RB/utility. For unclassified summer midfielders/defenders, the calculator position selector is blank until a specific role is supported.

See analysis/REMAINING_POSITION_RATINGS.md for every new draft and supporting primary context. Same overall factors apply across positions; detailed production splits remain proposed outside CDM. Components stay blank, and no invented production or acquisition-cost inputs are supplied.
