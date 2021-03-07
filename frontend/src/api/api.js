import axios from 'axios';

const APIURL = 'https://0.0.0.0:8000/api';
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

const register = async (data) => {
    return axios
        .post(`${APIURL}/register`, data)
        .then((response) => {
            return response.status == 200;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const login = async (data) => {
    return axios
        .post(`${APIURL}/login`, data)
        .then((response) => {
            return response.status == 200;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const logout = async () => {
    return axios
        .post(`${APIURL}/logout`)
        .then((response) => {
            return response.status == 200;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const getCardSuggestions = async (input) => {
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

const getCollectionCards = async (name) => {
    return axios
        .get(`${APIURL}/collection/${name}`)
        .then((response) => {
            return response.data;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const addCard = async (collection, card, edition, units) => {
    return axios
        .post(`${APIURL}/add/${collection}/${card}/${edition}/${units}`)
        .then((response) => {
            return response.status.success;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const addCollection = async (collection) => {
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

const downloadCards = async () => {
    return axios
        .get(`${APIURL}/download/scryfall/cards`)
        .then((response) => {
            return response.data.success;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

const syncDatabaseFromFile = async () => {
    return axios
        .get(`${APIURL}/synchronize/scryfall/cards`)
        .then((response) => {
            return response.data.success;
        })
        .catch((error) => {
            console.log(error);
            return null;
        });
};

export default {
    register,
    login,
    logout,
    getCardSuggestions,
    getAllEditions,
    getAllCollections,
    getCollectionCards,
    addCard,
    addCollection,
    downloadCards,
    syncDatabaseFromFile,
};
