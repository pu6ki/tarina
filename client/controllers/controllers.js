import { HomeController } from './HomeController.js';
import { HeaderController } from './HeaderController.js';
import { RegisterController } from './AuthControllers/RegisterController.js';
import { LoginController } from './AuthControllers/LoginController.js';
import { ProfileController } from './ProfileControllers/ProfileController.js';
import { StoriesController } from './StoriesControllers/StoriesController.js';
import { DetailedStoryController } from './StoriesControllers/DetailedStoryController.js' ;
import { NotFoundController } from './NotFoundController.js';

export let controllers = {
    home: HomeController,
    header: HeaderController,
    register: RegisterController,
    login: LoginController,
    profile: ProfileController,
    stories: StoriesController,
    detailedStory: DetailedStoryController,
    notFound: NotFoundController
}