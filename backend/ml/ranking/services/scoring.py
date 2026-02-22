def normalize_rating(rating):
    if rating is None:
        return 0.0
    return min(max(rating / 5.0, 0.0), 1.0)

def normalize_traffic(score):
    if score is None:
        return 0.0
    # traffic_score عندك يبدو 0..100
    return min(max(score / 100.0, 0.0), 1.0)

def budget_penalty(user_budget_level, poi):
    # MVP: ما عندنا سعر POI، فنسوي penalty خفيف حسب category أو نجرب none
    return 0.0
