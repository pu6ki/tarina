import { HomeController } from './HomeController.js';
import { HeaderController } from './HeaderController.js';
import { RegisterController } from './AuthControllers/RegisterController.js';
import { LoginController } from './AuthControllers/LoginController.js';
import { NotFoundController } from './NotFoundController.js';

export let controllers = {
    home: HomeController,
    header: HeaderController,
    register: RegisterController,
    login: LoginController,
    notFound: NotFoundController
}