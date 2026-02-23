from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

contacts = []
contact_id = 1

# HTML Template (Main Page)
main_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact List App</title>
</head>
<body>

<h2>Add Contact</h2>

<form method="POST" action="/add">
    <input type="text" name="name" placeholder="Enter Name" required>
    <input type="text" name="phone" placeholder="Enter Phone" required>
    <input type="email" name="email" placeholder="Enter Email" required>
    <button type="submit">Add Contact</button>
</form>

<hr>

<h2>Contact List</h2>

<ul>
{% for contact in contacts %}
    <li>
        {{ contact.name }}
        <a href="/contact/{{ contact.id }}">View Details</a>
    </li>
{% endfor %}
</ul>

</body>
</html>
"""

# HTML Template (Details Page)
details_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Contact Details</title>
</head>
<body>

<h2>Contact Details</h2>

<p><strong>ID:</strong> {{ contact.id }}</p>
<p><strong>Name:</strong> {{ contact.name }}</p>
<p><strong>Phone:</strong> {{ contact.phone }}</p>
<p><strong>Email:</strong> {{ contact.email }}</p>

<a href="/">Back</a>

</body>
</html>
"""

# Home - Show List
@app.route('/')
def home():
    return render_template_string(main_page, contacts=contacts)

# Add Contact
@app.route('/add', methods=['POST'])
def add_contact():
    global contact_id

    contact = {
        "id": contact_id,
        "name": request.form['name'],
        "phone": request.form['phone'],
        "email": request.form['email']
    }

    contacts.append(contact)
    contact_id += 1

    return redirect('/')

# View Contact Details
@app.route('/contact/<int:id>')
def contact_details(id):
    for contact in contacts:
        if contact["id"] == id:
            return render_template_string(details_page, contact=contact)
    return "Contact not found"

if __name__ == '__main__':
    app.run(debug=True)