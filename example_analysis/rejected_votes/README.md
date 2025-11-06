# Rejected Votes in Sri Lankan Parliamentary Elections

In this analysis, we explore two questions:

- Were rejected votes significantly higher in some election years?
- In particular electoral districts?
- In particular polling divisions/postal vote results?

We exclude results from 2000 because the Election Commission's [official results](https://elections.gov.lk/web/wp-content/uploads/election-results/parliamentary-elections/general-election-2000.pdf) do not contain rejected votes at a polling division level.

## Q1. Were % rejected votes significantly higher or lower in some election years?

Before we answer this question, let's clarify what *significantly higher* and *significantly lower* means.

If the percentage of rejected votes followed the *same pattern* in every election, then any differences we observe would simply be due to random chance. We can estimate what's "normal" by calculating the average (mean) percentage of rejected votes across all elections. If we assume this follows a normal distribution, we can calculate confidence intervals (CIs) that tell us the expected range of values at a certain confidence level (say 95%).

Now, if the percentage of rejected votes for any election year falls outside these confidence intervals, we can conclude that this election's rejection rate was significantly higher or lower than normal.

When we plot the data for election years, we get the following:

![By-Election-Year-1989-2024-LK.png](By-Election-Year-1989-2024-LK.png)

The mean rejection rate across all elections is 5.54%, and the 95% confidence interval ranges from 4.11% to 6.97%.

No election's rejection rate falls outside this range, though 2010 (6.91%) comes close.

Therefore, we can conclude that there is no significant evidence that rejected votes were notably higher or lower in any particular election year.


## Q2. Were rejected votes significantly higher in particular electoral districts?

When we apply the same analysis to electoral districts, we get the following plot.

![By-Ed-1989-2024-EC.png](By-Ed-1989-2024-EC.png)

The mean rejection rate across all elections remains unchanged at 5.54%, but the 95% confidence interval is larger, from 3.27% to 7.80%, since we have a different number of samples.

Nuwara Eliya (8.57%), Jaffna (8.39%) and Vanni (7.98%) have % rejected votes above the upper limit of the confidence interval. No electoral district is below the lower limit.

And so, we can conclude that there is evidence (95% condifience), that  Nuwara Eliya , Jaffna  and Vanni have % rejected cotes significantly higher than the limit.


## Q3. Were rejected votes significantly higher in particular polling divisions or postal vote results?

For polling divisions/postal votes, we get this plot. 

![By-Pd-1989-2024-EC.png](By-Pd-1989-2024-EC.png)

As before, the mean rejection rate across all elections remains unchanged at 5.54%, but the 95% confidence interval is even larger, from 2.53% to 8.54%.

Postal Votes for Batticaloa (1.69%), Kegalle (2.48%), and Ratnapura (2.36%) is below the lower limit of the confidence interval. Several results in the Kandy, Matale, Nuwara-Eliya, Jaffna, Vanni, and Badulla electoral districts are above the upper limit of the confidence interval.

Let's visualize these districts in further detail.

### Kandy 

![By-Pd-1989-2024-EC-04.png](By-Pd-1989-2024-EC-04.png)

- Teldeniya (8.82%)

### Matale 

![By-Pd-1989-2024-EC-05.png](By-Pd-1989-2024-EC-05.png)

- Rattota (8.60%)

### Nuwara-Eliya

![By-Pd-1989-2024-EC-06.png](By-Pd-1989-2024-EC-06.png)

- Nuwara Eliya Maskeliya (8.64%)
- Hanguranketha (9.07%)
- Walapane (9.48%)

### Jaffna 

![By-Pd-1989-2024-EC-10.png](By-Pd-1989-2024-EC-10.png)

- Vaddukoddai (9.72%)
- Kankesanthurai (8.57%)
- Kopay (9.04%)
- Udupiddy (8.69%)
- Chavakachcheri (10.10%)
- Kilinochchi (10.27%)

### Vanni 

![By-Pd-1989-2024-EC-11.png](By-Pd-1989-2024-EC-11.png)

- Mullaitivu (10.52%)

### Badulla 

![By-Pd-1989-2024-EC-19.png](By-Pd-1989-2024-EC-19.png)

- Passara (8.85%)

# Concluding Discussion

