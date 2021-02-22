<template>
  <div class="collection">
    <select
      v-model="selected_collection"
      @change="getCollectionCards"
      name="collection"
      id="collection"
    >
      <option v-for="collection in collections" :key="collection.key" :value="collection.name">
        {{ collection.name }}
      </option>
    </select>
    <div>
      <table v-if="hasCards">
        <thead>
          <tr>
            <th>Card name</th>
            <th>Set</th>
            <th>Price</th>
            <th>Price foil</th>
            <th>Release</th>
          </tr>
        </thead>
        <tfoot>
          <tr>
            <td colspan="2">total</td>
            <td colspan="3">9999</td>
          </tr>
        </tfoot>
        <tbody>
          <tr v-for="card in collectionCards" :key="card.id">
            <td>{{ card.name }}</td>
            <td>{{ card.edition }}</td>
            <td>{{ card.price }}</td>
            <td>{{ card.price_foil }}</td>
            <td>{{ card.release }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  computed: {
    collections: {
      get() {
        return this.$store.state.collection.allCollections;
      },
    },
    selected_collection: {
      get() {
        return this.$store.state.collection.collectionName;
      },
      set(value) {
        this.$store.dispatch('collection/updateCollection', value);
      },
    },
    collectionCards: {
      get() {
        return this.$store.state.collection.collectionCards;
      },
      set(value) {
        this.$store.dispatch('collection/setCollectionCards', value);
      },
    },
    hasCards: {
      get() {
        return this.collectionCards.length;
      },
    },
  },
  methods: {
    ...mapActions({
      getCollectionCards(dispatch) {
        dispatch('collection/getCollectionCards', this.selected_collection);
      },
      getAllCollections(dispatch) {
        dispatch('collection/getAllCollections');
      },
    }),
  },
  beforeMount() {
    this.getAllCollections();
  },
};
</script>

<style lang="scss" scoped>
.collection {
  table {
    border: 1px solid black;
    border-collapse: collapse;
  }
  td,
  th {
    border: 1px solid rgb(255, 255, 255);
    padding: 0.5rem;
    text-align: left;
  }
  tr:nth-child(even) {
    background: hsl(0, 0%, 35%);
  }
  tr:nth-child(odd) {
    background: hsl(0, 0%, 40%);
  }
}
</style>
