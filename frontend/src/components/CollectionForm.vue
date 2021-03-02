<template>
  <div class="container">
    <h2>Add new collection</h2>
    <form class="form" method="post" v-on:submit.prevent="addCollection">
      <div class="form__input">
        <label>Name</label>
        <input
          id="collectionName"
          v-model="name"
          class="form__input form__input--textbox"
          placeholder="Cool deck"
        />
      </div>
      <div class="form__input form__input__submit">
        <input type="submit" class="form__input__submit__button" value="Add" />
      </div>
    </form>
    <div v-if="showMsg" class="highlight--success">
      <span :class="`highlight--${this.msgType}`">{{ this.msg }}</span>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  computed: {
    name: {
      get() {
        return this.$store.state.collection.name;
      },
      set(value) {
        this.$store.dispatch('collection/updateName', value);
      },
    },
    showMsg: {
      get() {
        return this.$store.state.collection.showMsg;
      },
    },
    msgType: {
      get() {
        return this.$store.state.collection.msgType;
      },
    },
    msg: {
      get() {
        if (this.msgType == 'success') {
          return 'New collection added.';
        } else {
          return 'Failed to add new collection';
        }
      },
    },
  },
  methods: {
    ...mapActions({
      addCollection(dispatch) {
        dispatch('collection/addCollection', this.name);
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
}
.form {
  width: 100%;
  box-sizing: border-box;
  padding: 0 30px;

  &__input {
    height: 50px;
    margin-bottom: 10px;
    margin-top: 5px;
    width: 100%;
    display: flex;
    justify-content: center;
    input {
      margin: 0;
      border: 0;
    }
    :focus {
      outline: 0;
      box-shadow: 0 0 3pt 2pt $highlight-color;
      border: 0;
    }

    &--textbox {
      height: 30px;
      width: 240px;
      border-radius: 5px;
      padding: 0 0 0 10px;
    }

    label {
      width: 25%;
      height: 30px;
      padding-top: 4px;
    }

    &__submit {
      margin: 0 0 15px 0;
      align-items: flex-start;
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
}
.highlight {
  width: 300px;
  height: 100px;
  &--success {
    background-color: green;
  }
  &--failed {
    background-color: red;
  }
}
</style>
