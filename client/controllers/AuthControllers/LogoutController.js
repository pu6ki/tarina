import { HomeController } from '../HomeController.js';
import { HeaderController } from '../HeaderController.js';

export function LogoutController() {
    localStorage.removeItem('tarina-username');
    localStorage.removeItem('tarina-token');

    HeaderController();
    if (window.location.href === '/#/home') {
        HomeController();
    } else {
        window.location.href = '/#/home';
        HomeController();
    }
}