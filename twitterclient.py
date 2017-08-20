from flask import Flask, jsonify, render_template, request
from twitter_app import MyTwitterApp
# import requests

app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template('index.html')


@app.route("/")
def semantic_analysis():
    twit = MyTwitterApp()
    find_analysis = request.args.get("find_analysis")
    if not find_analysis:
        find_analysis = "Jab Harry Met Sejal Review"

    try:
        tws = twit.get_tweets(find_analysis)
    except Exception:
        return render_template("invalid.html", find_analysis=find_analysis)
    # tws = twit.get_tweet_sentiment(text=find_analysis)
    ptweets = [t for t in tws if t['sentiment'] == 'positive']

    pts = 100 * len(ptweets) / len(tws)
    ntweets = [t for t in tws if t['sentiment'] == 'negative']

    nts = 100 * len(ntweets) / len(tws)
    pt = []
    for t in ptweets[:10]:
        # print(t['text'])
        pt.append(t['text'])
    nt = []
    for t in ntweets[:10]:
        # print(t['text'])
        nt.append(t['text'])

    return render_template('index.html', find_analysis=find_analysis, ptweets=pts, ntweets=nts, pt=pt, nt=nt )

if __name__ == "__main__":
    app.run(debug=True)