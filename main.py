import random
from flask import Flask, render_template, request
import requests
import smtplib
import os

my_email = "roxxxxxxxxxxxxxm"
my_pass = os.environ.get("SMTP_MAIL_PASS")
receiver_email = "roxxxxxxxxxxxl.com"

response = requests.get("https://api.npoint.io/8ad86e271cd55a4122dc")
drama_data = response.json()

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", all_blog=drama_data)


@app.route("/<path:page>")
def static_page(page):
    return render_template(f"{page}.html")


@app.route("/<int:blog_id>")
def detail_blog(blog_id):
    for blog_detail in drama_data:
        post_id = blog_detail["id"]
        if blog_id == post_id:
            return render_template("post.html", blog_data=blog_detail)


@app.route("/favorite")
def my_favorite_page():
    data = random.sample(drama_data, 10)
    return render_template("index.html", all_blog=data)


@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        user = request.form.get("user_name")
        mail_id = request.form.get("mail")
        phone_num = request.form.get("mobile_num")
        text_messg = request.form.get("sms")

        if len(user) != 0:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(my_email, my_pass)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=receiver_email,
                    msg=f"subject: email from website\n\nuser: {user}\nemail id: {mail_id}\nphone no.{phone_num}\nmessage: {text_messg}"
                )

            return render_template("contact.html", msg_sent=True)
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=False)
