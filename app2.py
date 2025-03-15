from flask import Flask, request, jsonify, send_from_directory, render_template
from io import StringIO
from multiprocessing import Process, Queue
import sys
import back
import time
from threading import Thread

app = Flask(__name__)
sessions = {}  # 存放執行中的程式狀態

class InputNeeded(Exception):
    pass

class OutputWrapper:
    def __init__(self, output_queue):
        self.output_queue = output_queue
    
    def write(self, text):
        if text.strip():  # 避免空內容
            self.output_queue.put({"output": text})
    
    def flush(self):
        pass

class InputMock:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue
    
    def readline(self):
        self.output_queue.put({"needsInput": True})
        return self.input_queue.get() + '\n'

def run_in_process(session_id, code, input_queue, output_queue):
    sys.stdin = InputMock(input_queue, output_queue)
    sys.stdout = OutputWrapper(output_queue)
    try:
        executor = back.Executor()
        executor.execute(code)
        output_queue.put({"completed": True})
    except InputNeeded:
        pass
    except Exception as e:
        output_queue.put({"output": str(e), "completed": True})
    finally:
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__

def output_listener(session_id, output_queue):
    session = sessions[session_id]
    while True:
        try:
            msg = output_queue.get(timeout=0.1)
            if 'output' in msg:
                session["output_buffer"] += msg["output"]
            elif 'needsInput' in msg:
                print("needsInput", msg)
                session["needs_input"] = True
                break
            elif 'completed' in msg:
                session["completed"] = True
                break
        except Exception as e:
            if session['process'].exitcode is not None:
                break

@app.route('/')
def serve_index():
    return render_template('index2.html')

@app.route('/run', methods=['POST'])
def run_code():
    session_id = str(len(sessions))
    input_queue = Queue()
    output_queue = Queue()

    sessions[session_id] = {
        "output_buffer": "",  # 用於儲存輸出內容
        "input_queue": input_queue,
        "output_queue": output_queue,
        "process": None,
        "completed": False,
        "needs_input": False
    }

    p = Process(target=run_in_process, args=(session_id, request.json['code'], input_queue, output_queue))
    sessions[session_id]["process"] = p
    p.start()

    Thread(target=output_listener, args=(session_id, output_queue)).start()

    return jsonify({"sessionId": session_id})

@app.route('/status/<session_id>')
def get_status(session_id):
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    
    response = {
        "output": session["output_buffer"],
        "needsInput": session["needs_input"],
        "completed": session["completed"]
    }
    
    session["output_buffer"] = ""  # 清空緩衝
    
    return jsonify(response)

@app.route('/submit_input', methods=['POST'])
def submit_input():
    session["needs_input"] = True
    data = request.get_json()
    print(data)
    if not data or 'sessionId' not in data or 'input' not in data:
        return jsonify({"error": "無效的請求格式"}), 400

    session_id = data['sessionId']
    user_input = data['input']

    if session_id not in sessions:
        return jsonify({"error": "Session 不存在"}), 404

    session = sessions[session_id]
    if not session.get("needs_input", False):
        return jsonify({"error": "當前不需要輸入"}), 401

    session["input_queue"].put(user_input)  # 將輸入發送到子進程
    print("submit_input")
    session["needs_input"] = False  # 標記輸入已完成

    return jsonify({"message": "輸入已提交"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)
