init python:
    import random
    
    class ShakeTransform(object):
        def __init__(self, period=0.05, strength=10):
            self.period = period
            self.strength = strength
            self.time = 0
            
        def __call__(self, trans, st, at):
            self.time += st
            if self.time >= self.period:
                self.time = 0
                trans.xoffset = random.randint(-self.strength, self.strength)
                trans.yoffset = random.randint(-self.strength, self.strength)
            else:
                trans.xoffset = 0
                trans.yoffset = 0
            return 0

    def show_dramatic_text(text_content, duration=2.0, text_size=50, shake_power=10):
        renpy.music.stop(fadeout=0.5)
        renpy.scene()
        renpy.show("black")
        renpy.with_statement(Dissolve(0.5))
        renpy.pause(0.5)

        screen_text = Text(
            text_content,
            color="#ff0000",
            size=text_size,
            xalign=0.5,
            yalign=0.5,
            outlines=[(2, "#000000", 0, 0)]
        )
        
        renpy.show_screen("shake_screen", text_obj=screen_text, shake_power=shake_power)
        renpy.pause(duration)
        renpy.hide_screen("shake_screen")
        renpy.with_statement(Dissolve(0.5))

screen shake_screen(text_obj, shake_power):
    add text_obj at transform:
        function ShakeTransform(strength=shake_power)
        xalign 0.5
        yalign 0.5

define v = Character("Голос")
define y = Character("Вы")

default unlocked_levels = 1
default completed_levels = 0
default levels_data = {}
default hints_used = 0
default max_hints = 3
default last_rest_level = 0
default current_level = 1
default hints_pool = []

init python:
    def load_hints_from_file():
        hints = []
        try:
            with renpy.file("hints.txt") as f:
                for line in f:
                    line = line.decode('utf-8').strip()
                    if line and not line.startswith("#"):
                        hints.append(line)
        except:
            hints = [
                "Иногда ответ кроется в самом вопросе",
                "Попробуйте посчитать буквы",
                "Обратите внимание на числа",
                "Возможно, нужен нестандартный подход",
                "Подумайте о противоположностях"
            ]
        return hints

    def load_levels_from_file():
        levels = {}
        try:
            with renpy.file("levels.txt") as f:
                for line in f:
                    line = line.decode('utf-8').strip()
                    if not line or line.startswith("#"):
                        continue
                    
                    parts = line.split("|")
                    if len(parts) >= 6:
                        level_num = int(parts[0])
                        difficulty = parts[1]
                        level_name = parts[2]
                        level_task = parts[3]
                        level_answer = parts[4].lower()
                        level_hint = parts[5]
                        
                        levels[level_num] = {
                            "number": level_num,
                            "difficulty": difficulty,
                            "name": level_name,
                            "task": level_task,
                            "answer": level_answer,
                            "hint": level_hint,
                            "completed": False
                        }
        except:
            for i in range(1, 26):
                if i <= 9:
                    diff = "e"
                    name = f"Уровень {i}"
                    task = f"Задача уровня {i} (легкая)"
                elif i <= 19:
                    diff = "m"
                    name = f"Уровень {i}"
                    task = f"Задача уровня {i} (средняя)"
                else:
                    diff = "h"
                    name = f"Уровень {i}"
                    task = f"Задача уровня {i} (сложная)"
                
                levels[i] = {
                    "number": i,
                    "difficulty": diff,
                    "name": name,
                    "task": task,
                    "answer": str(i),
                    "hint": f"Подсказка для уровня {i}",
                    "completed": False
                }
        
        return levels
    
    def get_difficulty_color(difficulty):
        if difficulty == "e":
            return "#00FF00"
        elif difficulty == "m":
            return "#FFFF00"
        else:
            return "#FF0000"
    
    def get_level_scene(level_num):
        if level_num <= 9:
            return "bg puzzle_room_easy"
        elif level_num <= 19:
            return "bg puzzle_room"
        else:
            return "bg puzzle_room_hard"
    
    def get_difficulty_text(level_num):
        if level_num <= 9:
            return "Легкий"
        elif level_num <= 19:
            return "Средний"
        else:
            return "Сложный"
    
    def check_answer(user_answer, correct_answer):
        user_answer = user_answer.lower().strip()
        correct_answer = correct_answer.lower().strip()
        
        if user_answer == correct_answer:
            return True
        
        try:
            if float(user_answer) == float(correct_answer):
                return True
        except:
            pass
        
        return False
    
    def update_level_progress(level_num):
        if level_num in levels_data:
            levels_data[level_num]["completed"] = True
        
        new_completed = 0
        for i in range(1, 26):
            if i in levels_data and levels_data[i]["completed"]:
                new_completed = i
            else:
                break
        
        store.completed_levels = new_completed
        
        if store.unlocked_levels < store.completed_levels + 1 and store.unlocked_levels < 25:
            store.unlocked_levels = min(store.completed_levels + 1, 25)

