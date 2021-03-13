const USER_TOKEN = 'user_token';
const USER_ID = 'user_id';
const USERNAME = 'username';

const getCookie = (name) => {
    return (
        (name = new RegExp(
            '(?:^|;\\s*)' + ('' + name).replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&') + '=([^;]*)'
        ).exec(document.cookie)) && name[1]
    );
};

export default {
    getCookie,
    USER_TOKEN,
    USER_ID,
    USERNAME,
};
