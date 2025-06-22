# mock_data/file_storage.py

import json
import os

BASE_PATH = os.path.dirname(__file__)
SCENARIO_FILE = os.path.join(BASE_PATH, "scenarios.json")
BIDS_FILE = os.path.join(BASE_PATH, "bids.json")
EVALUATION_CRITERIA_FILE = os.path.join(BASE_PATH, "evaluation_criteria.json")


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------- 场景管理 ----------

def get_scenario(scenario_id):
    all_data = load_json(SCENARIO_FILE)
    return all_data.get(scenario_id)


def save_scenario(scenario_id, scenario_data):
    all_data = load_json(SCENARIO_FILE)
    all_data[scenario_id] = scenario_data
    save_json(SCENARIO_FILE, all_data)


def list_scenarios():
    return load_json(SCENARIO_FILE)


# ---------- 报价管理 ----------

def get_bids(scenario_id):
    all_data = load_json(BIDS_FILE)
    return all_data.get(scenario_id, {})


def save_bid(scenario_id, student_id, bid_data):
    all_data = load_json(BIDS_FILE)
    if scenario_id not in all_data:
        all_data[scenario_id] = {}
    all_data[scenario_id][student_id] = bid_data
    save_json(BIDS_FILE, all_data)


# ---------- 评估标准管理 ----------

def get_evaluation_criteria(scenario_id):
    all_data = load_json(EVALUATION_CRITERIA_FILE)
    return all_data.get(scenario_id)


def save_evaluation_criteria(scenario_id, criteria_data):
    all_data = load_json(EVALUATION_CRITERIA_FILE)
    all_data[scenario_id] = criteria_data
    save_json(EVALUATION_CRITERIA_FILE, all_data)


def list_evaluation_criteria():
    return load_json(EVALUATION_CRITERIA_FILE)
