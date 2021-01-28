<template>

  <nav class="menu">
      <div class="left-menu">
          <router-link class="menu-item large">liveTHREADDIT</router-link>
      </div>
      <div class="center-menu">

      </div>
      <div class="right-menu">
          <div class="menu-item icon"></div>
          <div class="menu-item icon"></div>
          <div class="menu-item icon"></div>
      </div>
  </nav>

</template>

<script>
export default {

}
</script>

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
}

.menu-item:hover {
    cursor: pointer;
}

.menu-item.large {
    font-size: 60px;
    font-family: 'Megrim';
    font-weight: 100;
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