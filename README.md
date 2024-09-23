# elections_lk

Python Library for Sri Lankan Elections Data.

## Install

```
pip install elections_lk-nuuuwan
```

## Example Usage

```python
from elections_lk import ElectionPresidential


election_list = ElectionPresidential.list_all()
for election in election_list:
    print(election.year)
```

```bash
1982
1988
1994
1999
2005
2010
2015
2019
2024
```

```python
latest_election = election_list[-1]
for result in latest_election.results[:10]:
    print(result.id)
```

```bash
EC-01A
EC-01B
EC-01C
EC-01D
EC-01E
EC-01F
EC-01G
EC-01H
EC-01I
EC-01J
```

```python
borella_result = latest_election.get_result('EC-01C')
print(borella_result.vote_summary)
print(borella_result.party_to_votes)
```

```bash
VoteSummary(electors=62623, polled=46564, valid=45486, rejected=1078)
PartyToVotes(idx={'NPP': 17290, 'SJB': 15497, 'IND16': 10188, 'SLPP': 1101, 'SLCP': 659, 'IND4': 77, 'IND13': 71, 'IND12': 71, 'IND9': 60, 'IND11': 44, 'JPF': 41, 'JSP': 33, 'DUNF': 32, 'SBP': 31, 'RJA': 29, 'IND5': 23, 'NSSP': 23, 'IND1': 18, 'ELPP': 18, 'DUA': 16, 'IND2': 15, 'AJP': 15, 'SPF': 14, 'IND10': 14, 'SEP': 14, 'USP': 13, 'UNFF': 13, 'IND15': 11, 'SLLP': 9, 'IND7': 8, 'APP': 7, 'IND14': 7, 'NIF': 6, 'IND6': 6, 'SLSP': 4, 'NSU': 4, 'NDF': 3, 'IND8': 1})
```
