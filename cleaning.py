import pandas as pd

frame_locs = pd.read_csv("frames.csv")
frame_locs = frame_locs.drop_duplicates(subset="frame", keep="last")
frame_locs.to_csv("frames_cleaned.csv")
