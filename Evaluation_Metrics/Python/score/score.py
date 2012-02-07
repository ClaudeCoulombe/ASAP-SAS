
"""
Calculates the quadratic weighted kappa inter-rater agreemeent
"""

def confusion_matrix(rater_a, rater_b,
		 min_rating=None, max_rating=None):
    assert(len(rater_a)==len(rater_b))
    if min_rating is None:
        min_rating = min(reduce(min, rater_a), reduce(min, rater_b))
    if max_rating is None:
        max_rating = max(reduce(max, rater_a), reduce(max, rater_b))
    num_ratings = max_rating - min_rating + 1
    conf_mat = [[0 for i in range(num_ratings)]
                for j in range(num_ratings)]
    for a,b in zip(rater_a,rater_b):
        conf_mat[a-min_rating][b-min_rating] += 1
    return conf_mat

def histogram(ratings, min_rating=None, max_rating=None):
    if min_rating is None: min_rating = reduce(min, ratings)
    if max_rating is None: max_rating = reduce(max, ratings)
    num_ratings = max_rating - min_rating + 1
    hist_ratings = [0 for x in range(num_ratings)]
    for r in ratings:
	    hist_ratings[r-min_rating] += 1
    return hist_ratings

def quadratic_weighted_kappa(rater_a, rater_b,
                             min_rating = None, max_rating = None):
    assert(len(rater_a) == len(rater_b))
    if min_rating is None:
	min_rating = min(reduce(min, rater_a), reduce(min, rater_b))
    if max_rating is None:
	max_rating = max(reduce(max, rater_a), reduce(max, rater_b))
    conf_mat = confusion_matrix(rater_a, rater_b,
				     min_rating, max_rating)
    num_ratings = len(conf_mat)
    num_scored_items = float(len(rater_a))

    hist_rater_a = histogram(rater_a, min_rating, max_rating)
    hist_rater_b = histogram(rater_b, min_rating, max_rating)

    numerator = 0.0
    denominator = 0.0

    for i in range(num_ratings):
	for j in range(num_ratings):
	    expected_count = (hist_rater_a[i]*hist_rater_b[j]
			      / num_scored_items) 
	    d = pow(i-j,2.0) / pow(num_ratings-1, 2.0)
	    numerator += d*conf_mat[i][j] / num_scored_items
	    denominator += d*expected_count / num_scored_items

    return 1.0 - numerator / denominator
