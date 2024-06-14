from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from summary_and_facts import get_summary_and_interesting_facts
load_dotenv()

# Flask web server
app = Flask(__name__)

# Homepage route template to display
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint for process
@app.route("/process", methods=["POST"])
def process():
    # Reference elements in html name element in form
    name = request.form["name"]
    # Pass in name into function
    summary, profile_pic_url, occupation, country  = get_summary_and_interesting_facts(name=name)

    if summary:
        summary_dict = summary.to_dict()
    else:
        summary_dict = {"summary":"No information", "facts": "No information"}
    
    return jsonify(
            {
                "summary_and_facts": summary_dict,
                "picture_url": profile_pic_url,
                "occupation": occupation,
                "country": country
            }
        )

# Launch flask
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)