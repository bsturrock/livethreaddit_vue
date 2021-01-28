<template>

  <nav class="menu">
      <div class="left-menu">
          <router-link :to="{name:'Home'}" class="menu-item large noselect">liveTHREADDIT</router-link>
      </div>
      <div class="center-menu">
          <div v-if='title && mode' class="menu-item noselect">{{ title }}</div>
      </div>
      <div class="right-menu">
            <div v-if='mode' class="menu-item icon noselect">
                <i v-if='notification' class="fas fa-bell"></i>
                <i v-if='!notification' class="far fa-bell"></i>
            </div>
            <div v-if='mode' class="menu-item icon noselect"><i class="fas fa-cog"></i></div>
            <div class="menu-item icon noselect">
                <i v-if='logged_in' class="fas fa-user"></i>
                <i v-if='!logged_in' class="far fa-user"></i>
            </div>
      </div>
  </nav>

</template>

<script>
import { ref } from 'vue'
export default {
    props: ['title', 'logged_in', 'notification', 'mode'],
    setup() {

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

</style>