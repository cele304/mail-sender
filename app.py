from flask import Flask, render_template, request, jsonify
import smtplib
from tkinter import messagebox

app = Flask(__name__)

# Postavi zadani email primatelja
default_to_address = "fcelepirovic30401@outlook.com"

@app.route('/')
def index():
    hide_to_address = True  # Postavite na False ako želite da bude vidljivo
    return render_template('forma.html', default_to_address=default_to_address, hide_to_address=hide_to_address)

# ... ostatak koda ...

@app.route('/send_mail', methods=['POST'])
def send_mail():
    try:
        # Get the email data from the form
        from_address = request.form.get('from_address')
        password = request.form.get('password')
        to_address = request.form.get('to_address') or default_to_address  # Ako je prazno, koristi zadani
        company_name = request.form.get('company_name')
        company_activity = request.form.get('company_activity')
        company_area = request.form.get('company_area')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        subject = request.form.get('subject')
        body = request.form.get('body')

        # Validate the required fields
        if not from_address or not password or not to_address or not company_name or not company_activity or not company_area or not start_date or not end_date or not subject or not body:
            return jsonify({'status': 'error', 'message': 'Please fill in all the fields.'})

        # Connect to the SMTP server
        smtp_server = "smtp.office365.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_address, password)

        # Create the email message
        message = f"Subject: {subject}\n\n"
        message += f"Company Name: {company_name}\n"
        message += f"Company Activity: {company_activity}\n"
        message += f"Company Area: {company_area}\n"
        message += f"Start Date: {start_date}\n"
        message += f"End Date: {end_date}\n\n"
        message += f"{body}"

        # Send the email
        server.sendmail(from_address, to_address, message)

        # Server clean up
        server.quit()

        return jsonify({'status': 'success', 'message': 'Email sent successfully!'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': f'An error occurred: {str(e)}'})

# ... ostatak koda ...


if __name__ == '__main__':
    app.run(debug=True)

