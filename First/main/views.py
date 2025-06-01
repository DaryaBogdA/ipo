import json, os
from django.shortcuts import render
from django.conf import settings

def index(request):
    return render(request, 'main/home.html')

def about_i(request):
    return render(request, 'main/about_i.html')

def about_shop(request):
    return render(request, 'main/about_shop.html')

def load_json_data():
    json_path = os.path.join(settings.BASE_DIR, "static", "main", "json", "dump.json")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    skills = [
        {
            "id": item["pk"],
            "title": item["fields"]["title"],
            "code": item["fields"]["code"],
            "desc": item["fields"]["desc"],
            "searchtag": item["fields"]["searchtag"]
        }
        for item in data if item.get("model") == "data.skill"
    ]

    return skills

def spec(request):
    data = load_json_data()
    return render(request, "main/qualification.html", {"skills": data})

def skill_detail(request, skill_id):
    skills = load_json_data()
    skill = next((s for s in skills if s["id"] == skill_id), None)
    return render(request, "main/skill_detail.html", {"skill": skill})







