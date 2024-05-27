from flask import Flask, flash, render_template, request, redirect, session, url_for
import WorkFunctions as wf
from models.Montage import Montage
from models.Camera import Camera
from models.PostProduction import PostProduction
import saveCond
import loadCond
import os
from functools import wraps


app = Flask(__name__)
app.secret_key = os.urandom(24)

studio = None
film_set = None
director = None
script = None
montage = Montage()
camera = Camera()
post_production = PostProduction()
load_number = 1


@app.route('/')
def index():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    
    # Проверяем размер файла info.pickle
    if os.path.getsize('info.pickle') > 0:
        camera, director, film_set, montage, post_production, script, studio, load_number = loadCond.load_condition() 
    else:
        # Если файл пустой, устанавливаем начальные значения переменных
        camera = Camera()
        director = None
        film_set = None
        montage = Montage()
        post_production = PostProduction()
        script = None
        studio = None
        load_number = 1
    
    if load_number == 1:
        return render_template('index.html')  # Отрисовываем шаблон index.html
    if load_number == 2:
        return redirect(url_for('create_filmset'))
    if load_number == 3:
        return redirect(url_for('create_script'))
    if load_number == 4:
        return redirect(url_for('create_director'))
    if load_number == 5:
        return redirect(url_for('create_actors'))
    if load_number == 6:
        return redirect(url_for('create_shots'))
    if load_number == 7:
        return redirect(url_for('change_number_actors'))
    if load_number == 8:
        return redirect(url_for('make_post_production'))
    if load_number == 9:
        return redirect(url_for('make_realization'))
    
    return render_template('index.html')

@app.route('/create_studio', methods=['GET', 'POST'])
def create_studio():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 1
    message = None
    message_type = None

    if request.method == 'POST':
        studio_name = request.form['studio_name']
        studio_number = int(request.form['studio_number'])
        old_number = int(request.form['old_number'])
        young_number = int(request.form['young_number'])

        try:
            studio = wf.create_studio(studio_name, studio_number, old_number, young_number)
            message = 'Студия успешно создана!'
            message_type = 'success'
            # Перенаправление на страницу создания площадки с передачей сообщения и его типа
            saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 2)
            return redirect(url_for('create_filmset', message=message, message_type=message_type))
        except ValueError as e:
            message = str(e)
            message_type = 'danger'

    return render_template('create_studio.html', message=message, message_type=message_type)



@app.route('/create_filmset', methods=['GET', 'POST'])
def create_filmset():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 2
    message = request.args.get('message')
    message_type = request.args.get('message_type')


    if request.method == 'POST':
        filmset_type = request.form['filmset_type']

        film_set = wf.create_filmset(filmset_type)
        if film_set is not None:
            message = 'Площадка успешно создана!'
            message_type = 'success'
            saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 3)
            return redirect(url_for('create_script', message=message, message_type=message_type))
        else:
            message = 'Ошибка при создании площадки. Пожалуйста, попробуйте еще раз.'
            message_type = 'danger'

    return render_template('create_filmset.html', message=message, message_type=message_type)


@app.route('/create_script', methods=['GET', 'POST'])
def create_script():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 3
    message = None
    message_type = None

    if request.method == 'POST':
        script_name = request.form['name']
        script_type = request.form['type']
        script_person_number = int(request.form['person_number'])
        script_plot = request.form['plot']
        script_experience = int(request.form['experience'])

        try:
            script = wf.create_script(script_name, script_type, script_person_number, script_plot, script_experience, film_set, studio)
            message = 'Сценарий успешно создан!'
            message_type = 'success'
            saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 4)
            return redirect(url_for('create_director'))
        except ValueError as e:
            message = str(e)
            message_type = 'danger'

    return render_template('create_script.html', message=message, message_type=message_type)

@app.route('/create_director', methods=['GET', 'POST'])
def create_director():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 4
    message = request.args.get('message')
    message_type = request.args.get('message_type')

    if request.method == 'POST':
        director_name = request.form['director_name']
        director_exp = int(request.form['director_exp'])

        try:
            director = wf.create_director(director_name, director_exp, script)
            message = 'Директор успешно создан!'
            message_type = 'success'
            saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 5)
            return redirect(url_for('create_actors', message=message, message_type=message_type))
        except ValueError as e:
            message = str(e)
            message_type = 'danger'
    
    return render_template('create_director.html', message=message, message_type=message_type)




