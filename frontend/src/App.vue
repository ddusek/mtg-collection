<template>
  <div id="app">
    <header>
      <h1>MTG_Collection</h1>
    </header>
    <div id="main">
      <div>
        <CardForm />
        <CollectionForm />
      </div>
      <CardsList />
    </div>
  </div>
</template>

<script>
import CardForm from './components/CardForm';
import CollectionForm from './components/CollectionForm';
import CardsList from './components/CardsList';

export default {
  components: { CardForm, CollectionForm, CardsList },
};
</script>
