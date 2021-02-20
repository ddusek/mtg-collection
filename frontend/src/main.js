import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import store from './store';
import './styles/main.scss';
import Home from './components/PageHome';
import Collections from './components/PageCollections';
import AddCollection from './components/PageAddCollection';
import AddCard from './components/PageAddCard';

Vue.use(VueRouter);

// 3. Create the router
const router = new VueRouter({
    mode: 'history',
    base: __dirname,
    routes: [
        { path: '/', component: Home },
        { path: '/collections', component: Collections },
        { path: '/add-collection', component: AddCollection },
        { path: '/add-card', component: AddCard },
    ],
});

new Vue({
    el: '#app',
    store,
    router,
    render: (h) => h(App),
});
