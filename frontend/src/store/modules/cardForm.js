import api from '../../api/cards';

const state = () => ({
    inputName: '',
    allEditions: [],
    addedSuccess: false,
});

const getters = {};

const actions = {
    async updateName({ commit }, payload) {
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
};

const mutations = {
    setName(state, payload) {
        state.inputName = payload;
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
