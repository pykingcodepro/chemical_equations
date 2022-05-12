from flask import Flask, render_template, request
from json_db_tools import ToolBox

app = Flask(__name__)

toolbox = ToolBox('database')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results/', methods = ['POST', 'GET'])
def results():

    comp_json_dict = toolbox.selectAllFrom('compound.json')

    
    eq_json_dict = toolbox.selectAllFrom('equation.json')

    num_dict = []
    for i in range(10):
        num_dict.append(str(i))

    data = {
        "search" : "",
        "comp_json_dict": comp_json_dict,
        "eq_json_dict": eq_json_dict,
        "num_dict": num_dict
    }
    if request.method == "GET":
        data["search"] = request.args['search']
    return render_template('searchedResult.html', data=data)

@app.route('/allEqn/')
def allEqn():

    comp_json_dict = toolbox.selectAllFrom('compound.json')

    eq_json_dict = toolbox.selectAllFrom('equation.json')

    num_dict = []
    for i in range(10):
        num_dict.append(str(i))

    return render_template('allEqn.html', data = { "comp_json_dict": comp_json_dict, "eq_json_dict": eq_json_dict, "num_dict": num_dict, })


@app.route('/admin/')
def admin():
    return render_template('admin.html')

@app.route('/admin/addComp/', methods= ["POST", "GET"])
def addComp():
    if request.method == "POST":
        comp_name = request.form['comp_name']
        comp_symbol = request.form['comp_symbol']
        comp_id = toolbox.selectAllFrom('compound.json')[-1]["comp_id"] + 1
        
        toolbox.insertInto('compound.json', {
            "comp_id": comp_id,
            "name": comp_name,
            "symbol": comp_symbol
        })
    return render_template('addComp.html')

@app.route('/admin/addEqn/', methods= ["POST", "GET"])
def addEqn():
    if request.method == "POST":
        data = request.form

        dataKeys = {
            "reactCompName": [],
            "reactCompMultiplier":[],
            "reactCompState":[],
            "prodCompName": [],
            "prodCompMultiplier":[],
            "prodCompState":[],
        }
        for dataKey in data.keys():
            if "reactCompName" in dataKey:
                dataKeys["reactCompName"].append(dataKey)
            elif "reactCompMultiplier" in dataKey:
                dataKeys["reactCompMultiplier"].append(dataKey)
            elif "reactCompState" in dataKey:
                dataKeys["reactCompState"].append(dataKey)
            elif "prodCompName" in dataKey:
                dataKeys["prodCompName"].append(dataKey)
            elif "prodCompMultiplier" in dataKey:
                dataKeys["prodCompMultiplier"].append(dataKey)
            elif "prodCompState" in dataKey:
                dataKeys["prodCompState"].append(dataKey)
        
        print(len(dataKeys["reactCompName"]))

        insertData = {
            "eq_id": "",
            "eq_name": "",
            "reactant": {
                "compounds": []
            },
            "arrow": {
                "conditions": {},
                "catalyst": [],
                "isReversible": False
            },
            "product": {
                "compounds": []
            },
        }

        comp_data = toolbox.selectAllFrom("compound.json")
        eq_data = toolbox.selectAllFrom("equation.json")


        react_comp_ids = []
        for i in range(len(dataKeys["reactCompName"])):
            for comp in comp_data:
                comp_key = dataKeys["reactCompName"][i]
                if data[comp_key].lower() == comp["symbol"].lower():
                    react_comp_ids.append(comp["comp_id"])
        
        if len(react_comp_ids) == 0:
            return render_template("addEqn.html")

        insertData["eq_id"] = len(eq_data) + 1
        for i in range(len(dataKeys["reactCompName"])):
            react_multi_key = dataKeys["reactCompMultiplier"][i]
            react_state_key = dataKeys["reactCompState"][i]
            insertData["reactant"]["compounds"].append({
                "comp_id": react_comp_ids[i],
                "multiplier": data[react_multi_key],
                "state": data[react_state_key]
            })


        prod_comp_ids = []
        for i in range(len(dataKeys["prodCompName"])):
            for comp in comp_data:
                comp_key = dataKeys["prodCompName"][i]
                if data[comp_key].lower() == comp["symbol"].lower():
                    prod_comp_ids.append(comp["comp_id"])

        if len(prod_comp_ids) == 0:
            return render_template("addEqn.html")

        insertData["eq_id"] = len(eq_data) + 1
        for i in range(len(dataKeys["prodCompName"])):
            prod_multi_key = dataKeys["prodCompMultiplier"][i]
            prod_state_key = dataKeys["prodCompState"][i]
            insertData["product"]["compounds"].append({
                "comp_id": prod_comp_ids[i],
                "multiplier": data[prod_multi_key],
                "state": data[prod_state_key]
            })
        

        toolbox.insertInto("equation.json", insertData)
    return render_template('addEqn.html')


if __name__ == '__main__':
    app.run(debug = True)