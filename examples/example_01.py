from elections_lk import ElectionPresidential

election_list = ElectionPresidential.list_all()
for election in election_list:
    print(election.year)

latest_election = election_list[-1]
for result in latest_election.results[:10]:
    print(result.id)

borella_result = latest_election.get_result('EC-01C')
print(borella_result.vote_summary)
print(borella_result.party_to_votes)

