import { requester } from '../../utils/requester.js';
import { templates } from '../../utils/templates.js';
import { validator } from '../../utils/validator.js';
import { formHandler } from '../../utils/formHandler.js';

import { DeleteStorylineController } from './DeleteStorylineController.js';
import { NotFoundController } from '../NotFoundController.js';

let dataFromAPI, username;

export function DetailedStoryController(id) {
    let token = localStorage.getItem('tarina-token');
    username = localStorage.getItem('tarina-username');
    const storyUrl = `http://tarina.herokuapp.com/api/story/${id}/`;

    let getData = requester.getJSON(storyUrl);
    let getTemplate = templates.get('StoryTemplates/story-detail');

    Promise.all([getData, getTemplate])
        .then((result) => {
            dataFromAPI = result[0];
            let hbTemplate = Handlebars.compile(result[1]);

            dataFromAPI.editable = username === dataFromAPI.author.user.username;

            let template = hbTemplate(dataFromAPI);
            $('#content').html(template);

            if (dataFromAPI.storyline_set) {
                dataFromAPI.storyline_set.forEach((el) => {
                    $(`.storyline-container #storyline-${el.id}`).on('click', () => {
                        $("[id^=info-container]").addClass('hide');

                        $(`.storyline-container #info-container-${el.id}`).toggleClass('hide');
                        $(`.storyline-container #info-container-${el.id}`).addClass('visible');
                    });

                    $(`#delete-${id}-storyline-${el.id}`).on('click', () => {
                        alertify.confirm('Are you sure you want to delete this storyline?', () => {
                            DeleteStorylineController(id, el.id);
                        });
                    });
                });
            }

            formHandler();

            $('.vote').on('click', () => {
                $(this).removeClass('vote').addClass('unvote')
                vote(id);
            });


            $('.unvote').on('click', () => {
                unvote(id);
            });

            $('#add-storyline').on('click', () => {
                addStoryline(id);
            });

            const domain = 'http://127.0.0.1:8080';

            let refreshId = setInterval(() => {
                loadStorylines(id);
                if (window.location.href !== `${domain}/#/stories/${id}/`) {
                    clearInterval(refreshId);
                }
            }, 1000);

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
            $('#new-storyline').val('');
        }).catch((err) => {
            Materialize.toast(err.responseJSON.message, 3000, 'red accent-2');
            return;
        });
}

export function loadStorylines(id) {
    const storylinesUrl = `http://tarina.herokuapp.com/api/story/${id}/storylines/`;
    let getData = requester.getJSON(storylinesUrl);
    let getTemplate = templates.get('partials/storyline');

    Promise.all([getData, getTemplate])
        .then((result) => {
            let newData = result[0];
            let storylinesToLoad = [];

            storylinesToLoad = newData.filter((obj) => {
                return !dataFromAPI.storyline_set.some((obj2) => {
                    return obj.id === obj2.id;
                });
            });

            dataFromAPI.storyline_set = newData;
            if (storylinesToLoad.length) {
                let hbTemplate = Handlebars.compile(result[1]);

                storylinesToLoad.forEach((el) => {
                    el.storyId = dataFromAPI.id;
                    el.editable = username === dataFromAPI.author.user.username;
                    let template = hbTemplate(el);
                    $('.storyline-container').append(template);
                    $(`.storyline-container #storyline-${el.id}`).on('click', () => {
                        $(`.storyline-container #info-container-${el.id}`).toggleClass('hide visible');
                    });
                    $(`#delete-${el.storyId}-storyline-${el.id}`).on('click', () => {
                        alertify.confirm('Are you sure you want to delete this storyline?', () => {
                            DeleteStorylineController(el.storyId, el.id);
                        });
                    });
                });
            }
        })
}

function vote(id) {
    const storyUrl = `http://tarina.herokuapp.com/api/story/${id}/vote/`;
    requester.putJSON(storyUrl)
        .then((result) => {
            DetailedStoryController(id);
        }).catch((err) => {
            Materialize.toast(err.responseJSON.message, 3000, 'red accent-2');
            console.log(err);
        })
}

function unvote(id) {
    const storyUrl = `http://tarina.herokuapp.com/api/story/${id}/unvote/`;
    requester.putJSON(storyUrl)
        .then((result) => {
            DetailedStoryController(id);
        }).catch((err) => {
            Materialize.toast(err.responseJSON.message, 3000, 'red accent-2');
            console.log(err);
        })
}
