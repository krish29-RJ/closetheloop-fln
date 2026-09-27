#!/usr/bin/env python3
"""
CloseTheLoop - Lightweight Local Prototype Server
==================================================
Runs with zero external dependencies using Python's standard library.
Provides REST API endpoints for:
- CSV Marksheet Ingestion & Validation
- AI Misconception Diagnosis (Claude 3.5 Sonnet Engine Simulation)
- CRC Review & 1-Click Approval
- Mobile Teacher Action Card Delivery & Re-test Signal
- DIET / Block Analytics Dashboard
"""

import http.server
import socketserver
import json
import os
import csv
import io
import urllib.parse
from typing import Dict, List

PORT = 3030

# Sample Assessment Standard Schema
CORRECT_ANSWERS = {
    "Q1": {"problem": "52 - 17", "correct": 35},
    "Q2": {"problem": "60 - 24", "correct": 36},
    "Q3": {"problem": "43 - 8",  "correct": 35},
    "Q4": {"problem": "71 - 39", "correct": 32},
    "Q5": {"problem": "85 - 28", "correct": 57}
}

# State SCERT Activity Bank
TLM_ACTIVITIES = {
    "GROUP_A": {
        "title": "Chalk Floor Number Line & Bead Jump",
        "misconception": "Backward Counting / Off-by-1 or 2 Gap",
        "scert_code": "FLN-NUM-G3-02",
        "duration": "20 mins",
        "tlm_needed": "Chalk, Veranda Floor, 100-Bead Mala",
        "steps": [
            "Draw a 0-100 number line with chalk on the classroom floor.",
            "Have students physically jump backward from 52 by 10s then 1s.",
            "Pair practice: Student A calls a number, Student B jumps backward."
        ],
        "exit_question": "45 - 6 (Solve on floor line)"
    },
    "GROUP_B": {
        "title": "Matchstick Bundles Tens-and-Ones Regrouping",
        "misconception": "Smaller-from-Larger Digit Fallacy (e.g., 52 - 17 = 45)",
        "scert_code": "FLN-NUM-G3-04",
        "duration": "30 mins",
        "tlm_needed": "Matchsticks, Rubber bands (Bundles of 10), Slate & Chalk",
        "steps": [
            "5 min: Represent 52 as 5 bundles of ten and 2 loose sticks.",
            "20 min: Untie 1 bundle into 10 loose sticks to borrow; solve 2 sums on slate together.",
            "5 min: Ask exit blackboard question; mark Completed or Needs Support."
        ],
        "exit_question": "43 - 8 (Solve with matchsticks)"
    },
    "GROUP_C": {
        "title": "Operation Symbol Sorting & Meaning Flashcards",
        "misconception": "Plus / Minus Sign Confusion (+ vs -)",
        "scert_code": "FLN-NUM-G3-01",
        "duration": "20 mins",
        "tlm_needed": "Cardboard Flashcards, Plus/Minus Symbol Cards, Slate",
        "steps": [
            "Show '+' card (Put Together) vs '-' card (Take Away) with physical pebble counts.",
            "Hold up 5 word problems and have children raise the correct sign card.",
            "Solve 3 contrasting problems side-by-side on slate (e.g., 10 + 5 vs 10 - 5)."
        ],
        "exit_question": "20 - 4 (Show sign card first)"
    }
}

# Global In-Memory State for Demo
DEMO_STATE = {
    "students": [],
    "diagnosed_groups": {},
    "crc_approved": False,
    "teacher_tasks": {
        "Group_A": {"status": "Pending", "exit_results": None},
        "Group_B": {"status": "Pending", "exit_results": None},
        "Group_C": {"status": "Pending", "exit_results": None}
    }
}

