import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';

import { AddStoryController } from './AddStoryController.js';
import { NotFoundController } from '../NotFoundController.js';

export function StoriesController(storiesUrl) {
    let token = localStorage.getItem('tarina-token');

    let templateName = (storiesUrl.endsWith('/personal/')) ?
        'personal-story-list' :
        'story-list';
    
    let getData = requester.getJSON(storiesUrl);
    let getTemplate = templates.get('StoryTemplates/'.concat(templateName));
    
    Promise.all([getData, getTemplate])
        .then((result) => {
            let data = result[0],
                hbTemplate = Handlebars.compile(result[1]);

            let template = hbTemplate(data);
            $('#content').html(template);
            
            $('#add-story').on('click', () => {
                AddStoryController();
            });
        }).catch((err) => {
            console.log(err);
            NotFoundController();
        });
}