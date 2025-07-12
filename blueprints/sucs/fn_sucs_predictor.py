from sklearn.ensemble import RandomForestRegressor

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def find_best_level(point, data_dict):
    all_criteria = []
    for record in data_dict.values():
        all_criteria.extend(record['criteria'])

    global_min = min(c['minPoint'] for c in all_criteria)
    global_max = max(c['maxPoint'] for c in all_criteria)

    clamped_point = clamp(point, global_min, global_max)

    for level in all_criteria:
        if level['minPoint'] <= clamped_point <= level['maxPoint']:
            return level['levelName']

    closest_level = None
    smallest_diff = float('inf')
    for level in all_criteria:
        diff = min(abs(clamped_point - level['minPoint']), abs(clamped_point - level['maxPoint']))
        if diff < smallest_diff:
            smallest_diff = diff
            closest_level = level['levelName']

    return closest_level or "Unclassified"

def predict_next_level(data_dict):
    sorted_keys = sorted(data_dict.keys(), key=lambda x: int(x))
    latest_keys = sorted_keys[-5:]

    X, y = [], []

    for idx, key in enumerate(latest_keys):
        record = data_dict[key]
        X.append([idx])
        y.append(record["resultPoint"])

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    next_index = len(X)
    predicted_point = model.predict([[next_index]])[0]

    predicted_level = find_best_level(predicted_point, data_dict)

    return {
        "predicted_point": round(predicted_point, 2),
        "predicted_level": predicted_level
    }
