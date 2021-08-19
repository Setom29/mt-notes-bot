import telebot
import config  # 'Notes' and 'Log' are created in config.py
import datetime
import os
from random import choice
from shutil import rmtree
import json

dir_lst = []

with open('Log/users.json', 'r', encoding='utf-8') as jf:
    users = json.load(jf)


def notes_state():
    global dir_lst
    dir_lst = sorted([el for el in os.listdir('Notes') if '.' not in el])


notes_state()

bot = telebot.TeleBot(config.token)


def new_note(message):  # create a note file
    name = message.text
    try:
        if not os.path.isdir(f'Notes/{name}'):
            os.mkdir(f'Notes/{name}')
            with open(f'Notes/{name}/{name}.txt', 'w+', encoding='utf-8') as wf:
                wf.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + '\n' + name + '\n')
            bot.send_message(message.chat.id, 'File created.')
            notes_state()  # reload the list of dirs
        else:
            bot.send_message(message.chat.id, f'{name} exists.')
    except FileNotFoundError:
        bot.send_message(message.chat.id, 'Unacceptable symbols detected.')
    except Exception as err:
        bot.send_message(message.chat.id, f'{err}')


def change_note(message, name):
    if message.text.lower() == 'end':
        bot.send_message(message.chat.id, 'Note edited')
    else:
        with open(f'Notes/{name}/{name}.txt', 'a', encoding='utf-8') as wf:
            wf.write(message.text + '\n')
            bot.send_message(message.chat.id,
                             'If you have finished writing the note - enter "end", otherwise continue writing.')
        bot.register_next_step_handler(message, change_note, name)


def choose_note(message):
    try:
        name = dir_lst[int(message.text.strip()) - 1]
        bot.send_message(message.chat.id, 'Start writing your note.')
        bot.register_next_step_handler(message, change_note, name)
    except ValueError:
        bot.send_message(message.chat.id, 'Value Error')
    except IndexError:
        bot.send_message(message.chat.id, 'Out of index.')


def delete_note(message):
    try:
        note_lst = list(map(int, message.text.strip().split()))
        for el in note_lst:
            rmtree(f'Notes/{dir_lst[el - 1]}')
        notes_state()
        bot.send_message(message.chat.id, 'Success!')
    except ValueError:
        bot.send_message(message.chat.id, 'Value error')
    except IndexError:
        bot.send_message(message.chat.id, 'Incorrect index')


def show(message):
    try:
        note_lst = int(message.text.strip()) - 1
        with open(f'Notes/{dir_lst[note_lst]}/{dir_lst[note_lst]}.txt', 'r', encoding='utf-8') as rf:
            bot.send_message(message.chat.id, ''.join(rf.readlines()))
        for el in os.listdir(f'Notes/{dir_lst[note_lst]}'):
            ext = el.split('.')[-1]
            if el != f'{dir_lst[note_lst]}.txt':
                if ext in ['jpg', 'jpeg', 'png', 'gif']:
                    with open(f'Notes/{dir_lst[note_lst]}/{el}', 'rb') as f:
                        bot.send_photo(message.chat.id, f, caption=f'{el}')
                else:
                    with open(f'Notes/{dir_lst[note_lst]}/{el}', 'rb') as f:
                        bot.send_document(message.chat.id, f)
    except ValueError:
        bot.send_message(message.chat.id, 'Value error')
    except IndexError:
        bot.send_message(message.chat.id, 'Out of index')


def share(message):
    try:
        note_lst = int(message.text.strip()) - 1
        with open(f'Notes/{dir_lst[note_lst]}/{dir_lst[note_lst]}.txt', 'r', encoding='utf-8') as rf:
            bot.send_document(message.chat.id, rf)
        for el in os.listdir(f'Notes/{dir_lst[note_lst]}'):
            if el != f'{dir_lst[note_lst]}.txt':
                with open(f'Notes/{dir_lst[note_lst]}/{el}', 'rb') as f:
                    bot.send_document(message.chat.id, f)
    except ValueError:
        bot.send_message(message.chat.id, 'Value error')
    except IndexError:
        bot.send_message(message.chat.id, 'Out of index')