def analyze_student_responses(rows: List[Dict]) -> Dict:
    """Diagnoses misconceptions from student rows."""
    group_a = []
    group_b = []
    group_c = []
    mastery = []

    for r in rows:
        roll = r.get("roll_no") or r.get("student_id")
        q1 = int(r.get("Q1_52_minus_17", 0))
        q2 = int(r.get("Q2_60_minus_24", 0))
        q3 = int(r.get("Q3_43_minus_8", 0))
        q4 = int(r.get("Q4_71_minus_39", 0))
        q5 = int(r.get("Q5_85_minus_28", 0))

        # Check for mastery
        correct_count = sum([
            q1 == 35, q2 == 36, q3 == 35, q4 == 32, q5 == 57
        ])
        if correct_count >= 4:
            mastery.append({"roll": roll, "score": f"{correct_count}/5"})
            continue

        # Check for sign confusion
        if q1 == 69 or q2 == 84 or q3 == 51:
            group_c.append({"roll": roll, "score": f"{correct_count}/5", "pattern": "Added instead of subtracted"})
        # Check for smaller-from-larger fallacy (52-17=45)
        elif q1 == 45 or q2 == 44 or q3 == 45:
            group_b.append({"roll": roll, "score": f"{correct_count}/5", "pattern": "Subtracted smaller from larger digit (7-2=5)"})
        # Check for number line / counting gap
        else:
            group_a.append({"roll": roll, "score": f"{correct_count}/5", "pattern": "Off-by-1 or 2 in backward counting"})

    return {
        "total_assessed": len(rows),
        "need_remedial_support": len(group_a) + len(group_b) + len(group_c),
        "groups": {
            "Group_A": {
                "name": "Group A: Number Line Gap",
                "count": len(group_a),
                "students": group_a,
                "tlm_activity": TLM_ACTIVITIES["GROUP_A"]
            },
            "Group_B": {
                "name": "Group B: Place Value & Borrowing Gap",
                "count": len(group_b),
                "students": group_b,
                "tlm_activity": TLM_ACTIVITIES["GROUP_B"]
            },
            "Group_C": {
                "name": "Group C: Plus/Minus Sign Confusion",
                "count": len(group_c),
                "students": group_c,
                "tlm_activity": TLM_ACTIVITIES["GROUP_C"]
            }
        },
        "mastery_count": len(mastery),
        "mastery_students": mastery
    }

class PrototypeHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/status":
            self.send_json(DEMO_STATE)
        elif parsed.path == "/api/sample-data":
            # Load default CSV
            csv_path = os.path.join(os.path.dirname(__file__), "sample_class3_subtraction.csv")
            with open(csv_path, "r") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            analysis = analyze_student_responses(rows)
            DEMO_STATE["students"] = rows
            DEMO_STATE["diagnosed_groups"] = analysis
            self.send_json(analysis)
        else:
            # Serve public static files
            if parsed.path == "/" or parsed.path == "":
                self.path = "/public/index.html"
            elif not parsed.path.startswith("/public/"):
                self.path = "/public" + parsed.path
            return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        data = json.loads(body.decode("utf-8")) if body else {}

        if parsed.path == "/api/approve-crc":
            DEMO_STATE["crc_approved"] = True
            self.send_json({"success": True, "message": "CRC Approved. Action Cards dispatched to Teacher WhatsApp/Portal."})

        elif parsed.path == "/api/complete-teacher-task":
            group = data.get("group", "Group_B")
            status = data.get("status", "Completed")
            exit_passed = data.get("exit_passed", 7)
            exit_total = data.get("exit_total", 8)
            DEMO_STATE["teacher_tasks"][group] = {
                "status": status,
                "exit_results": f"{exit_passed}/{exit_total} mastered exit ticket ({round((exit_passed/exit_total)*100)}%)"
            }
            self.send_json({"success": True, "task": DEMO_STATE["teacher_tasks"][group]})

        elif parsed.path == "/api/upload-csv":
            csv_content = data.get("csv_text", "")
            f = io.StringIO(csv_content)
            reader = csv.DictReader(f)
            rows = list(reader)
            analysis = analyze_student_responses(rows)
            DEMO_STATE["students"] = rows
            DEMO_STATE["diagnosed_groups"] = analysis
            DEMO_STATE["crc_approved"] = False
            self.send_json(analysis)
        else:
            self.send_error(404, "Endpoint not found")

    def send_json(self, data: Dict):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

def start_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PrototypeHandler) as httpd:
        print(f"================================================================")
        print(f"🚀 CloseTheLoop Prototype Server Running at:")
        print(f"👉 http://localhost:{PORT}")
        print(f"================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    start_server()
