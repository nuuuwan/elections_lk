# Rejected Votes in Sri Lankan Parliamentary Elections

In this analysis, we explore two questions:

- Were rejected votes significantly higher in some election years?
- In particular electoral districts?
- In particular polling divisions?

We exclude results from 2000 because the Election Commission's official results do not contain rejected votes at a polling division level.

## Q1. Were % rejected votes significantly higher or lower in some election years?

Before we answer this question, let's clarify what *significantly higher* and *significantly lower* means.

If the percentage of rejected votes followed the *same pattern* in every election, then any differences we observe would simply be due to random chance. We can estimate what's "normal" by calculating the average (mean) percentage of rejected votes across all elections. If we assume this follows a normal distribution, we can calculate confidence intervals (CIs) that tell us the expected range of values at a certain confidence level (say 95%).

Now, if the percentage of rejected votes for any election year falls outside these confidence intervals, we can conclude that this election's rejection rate was significantly higher or lower than normal.

When we plot the data for election years, we get the following:

![By-Election-Year-1989-2024-LK.png](By-Election-Year-1989-2024-LK.png)

The mean rejection rate across all elections is 5.58%, and the 95% confidence interval ranges from 4.13% to 7.03%.

No election's rejection rate falls outside this range, though 2010 (6.91%) comes close.

Therefore, we can conclude that there is no significant evidence that rejected votes were notably higher or lower in any particular election year.


## Q2. Were rejected votes significantly higher in particular electoral districts?

When we apply the same analysis to electoral districts, we get the following plot.

![By-Ed-1989-2024-EC.png](By-Ed-1989-2024-EC.png)

## Q2. Were rejected votes significantly higher in particular polling divisions?