def save_doc(message, file_name, downloaded_file):
    try:
        note_lst = int(message.text.strip()) - 1
        if file_name is None:
            pass
        src = f'Notes/{dir_lst[note_lst]}/' + f'{file_name}'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.chat.id, 'Image saved!')
    except ValueError:
        bot.send_message(message.chat.id, 'Value error')
    except IndexError:
        bot.send_message(message.chat.id, 'Out of index')
    except Exception as err:
        print(f'{err}')


def enter_user(message):
    try:
        users[int(message.text.strip())] = {'name': ''}
        bot.send_message(message.chat.id, 'Please, enter the name of new user.')
        bot.register_next_step_handler(message, enter_name, int(message.text))
    except Exception as err:
        bot.send_message(message.chat.id, str(err))


def enter_name(message, user_id):
    try:
        users[user_id]['name'] = message.text
        with open('Log/users.json', 'w', encoding='utf-8') as f:
            json.dump(users, f)
        bot.send_message(message.chat.id, 'Success.')
        bot.send_message(user_id, 'You added to the list of users.')
    except Exception as err:
        bot.send_message(message.chat.id, str(err))


@bot.message_handler(func=lambda message: str(message.chat.id) not in users.keys())
def access(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Enter the password or ask admin to share it.')
    elif message.text == config.password:
        bot.send_message(config.admin['s_adm'],
                         f'{message.chat.id}: {message.from_user.first_name} {message.from_user.last_name} sent the '
                         f'password.')
        bot.send_message(config.admin['s_adm'],
                         f'{message.chat.id}')
    else:
        with open('Log/unknown_users.txt', 'a+', encoding='utf-8') as wf:
            wf.write(str(message.chat.id) + ' : ' + message.text + '\n')
        bot.send_message(message.chat.id, "Sorry")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id, f'Hi, \n'
                         f'Available commands:\n'
                         f'start - main info\n'
                         f'stop - stop execution\n'
                         f'help - main info\n'
                         f'list_of_notes - enumerated list of notes\n'
                         f'new_note - creating a new note (name + date)\n'
                         f'edit_note - adding some lines to the note\n'
                         f'delete_notes - deleting a set of notes (only for admin)\n')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id, f'Hi, \n'
                         f'Available commands:\n'
                         f'start - main info\n'
                         f'stop - stop execution\n'
                         f'help - main info\n'
                         f'list_of_notes - enumerated list of notes\n'
                         f'new_note - creating a new note (name + date)\n'
                         f'edit_note - adding some lines to the note\n'
                         f'delete_notes - deleting a set of notes (only for admin)\n')


@bot.message_handler(commands=['stop'])
def stop_command(message):
    if message.chat.id in config.admin.values():
        bot.send_message(
            message.chat.id, f'Выключаюсь!')
        bot.stop_bot()
    else:
        bot.send_message(config.admin['s_adm'],
                         f'{message.chat.id} {message.from_user.first_name} {message.from_user.last_name} '
                         f'tried to stop bot.')
        bot.send_message(message.chat.id, 'Restricted operation')


@bot.message_handler(commands=['new_note'])
def enter_note(message):
    bot.send_message(message.chat.id, 'Enter the name of the note.')
    bot.register_next_step_handler(message, new_note)


@bot.message_handler(commands=['edit_note'])
def edit_note(message):
    note(message)
    bot.send_message(message.chat.id, 'Enter the file number.')
    bot.register_next_step_handler(message, choose_note)


