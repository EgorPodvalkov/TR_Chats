"""Main module that launch webserver for frontend based on Flask"""
# other libs
from flask import Flask, render_template, request, send_file, make_response
# my libs
from myCommonFeatures import log, path

app = Flask("TR chat front")


def generateResponse(data = ""):
    """Returns response with data"""
    response = make_response(data)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/")
def index():
    '''Renders index page on server'''
    return render_template("index.html")


@app.route("/get")
def get_resource():
    '''Gives files to server (res, ava, scr, sty)'''
    file_type = request.args.get("type")
    file_name = request.args.get("name")

    # checking only 3 first symbols of type
    if len(file_type) > 3:
        file_type = file_type[:3]

    # type checking
    TYPES = ["res", "ava", "scr", "sty"]
    if file_type not in TYPES:
        log(f"File type of [red]{file_name}[/red] not founded :(")
        return generateResponse()

    match file_type:
        # resourses
        case "res":
            try:
                file = send_file(path + "resources\\" + file_name)
                log(f"File [green]{file_name}[/green] is loaded! ")
                return file
            except:
                file = send_file(path + "resources\\no_img.png")
                log(f"File [red]{file_name}[/red] not founded :(")
                return file
        # avatars
        case "ava":
            try:
                file = send_file(path + "resources\\avatars\\" + file_name)
                log(f"Avatar [green]{file_name}[/green] is loaded! ")
                return file
            except:
                file = send_file(path + "resources\\no_img.png")
                log(f"Avatar [red]{file_name}[/red] not founded :(")
                return file
        # scripts
        case "scr":
            try:
                file = send_file(path + "scripts\\" + file_name)
                log(f"Script [green]{file_name}[/green] is loaded! ")
                return file
            except:
                log(f"Script [red]{file_name}[/red] not founded :(")
                return generateResponse()
        # style
        case "sty":
            try:
                file = send_file(path + "styles\\" + file_name)
                log(f"Style [green]{file_name}[/green] is loaded! ")
                return file
            except:
                log(f"Style [red]{file_name}[/red] not founded :(")
                return generateResponse()


@app.route("/joinWorkplace")
def join():
    '''Renders join page'''
    workplace_id = request.args.get("workplace_id")

    return render_template("join.html", workplace_id = workplace_id)


app.run(host="0.0.0.0", port=8080, debug=True)
