import { templates } from '../utils/templates.js';

export function NotFoundController() {
    templates.get('not-found')
        .then((result) => {
            let hbTemplate = Handlebars.compile(result),
                template = hbTemplate();

            $('#content').html(template);
        })
}