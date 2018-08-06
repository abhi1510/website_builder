import os
import shutil

BASE_DIR = os.getcwd()


def get_error(e_type, e_code, e_msg):
    return {
        'type': e_type,
        'code': e_code,
        'message': e_msg
    }


def create_site_dir(path):
    try:
        os.mkdir(path)
    except Exception as e:
        code, msg = e.args
        s_e = get_error(type(e).__name__, code, msg)
    else:
        s_e = None
    return s_e, path


def get_starter_code():
    file_path = os.path.join(BASE_DIR, 'starter_code.txt')
    f = open(file_path, encoding='utf-8')
    code = f.read()
    f.close()
    return code


def create_flask_app(path):
    try:
        with open(path + '/app.py', 'w', encoding='utf-8') as f:
            code = get_starter_code()
            f.write(code)
    except Exception as e:
        code, msg = e.args
        f_e = get_error(type(e).__name__, code, msg)
    else:
        f_e = None
    return f_e


def copy_templates(src, dest):
    try:
        shutil.copytree(src, dest)
    except Exception as e:
        code, msg = e.args
        c_e = get_error(type(e).__name__, code, msg)
    else:
        c_e = None
    return c_e


def get_input():
    hotel_name = input('Enter your hotel name: ')
    template_name = input('Enter your template name: ')
    return hotel_name, template_name


def run_application(app_path):
    os.system('python {}'.format(app_path))


if __name__ == '__main__':
    hotel_name, template_name = get_input()
    site_path = os.path.join(BASE_DIR, 'sites', hotel_name)
    error, path = create_site_dir(site_path)
    if not error:
        print('Created site directory!')
        error = create_flask_app(path)
        if not error:
            print('Created Flask App!')
            src_template = os.path.join(BASE_DIR, 'src_templates', template_name)
            dest_template = os.path.join(site_path, 'templates')
            error = copy_templates(src_template, dest_template)
            if not error:
                print('Copied templates\nNow going to start server...\n')
                run_application(site_path + '/app.py')
            else:
                print('Error coping templates', error)
        else:
            print('Error creating flask app', error)
    else:
        print('Error creating site directory', error)
