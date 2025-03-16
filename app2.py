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
            # 在每個輸出後添加換行符
            self.output_queue.put({"output": text.rstrip() + "\n"})
    
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
        # 錯誤訊息也添加換行符
        output_queue.put({"output": str(e) + "\n", "completed": True})
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
            if 'needsInput' in msg:
                print("needsInput", msg)
                session["needs_input"] = True
            if 'completed' in msg:
                session["completed"] = True
                break
        except Exception as e:
            if session['process'].exitcode is not None:
                break
            time.sleep(0.01)

@app.route('/')
def serve_index():
    return render_template('index2.html')

@app.route('/run', methods=['POST'])
def run_code():
    session_id = str(len(sessions))
    input_queue = Queue()
    output_queue = Queue()

    sessions[session_id] = {
        "output_buffer": "",
        "input_queue": input_queue,
        "output_queue": output_queue,
        "process": None,
        "completed": False,
        "needs_input": False
    }

    p = Process(target=run_in_process, args=(session_id, request.json['code'], input_queue, output_queue))
    sessions[session_id]["process"] = p
    p.start()

    listener_thread = Thread(target=output_listener, args=(session_id, output_queue))
    listener_thread.daemon = True
    listener_thread.start()
    sessions[session_id]["listener_thread"] = listener_thread

    return jsonify({"sessionId": session_id})

@app.route('/status/<session_id>')
def get_status(session_id):
    session = sessions.get(session_id)
    if not session:
        return jsonify({"error": "Session not found\n"}), 404
    
    response = {
        "output": session["output_buffer"],
        "needsInput": session["needs_input"],
        "completed": session["completed"]
    }
    
    session["output_buffer"] = ""  # 清空緩衝
    
    return jsonify(response)

@app.route('/submit_input', methods=['POST'])
def submit_input():
    data = request.get_json()
    print("Received input data:", data)
    if not data or 'sessionId' not in data or 'input' not in data:
        return jsonify({"error": "無效的請求格式\n"}), 400

    session_id = data['sessionId']
    user_input = data['input']

    if session_id not in sessions:
        return jsonify({"error": "Session 不存在\n"}), 404

    session = sessions[session_id]
    
    if not session.get("needs_input", False):
        print("Session doesn't need input currently")
        return jsonify({"error": "當前不需要輸入\n"}), 401

    print("Submitting input:", user_input)
    session["input_queue"].put(user_input)
    session["needs_input"] = False

    return jsonify({"message": "輸入已提交\n"})

@app.route('/stop', methods=['POST'])
def stop_execution():
    data = request.get_json()
    if not data or 'sessionId' not in data:
        return jsonify({"error": "無效的請求格式，缺少 sessionId\n"}), 400

    session_id = data['sessionId']
    if session_id not in sessions:
        return jsonify({"error": "Session 不存在\n"}), 404

    session = sessions[session_id]
    
    if session["completed"]:
        return jsonify({"message": "程式已完成，無需停止\n"}), 200

    process = session["process"]
    if process.is_alive():
        process.terminate()
        process.join()
        
        # 在終止訊息後添加換行符
        session["output_buffer"] += "程式已被強制終止\n"
        session["completed"] = True
        session["needs_input"] = False
        
        while not session["input_queue"].empty():
            session["input_queue"].get_nowait()
        while not session["output_queue"].empty():
            session["output_queue"].get_nowait()

        return jsonify({"message": "程式已成功終止\n"}), 200
    
    return jsonify({"message": "程式已在終止過程中\n"}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    