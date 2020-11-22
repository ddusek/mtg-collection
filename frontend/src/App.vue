<template>
    <div id="app">
        <header>
            <h1>MTG_Collection</h1>
        </header>
        <div id="main">
            <Form />
            <CardsList />
        </div>
    </div>
</template>

<script>
import Form from './components/CardsForm';
import CardsList from './components/CardsList';

export default {
    components: { Form, CardsList },
};
</script>