@bot.message_handler(commands=['list_of_notes'])
def note(message):
    os.chdir('Notes')
    dir_str = ''
    if not dir_lst:
        bot.send_message(message.chat.id, 'There are no notes.')
        os.chdir('..')
        return
    else:
        for ind, el in enumerate(dir_lst):
            dir_str += f'{ind + 1}) {el}\n'
        bot.send_message(message.chat.id, dir_str)
    os.chdir('..')


@bot.message_handler(commands=['delete_notes'])
def delete(message):
    if message.chat.id in config.admin.values():
        note(message)
        if dir_lst:
            bot.send_message(message.chat.id, 'Enter the file numbers like "1 2 3".')
            bot.register_next_step_handler(message, delete_note)
    else:
        bot.send_message(config.admin[0],
                         f'{message.from_user.first_name} {message.from_user.last_name} tried to delete a note.')
        bot.send_message(message.chat.id, 'If you need to delete a note, contact the administrator')


@bot.message_handler(commands=['show_note'])  # send text and images from the note to chat
def show_note(message):
    note(message)
    if dir_lst:
        bot.send_message(message.chat.id, 'Enter the file number.')
        bot.register_next_step_handler(message, show)


@bot.message_handler(commands=['share_note'])  # send note and docs
def share_note(message):
    note(message)
    if dir_lst:
        bot.send_message(message.chat.id, 'Enter the file number.')
        bot.register_next_step_handler(message, share)


@bot.message_handler(content_types=['document'])  # add docs to the note
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.send_message(message.chat.id, 'Enter the file number.')
        note(message)
        file_extension = message.document.file_name.split('.')[-1]
        if message.caption is None:
            bot.register_next_step_handler(message, save_doc,
                                           str(datetime.datetime.now().strftime(
                                               "%Y-%m-%d %H:%M:%S")) + '.' + file_extension, downloaded_file)
        else:
            bot.register_next_step_handler(message, save_doc, message.caption + '.' + file_extension, downloaded_file)
    except Exception as err:
        bot.reply_to(message, f'{err}')


@bot.message_handler(content_types=['sticker'])  # send sticker id
def sticker_id(message):
    bot.send_message(message.chat.id, str(message.sticker.file_id))


@bot.message_handler(commands=["add_user"])
def add_user(message):
    if message.chat.id in config.admin.values():
        bot.send_message(message.chat.id, "Enter user's id.")
        bot.register_next_step_handler(message, enter_user)
    else:
        bot.send_message(config.admin['s_adm'],
                         f'{message.from_user.first_name} {message.from_user.last_name} tried to open log file.')
        bot.send_message(message.chat.id, 'Restricted operation')


@bot.message_handler(commands=["show_users"])  # show config.users
def show_users(message):
    if message.chat.id in config.admin.values():
        bot.send_message(message.chat.id, '\n'.join([str(el) for el in users.items()]))
    else:
        bot.send_message(config.admin['s_adm'],
                         f'{message.from_user.first_name} {message.from_user.last_name} tried to open log file.')
        bot.send_message(message.chat.id, 'Restricted operation. Only for admin.')


@bot.message_handler(content_types=["text"])
def content_text(message):
    if message.text.lower() in ['hi', 'hello', 'привет']:
        sticker = choice(config.hi_stickers)
        try:
            bot.send_sticker(message.chat.id, choice(config.hi_stickers))
        except Exception:
            print(sticker)
    elif message.text.lower() == 'show all stickers':
        for el in config.hi_stickers:
            try:
                bot.send_sticker(message.chat.id, el)
            except Exception:
                print(el)
    else:
        bot.send_message(message.chat.id, "I don't understand.")


bot.polling(none_stop=True)

"""
commands for BotFather
start - info
help - info
list_of_notes - enumerated list of notes
new_note - create a new note (name + date)
edit_note - add some text to the note
show_note - show note
share_note - download txt file
delete_notes - delete a set of notes (for admin only)
stop - stop execution (for admin only)
add_user - add user in users' list (for admin only)
show_users - show list of users (for admin only)
log
"""
