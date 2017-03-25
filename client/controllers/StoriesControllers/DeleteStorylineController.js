import { requester } from '../../utils/requester.js';

import { DetailedStoryController } from './DetailedStoryController.js';

export function DeleteStorylineController(storyId, storylineId) {
    let storylineUrl = `https://tarina.herokuapp.com/api/story/${storyId}/storylines/${storylineId}/`;

    requester.delete(storylineUrl)
        .then((result) => {
            Materialize.toast('Storyline deleted successfully.', 3000, 'green accent-4');
            DetailedStoryController(storyId);
        })
}