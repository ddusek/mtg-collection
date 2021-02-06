<template>
  <div class="container">
    <h2>Add card to collection</h2>
    <form class="form" action="post" v-on:submit.prevent="addCard">
      <div class="form__input">
        <label>Name</label>
        <input
          id="inputName"
          v-model="name"
          @input="getSuggestions()"
          class="form__input--textbox"
          placeholder="Nicol Bolas, Dragon-God"
        />
      </div>
      <div class="form__input">
        <label>Edition</label>
        <select v-model="selected_edition" id="inputName" class="form__input--dropdown">
          <option v-for="edition in all_editions" v-bind:value="edition.key" :key="edition.id">
            {{ edition.name }}
          </option>
        </select>
      </div>
      <div class="form__input">
        <label>Is foil</label>
        <input class="form__input--checkbox" v-model="foil" type="checkbox" id="checkbox" />
      </div>
      <div class="form__submit">
        <input type="submit" class="form__submit__button" value="Add" />
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
        return this.$store.state.cardForm.inputName;
      },
      set(value) {
        this.$store.dispatch('cardForm/updateName', value);
      },
    },
    selected_edition: {
      get() {
        return this.$store.state.cardForm.inputEdition;
      },
      set(value) {
        this.$store.dispatch('cardForm/updateEdition', value);
      },
    },
    all_editions: {
      get() {
        return this.$store.state.cardForm.allEditions;
      },
    },
  },
  methods: {
    ...mapActions({
      getSuggestions(dispatch) {
        dispatch('suggest/getSuggestions', { inputName: this.name });
      },
      getAllEditions(dispatch) {
        dispatch('cardForm/getAllEditions');
      },
      addCard(dispatch) {
        dispatch('cardForm/addCard');
      },
    }),
  },
  beforeMount() {
    this.getAllEditions();
  },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 500px;
  height: 320px;
  background-color: rgb(55, 55, 55);
  font-size: 22px;
  margin-right: 100px;
  margin-bottom: 100px;

  h2 {
    background-color: rgb(25, 25, 25);
    width: 100%;
    text-align: center;
    margin: 0 0 20px 0;
    padding: 12px 0 5px 0;
  }

  .form {
    width: 90%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    &__input {
      height: 50px;
      margin: 0 0 10px 0;
      width: 100%;
      display: flex;
      align-items: flex-start;

      &--textbox {
        height: 25px;
        width: 250px;
      }

      &--checkbox {
        width: 20px;
        height: 20px;
      }

      label {
        width: 25%;
        padding-right: 25px;
      }
    }
    &__submit {
      margin: 0 0 15px 0;

      &__button {
        min-width: 350px;
        min-height: 40px;
      }
    }
  }
}
</style>
