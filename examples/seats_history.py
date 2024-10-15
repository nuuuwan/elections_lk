import os
from elections_lk import YEAR_TO_REGION_TO_SEATS
from utils import TSVFile
from gig import Ent
d_list = []
for year, region_to_seats in YEAR_TO_REGION_TO_SEATS.items():
    d = {'year': year}
    for ent_id, seats in region_to_seats.items():
        ent_name = Ent.from_id(ent_id).name
        d[ent_name] = seats
    d_list.append(d)

TSVFile(os.path.join('examples', 'seats_history.tsv')).write(d_list)