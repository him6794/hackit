import sys
import back
from flask import Flask, request, jsonify, send_from_directory
from io import StringIO

app = Flask(__name__, template_folder='templates')
sessions = {}  # 存放執行中的程式狀態

class InputNeeded(Exception):
    """ 自定義異常，用於標記需要輸入的情況 """
    pass

class InputMock:
    """ 模擬 input() 來攔截 back.py 的輸入 """
    def __init__(self, session_id):
        self.session_id = session_id
        self.buffer = None  # 存放使用者的輸入
    
    def readline(self):
        """ 模擬 input()，若無輸入則拋出異常 """
        if self.buffer is None:
            raise InputNeeded()
        user_input = self.buffer
        self.buffer = None
        return user_input + '\n'

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index2.html')

@app.route('/run', methods=['POST'])
def run_code():
    """ 開始執行程式 """
    session_id = str(len(sessions))  # 產生唯一的 session ID
    sessions[session_id] = {
        "code": request.json['code'],
        "completed": False,
        "output": "",
        "input_mock": InputMock(session_id),
    }
    return execute_code(session_id)

@app.route('/submit_input', methods=['POST'])
def submit_input():
    """ 接收使用者的輸入並繼續執行 """
    session_id = request.json['sessionId']
    user_input = request.json['input']
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 400
    sessions[session_id]["input_mock"].buffer = user_input
    return execute_code(session_id)

def execute_code(session_id):
    """ 執行程式碼並處理輸入需求 """
    session = sessions[session_id]
    sys.stdin = session["input_mock"]
    sys.stdout = StringIO()
    try:
        back.execute(session["code"])
        output = sys.stdout.getvalue()
        session["output"] += output
        session["completed"] = True
        return jsonify({"sessionId": session_id, "output": output, "needsInput": False})
    except InputNeeded:
        output = sys.stdout.getvalue()
        session["output"] += output
        return jsonify({"sessionId": session_id, "output": output, "needsInput": True})
    except Exception as e:
        return jsonify({"sessionId": session_id, "output": str(e), "needsInput": False})
    finally:
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)