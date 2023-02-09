"""Main module that launch webserver based on Flask"""
# other libs
from flask import Flask, render_template, request, send_file, make_response
# my libs
from myCommonFeatures import log, path

app = Flask("TR chat front")


def generateResponse(data):
    """Returns response with data"""
    response = make_response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/")
def index():
    '''Renders index page on server'''
    return render_template("index.html")


@app.route("/resource")
def get_resource():
    '''Gives files to server'''
    file_name = request.args.get("name")
    file_path = path + "resources\\" + file_name

    try:
        resource = send_file(file_path)
        log(f"File [green]{file_name}[/green] is loaded! ")
        return resource
    except:
        log(f"File [red]{file_name}[/red] not founded :(")
        return generateResponse("")


@app.route("/avatar")
def get_avatar():
    '''Gives avatars to server'''
    file_name = request.args.get("name")
    file_path = path + "resources\\avatars\\" + file_name

    try:
        resource = send_file(file_path)
        log(f"Avatar [green]{file_name}[/green] is loaded! ")
        return resource
    except:
        log(f"Avatar [red]{file_name}[/red] not founded :(")
        return generateResponse("")
    

app.run(host="0.0.0.0", port=8080, debug=True)
