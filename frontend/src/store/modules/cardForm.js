import api from '../../api/cards';

const state = () => ({
    cardName: '',
    collectionName: '',
    editionName: '',
    allEditions: [],
    allCollections: [],
    addedSuccess: false,
});

const getters = {};

const actions = {
    updateName({ commit }, payload) {
        commit('setName', payload);
    },
    async getAllEditions({ commit }) {
        let data = await api.getAllEditions();
        commit('setAllEditions', data);
    },
    async addCard({ commit }, payload) {
        let data = await api.addCard(payload.collection, payload.card, payload.units);
        commit('setAddedSuccess', data);
    },
    async getAllCollections({ commit }) {
        let data = await api.getAllCollections();
        commit('setAllCollections', data);
    },
};

const mutations = {
    setName(state, payload) {
        state.cardName = payload;
    },
    setAllEditions(state, payload) {
        state.allEditions = payload;
    },
    setAddedSuccess(state, payload) {
        state.addedSuccess = payload;
    },
    setAllCollections(state, payload) {
        state.allCollections = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
