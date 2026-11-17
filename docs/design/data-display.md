# Data-display standard

**Owner:** numbers, percentages, currencies, dates, identifiers, missing values and chart truthfulness.

## Missing and uncertain values

Do not display unknown or failed lookups as zero. Distinguish measured zero, not applicable and missing/unknown according to the field's actual schema. A null API value does not automatically mean "not applicable"; confirm its semantics before assigning a display label. Aggregates must disclose exclusions that materially affect interpretation.

## Numbers and currency

Use tabular numerals, right-align numeric columns, and preserve underlying precision in storage. Format values for reading without silently changing meaning. In constrained summary cards, abbreviations are acceptable with exact values available; use exact figures in operational tables.

Label currency and units wherever ambiguity exists. Explain denominators on percentages. Distinguish percentage-point changes from relative percentage changes; show precision justified by the source, not artificial decimals.

## Time and identifiers

Store/transmit timestamps in an unambiguous standard such as UTC ISO 8601 and render for the intended viewer with a visible timezone when showing clock times. Dates, deadlines and durations need domain-appropriate timezone handling; do not assume US conventions for every project.

Keep identifiers copyable in full. Abbreviate or truncate only when the complete value remains accessible. Long labels should not destroy layout or hide unique identifiers. Preserve original data in exports.

## Status and charts

Pair status color with clear text or another accessible cue. Use consistent labels for equivalent states. Sort workflow categories by meaningful order, not implementation enum indexes.

Charts need labeled axes, units, dates/range, source, and an accessible interpretation. Bar baselines should ordinarily start at zero; explain deliberate truncation. Use distinguishable categorical colors rather than similar tonal shades and avoid excessive simultaneous series. Respect data uncertainty and missing observations.