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
      <span class="synchronize__bottom__text" v-if="downloadInProgress"
        >downloading new file...</span
      >
      <span class="synchronize__bottom__text synchronize__bottom__text--error" v-if="downloadError"
        >There was some error downloading file.</span
      >
      <span class="synchronize__bottom__text" v-if="syncInProgress">Synchronizing database...</span>
      <span class="synchronize__bottom__text synchronize__bottom__text--error" v-if="syncError"
        >There was some error synchronizing database.</span
      >
    </div>
  </div>
</template>

<script>
import api from '../api/api';

export default {
  data() {
    return {
      downloadInProgress: false,
      downloadError: false,
      syncInProgress: false,
      syncError: false,
    };
  },
  methods: {
    async downloadFile() {
      this.downloadInProgress = true;
      this.downloadError = !(await api.downloadCards());
      this.downloadInProgress = false;
    },
    async syncDatabase() {
      this.syncInProgress = true;
      this.syncError = !(await api.syncDatabaseFromFile());
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

    &__text {
      font-size: 22px;

      &--error {
        background-color: red;
      }
    }
  }
}
</style>
