import axios from 'axios';

const APIURL = 'http://localhost:5000';

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

const addCard = async (collection, card, units) => {
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
    getCardSuggestions,
    getAllEditions,
    getAllCollections,
    getCollectionCards,
    addCard,
    addCollection,
    downloadCards,
    syncDatabaseFromFile,
};
