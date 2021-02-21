<template>
  <div class="container">
    <div>
      <CardForm />
    </div>
    <SuggestCardsList />
  </div>
</template>

<script>
import CardForm from './CardForm';
import SuggestCardsList from './SuggestCardsList';

export default {
  components: { CardForm, SuggestCardsList },
};
</script>

<style lang="scss" scoped>
.container {
  display: flex;
}
</style>
