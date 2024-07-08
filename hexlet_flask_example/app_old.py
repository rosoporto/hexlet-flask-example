from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from .scripts.get_first_elem_in_obj import get_first_elem
from .scripts.validator import validator
from .scripts.fake_generate import (
    initialize_faker,
    generate_users,
    generate_companies,
    generate_data
)
from .scripts.custom_fake_courses import (
    initialize_custom_faker,
    CourseProvider,
    generate_course
)
from .scripts.read_write_json_file import (
    read_json_file,
    write_json_file
)


SEED = 1234
fake = initialize_faker(SEED)
users = generate_users(20, fake)
companies = generate_companies(100, fake)
domains = generate_data(10, 'domains', fake)
phones = generate_data(10, 'phones', fake)

custom_fake = initialize_custom_faker(CourseProvider, SEED)
courses = generate_course(fake=custom_fake)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mdsgfmlkregipj56'


@app.route('/')
def index():
    return 'go to the /phones or /domains'


@app.route('/phones', methods=['GET'])
def get_phones():
    return jsonify(phones)


@app.route('/domains', methods=['GET'])
def get_domains():
    return jsonify(domains)


@app.get('/courses')
def get_courses():
    return render_template('courses/index.html', courses=courses)


@app.get('/courses/<int:id>')
def get_course(id):
    course = get_first_elem(courses, id)
    if course is None:
        return "Page not found", 404
    return jsonify(course)


@app.get('/companies/<int:id>')
def get_company(id):
    company = get_first_elem(companies, id)
    if company is None:
        return "Page not found", 404
    return jsonify(company), 200


@app.route('/users')
def get_users():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'users/show.html',
        users=sorted(users, key=lambda user: user['id'], reverse=False),
        user=user,
        errors=errors)


@app.route('/users/<int:id>')
def get_users_id(id):
    user = get_first_elem(users, id)
    if user is None:
        return 'Page not found', 404
    return render_template('users/show_user_id.html', user=user), 200


@app.post('/users/new')
def add_new_user():
    user = request.form.to_dict()
    errors = validator(user)
    if errors:
        flash('Data not validated', 'error')
        return render_template(
            'users/show.html',
            user=user,
            errors=errors
        ), 422
    users_from_file = 'hexlet-flask-example/users.json'
    users = read_json_file(users_from_file)
    id_user = (len(users) or 0) + 1
    new_user = {'id': id_user} | user
    users.append(new_user)
    write_json_file(users_from_file, users)
    flash('User has been add', 'info')
    return redirect('/users', code=302)


@app.route('/users/search')
def search_users():
    search_query = request.args.get('search', type=str).lower()
    print(request.args.to_dict())
    found_users = [
            user for user in users if user['first_name'].lower().startswith(search_query)
    ]
    if not found_users:
        found_users = users
    return render_template(
        'users/search_users.html',
        search=search_query,
        found_users=sorted(found_users, key=lambda user: user['id'], reverse=False)
    )