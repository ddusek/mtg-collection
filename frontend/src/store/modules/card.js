import api from '../../api/cards';

const state = () => ({
    cardName: '',
    editionName: '',
    foil: false,
    units: 1,
    allEditions: [],
    addedSuccess: false,
});

const getters = {};

const actions = {
    updateName({ commit }, payload) {
        commit('setName', payload);
    },
    updateCard({ commit }, payload) {
        commit('setName', payload.name);
        commit('setEdition', payload.edition);
    },
    updateEdition({ commit }, payload) {
        commit('setEdition', payload);
    },
    updateFoil({ commit }, payload) {
        commit('setFoil', payload);
    },
    updateUnits({ commit }, payload) {
        commit('setUnits', payload);
    },
    async getAllEditions({ commit }) {
        let data = await api.getAllEditions();
        commit('setAllEditions', data);
    },
    async addCard({ commit }, payload) {
        let data = await api.addCard(
            payload.collection,
            payload.card,
            payload.edition,
            payload.units
        );
        commit('setAddedSuccess', data);
    },
};

const mutations = {
    setName(state, payload) {
        state.cardName = payload;
    },
    setEdition(state, payload) {
        state.editionName = payload;
    },
    setFoil(state, payload) {
        state.foil = payload;
    },
    setUnits(state, payload) {
        state.units = payload;
    },
    setAllEditions(state, payload) {
        state.allEditions = payload;
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
