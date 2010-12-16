from pub4me.models import Pub, PubUser, UserAction_LikedPub, UserAction_GotSuggestion
from math import sqrt

def get_top_matches(pub_user):

	all_pubs = Pub.objects.all()
	ratings = {}
	for pub_user in PubUser.objects.all():
		user = pub_user.user
		liked_pubs = map(lambda lp: lp.pub, UserAction_LikedPub.objects.filter(user = pub_user))
		
		if len(liked_pubs) == 0: 
			continue
		
		ratings[user.username] = {}
		for pub in all_pubs:
			rate_pub(user.username, pub, liked_pubs, ratings)
					
	return get_recommendations(user.username, ratings, sim_distance, 5)
	
	
def rate_pub(username, pub, liked_pubs, ratings):
	#print "%s | %s" % ( pub in liked_pubs, pub, reduce(lambda x,y: x + y, map(lambda p: p.pub.name, liked_pubs)))
	if pub in liked_pubs:
		ratings[username][pub.name] = 1
	else:
		ratings[username][pub.name] = 0
		


def sim_distance(user1, user2, prefs):
    sum_of_pow = sum([pow(prefs[user1][item] - prefs[user2][item], 2)
                      for item in prefs[user1] if item in prefs[user2]])
    return 1.0/(1 + sum_of_pow)

def sim_pearson(user1, user2, prefs):
    n = len(prefs[user1])
    if len(prefs[user2]) != n:
        return -12 # fatal error, kernel panic 
                    # zakladamy ze kazdy ma wszyskie puby w preferencjach
    sum1 = sum([prefs[user1][pub] for pub in prefs[user1]])
    sum2 = sum([prefs[user2][pub] for pub in prefs[user2]])
    
    sum1Sq = sum([pow(prefs[user1][pub], 2) for pub in prefs[user1]])
    sum2Sq = sum([pow(prefs[user2][pub], 2) for pub in prefs[user2]])
    
    sumOfMultipl = sum([prefs[user1][pub]*prefs[user2][pub] 
                        for pub in prefs[user1] if pub in prefs[user2]])
    
    num = sumOfMultipl - (sum1*sum2/n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n)* (sum2Sq - pow(sum2, 2)/n))
    if den == 0: return 0
    
    return num/den

def top_matches(user, prefs, similarity=sim_pearson, n= 5):
    
    matches = [ (similarity(user, match_user, prefs), match_user) 
               for match_user in prefs.keys() if match_user != user]
    
    matches.sort()
    matches.reverse()
    return matches[0:n]



def get_recommendations(user, prefs, similarity=sim_pearson, n= 5):
    totals = {}
    simTotal = {}
    
    for match in prefs.keys():
        
        if match == user: continue
        sim = similarity(user, match, prefs)
        
        if sim <= 0: continue
        
        for pub in prefs[match]:
            if prefs[user][pub] == 0:
                # suma wszystkich polecen
                totals.setdefault(pub, 0)
                totals[pub] += prefs[match][pub]*sim
                #suma zbieznosci
                simTotal.setdefault(pub, 0)
                simTotal[pub] += sim
                
    
    rankings = [ (total/simTotal[pub], pub) for pub, total in totals.items()] 
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]