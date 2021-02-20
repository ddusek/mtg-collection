<template>
  <div id="app">
    <header>
      <h1>
        <router-link to="/">MTG Collection</router-link>
      </h1>
      <ul>
        <li><router-link to="/collections">Collections</router-link></li>
        <li><router-link to="/add-collection">Add collection</router-link></li>
        <li><router-link to="/add-card">Add card</router-link></li>
      </ul>
    </header>
    <div id="main">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  components: {},
};
</script>

<style lang="scss">
@import 'styles/_variables';
header {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
  background-color: $header-color;
  border-bottom: 2px $highlight-color solid;

  .title {
    width: 250px;
    margin-left: 25px;
  }

  .menu {
    display: flex;
    padding-inline-start: 0;
    width: 100%;
    align-content: flex-end;
  }

  .item {
    margin: 0 30px;
    list-style-type: none;

    a {
      color: $primary-text-color;
    }
  }
}
</style>
