<template>
<link href="https://fonts.googleapis.com/css2?family=Megrim&family=Nunito&display=swap" rel="stylesheet">
  <Nav :mode='false'/>
  <form class="search-form">
    <input v-model='search_content' @mousedown='handleInputClick' class='search' type="text">
    <button class="search-button noselect">GO</button>
  </form>
</template>

<script>
import { ref } from 'vue'
import Nav from '../components/Nav.vue'
export default {
  name: 'Home',
  components: {Nav},

  setup() {

    const search_content = ref('Enter a Reddit thread...')
    const default_search_value = ref(true)

    const handleInputClick = () => {
      if(default_search_value.value){
        default_search_value.value = false;
        search_content.value = ''
      }
    }

    return {search_content, default_search_value, handleInputClick}

  }

}
</script>

<style>

.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Old versions of Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}

  body {
    background: url('~@/assets/background.jpg')no-repeat center center fixed;
    background-size: cover;
  }

  .search-form {
  width: 60%;
  margin: 300px auto;
}

.search-form input {
  width: 100%;
  font-size: 28px;
  border: none;
  padding: 10px 5px 10px 5px;
  color: rgb(50,50,50);
  letter-spacing: 2px;;
}

.search-form input.def {
  color: rgb(110, 110, 110);
  font-size: 28px;
}

.search-form input:focus {
  outline: none;
}

.button-holder {
  margin: 50px auto; 
}

.search-button {
  width: 200px;
  padding: 20px;
  margin: auto;
  margin-top: 50px;
  display: block;
  border: 3px solid white;
  border-radius: 50px;
  color: white;
  background: rgba(255,255,255,0.2);
  font-family: 'Nunito';
  text-transform: uppercase;
  transition: .2s;
  font-size: 24px;
  text-align: center;
  font-weight: bold;
  letter-spacing: 3px;
}

.search-button:hover {
  background: rgba(255,255,255,0.5);
  cursor: pointer;
}
</style>