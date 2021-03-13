<template>
  <div class="auth">
    <Login v-if="!$store.state.user.loggedIn" />
    <Register v-if="!$store.state.user.loggedIn" />
    <Logout v-if="$store.state.user.loggedIn" />
  </div>
</template>

<script>
import Login from './Login';
import Register from './Register';
import Logout from './Logout';

export default {
  components: { Login, Register, Logout },
};
</script>

<style lang="scss" scoped>
@import '../styles/_variables';
.auth {
  display: flex;
  padding: 0 10px;
}
</style>
