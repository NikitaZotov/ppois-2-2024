from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import ForeignKey
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from sqlalchemy.orm import relationship


from forms import ActorForm, DirectorForm, PlatformForm, ScriptForm, StudioForm
from models import db, Studio, Platform, Script, Actor, Director
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    studios = Studio.query.all()
    return render_template('index.html', studios=studios)

@app.route('/add/studio', methods=['GET', 'POST'])
def add_studio():
    form = StudioForm()
    platforms = Platform.query.all()  # Получаем все площадки из базы данных

    if platforms:
        form.platforms.choices = [(platform.id, platform.platform_name) for platform in platforms]
    else:
        form.platforms.choices = []
        form.platforms.render_kw = {'disabled': 'disabled'}  # Делаем поле неактивным, если нет платформ

    if form.validate_on_submit():
        studio = Studio(name=form.name.data)

        # Проверяем, выбрана ли хотя бы одна площадка
        if form.platforms.data:
            selected_platforms = form.platforms.data
            studio.platforms = [Platform.query.get(platform_id) for platform_id in selected_platforms if platform_id]

            # Сохраняем студию в базу данных
            db.session.add(studio)
            db.session.commit()
            flash('Studio added successfully!', 'success')
            return redirect(url_for('index'))
        else:
            # Если не выбрана ни одна площадка, выводим сообщение об ошибке
            flash('Please select at least one platform for the studio', 'error')
    studios = Studio.query.all()  # Получаем список всех студий
    return render_template('studio_form.html', form=form, studios=studios)

@app.route('/edit_studio/<int:studio_id>', methods=['POST'])
def edit_studio(studio_id):
    studio = Studio.query.get_or_404(studio_id)
    new_name = request.form.get('name')
    if new_name:
        studio.name = new_name
        db.session.commit()
        return jsonify({'name': studio.name})
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/delete_studio/<int:studio_id>', methods=['POST'])
def delete_studio(studio_id):
    studio = Studio.query.get_or_404(studio_id)
    db.session.delete(studio)
    db.session.commit()
    return jsonify({'message': 'Studio deleted successfully'})

@app.route('/add/script', methods=['GET', 'POST'])
def add_script():
    form = ScriptForm()
    if form.validate_on_submit():
        script = Script(title=form.title.data,
                        description=form.description.data)
        db.session.add(script)
        db.session.commit()
        flash('Script added successfully!', 'success')
        return redirect(url_for('index'))
    scripts = Script.query.all()
    return render_template('script_form.html', scripts=scripts, form=form)


@app.route('/edit_script/<int:script_id>', methods=['POST'])
def edit_script(script_id):
    script = Script.query.get_or_404(script_id)
    new_title = request.form.get('title')
    new_description = request.form.get('description')
    if new_title and new_description:
        script.title = new_title
        script.description = new_description
        db.session.commit()
        return jsonify({'title': script.title, 'description': script.description})
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/delete_script/<int:script_id>', methods=['POST'])
def delete_script(script_id):
    script = Script.query.get_or_404(script_id)
    db.session.delete(script)
    db.session.commit()
    return jsonify({'message': 'Script deleted successfully'})

