import datetime
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    g,
    make_response,
    json,
    session
)
from .scripts.validator import validator
from .scripts.get_first_elem_in_obj import get_first_elem
from .scripts.update_data_by_id import update_data_by_id
from .scripts.delete_data_by_id import delete_data_by_id
from .scripts.read_write_json_file import (
    read_json_file,
    write_json_file
)


users_from_file = 'hexlet-flask-example/users.json'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mdsgfmlkregipj56'
app.permanent_session_lifetime = datetime.timedelta(days=365)


@app.before_request
def before_request():
    g.users = read_json_file(users_from_file)
    if not session.modified:
        session.modified = True


def rewrite_base(data):
    g.users = data
    write_json_file(users_from_file, g.users)


@app.route('/')
def index():
    guest = request.cookies.get('username', default=None)
    if guest is None:
        resp = make_response(redirect(url_for('get_users'), code=322))
        resp.set_cookie('username', 'guest', max_age=3600)
        return resp
    return redirect(url_for('get_users'), code=322)


@app.route('/users')
def get_users():
    user = {'name': '', 'email': ''}
    errors = {}

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('per', 2, type=int)
    offset = (page - 1) * limit
    slice_of_users = g.users[offset:offset + limit]

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if len(slice_of_users) == limit else None

    return render_template(
        'users/show.html',
        user=user,
        users=slice_of_users,
        errors=errors,
        limit=limit,
        page=page,
        prev_page=prev_page,
        next_page=next_page
    )


@app.route('/users/<int:id>')
def get_users_id(id):
    guest = request.cookies.get('username', default=None)
    user = get_first_elem(g.users, id)
    if user is None:
        return 'Page not found', 404
    return render_template(
        'users/show_user_id.html',
        user=user,
        guest=guest), 200


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
    id_user = (len(g.users) or 0) + 1
    new_user = {'id': id_user} | user
    g.users.append(new_user)
    write_json_file(users_from_file, g.users)
    flash('User has been add', 'info')
    return redirect('/users', code=302)


@app.route('/users/<int:id>/edit')
def edit_user(id):
    user = get_first_elem(g.users, id)
    if user is None:
        return 'Page not found', 404
    errors = {}
    return render_template('users/edit_user.html', user=user, errors=errors), 200


@app.route('/users/<int:id>/patch', methods=['POST'])
def patch_user(id):
    user = get_first_elem(g.users, id)
    data_from_form = request.form.to_dict()
    errors = validator(data_from_form)
    if errors:
        return render_template(
            'users/edit_user.html',
            user=user,
            errors=errors), 422

    updated_user, data = update_data_by_id(id, g.users, data_from_form)
    if updated_user:
        rewrite_base(data)
        flash('Данные обновлены', 'success')
        return redirect(url_for('get_users_id', id=id))
    else:
        errors = {}
    return render_template(
        'users/edit_user.html',
        user=user,
        errors=errors), 200


@app.post('/users/<int:id>/delete')
def delete_user(id):
    user = get_first_elem(g.users, id)
    user_id = user['id']
    result, data = delete_data_by_id(user_id, g.users)
    if result:
        rewrite_base(data)
        flash(f'User with id {user_id} has been deleted', 'success')
        return redirect(url_for('get_users'))
    else:
        flash(f'Failed to delete user with id {user_id}', 'error')
        return redirect(url_for('get_users_id', id=user_id))


# Work with cookie
@app.route('/cart')
def show_cart():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    return render_template('courses/cart.html', cart=cart)


@app.post('/add-courses')
def add_courses():
    cart = json.loads(request.cookies.get('cart', json.dumps({})))
    id_course = request.form['item_id']
    name_course = request.form['item_name']

    course = cart.setdefault(id_course, {'name': name_course, 'count': 0})
    course['count'] += 1

    encoding_cart = json.dumps(cart)
    print(encoding_cart)
    response = redirect('/cart')
    response.set_cookie('cart', encoding_cart)
    return response


@app.post('/add-courses/clean')
def clear_cart():
    response = redirect('/cart')
    response.delete_cookie('cart')
    return response
# End work with cookie


# Work with session
@app.route('/registration')
def registration():
    user = {}
    errors = {}
    return render_template(
        'users/registration.html',
        user=user,
        errors=errors
    )


@app.post('/registration/new')
def registration_new():
    new_user = request.form.to_dict()
    errors = validator(new_user)
    if errors:
        return render_template(
            'users/registration.html',
            user=new_user,
            errors=errors), 422
    session['users'] = new_user
    flash('Success', 'success')
    return redirect(url_for('session_hall'))


@app.route('/session_hall')
def session_hall():
    if session.get('users') is None:
        flash('Please register', 'success')
        return redirect(url_for('registration'))
    return render_template('users/session_hall.html', users=session['users'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
