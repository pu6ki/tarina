import { templates } from '../utils/templates.js';

export function HomeController() {
    templates.get('home')
        .then((result) => {
            $('#content').html(result);
            $('.parallax').parallax();
        });
}