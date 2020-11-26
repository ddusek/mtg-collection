import api from '../../api/cards';

const state = () => ({
    items: [],
});

const getters = {};

const actions = {
    async getSuggestions({ commit }, payload) {
        let data = await api.GetCardSuggestions(payload.inputName);
        commit('setItems', data);
    },
};

const mutations = {
    setItems(state, payload) {
        state.items = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
