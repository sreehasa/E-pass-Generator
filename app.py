import requests
from flask import Flask, render_template, request
from twilio.rest import Client

account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('login_page.html')


@app.route('/user_registration_dtls', methods=['GET', 'POST'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    # source_dt = request.form['source']
    destination_st = request.form['dest_state']
    # destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    date = request.form['travel']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()

    destination_state_population = json_data[destination_st]["meta"]["population"]
    destination_state_confirmed_cases = json_data[destination_st]["total"]["confirmed"]
    print(destination_state_confirmed_cases / destination_state_population)
    travel_pass = (destination_state_confirmed_cases / destination_state_population) * 100

    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="",
                               from_="",
                               body="Hello " + " " + full_name + " " + "Yours Travel From" + " " +
                                    "To" + " " + "Has" + " " + status + "On" + " " + date + " " + " ,Apply later")

        return render_template('user_registration_dtls.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=destination_st,
                               var5=phoneNumber, var6=date, var7=status)

    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to="",
                               from_="",
                               body="Hello " + " " + full_name + " " + "Yours Travel From" + " " +
                                    "To" + " " + "Has" + " " + status + "On" + " " + date + " " + " ,Apply later")
        return render_template('user_registration_dtls.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=destination_st,
                               var5=phoneNumber, var6=date, var7=status)


if __name__ == "__main__":
    app.run(port=9001, debug=True)