The following discussion contains speculations and opinions about possible reasons for the observed patterns. These speculations are NOT based on data or rigorous analysis, but rather on contextual knowledge and general observations. They should be viewed as hypotheses that would require further investigation and proper research to validate.

## Summary of Key Findings

The data reveals three notable patterns:

1. **Temporal stability**: Rejection rates have remained relatively consistent across election years (1989-2024), with no individual year showing statistically significant deviation from the mean of 5.54%. The highest rate was in 2010 (6.91%) and the lowest in 2015 (4.42%), but both fall within the 95% confidence interval (4.11% to 6.97%).

2. **Geographic concentration**: Higher rejection rates are concentrated in specific regions:
   - **Northern Province**: Jaffna (8.39%) and Vanni (7.98%) districts significantly exceed the national average
   - **Central Highlands**: Nuwara Eliya (8.57%) leads all districts, followed by Matale (7.50%) and parts of Kandy (6.53%) and Badulla (6.79%)
   - **Lowest rates**: Matara (4.37%), Galle (4.45%), and Colombo (4.50%) show the lowest district-level rejection rates

3. **Postal vote anomaly**: Postal votes consistently show significantly lower rejection rates than their corresponding districts:
   - Batticaloa postal (1.69%) vs district average (6.19%)
   - Ratnapura postal (2.36%) vs district average (5.32%)
   - Kegalle postal (2.48%) vs district average (4.85%)
   - Most districts show postal vote rejection rates between 2-3%, well below the national average of 5.54%

## Possible Explanations (Speculative)

### Why might the Northern Province have higher rejection rates?

The Northern Province, particularly districts like Jaffna, Vanni, Mullaitivu, and Kilinochchi, experienced prolonged civil conflict and displacement. The data shows exceptionally high rates in specific polling divisions:
- Mullaitivu (10.52%) - the highest rate in the country
- Kilinochchi (10.27%)
- Chavakachcheri (10.10%)
- Vaddukoddai (9.72%)

Possible contributing factors could include:

- **Voter unfamiliarity**: Displacement and conflict may have disrupted civic education and voting experience across generations
- **Language and literacy**: Different linguistic contexts might affect ballot comprehension
- **Administrative challenges**: Post-conflict reconstruction may have affected electoral infrastructure and voter education programs
- **Population changes**: Significant displacement and resettlement may have created communities with varying levels of electoral experience

Interestingly, postal votes in both Jaffna (3.01%) and Vanni (3.50%) are significantly lower than their district averages, following the national pattern.

### Why might the Central Highlands have higher rejection rates?

The Central Highlands, particularly the estate sector areas, show elevated rejection rates. Nuwara Eliya district (8.57%) has the highest district-level rate in the country, with several polling divisions showing very high rates:
- Walapane (9.48%)
- Hanguranketha (9.07%)
- Nuwara Eliya-Maskeliya (8.64%)
- Teldeniya in Kandy (8.82%)
- Passara in Badulla (8.85%)

Possible factors include:

- **Socioeconomic factors**: Estate communities have historically faced educational and economic challenges
- **Language barriers**: Tamil-speaking estate communities may face challenges with ballot design or instructions
- **Civic education access**: Geographic isolation and work patterns in estate areas may limit access to voter education
- **Historical context**: Historical disenfranchisement of the estate Tamil community means some areas may have relatively recent voting experience

The contrast is stark: while Nuwara Eliya district shows 8.57%, its postal votes are only 3.39% - less than half the district rate.

### Why might postal votes have lower rejection rates?

The significantly lower rejection rates in postal votes is consistent across almost all districts. The data shows:
- **Lowest postal rates**: Batticaloa (1.69%), Matara (2.30%), Ratnapura (2.36%), Kegalle (2.48%)
- **Typical postal range**: Most districts show postal rates between 2.5-3.5%
- **Largest gaps**: Districts with high regular rates show the biggest postal vote differences
  - Batticaloa: 1.69% (postal) vs 6.19% (district) - a 3.7× difference
  - Nuwara Eliya: 3.39% (postal) vs 8.57% (district) - a 2.5× difference
  - Jaffna: 3.01% (postal) vs 8.39% (district) - a 2.8× difference

Possible explanations include:

