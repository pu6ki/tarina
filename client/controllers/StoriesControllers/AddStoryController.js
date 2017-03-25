import { templates } from '../../utils/templates.js';
import { requester } from '../../utils/requester.js';
import { validator } from '../../utils/validator.js';

export function AddStoryController() {
    templates.get('StoryTemplates/add-story')
        .then((result) => {
            let hbTemplate = Handlebars.compile(result);
            let template = hbTemplate();

            $('#content').html(template);
            $('#innitial-storyline').spellAsYouType();
            $('#submit').on('click', () => {
                postStory();
            });
        }); 
}

function getTitleFromTemplate() {
    let data = {
        title: ""
    };

    if (validator.title($('#story-title').val())) {
        data.title = $('#story-title').val();
    } else {
        Materialize.toast('Title should be between 3 and 100 characters long.', 3000, 'red accent-2');
        return;
    }

    return data;
}

function getInitialStorylineFromTemplate() {
    let data = {
        content: ""
    };

    if (validator.storyline($('#initial-storyline').val())) {
        data.content = $('#initial-storyline').val();
    } else {
        Materialize.toast('Storyline should be between 3 and 250 characters long.', 3000, 'red accent-2');
        return;
    }

    return data;
}

function postStory() {
    let domain = 'https://tarina.herokuapp.com/api';
    let postStoryUrl = `${domain}/story/`;

    requester.postJSON(postStoryUrl, getTitleFromTemplate())
        .then((result) => {
            let storyId = result.id;
            let postStorylineUrl = `${postStoryUrl}${storyId}/storylines/`;
            return requester.postJSON(postStorylineUrl, getInitialStorylineFromTemplate());
        }).then((result) => {
            Materialize.toast('Story added successfully.', 3000, 'green accent-4');
            window.location.href = `/#/stories/${result.story_id}/`;
        }).catch((err) => {
            Materialize.toast(err.responseJSON, 3000, 'red accent-2');
        });
}