# from DBRet.deploy import *
# from vul_detection.vul_main import *
from flask_cors import CORS  # import flask_cors
from flask import Flask, request, jsonify
app = Flask(__name__)
# from Pipeline_Interface import QAgent_product
# from Configuration import *
# from MainFunctions.TestGenerator import *
# from MainFunctions.TestFix import *
# from MainFunctions.DecisionMaker import *
# from MainFunctions.BugFix import *
from classical.main import main_for_api
# from SearchBasedBugFixing.bugFixLogic import *
CORS(app)  # enable CORS
import subprocess

# def setupQAgent():
#     try:
#         print("All imports successful!")
#         testGenerator = TestGenerator(GenUnitTestChain, db, globals())
#         testRegenerator = TestFix(
#             UnitTestFeedbackChain,
#             globals(),
#             True,
#         )
#         judgeGenerator = DecisionMaker(judgeChain, globals())
#         bugFixGenerator = BugFix(bugFixChain, globals(), True)
#         return testGenerator, testRegenerator, bugFixGenerator, judgeGenerator
#     except Exception as e:
#         print(e)
#         exit(-1)


# testGenerator, testRegenerator, bugFixGenerator, judgeGenerator = setupQAgent()


# @app.route('/qagentai', methods=['POST'])
# def run_python():
#     code = request.json.get('code')
#     description = request.json.get('description')
#     if code:
#         try:
#             # execute the main function
#             print("Running QAgentAI")
#             result = QAgent_product(
#                 code, description, testGenerator, testRegenerator, bugFixGenerator, judgeGenerator)
#             print(result)
#             return jsonify({'output': list(result)})
#         except Exception as e:
#             return jsonify({'error': str(e)}), 400
#     else:
#         return jsonify({'error': 'No code provided'}), 400


# from DBRet import DiskANN,unixcoder
# from DBRet.deploy import *

@app.route('/query', methods=['POST'])
def query():
    try:
        code = request.json['code']
        codes, tests = query_db(code)
        return jsonify({'codes': codes, 'tests': tests})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/vuldetect', methods=['POST'])
def vulDetect():
    try:
        code = request.json['code']
        print(type(code))
        vuls = main_vul(code)
        return jsonify(vuls)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/run-classical', methods=['POST'])
def generate_classical():
    code = request.json.get('code')
    if code:
        try:
            # execute the main function
            result = main_for_api(code)
            print(result)
            return jsonify({'output': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No code provided'}), 400


code = """def simple_function(x, y):
    query = "SELECT * FROM products WHERE id=" +  str(x) + " AND name='" + str(y) + "'"
    query += "'; DROP TABLE users; --"

    a = x + y
    os.system("echo Hello from the system!")
    if x == 0:
        print("x is zero!")
    b = x * y
    c = eval(input("Enter an expression: "))
    return a, b
 """
# print(main_vul(code))

@app.route('/run-fixbugs', methods=['POST'])
def generate_fixbugs():
    # inputs = '[[1, 2],[3, 89]]'
    # outputs = '[[3], [92]]'
    # methodName = 'add'
    # code = 'def add(a, b): return a - b'
    # outputs = bugFix(code, methodName, inputs, outputs)
    # print(outputs)
    code = request.json.get('code')
    inputs = request.json.get('test_cases_inputs')
    # print(inputs)
    for i, input in enumerate(inputs):
        for j, inp in enumerate(input):
            if inputs[i][j].lower() == 'void':
                inputs[i][j] = 'void'
            else:
                inputs[i][j] = eval(inputs[i][j])
            
    outputs = request.json.get('test_cases_outputs')
    for i, output in enumerate(outputs):
        for j, inp in enumerate(output):
            outputs[i][j] = eval(outputs[i][j])
    
    # print(inputs)
    # print(outputs)
    function_name = request.json.get('function_name')
    # print(function_name)
    # print(code)
    if code:
        try:
            try:
                # result = subprocess.run(['ls'])
                result = subprocess.run(["python3", "/root/BugFix/LLM-Test-Generator/SearchBasedBugFixing/main.py", str(code), str(function_name), str(inputs), str(outputs)], capture_output=True, text=True)
                # Access the stdout and stderr attributes of the result
                
                stdout = result.stdout
                print(stdout)
                stderr = result.stderr
                print(stderr)
                
                result = stdout
                print(result)
            except subprocess.CalledProcessError as e:
                print("Error:", e)
            except Exception as e:
                print("Error:", e)
            # try:
            #     outs, errs = p.communicate(timeout=3)
            # except TimeoutExpired:
            #     kill(p.pid)
            #     return -1; # means there is error incurred
            # return 0 # means no error
            # result = bugFix(code, function_name, inputs, outputs)
            # result = main_vul(code)
            print(result)
            if (result == ''):
                return jsonify({'output': 'No Fixes found'})
            return jsonify({'output': result})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No code provided'}), 400

# generate_fixbugs()

if __name__ == '__main__':
    # app.run(port=8080,debug=True, use_reloader=False)
    app.run(port=8080)

