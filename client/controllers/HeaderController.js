import { requester } from '../utils/requester.js';
import { templates } from '../utils/templates.js';
import { LogoutController } from './AuthControllers/LogoutController.js';

export function HeaderController() {
    let token = localStorage.getItem('tarina-token');
    let userData = {
        id: localStorage.getItem('tarina-id'),
        username: localStorage.getItem('tarina-username')
    };

    if (token) {
        templates.get('HeaderTemplates/authorized-header')
            .then((result) => {
                let hbTemplate = Handlebars.compile(result);
                let template = hbTemplate(userData);

                $('#nav-wrapper').html(template);
                $('.button-collapse').sideNav();
                $('.side-nav li a').on('click', () => {
                    $('.button-collapse').sideNav('hide');
                });
                $('.dropdown-button').dropdown({
                    belowOrigin: true
                });
                $('.logout').on('click', () => {
                    LogoutController();
                    Materialize.toast('Logged out successfully!', 3000, 'green accent-4');
                })
            })
    } else {
        templates.get('HeaderTemplates/unauthorized-header')
            .then((result) => {
                let hbTemplate = Handlebars.compile(result);
                let template = hbTemplate();

                $('#nav-wrapper').html(template);
                $('.button-collapse').sideNav();
                $('.side-nav li a').on('click', () => {
                    $('.button-collapse').sideNav('hide');
                });
            });
    }
}