- **Education and literacy**: Postal voters (government servants, police, military) may have higher average education levels
- **Time and care**: Postal voting allows more time to carefully complete the ballot compared to polling station voting
- **Assistance and guidance**: Postal voting may involve more administrative support or clearer instructions
- **Sample bias**: The postal vote population is not representative of the general population

The consistency of this pattern across all districts strongly suggests that voter characteristics and voting conditions, rather than geographic or community factors, are the primary drivers of rejection rates.

## Need for Further Research

These observations raise important questions that warrant systematic investigation:

- What role does voter education play in ballot rejection rates?
- How do linguistic and cultural factors affect ballot comprehension?
- What impact does socioeconomic status have on voting accuracy?
- Are there design improvements to ballots that could reduce rejection rates?
- How effective are current voter education programs in different regions?

Understanding these patterns could help election authorities develop targeted interventions to ensure every vote counts and that all communities can participate effectively in the democratic process.

# Appendix: Code & Data used in this Analysis

- [https://github.com/nuuuwan/elections_lk](https://github.com/nuuuwan/elections_lk)

# Appendix: Statistics

## Mean % Rejected by Year

- 1989 (6.13%)
- 1994 (4.80%)
- 2001 (5.23%)
- 2004 (5.47%)
- 2010 (6.91%)
- 2015 (4.42%)
- 2020 (6.03%)
- 2024 (5.65%)

## Mean % Rejected by Electoral District

- Colombo (4.50%)
- Gampaha (4.64%)
- Kalutara (5.55%)
- Kandy (6.53%)
- Matale (7.50%)
- Nuwara-Eliya (8.57%)
- Galle (4.45%)
- Matara (4.37%)
- Hambantota (4.54%)
- Jaffna (8.39%)
- Vanni (7.98%)
- Batticaloa (6.19%)
- Digamadulla (5.11%)
- Trincomalee (5.60%)
- Kurunegala (4.94%)
- Puttalam (6.37%)
- Anuradhapura (5.78%)
- Polonnaruwa (5.38%)
- Badulla (6.79%)
- Moneragala (6.43%)
- Ratnapura (5.32%)
- Kegalle (4.85%)

## Mean % Rejected by Polling Division/Postal Votes

- Colombo North (7.21%)
- Colombo Central (6.62%)
- Borella (5.01%)
- Colombo East (4.86%)
- Colombo West (4.33%)
- Dehiwala (3.75%)
- Ratmalana (4.17%)
- Kolonnawa (4.75%)
- Kotte (3.38%)
- Kaduwela (3.66%)
- Avissawella (5.45%)
- Homagama (4.22%)
- Maharagama (3.34%)
- Kesbewa (3.70%)
- Moratuwa (4.15%)
- Postal Colombo (2.70%)
- Wattala (5.27%)
- Negombo (5.69%)
- Katana (5.15%)
- Divulapitiya (4.92%)
- Mirigama (4.83%)
- Minuwangoda (4.55%)
- Attanagalla (4.89%)
- Gampaha (4.02%)
- Ja Ela (4.27%)
- Mahara (4.29%)
- Dompe (4.35%)
- Biyagama (4.29%)
- Kelaniya (4.79%)
- Postal Gampaha (3.07%)
- Panadura (4.72%)
- Bandaragama (4.95%)
- Horana (5.14%)
- Bulathsinhala (6.99%)
- Mathugama (6.68%)
- Kalutara (5.26%)
- Beruwala (5.51%)
- Agalawatta (6.78%)
- Postal Kalutara (2.71%)
- Galagedara (6.09%)
- Harispattuwa (6.55%)
- Pathadumbara (7.54%)
- Ududumbara (8.51%)
- Teldeniya (8.82%)
- Kundasale (6.38%)
- Hewaheta (7.95%)
- Senkadagala (4.71%)
- Mahanuwara (4.13%)
- Yatinuwara (5.07%)
- Udunuwara (5.84%)
- Gampola (7.73%)
- Nawalapitiya (7.54%)
- Postal Kandy (3.07%)
- Dambulla (7.57%)
- Laggala (7.63%)
- Matale (7.10%)
- Rattota (8.60%)
- Postal Matale (3.30%)
- Nuwara Eliya Maskeliya (8.64%)
- Kothmale (8.01%)
- Hanguranketha (9.07%)
- Walapane (9.48%)
- Postal Nuwara-Eliya (3.39%)
- Balapitiya (4.61%)
- Ambalangoda (4.47%)
- Karandeniya (4.45%)
- Bentara Elpitiya (4.74%)
- Hiniduma (4.87%)
- Baddegama (5.50%)
- Ratgama (4.61%)
- Galle (3.54%)
- Akmeemana (3.87%)
- Habaraduwa (4.48%)
- Postal Galle (2.45%)
- Deniyaya (6.17%)
- Hakmana (5.32%)
- Akuressa (4.42%)
- Kamburupitiya (4.35%)
- Devinuwara (3.59%)
- Matara (3.11%)
- Weligama (4.11%)
- Postal Matara (2.30%)
- Mulkirigala (5.09%)
- Beliatta (4.07%)
- Tangalle (4.37%)
- Thissamaharama (4.81%)
- Postal Hambantota (2.54%)
- Kayts (8.45%)
- Vaddukoddai (9.72%)
- Kankesanthurai (8.57%)
- Manipay (8.41%)
- Kopay (9.04%)
- Udupiddy (8.69%)
- Point Pedro (7.58%)
- Chavakachcheri (10.10%)
- Nallur (6.05%)
- Jaffna (6.43%)
- Kilinochchi (10.27%)
- Postal Jaffna (3.01%)
- Mannar (7.00%)
- Vavuniya (7.97%)
- Mullaitivu (10.52%)
- Postal Vanni (3.50%)
- Kalkudah (6.81%)
- Batticaloa (5.34%)
- Paddiruppu (7.72%)
- Postal Batticaloa (1.69%)
- Ampara (6.05%)
- Samanthurai (4.48%)
- Kalmunai (4.08%)
- Pothuvil (5.04%)
- Postal Digamadulla (4.45%)
- Seruvila (6.21%)
- Trincomalee (5.81%)
- Muttur (5.27%)
- Postal Trincomalee (3.44%)
- Galgamuwa (5.33%)
- Nikaweratiya (6.25%)
- Yapahuwa (5.47%)
- Hiriyala (5.55%)
- Wariyapola (4.91%)
- Panduwasnuwara (4.75%)
- Bingiriya (4.29%)
- Katugampola (4.64%)
- Kuliyapitiya (4.70%)
- Dambadeniya (4.10%)
- Polgahawela (4.61%)
- Kurunegala (4.39%)
- Mawathagama (5.48%)
- Dodangaslanda (6.58%)
- Postal Kurunegala (2.74%)
- Puttalam (7.74%)
- Anamaduwa (7.28%)
- Chilaw (6.00%)
- Nattandiya (5.39%)
- Wennappuwa (5.49%)
- Postal Puttalam (3.13%)
- Medawachchiya (5.90%)
- Horowpothana (5.86%)
- Anuradhapura East (5.02%)
- Anuradhapura West (6.29%)
- Kalawewa (6.01%)
- Mihinthale (6.28%)
- Kekirawa (6.38%)
- Postal Anuradhapura (3.75%)
- Minneriya (5.65%)
- Medirigiriya (4.98%)
- Polonnaruwa (5.65%)
- Postal Polonnaruwa (3.65%)
- Mahiyanganaya (5.45%)
- Viyaluwa (8.11%)
- Passara (8.85%)
- Badulla (5.28%)
- Hali Ela (7.84%)
- Uva Paranagama (7.18%)
- Welimada (6.50%)
- Bandarawela (6.55%)
- Haputale (8.16%)
- Postal Badulla (3.01%)
- Bibile (7.07%)
- Monaragala (7.25%)
- Wellawaya (5.95%)
- Postal Moneragala (3.07%)
- Eheliyagoda (4.89%)
- Ratnapura (4.89%)
- Pelmadulla (6.18%)
- Balangoda (6.33%)
- Rakwana (5.85%)
- Nivithigala (5.32%)
- Kalawana (5.58%)
- Kolonna (4.68%)
- Postal Ratnapura (2.36%)
- Dedigama (4.34%)
- Galigamuwa (4.53%)
- Kegalle (4.17%)
- Rambukkana (4.62%)
- Mawanella (4.56%)
- Aranayaka (5.05%)
- Yatiyanthota (6.59%)
- Ruwanwella (4.70%)
- Deraniyagala (6.34%)
- Postal Kegalle (2.48%)