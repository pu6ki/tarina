import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';
import { validator } from '../../utils/validator.js';
import { formHandler } from '../../utils/formHandler.js';

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

            formHandler();

            $('#add-storyline').on('click', () => {
                addStoryline(id);
            })

        }).catch((err) => {
            NotFoundController();
            console.log(err);
        });
}

function addStoryline(id) {
    const storyUrl = `http://tarina.herokuapp.com/api/story/${id}/storylines/`;

    let data = {
        content: ''
    }

    if (validator.storyline($('#new-storyline').val())) {
        data.content = $('#new-storyline').val();
    } else {
        Materialize.toast('Storyline should be between 3 and 250 characters long.', 3000, 'red accent-2');
        return;
    }

    requester.postJSON(storyUrl, data)
        .then((result) => {
            Materialize.toast('Storyline added successfully.', 3000, 'green accent-4');
        }).catch((err) => {
            Materialize.toast('You are not allowed to add two consecutive story lines.', 3000, 'red accent-2');
            return;
        });
}