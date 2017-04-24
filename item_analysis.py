#!/usr/bin/env python
import numpy, d2_items, d2_heroes
import matplotlib.pyplot as plt
from matplotlib import gridspec

debug = True # turn this on to reduce the number of matches read in

# split string into substrings of length n
def split_string(string,n):
    return [string[i:i+n] for i in range(0,len(string),n)]
# end split_string

# parse match info for particular hero
def parse_match_items(match_line,hero_id):
    # note: last char on match_line is a comma
    match = match_line.split(',')[:-1]
    [match_id,match_time,radiant_win,hero_str] = match[:4]
    player_items = [foo.strip() for foo in match[4:]]
    hero_ids = split_string(hero_str,3)
    player_items = [split_string(player_items[i],3) \
                    for i in range(0,len(player_items))]
    if hero_id in hero_ids:
        ind = hero_ids.index(hero_id)
        won = 0
        if (ind < 5 and radiant_win=="True") or \
           (ind >= 5 and radiant_win=="False"):
            won = 1
        items = player_items[hero_ids.index(hero_id)]
        return (won,items)
    return (-1,[])      
# end parse_match_items

# best items for a given hero, based on win rate
def best_item(hero,wins,games,num_games,num_wins,comp_wins,comp_games):
    win_rates = numpy.zeros(len(games))
    for ind,it in numpy.ndenumerate(wins):
        if games[ind] > 0:
            win_rates[ind] = wins[ind] / games[ind]
        else:
            win_rates[ind] = 0
    # figure out win rates when item is not built
    comp_item_wrs = [a/b for a,b in zip(comp_wins,comp_games)]
    items = range(1,len(win_rates)+1)
    # remove under-represented items
    # (defined as being built in fewer than 5% of matches)
    frac_games = [a/(num_games) for a in games]
    win_rates = [a if b>=0.05 else 0 for a,b in zip(win_rates,frac_games)]
    plt.figure(figsize=(10,6))
    gs = gridspec.GridSpec(1,2,width_ratios=[5,2])
    ax1 = plt.subplot(gs[0])
    ax1.bar(items,win_rates,linewidth=0)
    top_items = sorted([(i,a) for i,a in enumerate(win_rates)],\
                        key=lambda x:x[1],reverse=True)
    top_items = top_items[:10]
    ax1text = plt.subplot(gs[1])
    ax1text.axis('off')
    for i,top in enumerate(top_items):
        ax1text.text(0,1.0-(i+1.0)/len(top_items), \
                     "{0:>3} {1} ({2:.1f}% wr, {3:.1f}% adv)" \
                     .format(i+1,d2_items.item_name(top[0]+1),\
                     top[1]*100,top[1]*100-comp_item_wrs[top[0]]*100), \
                     transform=ax1text.transAxes)
    ax1.set_title("Win rates for %s with different items" \
                  % d2_heroes.hero(hero))
    plt.savefig("figures/%s_best_items.pdf" % hero)
    plt.close()
# end best_item

# pairwise item synergies for a given hero
def item_synergies(hero,games,num_games,win_rates):
    x = range(1,len(win_rates)+1)
    # remove under-represented item pairs
    # (defined as being built in fewer than 1% of matches)
    frac_games = games / num_games
    wrs = []
    for ind,wr in numpy.ndenumerate(win_rates):
        if frac_games[ind] < 0.01:
            win_rates[ind] = -1
        else:
            wrs.append(wr)
    # mask items for which we have no data
    win_rates = numpy.ma.masked_less(win_rates,0)
    fig = plt.figure(figsize=(10,6))
    gs = gridspec.GridSpec(1,2,width_ratios=[5,2])
    ax1 = plt.subplot(gs[0])
    mesh = ax1.pcolormesh(x,x,win_rates,cmap='cool')
    cbar = fig.colorbar(mesh,ticks=numpy.arange(\
            0.0,1.1,(max(wrs)-min(wrs))/10.0))
    cbar.set_label("win rate")
    # now list the top 10 synergies to the right of the plot
    # first we need to identify the best item pairs
    wrs = []
    for ind,wr in numpy.ndenumerate(win_rates):
        # only take unique pairs, as (a,b) = (b,a)
        if ind[1]<=ind[0]:
            wrs.append(((ind),wr))
    wrs = sorted(wrs,key=lambda x:x[1],reverse=True)
    wrs = wrs[:10]
    ax1text = plt.subplot(gs[1])
    ax1text.axis('off')
    for i,top in enumerate(wrs):
        ax1text.text(0,1.0-(i+1.0)/len(wrs), \
                     "{0:>3} {1}+{2} ({3:.1f}%)".format( \
                     i+1,d2_items.item_name(top[0][0]+1), \
                     d2_items.item_name(top[0][1]+1),top[1]*100), \
                     transform=ax1text.transAxes)
    ax1.set_title("Item synergies for %s" % d2_heroes.hero(hero))
    plt.savefig("figures/%s_item_synergies.pdf" % hero)
    plt.close()
