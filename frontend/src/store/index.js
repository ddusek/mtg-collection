import Vue from 'vue';
import Vuex from 'vuex';
import suggest from './modules/suggest';
import card from './modules/card';
import collection from './modules/collection';
import user from './modules/user';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        suggest,
        card,
        collection,
        user,
    },
});
