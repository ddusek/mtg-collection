import axios from 'axios';

const APIURL = 'http://localhost:5000/';

const GetSuggestion = async (input) => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    return axios
        .get(`${APIURL}suggest/${input}`)
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

export default {
    GetSuggestion,
};
