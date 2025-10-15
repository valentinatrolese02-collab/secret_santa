from flask import Flask, request, render_template, abort
import random
import string

app = Flask(__name__)

participants = ["Braggio", "Margherota", "Baratto", "G Galaxy", "Valenushka"]
photos = {
    "Braggio": "braggio.jpg",
    "Margherota": "marghe.jpg",
    "Baratto": "baratto.jpg",
    "G Galaxy": "galaxy.jpg",
    "Valenushka": "vale.jpg"
}


def secret_santa(participants):
    givers = participants[:]
    receivers = participants[:]
    while True:
        random.shuffle(receivers)
        if all(g != r for g, r in zip(givers, receivers)):
            break
    return dict(zip(givers, receivers))

assignments = secret_santa(participants)

# Genera token casuali univoci per ogni partecipante
def generate_token(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

tokens = {participant: generate_token() for participant in participants}
token_to_participant = {v: k for k, v in tokens.items()}

@app.route("/")
def home():
    links = [(p, tokens[p]) for p in participants]
    return render_template("index.html", links=links)


@app.route("/secret/<token>")
def secret(token):
    participant = token_to_participant.get(token)
    if not participant:
        abort(404)
    receiver = assignments[participant]
    receiver_img = photos.get(receiver)
    return render_template("secret.html", participant=participant, receiver=receiver, receiver_img=receiver_img)


if __name__ == "__main__":
    app.run(debug=True)
