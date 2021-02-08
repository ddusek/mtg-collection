import axios from 'axios';

const APIURL = 'http://localhost:5000';

const getCardSuggestions = async (input) => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    return axios
        .get(`${APIURL}/suggest/${input}`)
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const getAllEditions = async () => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    return axios
        .get(`${APIURL}/editions`)
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const getAllCollections = async () => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    return axios
        .get(`${APIURL}/collections`)
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const addCard = async (collection, card, units) => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    return axios
        .post(`${APIURL}/add/${collection}/${card}/${units}`)
        .then((response) => {
            return response.status.success;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const addCollection = async (collection) => {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    return axios
        .post(`${APIURL}/add/${collection}`)
        .then((response) => {
            return response.status == 200;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

export default {
    getCardSuggestions,
    getAllEditions,
    getAllCollections,
    addCard,
    addCollection,
};
