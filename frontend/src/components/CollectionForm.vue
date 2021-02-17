<template>
  <div class="container">
    <h2>Add new collection</h2>
    <form class="form" action="post" v-on:submit.prevent="addCollection">
      <div class="form__input">
        <label>Name</label>
        <input
          id="collectionName"
          v-model="name"
          class="form__input--textbox"
          placeholder="Cool deck"
        />
      </div>
      <div class="form__submit">
        <input type="submit" class="form__submit__button" value="Add" />
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
.container {
  display: flex;
  align-items: center;
  flex-direction: column;
  width: 500px;
  height: 220px;
  background-color: rgb(55, 55, 55);
  font-size: 22px;
  margin-right: 100px;

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
  .highlight {
    width: 300;
    height: 100px;
    &--success {
      background-color: green;
    }
    &--failed {
      background-color: red;
    }
  }
}
</style>
