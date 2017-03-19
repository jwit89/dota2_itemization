#!/usr/bin/env python
import os, json
import urllib
import time

# read in API key from $D2_API_KEY
API_KEY=os.environ['D2_API_KEY']

# get match info
def get_matches(start_at_match_id=0,end_time=0):
    optional_params = [
                       "key=%s"                    % API_KEY,
                       "start_at_match_seq_num=%d" % start_at_match_id
                      ]
    url = (
           "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory"+
           "BySequenceNum/v1/?"
          )
    url += "matches_requested=100" # max number we can request at a time
    for param in optional_params:
        url += "&"+param
    print start_at_match_id
    try:
        match_list = json.loads(urllib.urlopen(url).read())
        match_list = match_list['result']['matches']
    except ValueError:
        # if the matchmaking server is busy we'll get a value error
        # just wait a bit and try again
        print "Issue pulling %d from server..." % start_at_match_id
        time.sleep(30)
        return start_at_match_id
    # break out if we started with an invalid id
    if not match_list:
        return -1
    for  match in match_list:
        # just look at all pick (game_mode = 1)
        if match['game_mode'] != 1:
            continue
        # make sure there's 10 people (no bots)
        if match['human_players'] != 10:
            continue
        # make sure no one left the game early
        # while we're at it, let's record each players' hero/items
        has_leaver= False
        players = match['players']
        hero_string = ""
        item_strings = []
        for player in players:
            if player['leaver_status'] > 0:
                has_leaver=True
                break
            hero_string += "%03d" % player['hero_id']
            item_strings.append(
                                "%03d" % player['item_0'] +
                                "%03d" % player['item_1'] +
                                "%03d" % player['item_2'] +
                                "%03d" % player['item_3'] +
                                "%03d" % player['item_4'] +
                                "%03d" % player['item_5'] +
                                "%03d" % player['backpack_0'] +
                                "%03d" % player['backpack_1'] +
                                "%03d" % player['backpack_2']
                    )
        if has_leaver:
            continue
        # output looks like
        # match_id, start_time, radiant_win, heroes, items
        # heroes and items are strings of three digit id numbers
        with open("data/matches.csv",'a') as f:
            f.write(str(match['match_id'])+","+
                     str(match['start_time'])+","+
                     str(match['radiant_win'])+","+
                     hero_string+",")
            for item_string in item_strings:
                f.write(item_string+",")
            f.write("\n")
    # increment id at which we should start, or terminate
    if match_list[-1]['start_time'] > end_time: # 3/15/2017
        return -1
    else:
        return match_list[-1]['match_seq_num']+1
# end get_matches
    

# main function
def main():
    start_id = 2619674995 # 02/15/2017
    end_time = 1489620480 # 03/15/2017
    while start_id > 0:
        start_id = get_matches(start_id,end_time)
        time.sleep(1) # wait between api calls
# end main


if __name__ == "__main__":
    main()