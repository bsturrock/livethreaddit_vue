<template>
<link href="https://fonts.googleapis.com/css2?family=Megrim&family=Nunito&family=Share+Tech+Mono&display=swap" rel="stylesheet">
  <Nav @login='handleLoginClick' @logout='handleLogoutClick' :logged_in="logged_in" :mode='false'/>
  <form @submit.prevent='handleForm' class="search-form">
    <input v-model='search_content' @mousedown='handleInputClick' class='search' type="text">
    <button class="search-button noselect">GO</button>
  </form>
</template>

<script>

import { ref, computed } from 'vue'
import Nav from '../components/Nav.vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  name: 'Home',
  components: {Nav},

  setup() {
    const logged_in = ref(false)
    const search_content = ref('Enter a Reddit thread...')
    const default_search_value = ref(true)
    const route = useRoute()
    const router = useRouter()

    const handleInputClick = () => {
      if(default_search_value.value){
        default_search_value.value = false;
        search_content.value = ''
      }
    }

    const handleLoginClick = async () => {
      document.cookie = 'redirect=http://localhost:8080' + route.path;
        let response = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({
                'redirect' : 'http://localhost:8080' + route.path
            })
        })

      let response_json = await response.json()
      let redirect_uri = response_json.url
      window.location = redirect_uri
    }

    const handleLogoutClick = () => {
      document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      checkForLogin()
    }

    const checkForLogin = () => {
      var b = document.cookie.match('(^|;)\\s*' + 'user' + '\\s*=\\s*([^;]+)');
      logged_in.value =  b ? b.pop() : false; 
    }

    const handleForm = () => {
      let parts = search_content.value.split('/')
      let newuri = 'http://localhost8080:/r/' + parts[4] + '/comments/' + parts[6]
      router.push({name: 'LiveThread', params: {subreddit: parts[4], threadid: parts[6], temptitle: parts[7]}})
    }      
    

    checkForLogin()

    return {search_content, default_search_value, handleInputClick, handleLoginClick, logged_in, checkForLogin, handleLogoutClick, handleForm}

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