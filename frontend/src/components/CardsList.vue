<template>
  <div class="suggestions">
    <button
      class="suggestions__card"
      v-for="card in suggestedCards"
      :key="card.key"
      @click="updateName(card.key)"
    >
      <label
        class="suggestions__card--name"
        :class="{
          'suggestions__card--highlighted': $store.state.card.inputName == card.name,
        }"
      >
        {{ card.name }}
      </label>
      <label class="suggestions__card--edition">{{ card.edition }}</label>
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
      updateName(dispatch, value) {
        dispatch('card/updateName', value);
      },
    }),
  },
};
</script>

<style lang="scss" scoped>
@import '../styles/_variables';
.suggestions {
  display: flex;
  flex-direction: column;
  width: 700px;

  button {
    background-color: $card-button-color;
  }

  button:hover {
    background-color: $card-button-hover;
    cursor: pointer;
  }

  button:focus {
    background-color: rgb(25, 125, 25);
  }

  &__card {
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 5px;
    font-size: 20px;
    :hover {
      cursor: pointer;
    }
    &--name {
      color: rgb(225, 225, 225);
    }

    &--highlighted {
      background-color: red;
    }

    &--edition {
      color: rgb(155, 155, 0);
    }
  }
}
</style>
