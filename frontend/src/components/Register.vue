<template>
  <div>
    <div class="container">
      <h2>Register new account</h2>
      <form method="post" v-on:submit.prevent="register">
        <div class="form__input">
          <input
            id="register-username"
            class="form__input--textbox"
            type="text"
            placeholder="Username"
            autocomplete="0"
            v-model="username"
          />
        </div>
        <div class="form__input">
          <input
            id="register-email"
            class="form__input--textbox"
            type="text"
            placeholder="Email"
            v-model="email"
          />
        </div>
        <div class="form__input">
          <input
            id="register-password"
            class="form__input--textbox"
            type="password"
            placeholder="Password"
            v-model="password"
          />
        </div>
        <div class="form__input">
          <input
            id="register-password-repeat"
            class="form__input--textbox"
            type="password"
            placeholder="Repeat password"
          />
        </div>
        <div class="form__input form__submit">
          <input type="submit" class="form__submit__button" value="Register" />
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
export default {
  data() {
    return {
      username: '',
      password: '',
      email: '',
    };
  },
  methods: {
    ...mapActions({
      register(dispatch) {
        dispatch('auth/register', {
          username: this.username,
          password: this.password,
          email: this.email,
        });
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

    &--textbox {
      height: 30px;
      width: 300px;
      border-radius: 5px;
      padding: 0 0 0 10px;
    }

    label {
      width: 25%;
      height: 30px;
      padding-top: 4px;
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
