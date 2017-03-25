import { HomeController } from './HomeController.js';
import { RegisterController } from './AuthControllers/RegisterController.js';
import { HeaderController } from './HeaderController.js';

export let controllers = {
    home: HomeController,
    header: HeaderController,
    register: RegisterController
}