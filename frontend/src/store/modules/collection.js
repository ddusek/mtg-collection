import api from '../../api/cards';

const state = () => ({
    name: '',
    showMsg: false,
    msgType: '',
    allCollections: [],
    collectionCards: [],
    collectionName: '',
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
    async getCollectionCards({ commit }, payload) {
        let data = await api.getCollectionCards(payload);
        commit('setCollectionCards', data);
    },
    async getAllCollections({ commit }) {
        let data = await api.getAllCollections();
        commit('setAllCollections', data);
    },
    updateCollection({ commit }, payload) {
        commit('setCollection', payload);
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
    setCollectionCards(state, payload) {
        state.collectionCards = payload;
    },
    setAllCollections(state, payload) {
        state.allCollections = payload;
    },
    setCollection(state, payload) {
        state.collectionName = payload;
    },
};

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations,
};
