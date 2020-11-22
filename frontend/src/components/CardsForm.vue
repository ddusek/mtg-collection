<template>
    <div class="container">
        <h2>Add card to collection</h2>
        <form class="form-inputs" autocomplete="off">
            <div class="form-item">
                <label>Card Name</label>
                <input
                    id="cardinputName"
                    v-model="name"
                    @input="getSuggestions()"
                    class="textbox"
                    placeholder="Nicol Bolas, Dragon-God"
                />
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
            suggestedCards: [],
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
    },
    methods: {
        ...mapActions({
            getSuggestions(dispatch) {
                dispatch('cards/getSuggestions', { inputName: this.name });
            },
        }),
    },
};
</script>
