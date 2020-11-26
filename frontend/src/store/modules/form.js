import api from '../../api/cards';

const state = () => ({
    inputName: '',
    allEditions: [],
});

const getters = {};

const actions = {
    async updateName({ commit }, payload) {
        commit('setName', payload);
    },
    async getAllEditions({ commit }) {
        let data = await api.GetAllEditions();
        commit('setAllEditions', data);
    },
};

const mutations = {
    setName(state, payload) {
        state.inputName = payload;
    },
    setAllEditions(state, payload) {
        state.allEditions = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
