import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import store from './store';
import Home from './components/PageHome';
import Collections from './components/PageCollections';
import AddCollection from './components/PageAddCollection';
import AddCard from './components/PageAddCard';
import Authentication from './components/PageAuthentication';
import './styles/main.scss';

Vue.use(VueRouter);

const router = new VueRouter({
    mode: 'history',
    base: __dirname,
    routes: [
        { path: '/', component: Home },
        { path: '/collections', component: Collections },
        { path: '/add-collection', component: AddCollection },
        { path: '/add-card', component: AddCard },
        { path: '/authentication', component: Authentication },
    ],
});

new Vue({
    el: '#app',
    store,
    router,
    render: (h) => h(App),
});