label start:
    play music "menu.mp3"
    scene bg castle with dissolve
    v "Приветствую, путник."
    
    $ levels_data = load_levels_from_file()
    $ hints_pool = load_hints_from_file()

label important_choice:
    menu:
        v "Вы готовы?"
        
        "Да.":
            stop music fadeout 1.0
            "Прекрасно.."
            scene black with dissolve
            play sound "fall.wav"
            pause 1.0
            jump new_page
            
        "Нет.":
            "Что ж.."
            window hide
            $ show_dramatic_text("На этом ваше путешествие окончено..", 3.0, 60, 50)
            scene black with dissolve
            "Game over."
            return

label new_page:
    "Кажется, приземление прошло не очень удачно.."
    y "Где это я..?"
    play sound "rolling_paper.wav"
    play music "tutorial.mp3"
    scene bg map with dissolve
    
    v "Добро пожаловать на карту."
    v "Ваше приключение начнётся прямо..."
    
    "Что дальше?"
    
    menu:
        "пропустить обучение":
            scene black with dissolve
            "Что ж, удачи =)"
            v "...сейчас!"
            scene bg dungeon with dissolve
            "Чёрная пелена постепенно отступает, и к вам медленно возвращается зрение.."
            jump explore
        "играю впервые":
            jump check_map

label explore:
    play sound "dungeon.wav"
    scene bg dungeon with dissolve
    
    python:
        if not levels_data:
            levels_data = load_levels_from_file()
    
    "Перед вами появляется магический свиток с картой подземелья..."
    
    menu:
        "Что делать?"
        
        "Посмотреть карту подземелья":
            call screen level_selection
            
        "Осмотреться вокруг":
            "Вы находитесь в стартовой комнате подземелья..."
            "Перед вами несколько дверей, ведущих в разные части лабиринта."
            jump explore
        
        "Отдохнуть" if completed_levels - last_rest_level >= 5 or (completed_levels == 0 and last_rest_level == 0):
            $ last_rest_level = completed_levels
            $ hints_used = 0
            $ max_hints = renpy.random.randint(1, 3)
            "Вы отдыхаете и восстанавливаете силы..."
            "Лимит подсказок обновлен: теперь доступно [max_hints] подсказок."
            jump explore
        
        "Проверить выход" if completed_levels == 25:
            play sound "door.wav"
            scene black with dissolve
            jump win


label check_map:
    play sound "rolling_paper.wav"
    scene bg map with dissolve
    "Logica - игра, в которой вам придётся проявить немалую смекалку чтобы выбраться из подземелья."
    play sound "page_turn.wav"
    "Каждая комната - загадка.."
    play sound "page_turn.wav"
    "Для прохождения нужно разгадать их все."
    play sound "page_turn.wav"
    "Если решение не получается, то вы можете воспользоваться подсказкой."
    play sound "page_turn.wav"
    "Но будьте осторожны, использование подсказок вытягивает из вас силы.."
    play sound "page_turn.wav"
    "Никто не знает, какой раз станет последним.."
    play sound "rolling_paper.wav"
    scene black with dissolve
    menu:
        "Вы готовы продолжить?"

        "Нет (прочитать обучение вновь)":
            jump check_map

        "Да":
            scene black with dissolve
            "Что ж, удачи =)"
            v "...сейчас!"
            scene bg dungeon with dissolve
            "Чёрная пелена постепенно отступает, и к вам медленно возвращается зрение.."
            jump explore

