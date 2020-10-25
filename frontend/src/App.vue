<template>
    <div id="app">
        <header>
            <h1>MTG_Collection</h1>
        </header>
        <div id="main">
            <Form />
        </div>
    </div>
</template>

<script>
import Form from './components/CardsForm';
export default {
    components: { Form },
};
</script>
