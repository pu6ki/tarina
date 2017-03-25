import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';

import { DeleteStorylineController } from './DeleteStorylineController.js';
import { NotFoundController } from '../NotFoundController.js';

export function DetailedStoryController(id) {
    let token = localStorage.getItem('tarina-token');
    let username = localStorage.getItem('tarina-username');
    const storyUrl = `http://tarina.herokuapp.com/api/story/${id}/`;

    let getData = requester.getJSON(storyUrl);
    let getTemplate = templates.get('StoryTemplates/story-detail');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0],
                hbTemplate = Handlebars.compile(result[1]);

            data.editable = username === data.author.user.username;

            console.log(data);

            let template = hbTemplate(data);
            $('#content').html(template);

            if (data.storyline_set) {
                data.storyline_set.forEach((el) => {
                    $(`.storyline-container #storyline-${el.id}`).on('click', () => {
                        $(`.storyline-container #info-container-${el.id}`).toggleClass('hide visible');
                    });

                    $(`#delete-${id}-storyline-${el.id}`).on('click', () => {
                        DeleteStorylineController(id, el.id);
                    });
                });
            }

        }).catch((err) => {
            console.log(err);
            NotFoundController();
        });
}