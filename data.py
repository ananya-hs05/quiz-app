import requests
def get_question_data(amount=10, category=None, difficulty=None, q_type="boolean"):
    parameters = {
        "amount": amount,
        "type": q_type
    }
    if category:
        parameters["category"] = category
    if difficulty:
        parameters["difficulty"] = difficulty

    response = requests.get("https://opentdb.com/api.php", params=parameters)
    response.raise_for_status()
    data = response.json()
    return data["results"]
