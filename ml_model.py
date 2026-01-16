def predict_prob(rating_a, rating_b):
    total = rating_a + rating_b
    if total == 0:
        return 0.5, 0.5
    return rating_a / total, rating_b / total