@app.route('/add_platform', methods=['GET', 'POST'])
def add_platform():
    form = PlatformForm()
    form.actors.choices = [(actor.id, actor.name) for actor in Actor.query.all()]
    form.scripts.choices = [(script.id, script.title) for script in Script.query.all()]
    form.directors.choices = [(director.id, director.name) for director in Director.query.all()]

    if form.validate_on_submit():
        # Проверка, что по крайней мере один актер, сценарий или режиссер был выбран
        if not form.actors.data or not form.scripts.data or not form.directors.data:
            flash('Please select at least one actor, script, or director.', 'error')
        else:
            platform = Platform(platform_name=form.platform_type.data)
            db.session.add(platform)
            db.session.commit()

            # Получаем выбранных актеров из формы и добавляем их к платформе
            selected_actors_ids = form.actors.data
            selected_actors = Actor.query.filter(Actor.id.in_(selected_actors_ids)).all()
            platform.actors.extend(selected_actors)

            # Получаем выбранные сценарии из формы и добавляем их к платформе
            selected_scripts_ids = form.scripts.data
            selected_scripts = Script.query.filter(Script.id.in_(selected_scripts_ids)).all()
            platform.scripts.extend(selected_scripts)

            # Получаем выбранных режиссеров из формы и добавляем их к платформе
            selected_directors_ids = form.directors.data
            selected_directors = Director.query.filter(Director.id.in_(selected_directors_ids)).all()
            platform.directors.extend(selected_directors)

            db.session.commit()

            flash('Platform added successfully!', 'success')
            return redirect(url_for('index'))
    else:
        # Инициализация выбора актеров, сценариев и режиссеров
        form.actors.choices = [(actor.id, actor.name) for actor in Actor.query.all()]
        form.scripts.choices = [(script.id, script.title) for script in Script.query.all()]
        form.directors.choices = [(director.id, director.name) for director in Director.query.all()]

    platforms = Platform.query.all()
    return render_template('platform_form.html', platforms=platforms, form=form)

@app.route('/edit_platform/<int:platform_id>', methods=['POST'])
def edit_platform(platform_id):
    platform = Platform.query.get_or_404(platform_id)
    new_name = request.form.get('platform_name')
    new_actors = request.form.getlist('actors')
    new_scripts = request.form.getlist('scripts')
    new_directors = request.form.getlist('directors')

    if new_name:
        platform.platform_name = new_name
        
    if new_actors:
        platform.actors = Actor.query.filter(Actor.id.in_(new_actors)).all()
    if new_scripts:
        platform.scripts = Script.query.filter(Script.id.in_(new_scripts)).all()
    if new_directors:
        platform.directors = Director.query.filter(Director.id.in_(new_directors)).all()

    db.session.commit()
    return jsonify({'platform_name': platform.platform_name})


@app.route('/delete_platform/<int:platform_id>', methods=['POST'])
def delete_platform(platform_id):
    platform = Platform.query.get_or_404(platform_id)
    db.session.delete(platform)
    db.session.commit()
    return jsonify({'message': 'Platform deleted successfully'})

@app.route('/add/director', methods=['GET', 'POST'])
def add_director():
    form = DirectorForm()
    if form.validate_on_submit():
        director = Director(name=form.name.data)
        db.session.add(director)
        db.session.commit()
        flash('Director added successfully!', 'success')
        return redirect(url_for('index'))
    directors = Director.query.all()
    return render_template('director_form.html', directors=directors, form=form)


@app.route('/edit_director/<int:director_id>', methods=['POST'])
def edit_director(director_id):
    director = Director.query.get_or_404(director_id)
    new_name = request.form.get('name')
    if new_name:
        director.name = new_name
        db.session.commit()
        return jsonify({'name': director.name})
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/delete_director/<int:director_id>', methods=['POST'])
def delete_director(director_id):
    director = Director.query.get_or_404(director_id)
    db.session.delete(director)
    db.session.commit()
    return jsonify({'message': 'Director deleted successfully'})

@app.route('/add/actor', methods=['GET', 'POST'])
def add_actor():
    form = ActorForm()
    if form.validate_on_submit():
        actor = Actor(name=form.name.data)
        db.session.add(actor)
        db.session.commit()
        flash('Actor added successfully!', 'success')
        return redirect(url_for('index'))
    
    actors = Actor.query.all()
    return render_template('actor_form.html', actors=actors, form=form)

@app.route('/edit_actor/<int:actor_id>', methods=['POST'])
def edit_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    new_name = request.form.get('name')
    if new_name:
        actor.name = new_name
        db.session.commit()
        return jsonify({'name': actor.name})
    return jsonify({'error': 'Invalid input'}), 400

@app.route('/delete_actor/<int:actor_id>', methods=['POST'])
def delete_actor(actor_id):
    actor = Actor.query.get_or_404(actor_id)
    db.session.delete(actor)
    db.session.commit()
    return jsonify({'message': 'Actor deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