@app.route('/create_actors', methods=['GET', 'POST'])
def create_actors():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 5
    message = request.args.get('message')
    message_type = request.args.get('message_type')

    if request.method == 'POST':
        actor_name = request.form['actor_name']
        actor_age = int(request.form['actor_age'])

        try:
            if wf.create_actors(studio, actor_name, actor_age):
                message = 'Актер успешно создан!'
                message_type = 'success'
                if not studio.compare_numbers_people():
                    message = 'Все актеры созданы!'
                    message_type = 'success'
                    saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 6)
                    return redirect(url_for('create_shots', message=message, message_type=message_type))
            else:
                message = 'Невозможно добавить актера!'
                message_type = 'danger'

        except ValueError as e:
            message = str(e)
            message_type = 'danger'

    return render_template('create_actors.html', message=message, message_type=message_type)




@app.route('/create_shots', methods=['GET', 'POST'])
def create_shots():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 6
    message = request.args.get('message')
    message_type = request.args.get('message_type')

    if request.method == 'POST':
        direction = request.form['direction']

        try:
            # Используем функцию create_shots
            if wf.create_shots(camera, montage, direction):
                message = 'Съемка успешно создана!'
                message_type = 'success'
                saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 7)
                return render_template('create_shots.html', message=message, message_type=message_type)
            else:
                saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 7)
                message = 'Невозможно повернуть камеру!'
                message_type = 'danger'
                return render_template('create_shots.html', message=message, message_type=message_type)
        except ValueError as e:
            message = str(e)
            message_type = 'danger'

    return render_template('create_shots.html', message=message, message_type=message_type)


@app.route('/make_post_production', methods=['GET', 'POST'])
def make_post_production():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 8
    num_shots = len(montage.get_shot_list())  # Получаем количество кадров в монтаже
    if request.method == 'POST':
        action = request.form['action']
        pos1 = int(request.form['position'])
        pos2 = request.form.get('new_position')
        if pos2:
            pos2 = int(pos2)
        
        try:
            # Выполнить действие
            if action == 'del':
                # Предполагаем, что wf.make_post_production возвращает True при успешном выполнении
                if wf.make_post_production(post_production, montage, action, pos1):
                    flash(f'Successfully deleted shot at position {pos1}', 'success')
                else:
                    flash(f'Error deleting shot at position {pos1}', 'danger')
            elif action == 'ch':
                if wf.make_post_production(post_production, montage, action, pos1, pos2):
                    flash(f'Successfully moved shot from position {pos1} to {pos2}', 'success')
                else:
                    flash(f'Error moving shot from position {pos1} to {pos2}', 'danger')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
        
        saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 8)
        return redirect(url_for('make_post_production'))

    # Получаем список кадров и их позиций из монтажа
    shots_and_positions = [(shot, i+1) for i, shot in enumerate(montage.get_shot_list())]
    
    return render_template('make_post_production.html', shots_and_positions=shots_and_positions, num_shots=num_shots)




@app.route('/make_realization', methods=['GET', 'POST'])
def make_realization():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    load_number = 9
    if request.method == 'POST':
        wf.make_realization(post_production, studio, script, director, montage)
        return redirect(url_for('index'))

    # Получаем данные для отображения
    script_name = script.get_name()
    script_type = script.get_film_type()
    script_description = script.get_plot()
    participants = studio.get_list_old_persons() + studio.get_list_young_persons()
    montage_shots = montage.get_shot_list()
    saveCond.save_condition(camera=None, director=None, film_set=None, montage=None, post_production=None, script=None, studio=None, load_number=1)

    # Передаем данные в шаблон
    return render_template('make_realization.html', script_name=script_name, script_type=script_type,
                           script_description=script_description, participants=participants,
                           director=director, montage_shots=montage_shots)


@app.route('/change_number_actors', methods=['GET', 'POST'])
def change_number_actors():
    global studio, film_set, director, script, montage, camera, post_production, load_number
    # load_number = 7
    message = None
    message_type = None

    if request.method == 'POST':
        number = int(request.form['number'])
        young_number = int(request.form['young_number'])
        old_number = int(request.form['old_number'])

        # Load necessary dependencies
        # camera, director, film_set, montage, post_production, script, studio, load_number = loadCond.load_condition()
        wf.change_number_actors(studio, number, script, old_number, young_number)
        saveCond.save_condition(camera, director, film_set, montage, post_production, script, studio, load_number = 7)
        
        if studio.compare_numbers_people():
            message = 'Добавьте новых актеров.'
            message_type = 'success'
            return redirect(url_for('create_actors', message=message, message_type=message_type))
        
        return redirect('change_number_actors')
    
    return render_template('change_number_actors.html', message=message, message_type=message_type)


if __name__ == '__main__':
    app.run(debug=True)
    # check_page()
