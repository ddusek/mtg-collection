<template>
  <div id="app">
    <header>
      <h1>
        <router-link to="/">MTG_Collection</router-link>
      </h1>
      <ul>
        <li><router-link to="/collections">collections</router-link></li>
        <li><router-link to="/add-collection">add collection</router-link></li>
        <li><router-link to="/add-card">add card</router-link></li>
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
