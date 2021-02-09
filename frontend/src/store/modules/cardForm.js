import api from '../../api/cards';

const state = () => ({
    cardName: '',
    collectionName: '',
    editionName: '',
    units: 1,
    allEditions: [],
    allCollections: [],
    addedSuccess: false,
});

const getters = {};

const actions = {
    updateName({ commit }, payload) {
        commit('setName', payload);
    },
    updateUnits({ commit }, payload) {
        commit('setUnits', payload);
    },
    async getAllEditions({ commit }) {
        let data = await api.getAllEditions();
        commit('setAllEditions', data);
    },
    async getAllCollections({ commit }) {
        let data = await api.getAllCollections();
        commit('setAllCollections', data);
    },
    async addCard({ commit }, payload) {
        let data = await api.addCard(payload.collection, payload.card, payload.units);
        commit('setAddedSuccess', data);
    },
};

const mutations = {
    setName(state, payload) {
        state.cardName = payload;
    },
    setUnits(state, payload) {
        state.units = payload;
    },
    setAllEditions(state, payload) {
        state.allEditions = payload;
    },
    setAllCollections(state, payload) {
        state.allCollections = payload;
    },
    setAddedSuccess(state, payload) {
        state.addedSuccess = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
