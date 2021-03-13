import api from '../../api/api';
import cookies from '../../js/cookies';
const state = () => ({
    statesSet: false,
    loggedIn: false,
    username: '',
    userID: '',
});

const getters = {};

const actions = {
    async login({ commit }, payload) {
        let data = await api.login(payload);
        if (data !== null && data.success === true) {
            commit('setStatesSet');
            commit('setLoggedIn', true);
            commit('setUsername', data.username);
            commit('setUserID', data.userID);
        }
    },
    async register({ commit }, payload) {
        let data = await api.register(payload);
        if (data !== null && data.success === true) {
            commit('setStatesSet');
            commit('setLoggedIn', true);
            commit('setUsername', data.username);
            commit('setUserID', data.userID);
        }
    },
    async logout({ commit }) {
        let data = await api.logout();
        if (data !== null && data.success === true) {
            commit('setStatesSet');
            commit('setLoggedIn', false);
            commit('setUsername', '');
            commit('setUserID', 0);
        }
    },
    setStatesFromCookie({ commit }) {
        commit('setStatesSet');
        commit('setLoggedIn', !!cookies.getCookie(cookies.USER_TOKEN));
        commit('setUsername', cookies.getCookie(cookies.USERNAME));
        commit('setUserID', cookies.getCookie(cookies.USER_ID));
    },
};

const mutations = {
    setStatesSet(state) {
        state.statesSet = true;
    },
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
