export let validator = {
    name: (name) => {
        if (typeof name === 'string') {
            if (name.length >= 3 && name.length <= 30) {
                return true;
            }
        }
        return false;
    },
    password: (password) => {
        // Password should contain atleast one number and one special character and capital letter and be between 6 and 16 symbols long
        let regexPattern = /^(?=.*[0-9])[a-zA-Z0-9!]{6,16}$/;
        return regexPattern.test(password);
    },
    title: (title) => {
        if (typeof title === 'string') {
            if (title.length >= 3 && title.length <= 100) {
                return true;
            }
        }
        return false;
    },
    storyline: (storyline) => {
        if (typeof storyline === 'string') {
            if (storyline.length >= 3 && storyline.length <= 250) {
                return true;
            }
        }
        return false;
    }
}