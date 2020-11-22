const state = () => ({
    inputName: '',
});

const getters = {};

const actions = {
    async updateName({ commit }, payload) {
        commit('setName', payload);
    },
};

const mutations = {
    setName(state, payload) {
        state.inputName = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
