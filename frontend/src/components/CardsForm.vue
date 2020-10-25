<template>
    <div class="container">
        <h2>Add card to collection</h2>
        <form class="form-inputs">
            <div class="form-item">
                <label>Card name</label>
                <input
                    v-model="name"
                    @change="getSuggestions"
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
import suggestions from '../api/suggestions';
export default {
    data: function () {
        return {
            name: '',
            foil: '',
            testData: '',
        };
    },
    methods: {
        getSuggestions: async function () {
            this.testData = await suggestions.GetSuggestion();
        },
    },
};
</script>
