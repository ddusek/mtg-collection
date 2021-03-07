<template>
  <div>
    <div class="container">
      <h2>Already logged in</h2>
      <div class="form__input form__submit">
        <button class="form__submit__button" v-on:click="logout">Log out</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  data() {
    return {};
  },
  methods: {
    ...mapActions({
      logout(dispatch) {
        dispatch('auth/logout');
      },
    }),
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
  margin: 0 10px;
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
