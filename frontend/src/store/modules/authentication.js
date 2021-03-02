import api from '../../api/api';

const state = () => ({
    loggedIn: false,
    username: '',
    userID: '',
});

const getters = {};

const actions = {
    updateLoggedIn({ commit }, payload) {
        commit('setLoggedIn', payload);
    },
    updateUsername({ commit }, payload) {
        commit('setUsername', payload.name);
    },
    updateUserID({ commit }, payload) {
        commit('setUserID', payload);
    },
    async login({ commit }, payload) {
        let data = await api.login(payload.username, payload.password);
        if (data !== null && data.success === true) {
            commit('setLoggedIn', true);
            commit('setUsername', data.username);
            commit('setUserID', data.userID);
        }
    },
    async register({ commit }, payload) {
        let data = await api.register(payload);
        if (data !== null && data.success === true) {
            commit('setLoggedIn', true);
            commit('setUsername', data.username);
            commit('setUserID', data.userID);
        }
    },
    async logout({ commit }) {
        let data = await api.logout();
        if (data !== null && data.success === true) {
            commit('setLoggedIn', false);
            commit('setUsername', '');
            commit('setUserID', 0);
        }
    },
};

const mutations = {
    setLoggedIn(state, payload) {
        state.loggedIn = payload;
    },
    setUsername(state, payload) {
        state.username = payload;
    },
    setUserID(state, payload) {
        state.userID = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
