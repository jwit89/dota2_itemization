#!/usr/bin/env python
import numpy, item_analysis
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPClassifier
import random, sys

# parse match info
def parse_match_draft(match_line):
    # note: last char on match_line is a comma
    match = match_line.split(',')[:-1]
    # we don't care about items for this analysis
    [match_id,match_time,radiant_win,hero_str] = match[:4]
    if radiant_win=="True":
        won = 1
    else:
        won = 0
    hero_ids = item_analysis.split_string(hero_str,3)
    return (won,hero_ids)
# end parse_match_draft

# given path to file containing matches, open and read in
def read_matches(path_to_file,sets=1,num_matches=sys.maxint):
    # load the the data we scraped from the csv file
    wins = []
    hero_ids = []
    match_num = 0
    with open(path_to_file,'r') as f:
        for line in f:
            if random.random() > 1.0/sets:
                continue
            match_num += 1
            (won,heroes) = parse_match_draft(line)
            wins.append(won)
            hero_ids.append([int(foo) for foo in heroes])
            if match_num >= num_matches:
                break
    return (wins,hero_ids)
# end read_matches

# build feature vector (assumes no interactions)
def build_features(heroes):
    features = []
    for draft in heroes:
        # 114 possible hero ids
        # 0-113 = radiant, 113-227 = dire
        feature = [0]*228
        # first five are radiant heroes
        for hero in draft[:5]:
            feature[hero-1] = 1
        # last five are dire heroes
        for hero in draft[5:]:
            feature[113+hero] = 1
        features.append(feature)
    return features
# end build_features

# build feature vector of all heroes plus top pairs for each hero
def build_features_pairs(heroes,synergies):
    num_syns = sum([len(foo) for foo in synergies])
    features = []
    for draft in heroes:
        # 114 heroes + num_syns pairs
        # 0-113 = radiant, 114-227 = dire, 228+ = pairs
        feature = [0]*(228 + num_syns)
        # first five are radiant heroes
        for hero1 in draft[:5]:
            feature[hero1-1] = 1
            for hero2 in draft[:5]:
                try:
                    index = 228 + synergies.index(sorted([hero1,hero2]))
                    feature[index] = 1
                except ValueError:
                    # the hero pair is not in the list of synergies
                    pass
        # last five are dire heroes
        for hero1 in draft[5:]:
            feature[hero1-1+114] = 1
            for hero2 in draft[5:]:
                try:
                    index = 228 + synergies.index(sorted([hero1,hero2]))
                    feature[index] = 1
                except ValueError:
                    # the hero pair is not in the list of synergies
                    pass
        features.append(feature)
    return features
# end build_features

# identify top partners for each hero
def top_pairs(heroes,wins,n_top=5):
    partner_wins = numpy.zeros((228,228))
    partner_games = numpy.zeros((228,228))
    num_games = [0]*228
    for i,draft in enumerate(heroes):
        for hi,hero1 in enumerate(draft):
            if hi < 5: # radiant
                num_games[hero1-1] += 1
            else: # dire
                num_games[hero1-1+114] += 1
            for hj,hero2 in enumerate(draft):
                if hi == hj:
                    continue
                if hi < 5 and hj < 5: # radiant
                    if wins[i]:
                        partner_wins[hero1-1][hero2-1] += 1
                    partner_games[hero1-1][hero2-1] += 1
                elif hi > 4 and hj > 4: # dire
                    if not wins[i]:
                        partner_wins[hero1-1+114][hero2-1+114] += 1
                    partner_games[hero1-1+114][hero2-1+114] += 1
    # remove underrepresented hero pairs and calculate win rates
    win_rates = numpy.zeros((228,228))
    top_partners = []
    for i,hero1_games in enumerate(partner_games):
        for j,hero2_games in enumerate(hero1_games):
            win_rates[i][j] = -1.0
            if hero2_games < 0.05*num_games[i]:
                continue
            if partner_wins[i][j] > 0:
                win_rates[i][j] = partner_wins[i][j] / \
                         (0.0 + partner_games[i][j])
        # grab the top n_top from each
        top_partners.append(list(numpy.argsort(win_rates[i])[::-1][:n_top]))
    # top_partners is a list of length 114
    # the ith element is a list of the top 5 partners for hero i+1
    # first remove duplicates
    for hero1,partners in enumerate(top_partners):
        for hero2 in partners:
            if hero1 in top_partners[hero2]:
                top_partners[hero1].remove(hero2)
    # now flatten into a single list
    # make each element [hero1, hero2] with hero1 < hero2
    flattened = []
    for hero1,partners in enumerate(top_partners):
        for hero2 in partners:
            flattened.append(sorted([hero1+1,hero2+1]))
    return flattened
