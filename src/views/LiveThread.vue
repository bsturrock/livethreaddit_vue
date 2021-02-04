<template>
<link href="https://fonts.googleapis.com/css2?family=Megrim&family=Nunito&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<div class="real-content">
    <Nav @login='handleLoginClick' @logout='handleLogoutClick' :title='title' :logged_in="logged_in" :subreddit='subreddit' :threadid='threadid' :mode='true'/>
    <div v-if='!loading_data' class="spinner">
        <Spinner />
        <h2 class="spinner_text">Loading your liveTHREADDIT</h2>
        <div class="spinner_item">
            <i v-if='!connection' class="spinner_item_icon far fa-square"></i>
            <i v-if='connection' class="spinner_item_icon far fa-check-square"></i>
            <h2 class="spinner_item_text">Connecting to Reddit thread</h2>
        </div>
        <div class="spinner_item">
            <i v-if='!title' class="spinner_item_icon far fa-square"></i>
            <i v-if='title' class="spinner_item_icon far fa-check-square"></i>
            <h2 class="spinner_item_text">Getting thread details</h2>
        </div>
    </div>
        <CommentBox @lock='handleLock' v-if='loading_data && !lock' :threadid='threadid' :logged_in='logged_in'/>
        <div v-if='lock' class="errorblock">
            <i class="icon-large fas fa-lock"></i>
            <h1>THREAD HAS BEEN LOCKED</h1>
            <router-link class='backtohome' :to="{name:'Home'}">Try a new thread?</router-link>
        </div>
</div>
</template>

<script>
import { ref } from 'vue'
import Nav from '../components/Nav.vue'
import Spinner from '../components/Spinner.vue'
import CommentBox from '../components/CommentBox.vue'
import { useRoute } from 'vue-router'
export default {
    name: 'LiveThread',
    props: ['subreddit', 'threadid', 'temptitle'],
    components: { Nav, Spinner, CommentBox},
    setup(props, { emit }) {

    const logged_in = ref(false)
    const connection = ref(false)
    const route = useRoute()
    const loading_data = ref(false)
    const title = ref('')
    const lock = ref(false)

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

    checkForLogin() 

    const initRedditStream = async () => {
        let response = await fetch('http://localhost:5000/init', {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({
                'threadid' : props.threadid,
                'subreddit' : props.subreddit,
                'title' : title.value
            })
        })          
        let response_json = await response.json()
        connection.value = true
    }

    initRedditStream()

    const getThreadTitle = async () => {
        let response = await fetch('http://localhost:5000/title', {
            method: 'POST',
            headers: {'Content-Type' : 'application/json'},
            body: JSON.stringify({
                'threadid' : props.threadid
            })
        })        
        let response_json = await response.json()
        title.value = response_json.title


        function go() {
            loading_data.value = true
        }

        setTimeout(go,2000)
        
    }
    
    const handleLock = () => {
        lock.value = true
    }

    getThreadTitle()


    return {handleLoginClick, handleLogoutClick, logged_in, checkForLogin, loading_data, title, connection, handleLock, lock}

    }
}
</script>

<style>

    .backtohome {
        border: 3px solid white;
        border-radius: 50px;
        color: white;
        background: rgba(255,255,255,0.2);
        font-family: 'Nunito';
        text-transform: uppercase;
        transition: .2s;
        font-size: 14px;
        text-align: center;
        font-weight: bold;
        letter-spacing: 3px;
        text-decoration: none;
        padding: 20px;
        margin-top: 50px;
        display: inline-block;
    }

    .backtohome:hover {
        background: rgba(255,255,255,0.6);
    }

    .icon-large {
        font-size: 70px;
        padding: 25px;
    }

    .errorblock {
        margin: auto;
        color: white;
        font-family: 'Nunito';
        margin-top: 200px;

    }

    .real-content {
        height: 100vh;
    }
    .spinner {
        padding: 50px;
        margin: auto;
        margin-top: 300px;
        margin-bottom: 50px;
    }

    .spinner_text {
        color: white;
        font-family: 'Megrim';
        font-size: 30px;
        text-align: center;
    }

    .spinner_item {
        display: flex;
        margin: auto;
        width: 500px;
        justify-content: center;
        align-content: center;
        align-items: center;
    }

    .spinner_item_icon {
        color: white;
        font-size: 20px;
        padding: 10px;
        margin: 0;
    }

    .spinner_item_text {
        color: white;
        font-size: 20px;
        font-family: 'Nunito';
    }

</style>