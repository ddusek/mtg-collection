<template>
  <div class="container">
    <div>
      <CardForm />
    </div>
    <CardsList />
  </div>
</template>

<script>
import CardForm from './CardForm';
import CardsList from './CardsList';

export default {
  components: { CardForm, CardsList },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
}
</style>
