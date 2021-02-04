<template>

  <nav class="menu">
      <div class="left-menu">
          <router-link :to="{name:'Home'}" class="menu-item large noselect">liveTHREADDIT</router-link>
      </div>
      <div class="center-menu">
          <a v-if='title && mode' :href='titleurl' class="menu-item noselect">{{ title }}</a>
      </div>
      <div class="right-menu">
            <div v-if='mode' class="menu-item icon noselect">
                <i v-if='notification' class="fas fa-bell"></i>
                <i v-if='!notification' class="far fa-bell"></i>
            </div>
            <div v-if='mode' class="menu-item icon"><i class="fas fa-cog"></i></div>
            <div v-if='logged_in && !hoveringuser' @mouseenter='handleHoverEnter' class="menu-item icon noselect login">
                <i class="fas fa-user"></i>
            </div>
            <div v-if='logged_in && hoveringuser' @click='handleLogoutClick' @mouseleave='handleHoverLeave' class="menu-item icon noselect login">
                <i class="far fa-user"></i>
            </div>
            <div v-if='!logged_in' @click='handleLoginClick' class="menu-item icon noselect">
                <i  class="far fa-user"></i>
            </div>
      </div>
  </nav>

</template>

<script>
import { ref } from 'vue'
export default {
    props: ['title', 'logged_in', 'notification', 'mode', 'threadid', 'subreddit'],
    setup(props, { emit }) {
    
        const titleurl = 'https://www.reddit.com/r/' + props.subreddit + '/comments/' + props.threadid + '/'
        const hoveringuser = ref(false)
        const handleLoginClick = () => {
            emit('login')
        }

        const handleHoverEnter = () => {
            hoveringuser.value = true
        }

        const handleHoverLeave = () => {
            hoveringuser.value = false
        }

        const handleLogoutClick = () => {
            emit('logout')
        }

    return {handleLoginClick, handleLogoutClick, titleurl, hoveringuser, handleHoverEnter, handleHoverLeave}
    }
}
</script>s

<style>

.menu {
    display: flex;
    justify-content: center;
}

.menu-item {
    display: block;
    padding: 10px 25px;
    color: white;
    text-decoration: none;
    text-align: center;
    font-size: 24px;
    font-family: 'Nunito';
    transition: .2s;
}

.menu-item:hover {
    cursor: pointer;
    text-shadow: 0px 0px 10px white;
}

.menu-item.large {
    font-size: 60px;
    font-family: 'Megrim';
    font-weight: 500;
}

.left-menu {
    display: flex;
    flex: 1;
    justify-content: flex-start;
    align-items: center;
}

.right-menu {
    display: flex;
    flex: 1;
    justify-content: flex-end;
    align-items: center;
}

.center-menu {
    display: flex;
    flex: 2;
    justify-content: space-around;
    align-items: center;
}

.menu-item.icon.login:hover {
    text-shadow: 0px 0px 10px rgb(255, 83, 83);
    color:  rgb(255, 83, 83);
}

</style>