screen level_selection():
    tag menu
    add "bg map"
    
    frame:
        xalign 0.5
        yalign 0.1
        xpadding 50
        ypadding 30
        
        vbox:
            spacing 10
            text "{b}ВЫБОР УРОВНЯ{/b}" size 40 xalign 0.5
            
            hbox:
                spacing 50
                text "Открыто: [unlocked_levels]/25"
                text "Пройдено: [completed_levels]/25"
                text "Подсказки: [hints_used]/[max_hints]"
            
            if completed_levels - last_rest_level >= 5:
                text "Можно отдохнуть!" color "#00FF00" xalign 0.5
            else:
                text "До отдыха: [5 - (completed_levels - last_rest_level)] ур." color "#000000" xalign 0.5
            
            null height -10
            
            textbutton "Вернуться в лагерь" action Jump("explore") xalign 0.5
    
    grid 5 5:
        xalign 0.5
        yalign 0.8
        xspacing 20
        yspacing 20
        
        for i in range(1, 26):
            $ level_info = levels_data.get(i)
            if level_info:
                $ is_locked = (i > unlocked_levels)
                $ is_completed = level_info["completed"]
                
                if is_locked:
                    button:
                        xsize 100
                        ysize 100
                        background Solid("#8a7341", xsize=100, ysize=100)
                        hover_background Solid("#3c1f1480", xsize=100, ysize=100)
                        action NullAction()
                        
                        text "{b}[i]{/b}" size 36 color "#000000" xalign 0.5 yalign 0.5
                        
                else:
                    button:
                        xsize 100
                        ysize 100
                        
                        if level_info['difficulty'] == "e":
                            background Solid("#00CC00", xsize=100, ysize=100)
                            hover_background Solid("#00FF00", xsize=100, ysize=100)
                        elif level_info['difficulty'] == "m":
                            background Solid("#FFAA00", xsize=100, ysize=100)
                            hover_background Solid("#FFCC00", xsize=100, ysize=100)
                        else:
                            background Solid("#CC0000", xsize=100, ysize=100)
                            hover_background Solid("#FF0000", xsize=100, ysize=100)
                        
                        action [SetVariable("current_level", i), Jump("level_generic")]
                        
                        text "[i]" size 36 color "#FFFFFF" outlines [(3, "#000000", 0, 0)] xalign 0.5 yalign 0.5
                        
                        if is_completed:
                            text "✓" size 48 color "#00FF00" outlines [(3, "#000000", 0, 0)] xalign 0.5 yalign 0.5
                        
            else:
                button:
                    xsize 100
                    ysize 100
                    background Solid("#444444", xsize=100, ysize=100)
                    text "?" size 36 color "#FFFFFF" xalign 0.5 yalign 0.5
                    action NullAction()

label game_over_hints:
    scene black with dissolve
    "Вы полагались на подсказки слишком часто..."
    "Ваши силы окончательно иссякли, и тьма поглотила вас."
    window hide
    $ show_dramatic_text("СМЕРТЬ ОТ ИСТОЩЕНИЯ", 3.0, 60, 20)
    "Game Over"
    return

label level_generic:
    $ level_num = current_level
    
    $ level_info = levels_data.get(level_num)
    if not level_info:
        $ level_info = {"name": f"Уровень {level_num}", "task": "Задача не найдена", "difficulty": "m", "answer": "0", "hint": "Нет подсказки"}
    
    $ diff_text = get_difficulty_text(level_num)
    $ scene_img = get_level_scene(level_num)
    
    if not renpy.has_image(scene_img):
        $ scene_img = "bg puzzle_room"
    
    scene expression scene_img with dissolve
    
    "=== [level_info['name']] ==="
    "Сложность: [diff_text]"
    "Кто знает, сколько ещё вы протянете..."
    ""
    
    $ task_text = level_info['task']
    "[task_text]"
    
    menu:
        "Ваши действия:"
        
        "Попытаться решить":
            $ user_answer = renpy.input("Ваш ответ:", length=50).strip()
            if user_answer:
                if check_answer(user_answer, level_info['answer']):
                    "Верно! Головоломка решена!"
                    $ update_level_progress(level_num)
                else:
                    "Неверно. Попробуйте еще раз или используйте подсказку."
                    jump level_generic
            else:
                "Вы не дали ответа."
                jump level_generic
            
        "Использовать подсказку":
            if hints_used >= max_hints:
                "Вы использовали слишком много подсказок!"
                "Ваши силы иссякли..."
                jump game_over_hints
            else:
                $ hints_used += 1
                if hints_pool:
                    $ hint_text = random.choice(hints_pool)
                    "[hint_text]"
                else:
                    "[level_info['hint']]"
                jump level_generic
        
        "Вернуться к карте":
            "Вы возвращаетесь к карте подземелья."
    
    call screen level_selection
    return

label win():
    scene bg castle with dissolve
    "Дверь поддаётся, и вам наконец-то удаётся выбраться"
    "Подземелье остаётся где-то позади.."
    v"Поздравляю.. "
    v"Не многим удавалось пережить то, через что вы прошли"
    v"До скорых встреч... =)"
    scene black with dissolve
    "Спасибо за игру <3"
    return


label freemode():
    v"Вы находитесь в свободном режиме, здесь вам доступны все задачи из банка игры.."
    menu:
        "Продолжить?"

        "Да":
            jump freemode_main

        "Выйти в меню":
            scene black with dissolve
            stop music
            "Загрузка..."
            return    
        
label freemode_main():
    stop music
    scene bg map with dissolve
