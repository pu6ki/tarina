import { controllers } from './controllers/controllers.js';

const storiesUrl = 'https://tarina.herokuapp.com/api/story/';

HandlebarsIntl.registerWith(Handlebars);

var router = new Navigo(null, true);

window.onbeforeunload = controllers.header();

router
    .on('/', () => {
        controllers.header();
        router.navigate('/home');
    })
    .on('/home', () => {
        controllers.home();
    })
    .on('/login', () => {
        controllers.login();
    })
    .on('/register', () => {
        controllers.register();
    })
    .on(`/profile/:id`, (params) => {
        controllers.profile(params.id);
    })
    .on('/stories', () => {
        controllers.stories();
    })
    .on('/stories/:id', (params) => {
        controllers.detailedStory(params.id);
    })
    .resolve();
