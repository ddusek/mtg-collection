<template>
    <div class="suggestions">
        <button
            class="card"
            v-for="card in suggestedCards"
            :key="card.key"
            @click="updateName(card.key)"
        >
            <label class="name" :class="{ highlighted: $store.state.form.inputName == card.name }">
                {{ card.name }}
            </label>
            <label class="edition">{{ card.edition }}</label>
        </button>
    </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    computed: {
        suggestedCards() {
            return this.$store.state.cards.items;
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
