import Vue from 'vue';
import Vuex from 'vuex';
import suggest from './modules/suggest';
import cardForm from './modules/cardForm';
import collectionForm from './modules/collectionForm';

Vue.use(Vuex);

export default new Vuex.Store({
    modules: {
        suggest,
        cardForm,
        collectionForm,
    },
});
