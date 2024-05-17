from flask import Flask, request, jsonify
from Pipeline_Interface import QAgent_product
app = Flask(__name__)
from flask_cors import CORS  # import flask_cors
# from Configuration import *
# from MainFunctions.TestGenerator import *
# from MainFunctions.TestFix import *
# from MainFunctions.DecisionMaker import *
# from MainFunctions.BugFix import *
from vul_detection.vul_main import *

from DB.deploy import *
CORS(app)  # enable CORS


def setupQAgent():
    try:
        print("All imports successful!")
        testGenerator = TestGenerator(GenUnitTestChain, db, globals())
        testRegenerator = TestFix(
            UnitTestFeedbackChain,
            globals(),
            True,
        )
        judgeGenerator = DecisionMaker(judgeChain, globals())
        bugFixGenerator = BugFix(bugFixChain, globals(), True)
        return testGenerator, testRegenerator, bugFixGenerator, judgeGenerator
    except Exception as e:
        print(e)
        exit(-1)

testGenerator, testRegenerator, bugFixGenerator, judgeGenerator = setupQAgent()

@app.route('/run-qagentai', methods=['POST'])
def run_python():
    code = request.json.get('code')
    description = request.json.get('description')
    if code:
        try:
            # execute the main function
            print("Running QAgentAI")
            result = QAgent_product(code, description, testGenerator, testRegenerator, bugFixGenerator, judgeGenerator)
            print(result)
            return jsonify({'output': list(result)})
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'error': 'No code provided'}), 400

# from DBRet import DiskANN,Graph,unixcoder
from DBRet.deploy import *
@app.route('/query', methods=['POST'])
def query():
    try: 
        
        code = request.json['code']
        codes,tests = query_db(code)
        return jsonify({'codes': codes, 'tests': tests}) 
    except Exception as e:
        return jsonify({"error":str(e)})

if __name__ == '__main__':
    app.run(port=8080)