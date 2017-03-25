import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';
import { formHandler } from '../../utils/formHandler.js';

import { HeaderController } from '../HeaderController.js';
import { HomeController } from '../HomeController.js';

export function LoginController() {
    templates.get('AuthTemplates/login-template')
        .then((result) => {
            let hbTemplate = Handlebars.compile(result);
            let template = hbTemplate();

            $('#content').html(template);
            
            formHandler();

            $('#submit').on('click', () => {
                login();
            })
        });
}

function getDataFromTemplate() {
    let body = {
        username: '',
        password: ''
    };

    body.username = $('#username').val();
    body.password = $('#password').val();

    return body;
}

function login() {
    let loginUrl = 'https://tarina.herokuapp.com/api/login/';

    requester.postJSON(loginUrl, getDataFromTemplate())
        .then((result) => {
            if (result.token) {
                localStorage.setItem('tarina-username', result.username);
                localStorage.setItem('tarina-token', result.token);
                localStorage.setItem('tarina-id', result.id);
            }

            Materialize.toast('Logged in successfully!', 3000, 'green accent-4');
            window.location.href = "/#/home";
            HeaderController();
            HomeController();
        })
        .catch((err) => {
            Materialize.toast(err.responseJSON.message, 3000, 'red accent-2');
            return;
        })
}