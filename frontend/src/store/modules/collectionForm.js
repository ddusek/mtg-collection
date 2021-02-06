import api from '../../api/cards';

const state = () => ({
    name: '',
    showMsg: false,
    msgType: '',
});

const getters = {};

const actions = {
    async updateName({ commit }, payload) {
        commit('setName', payload);
    },
    async addCollection({ commit }, payload) {
        let data = await api.addCollection(payload);
        commit('setShowMessage', data);
    },
    async showMessage({ commit }) {
        commit('setShowMessage');
    },
};

const mutations = {
    setName(state, payload) {
        state.name = payload;
    },
    setShowMessage(state, payload) {
        if (payload == true) {
            state.msgType = 'success';
        } else {
            state.msgType = 'failed';
        }
        state.showMsg = true;
        setTimeout(() => {
            state.showMsg = false;
        }, 3000);
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
