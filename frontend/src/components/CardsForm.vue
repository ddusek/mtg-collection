<template>
    <div class="form">
        <h2>Add card to collection</h2>
        <form class="form-inputs" autocomplete="off">
            <div class="form-item">
                <label>Name</label>
                <input
                    id="cardInputName"
                    v-model="name"
                    @input="getSuggestions()"
                    class="textbox"
                    placeholder="Nicol Bolas, Dragon-God"
                />
            </div>
            <div class="form-item">
                <label>Edition</label>
                <select v-model="selected_edition" id="cardInputName" class="dropdown">
                    <option
                        v-for="edition in all_editions"
                        v-bind:value="edition.key"
                        :key="edition.id"
                    >
                        {{ edition.name }}
                    </option>
                </select>
            </div>
            <div class="form-item">
                <label>Is foil</label>
                <input class="checkbox" v-model="foil" type="checkbox" id="checkbox" />
            </div>
            <div class="form-submit">
                <input type="submit" class="button" value="Add" />
            </div>
        </form>
    </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    data: function () {
        return {
            foil: '',
        };
    },
    computed: {
        name: {
            get() {
                return this.$store.state.form.inputName;
            },
            set(value) {
                this.$store.dispatch('form/updateName', value);
            },
        },
        selected_edition: {
            get() {
                return this.$store.state.form.inputEdition;
            },
            set(value) {
                this.$store.dispatch('form/updateEdition', value);
            },
        },
        all_editions: {
            get() {
                return this.$store.state.form.allEditions;
            },
        },
    },
    methods: {
        ...mapActions({
            getSuggestions(dispatch) {
                dispatch('cards/getSuggestions', { inputName: this.name });
            },
            getAllEditions(dispatch) {
                dispatch('form/getAllEditions');
            },
        }),
    },
    beforeMount() {
        this.getAllEditions();
    },
};
</script>
