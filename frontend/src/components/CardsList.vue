<template>
    <div class="suggestions">
        <button
            class="card"
            v-for="card in suggestedCards"
            :key="card.key"
            v-on:click="updateName(card.key)"
        >
            <label class="name">{{ card.name }}</label>
            <label class="edition">{{ card.edition }}</label>
        </button>
    </div>
</template>

<script>
import { mapActions } from 'vuex';
import store from '../store/index';

export default {
    computed: {
        suggestedCards() {
            return store.state.cards.items;
        },
    },
    methods: {
        ...mapActions({
            updateName(dispatch, value) {
                dispatch('form/updateName', value);
            },
        }),
    },
};
</script>
