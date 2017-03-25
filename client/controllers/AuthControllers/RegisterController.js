import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';
import { formHandler } from '../../utils/formHandler.js';
import { validator } from '../../utils/validator.js';

export function RegisterController() {
    templates.get('AuthTemplates/register-template')
        .then((result) => {
            let hbTemplate = Handlebars.compile(result);
            let template = hbTemplate();

            $('#content').html(template);

            formHandler();

            $('#submit').on('click', () => {
                register();
            });
        });
}

function getDataFromTemplate() {
    let body = {
        username: '',
        first_name: '',
        last_name: '',
        password: '',
    }

    if (validator.name($('#username').val())) {
        body.username = $('#username').val();
    } else {
        Materialize.toast('Invalid username.', 3000, 'red accent-2');
    }
    if (validator.name($('#first-name').val())) {
        body.first_name = $('#first-name').val();
    } else {
        Materialize.toast('Invalid first name.', 3000, 'red accent-2');
    }
    if (validator.name($('#last-name').val())) {
        body.last_name = $('#last-name').val();
    } else {
        Materialize.toast('Invalid last name.', 3000, 'red accent-2');
    }
    if (validator.password($('#password').val())) {
        if ($('#verify-password').val() === $('#password').val()) {
            body.password = $('#password').val();
        } else {
            Materialize.toast('Passwords doesn\'t match', 3000, 'red accent-2');
        }
    } else {
        Materialize.toast('Password should contain atleast one number and one special character and capital letter and be between 6 and 16 symbols long.', 3000, 'red accent-2');
    }

    return body;
}

function register() {
    let registerUrl = 'https://tarina.herokuapp.com/api/register/';
    let data = getDataFromTemplate();
    if (data.username) {
        requester.postJSON(registerUrl, data)
            .then((result) => {
                if (result) {
                    Materialize.toast('Registered successfully! Now you can log-in!', 3000, 'green accent-4');
                    window.location.href = '#/login';
                }
            })
            .catch((err) => {
                Materialize.toast(err.responseJSON.message, 3000, 'red accent-2');
            })
    }
}