
from mne_bids import BIDSPath, read_raw_bids
import os
import pandas as pd
import mne

bids_path = BIDSPath(subject='001', 
                     session='001',
                     task='compr',
                     root='~/data/meg_sherlock2')

raw = read_raw_bids(bids_path, verbose=False)


# set MEG data type
new_ch_types = dict()
for i in raw.ch_names:
    if i.startswith('M'):
        new_ch_types[i] = "grad"
        
raw.set_channel_types(new_ch_types)

fn = os.path.join(str(bids_path.directory), "meg", bids_path.basename + '_events.tsv')
ev = pd.read_csv(fn, sep='\t')

words = ev.loc[ev.type == "word_onset_01", :]

ann = mne.Annotations(onset=words.onset.to_list(), 
                      duration=words.duration.to_list(), 
                      description=words.value.to_list())

raw.set_annotations(ann)

events = mne.events_from_annotations(raw, verbose=False)