# end item_synergies

# popular item choices for given hero
def popular_item_choices(hero,games,wins,num_games,num_wins):
    items = range(1,len(games))
    # how often was each item built for any game
    total_freqs = [a/num_games for a in games[1:]]
    # how often was each item built for a won game
    wins_freqs = [a/num_wins for a in wins[1:]]
    # make the figure
    # we're going to list the top 10 items to the right of each plot
    plt.figure(figsize=(10,6))
    gs = gridspec.GridSpec(2,2,width_ratios=[5,2])
    ax1 = plt.subplot(gs[0])
    ax1.bar(items,total_freqs,linewidth=0)
    ax2 = plt.subplot(gs[2])
    ax2.bar(items,wins_freqs,linewidth=0)
    sort_tot_freqs = sorted(zip(items,total_freqs),key=lambda x: x[1],\
                            reverse=True)
    sort_win_freqs = sorted(zip(items,wins_freqs),key=lambda x: x[1],\
                            reverse=True)
    ax1text = plt.subplot(gs[1])
    ax1text.axis('off')
    top_total = sort_tot_freqs[:10]
    for i,top in enumerate(top_total):
        ax1text.text(0,1.0-(i+1.0)/len(top_total), \
                     "{0:>3} {1} ({2:.1f}%)".format( \
                     i+1,d2_items.item_name(top[0]),top[1]*100), \
                     transform=ax1text.transAxes)
    ax2text = plt.subplot(gs[3])
    ax2text.axis('off')
    top_wins = sort_win_freqs[:10]
    for i,top in enumerate(top_wins):
        ax2text.text(0,1.0-(i+1.0)/len(top_wins), \
                     "{0:>3} {1} ({2:.1f}%)".format( \
                     i+1,d2_items.item_name(top[0]),top[1]*100), \
                     transform=ax2text.transAxes)
    ax1.set_title("Popularity of items on %s across all games" \
              % d2_heroes.hero(hero))
    ax2.set_title("Popularity of items on %s across won games" \
              % d2_heroes.hero(hero))
    plt.savefig("figures/%s_item_choices.pdf" % hero)
    plt.close()
# end popular_item_choices

# load data from file for given hero and perform analysis of item choices
def analyze_hero_items(hero,path_to_file):
    # track number of wins and number of games with each item
    # there are 266 unique item_ids in dota 2 (000 is empty)
    # last column will be non-pairwise
    item_wins = numpy.zeros((266,267))
    item_games = numpy.zeros((266,267))
    item_win_rates = numpy.zeros((266,267))
    # also track number of games/wins when a particular item was not built
    comp_item_wins = numpy.zeros(266)
    comp_item_games = numpy.zeros(266)
    num_games = 0
    num_wins = 0
    # load the the data we scraped from the csv file
    with open(path_to_file,'r') as f:
        match_num = 0
        for line in f:
            (won,items) = parse_match_items(line,hero)
            match_num += 1
            if won < 0: # hero not in game
                continue
            for ind1,it1 in enumerate(items):
                for it2 in items[:ind1]+items[ind1+1:]:
                    if won > 0: # game was won
                        item_wins[int(it1),int(it2)] += 1
                    item_games[int(it1),int(it2)] += 1
            for it1 in set(items):
                if won > 0: # game was won
                    item_wins[int(it1),-1] += 1
                item_games[int(it1),-1] += 1
            if won > 0:
                num_wins += 1
            num_games += 1
            for it in range(0,len(comp_item_wins)):
                if "%03d" % it not in items:
                    if won:
                        comp_item_wins[it] += 1
                    comp_item_games[it] += 1
            # if we're debugging, just use the first 5000 matches
            if debug and match_num > 5000:
                break
    for ind,it in numpy.ndenumerate(item_wins):
        if item_games[ind] > 0:
            item_win_rates[ind] = item_wins[ind] / item_games[ind]
        else:
            item_win_rates[ind] = -1
    best_item(hero,item_wins[1:,-1],item_games[1:,-1],num_games,num_wins,\
              comp_item_wins,comp_item_games)
    item_synergies(hero,item_games[1:,1:266],num_games, \
                             item_win_rates[1:,1:266])
    popular_item_choices(hero,item_games[:,-1],item_wins[:,-1], \
                           num_games,num_wins)
# end analyze_hero_items
        
def main():
    for hero in range(114,115):
        # make sure the hero id is valid
        if d2_heroes.hero(hero) == "N/A":
            continue
        print hero
        hero = "%03d" % hero
        analyze_hero_items(hero,"data/matches.csv")
# end main

if __name__ == "__main__":
    main()