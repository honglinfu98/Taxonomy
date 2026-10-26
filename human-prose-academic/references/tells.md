# Tells in academic prose

These pairs illustrate a change in style. Use a revision only when it preserves the underlying claim. Numbers and findings below are illustrative.

## Rhetorical setup

| Draft | Plainer version |
|---|---|
| This is not merely an implementation detail; it is a fundamental methodological concern. | The sampling procedure biases the estimate. |
| The explanation is straightforward: both models share the same assumption. | Both models share the same assumption. |
| The estimator is consistent — under the independence assumption — as the sample grows. | Under the independence assumption, the estimator is consistent as the sample grows. |

Keep a contrast when it carries the argument. "The bound holds in expectation, not for every realization" states a mathematical distinction that a shorter positive claim might lose.

## Vocabulary and compounds

| Draft | Plainer version |
|---|---|
| We utilize a regression model to facilitate the analysis. | We fit a regression model. |
| The framework offers a robust, seamless solution. | The method converged in all trials with up to 20% missing observations. |
| This assumption is load-bearing for the proof. | The proof depends on this assumption. |
| Our approach achieves state-of-the-art performance. | Our approach had the lowest mean error among the five methods evaluated. |

The last two performance examples require supporting results. If the draft lacks them, flag the missing evidence rather than manufacture specificity.

Keep "robust regression", "orthogonal vectors", "statistically significant", and other precise terms when they are accurate. Conventional compounds such as "peer-reviewed", "double-blind", "cross-sectional", "well-defined", and "zero-knowledge" carry useful meaning. Decorative compounds such as "ground-breaking" and "best-in-class" usually need evidence or deletion.

The checker reads [wordlist.txt](wordlist.txt). A hit is a request to inspect the usage, never an instruction to replace every occurrence.

## Redundant conclusions

| Draft | Plainer version |
|---|---|
| The error fell from 0.12 to 0.08. Overall, these results demonstrate the effectiveness of our approach. | The error fell from 0.12 to 0.08. |
| The study sampled a single hospital. This means that the study was limited in scope. | The study sampled a single hospital. |

A useful next sentence would identify which inference that sampling choice limits. Keep conclusions that integrate findings or explain consequences the reader has not yet been given.

## Lists and artificial rhythm

"The method is efficient, scalable, and robust" makes three separate claims without giving the reader evidence. Name the properties actually evaluated and report the relevant results. There may be one result or several.

Use prose to connect premises and conclusions. Keep a list for independent assumptions, experimental steps, or research questions that readers need to locate separately.

## Generic future work and review requests

| Draft | More useful feedback |
|---|---|
| Future work should explore broader applications. | Identify the population or setting the current evidence does not cover. |
| The authors should conduct more experiments. | Name the unresolved claim and the comparison needed to assess it. |
| The discussion should be more comprehensive. | Identify the missing interpretation or relevant body of work. |

Do not invent an experiment, limitation, or literature gap to fill a conventional closing paragraph. A review request should explain how the change would help assess the paper's claims.

## Throat clearing and buried verbs

| Draft | Plainer version |
|---|---|
| It is important to note that the estimate depends on the prior. | The estimate depends on the prior. |
| A comparison of the models was performed by the authors. | We compared the models. |
| The implementation of the procedure allows for the estimation of the parameter. | The procedure estimates the parameter. |

"Samples were stored at −80 °C" is a useful passive construction when the actor does not matter. First person should follow the document's conventions.

## Uncertainty and scope

| Draft | Plainer version |
|---|---|
| The results may potentially suggest a possible association. | The results suggest an association. |
| This conclusively proves the method's superiority. | The method had lower error on the evaluated datasets. |

Preserve meaningful uncertainty. An observational association cannot be rewritten as a causal result. A nonsignificant result cannot become proof of no effect. "Significant" should say whether it refers to a statistical test or a practical difference; practical importance needs its own evidence.
