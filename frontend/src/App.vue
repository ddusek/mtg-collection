<template>
  <div id="app">
    <header>
      <h1>MTG_Collection</h1>
    </header>
    <div id="main">
      <div>
        <CardForm />
        <CollectionForm />
        <Synchronize />
        <Collection />
      </div>
      <CardsList />
    </div>
  </div>
</template>

<script>
import CardForm from './components/CardForm';
import CollectionForm from './components/CollectionForm';
import CardsList from './components/CardsList';
import Synchronize from './components/Synchronize';
import Collection from './components/Collection';

export default {
  components: { CardForm, CollectionForm, CardsList, Synchronize, Collection },
};
</script>
