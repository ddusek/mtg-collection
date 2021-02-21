<template>
  <div class="suggestions">
    <button
      class="suggestions__card"
      v-for="card in suggestedCards"
      :key="card.key"
      @click="updateCard(card)"
    >
      <label
        class="suggestions__card--name"
        :class="{
          'suggestions__card--highlighted': $store.state.card.inputName == card.name,
        }"
      >
        {{ card.name }}
      </label>
      <label class="suggestions__card--edition">
        {{ card.edition }}
      </label>
    </button>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  computed: {
    suggestedCards() {
      return this.$store.state.suggest.items;
    },
  },
  methods: {
    ...mapActions({
      updateCard(dispatch, value) {
        dispatch('card/updateCard', value);
      },
    }),
  },
};
</script>

<style lang="scss" scoped>
@import '../styles/_variables';
.suggestions {
  display: flex;
  flex-flow: column wrap;
  height: 500px;

  button {
    background-color: $background-color-medium;
    height: 50px;
  }

  button:hover {
    background-color: $highlight-color-dark;
    cursor: pointer;
  }

  button:focus {
    background-color: $highlight-color;
    outline: 0;
  }

  &__card {
    min-width: 300px;
    display: flex;
    flex-direction: column;
    font-size: 20px;
    border: 0;
    :hover {
      cursor: pointer;
    }
    &--name {
      color: $primary-text-color;
      font-weight: 1000;
      overflow: visible;
    }

    &--highlighted {
      background-color: red;
    }

    &--edition {
      color: $primary-text-color;
      font-size: 16px;
    }
  }
}
</style>
