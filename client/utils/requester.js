let requester = {
    get(url) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "GET",
                beforeSend: (xhr) => {
                    if (window.localStorage.getItem('tarina-token')) {
                        let token = window.localStorage.getItem('tarina-token');
                        xhr.setRequestHeader('Authorization', `Token ${token}`);
                    }
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },
    postJSON(url, body, options = {}) {
        let promise = new Promise((resolve, reject) => {
            var headers = options.headers || {};

            $.ajax({
                url,
                headers,
                method: "POST",
                contentType: "application/json",
                data: JSON.stringify(body),
                crossDomain: true,
                beforeSend: (xhr) => {
                    if (window.localStorage.getItem('tarina-token')) {
                        let token = window.localStorage.getItem('tarina-token');
                        xhr.setRequestHeader('Authorization', `Token ${token}`);
                    }
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },
    getJSON(url) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "GET",
                contentType: "application/json",
                beforeSend: (xhr) => {
                    if (window.localStorage.getItem('tarina-token')) {
                        let token = window.localStorage.getItem('tarina-token');
                        xhr.setRequestHeader('Authorization', `Token ${token}`);
                    }
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    },
    delete(url) {
        let promise = new Promise((resolve, reject) => {
            $.ajax({
                url,
                method: "DELETE",
                beforeSend: (xhr) => {
                    if (window.localStorage.getItem('tarina-token')) {
                        let token = window.localStorage.getItem('tarina-token');
                        xhr.setRequestHeader('Authorization', `Token ${token}`);
                    }
                },
                success(response) {
                    return resolve(response);
                },
                error(response) {
                    return reject(response);
                }
            });
        });
        return promise;
    }
};

export { requester };