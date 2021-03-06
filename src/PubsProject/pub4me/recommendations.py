from pub4me.models import Pub, PubUser, UserAction_LikedPub, UserAction_GotSuggestion
from django.contrib.auth.models import User
from math import sqrt
from django.core.cache import cache

# pobiera liste wszystkich wybranych przez usera pub'ow
# ustawia im ocene na 1 i porownuje z lista zcache'owanych ocen innych uzytkownikow
def get_top_matches( liked_pubs):
#	user = pub_user.user
#	liked_pubs = {}
#	for pub in UserAction_LikedPub.objects.filter(user = pub_user):
#		liked_pubs[pub.pub.name] = 1

	return get_recommended_pubs(liked_pubs, get_pub_matches_data_set(), 5)

# sprawdza czy jest w cache'u lista pubow podobnych do danego pubu
# wg ocen dotychczasowych uzytkownikow
# jezeli jest to pobieramy ja i zwracamy, jezeli nie to tworzymy nowa
def get_pub_matches_data_set():
	pub_ratings = cache.get('pub_ratings', None) # returns None if empty or expired
	if pub_ratings == None:
		pub_ratings = refresh_cache()
		#pub_ratings = calculate_similar_pubs(get_pub_rating(), n=5)
		#cache.set('pub_ratings', pub_ratings)
	return pub_ratings

def refresh_cache():
	pub_ratings = calculate_similar_pubs(get_pub_rating(), n=5)
	cache.set('pub_ratings', pub_ratings)
	return pub_ratings


#user ratings prefs[username]
#pub_match_list => pub oriented best matches for each pub
# user_ratings => puby ktore lubi user {nazwa_pubu: 1 }
# pub_match_list => lista pubow oraz n najbardziej podobnych do danego pubu {pub_name: [ (similarity1, pub1), (similarity2, pub2), itp]}
def get_recommended_pubs(user_ratings, pub_match_list, n = 10):
    scores = {}
    total_sim = {}
    
    #po wszystkich wybranych pubach
    for (pub, rating) in user_ratings.items():
        
        # iterujemy po wszystkich pubach najbardziej przypominjacych ten pub (top matches)
        for (similarity, match_pub) in pub_match_list[pub]:
            
            #jezeli ten pub zostal juz wybrany przez tego user to pomijamy
            # !!!!!!!!!!!!!!!!!! moze powinnismy to gdzies zapisac??
            if match_pub in user_ratings: continue
            
            scores.setdefault(match_pub, 0)
            #czyli wyliczamy iloczyn tego jak nam sie podobal dany PUB oraz tego jak bardzo MATCH_PUB jest do niego podobny
            # zapisujemy pod match_pub
            scores[match_pub] += similarity*rating
            
            total_sim.setdefault(match_pub, 0)
            #i dla kazdego MATCH_PUB zapisujemy sume jego podobiestw do naszego PUB
            total_sim[match_pub] += similarity
            
    # zapisujemy iloraz iloczynu podobienstwa i tego jak dany pub nam sie podobal dzielonego
    # przez sume wszystkich podobienstw do tego pubu   
    rankings = [(score/total_sim[pub], pub) for pub, score in scores.items()]
    
    #sortujemy i zwracamy najlepsze wyniki
    rankings.sort()
    rankings.reverse()
    return rankings[0:n]

# tworzy liste wszystkich pub'ow i ich notowan dla kazdego uzytkownika
# jezeli uztkownik kiedys wybral ten pub to przypisujemy mu 1
# jezeli nie to 0
def get_pub_rating():
	rating = {}
	for pub in Pub.objects.filter(active = True):
		rating.setdefault(pub.name, {})
#TODO zoptymalizowac bo to troche rozrzutne	
		for user in User.objects.all():
			rating[pub.name][user.username] = 0
		
		for rated_pub in pub.useraction_likedpub_set.all():
			rating[pub.name][rated_pub.user.user.username] = 1
	
#		for rated_pub in pub.useraction_likedpub_set.all():
#			rating[pub.name][rated_pub.user.user.username] = 2
			
	return rating
		
def rate_pub(username, pub, liked_pubs, ratings):
	#print "%s | %s" % ( pub in liked_pubs, pub, reduce(lambda x,y: x + y, map(lambda p: p.pub.name, liked_pubs)))
	if pub in liked_pubs:
		ratings[username][pub.name] = 1
	else:
		ratings[username][pub.name] = 0
		


def sim_distance(user1, user2, prefs):
    sum_of_pow = sum([pow(prefs[user1][item] - prefs[user2][item], 2)
                      for item in prefs[user1] if item in prefs[user2]])
    if sum_of_pow == 0: return 0
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

# oblicza najbardziej podobne wyniki dla danego obiektu 
# obliczajac jego oleglosc od wszystkich innych obietkow w kolekcji preferencji uzytkownikow
# zwraca n najblizszych wynikow (tych o najmniejszej odleglosci, najwyzszej similarityy)
# pobiera sposob liczenia odleglosci: 
def top_matches(pub_liked_by, prefs, similarity=sim_pearson, n= 5):
    
    matches = [ (similarity(pub_liked_by, pub, prefs), pub) 
               for pub in prefs.keys() if pub != pub_liked_by]
    
    matches.sort()
    matches.reverse()
    return matches[0:n]


def transform_prefs(prefs):
	result = {}
	for user in prefs:
		for pub in prefs[user]:
			result[pub][user] = result[user][pub]
	
	return result


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
   
def transform_prefs(prefs):
    result = {}
    for user in prefs:
        for pub in prefs[user]:
            result.setdefault(pub, {})
            result[pub][user] = prefs[user][pub]
    
    return result

#Buduje liste n najbardziej podobnych pubow do kazdego pubu 
# i zwraca slownik z najlepszymi dopasowaniami    
# korzystamy z Euclidesowskiej definicjie odleglosci
#zakladamy ze prefs sa juz Pub oriented tzn wywolania sa z calculate_similar_pubs(transform_prefs(prefs))
def calculate_similar_pubs(prefs, n=10):
    result = {}
    for pub in prefs:
        scores = top_matches(pub, prefs, n=n, similarity=sim_distance)
        result[pub] = scores
    return result
   

