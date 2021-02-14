<template>
  <div class="synchronize">
    <div class="synchronize__top">
      <span class="synchronize__top__button" v-on:click="syncDatabase()"> sync db </span>
      <span
        class="synchronize__top__button synchronize__top__button--m10"
        v-on:click="downloadFile()"
      >
        download data
      </span>
    </div>
    <div class="synchronize__bottom">
      <span>progress bar</span>
      <span v-if="downloadInProgress">downloading new file...</span>
      <span v-if="syncInProgress">Synchronizing database...</span>
    </div>
  </div>
</template>

<script>
import api from '../api/cards';

export default {
  data() {
    return {
      downloadInProgress: false,
      syncInProgress: false,
    };
  },
  methods: {
    downloadFile() {
      this.downloadInProgress = true;
      api.downloadCards();
      this.downloadInProgress = false;
    },
    syncDatabase() {
      this.syncInProgress = true;
      api.syncDatabaseFromFile();
      this.syncInProgress = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.synchronize {
  margin-top: 50px;
  width: 410px;
  height: 110px;
  display: flex;
  flex-direction: column;
  border: 2px red solid;
  text-align: center;

  &__top {
    width: 100%;
    display: flex;

    &__button {
      background-color: rgb(55, 55, 55);
      width: 200px;
      height: 50px;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      &--m10 {
        margin-left: 10px;
      }
    }
  }

  &__bottom {
    width: 100%;
    height: 50px;
    display: flex;
    flex-direction: column;
    margin-top: 10px;
    background-color: rgb(55, 55, 55);
  }
}
</style>
