<template>
  <div class="container">
    <h2>Add card to collection</h2>
    <form class="form" action="post" v-on:submit.prevent="addCard">
      <div class="form__input">
        <label>Card name</label>
        <input
          id="cardName"
          v-model="name"
          @input="getSuggestions()"
          class="form__input--textbox"
          placeholder="Nicol Bolas, Dragon-God"
          autocomplete="off"
        />
      </div>
      <div class="form__input">
        <label>Edition</label>
        <select v-model="selected_edition" id="edition" class="form__input--dropdown">
          <option
            v-for="edition in all_editions"
            v-bind:value="edition.key"
            :key="edition.id"
            :selected="edition.name === selected_edition"
          >
            {{ edition.name }}
          </option>
        </select>
      </div>
      <div class="form__input">
        <label>Is foil</label>
        <div class="form__input--checkbox">
          <input
            class="form__input--checkbox regular-checkbox"
            v-model="foil"
            type="checkbox"
            id="checkbox"
          />
        </div>
      </div>
      <div class="form__input">
        <label>Units</label>
        <input
          id="cardUnits"
          type="number"
          v-model="units"
          class="form__input--textbox form__input--textbox__number"
          min="1"
          max="999"
        />
        <div class="form__input__edit">
          <button
            type="button"
            class="form__input__edit__button form__input__edit__button--increment"
            v-on:click="units++"
            :disabled="units >= 999"
          >
            ▲
          </button>
          <button
            type="button"
            class="form__input__edit__button form__input__edit__button--decrement"
            v-on:click="units--"
            :disabled="units <= 1"
          >
            ▼
          </button>
        </div>
      </div>
      <div class="form__input">
        <label>Collection</label>
        <select v-model="selected_collection" id="collection" class="form__input--dropdown">
          <option
            v-for="collection in all_collections"
            :value="collection.key"
            :key="collection.id"
          >
            {{ collection.name }}
          </option>
        </select>
      </div>
      <div class="form__input form__submit">
        <input type="submit" class="form__submit__button" value="Add" />
      </div>
    </form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  computed: {
    name: {
      get() {
        return this.$store.state.card.cardName;
      },
      set(value) {
        this.$store.dispatch('card/updateName', value);
      },
    },
    all_editions: {
      get() {
        return this.$store.state.card.allEditions;
      },
    },
    all_collections: {
      get() {
        return this.$store.state.collection.allCollections;
      },
    },
    selected_edition: {
      get() {
        return this.$store.state.card.editionName;
      },
      set(value) {
        this.$store.dispatch('card/updateEdition', value);
      },
    },
    foil: {
      get() {
        return this.$store.state.card.foil;
      },
      set(value) {
        this.$store.dispatch('card/updateFoil', value);
      },
    },
    units: {
      get() {
        return this.$store.state.card.units;
      },
      set(value) {
        this.$store.dispatch('card/updateUnits', value);
      },
    },
    selected_collection: {
      get() {
        return this.$store.state.collection.collectionName;
      },
      set(value) {
        this.$store.dispatch('collection/updateCollection', value);
      },
    },
  },
  methods: {
    ...mapActions({
      getSuggestions(dispatch) {
        dispatch('suggest/getSuggestions', { cardName: this.name });
      },
      getAllEditions(dispatch) {
        dispatch('card/getAllEditions');
      },
      getAllCollections(dispatch) {
        dispatch('collection/getAllCollections');
      },
      addCard(dispatch) {
        dispatch('card/addCard', {
          collection: this.selected_collection,
          card: this.name,
          units: this.units,
        });
      },
    }),
  },
  beforeMount() {
    this.getAllEditions();
    this.getAllCollections();
  },
};
</script>

<style lang="scss" scoped>
@import '../styles/_variables';

.container {
  background-color: $background-color-medium;
  display: flex;
  flex-direction: column;
  width: 450px;
}
.form {
  width: 100%;
  box-sizing: border-box;
  padding: 0 30px;

  &__input {
    height: 50px;
    margin-bottom: 10px;
    width: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    input {
      margin: 0;
      border: 0;
    }
    :focus {
      outline: 0;
      box-shadow: 0 0 3pt 2pt $highlight-color;
      z-index: 10;
      border: 0;
    }

    &--textbox {
      height: 30px;
      width: 240px;
      border-radius: 5px;
      padding: 0 0 0 10px;

      &__number {
        width: 210px;
        height: 30px;
        border-radius: 5px 0 0 5px;
      }
    }

    &--dropdown {
      height: 30px;
      width: 250px;
      border-radius: 5px;
      padding: 0 0 0 5px;
      background-color: #ffffff;
    }

    &--checkbox {
      padding-right: 225px;
      height: 20px;
      width: 20px;
      margin-top: 3px;

      .regular-checkbox {
        -webkit-appearance: none;
        background-color: #ffffff;
        padding: 0;
        border-radius: 4px;
        position: relative;
      }

      .regular-checkbox:checked {
        background-color: $highlight-color;
      }

      .regular-checkbox:checked:after {
        content: '\2714';
        font-size: 18px;
        position: absolute;
        top: -1px;
        left: 2px;
        color: #ffffff;
      }
    }

    label {
      width: 25%;
      height: 30px;
      padding-top: 4px;
    }

    &__edit {
      display: flex;
      flex-direction: column;

      :hover {
        background-color: $highlight-color;
      }
      &__button {
        height: 15px;
        width: 28px;
        padding: 0;
        border: 0;
        font-size: 12px;
        background-color: #ffffff;

        &--increment {
          border-radius: 0 6px 0 0;
        }
        &--decrement {
          border-radius: 0 0 6px 0;
        }
      }
    }
  }
  &__submit {
    margin: 0 0 15px 0;
    :hover {
      background-color: $highlight-color;
    }

    &__button {
      min-width: 350px;
      min-height: 40px;
      border-radius: 5px;
    }
  }
}
</style>