# end top_pairs

# analyze draft
def analyze_draft(how="logreg_mono"):
    num = []
    train_score = []
    test_score = []
    for num_matches in range(100,1001,100)+\
                            range(2000,20000,1000)+\
                                 range(20000,100001,10000)+[125000]:
        (wins,heroes) = read_matches("data/matches.csv", \
            num_matches=num_matches)
        if "logreg" in how: # logistic regression
            if how == "logreg_mono":
                # logistic regression with no interactions
                features = build_features(heroes)
            elif how == "logreg_pairs":
                # logistic regression with top pairwise synergies included
                synergies = top_pairs(heroes,wins)
                features = build_features_pairs(heroes,synergies)
            # split into training and test sets
            feat_train, feat_test, win_train, win_test = \
                train_test_split(features,wins,test_size=0.2)
            # train the model
            model = LogisticRegression()
            model = model.fit(feat_train,win_train)
            # store performance for learning curve
            print num_matches, len(feat_train)
            num.append(len(feat_train))
            train_score.append(model.score(feat_train,win_train))
            test_score.append(model.score(feat_test,win_test))
        elif "k-NN" in how: # nearest neighbors
            features = build_features(heroes)
             # split into training and test sets
            feat_train, feat_test, win_train, win_test = \
                train_test_split(features,wins,test_size=0.2)
            num_neighbors = 11
            #num_neighbors = int(how.split("_")[-1])
            model = KNeighborsClassifier(num_neighbors,weights='uniform',metric=how.split("_")[-1])#,metric=knn_weight,\
                                         #metric_params={'power':4})
            # train the model
            model = model.fit(feat_train,win_train)
            train_sc = accuracy_score(win_train,model.predict(feat_train))
            test_sc = accuracy_score(win_test,model.predict(feat_test))
            print num_matches, len(feat_train), train_sc, test_sc
            num.append(len(feat_train))
            train_score.append(train_sc)
            test_score.append(test_sc)
        elif "neural" in how: # neural network
            features = build_features(heroes)
             # split into training and test sets
            feat_train, feat_test, win_train, win_test = \
                train_test_split(features,wins,test_size=0.2)
            alph = 0.1
            hidden = 15
            model = MLPClassifier(alpha=alph,hidden_layer_sizes=(hidden,))
            # train the model
            model = model.fit(feat_train,win_train)
            # score the model
            train_sc = accuracy_score(win_train,model.predict(feat_train))
            test_sc = accuracy_score(win_test,model.predict(feat_test))
            print num_matches, len(feat_train), train_sc, test_sc
            num.append(len(feat_train))
            train_score.append(train_sc)
            test_score.append(test_sc)
    plt.plot(num,train_score,c='r',label='Train')
    plt.plot(num,test_score,c='b',label='Test')
    plt.legend()
    plt.xlabel("Number of Training Matches")
    plt.ylabel("Model Accuracy")
    plt.title("%s (%.1f%% Train, %.1f%% Test)" % \
              (how,train_score[-1]*100,test_score[-1]*100))
    plt.show()
    plt.savefig("figures/draft_analysis_%s.pdf" % how)
    plt.close()
# end analyze_draft

# custom weight for k-NN
def knn_weight(x,y,**kwargs):
    wt = sum([ int(a) & int(b) for a,b in zip(x,y)])/(0.0 + sum(x)) \
            ** kwargs['power']
    return wt
# end knn_weight

# main function
def main():
    analyze_draft(how="logreg_mono")
    #analyze_draft(how="logreg_pairs")
    #for method in ['jaccard','matching','dice','kulsinski','rogerstanimoto','russellrao','sokalmichener','sokalsneath']:
    #    print method
    #    analyze_draft(how="k-NN-uni_%s" % method)
    #analyze_draft(how="neural_%f_%d" % (alpha,hidden))
    #analyze_draft(how="neural")
# end main


if __name__ == "__main__":
    main()