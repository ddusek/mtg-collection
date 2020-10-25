<template>
    <div class="container">
        <h2>Add card to collection</h2>
        <form class="form-inputs" autocomplete="off">
            <div class="form-item autocomplete">
                <label>Card name</label>
                <input
                    id="cardname"
                    v-model="name"
                    @input="autocomplete()"
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
import autocomplete from '../helpers/autocomplete';

export default {
    data: function () {
        return {
            name: '',
            foil: '',
            suggestionsData: '',
        };
    },
    methods: {
        autocomplete: async function () {
            if (this.name.length > 2) {
                this.suggestionsData = await suggestions.GetSuggestion(this.name);
                console.log(this.suggestionsData);
                autocomplete.Autocomplete(
                    document.getElementById('cardname', this.suggestionsData)
                );
            }
        },
    },
};
</script>
