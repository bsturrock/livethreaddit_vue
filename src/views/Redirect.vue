<template>
  
</template>

<script>
    import { useRouter, useRoute } from 'vue-router'
export default {
    setup() {
        const router = useRouter()
        router.go(-2)

    }
}
</script>

<style>

</style>