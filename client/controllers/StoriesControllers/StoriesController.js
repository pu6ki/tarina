import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';
import { AddStoryController } from './AddStoryController.js';

export function StoriesController() {
    const storiesUrl = 'https://tarina.herokuapp.com/api/story/';
    let getData = requester.getJSON(storiesUrl);
    let getTemplate = templates.get('StoryTemplates/story-list');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0];
            let hbTemplate = Handlebars.compile(result[1]);
            let template = hbTemplate(data);
            
            $('#content').html(template);
            $('#add-story').on('click', () => {
                AddStoryController();
            })
        });
}
