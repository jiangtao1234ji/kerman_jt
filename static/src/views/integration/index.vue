<template>
  <div class="integration-container">
    <card
      label="Disqus"
      name="disqus"
      :initial="integration.disqus"
      :fields="['shortname']"
      image="https://c.disquscdn.com/next/1c57e77/marketing/assets/img/brand/disqus-social-icon-white-blue.svg"
    />
    <card
      label="Google Analytics"
      name="google_analytics"
      :initial="integration.google_analytics"
      :fields="['id']"
      image="https://icon-icons.com/icons2/1945/PNG/128/iconfinder-addthis-4661579_122447.png"
    />
    <card
      label="Tencent COS"
      name="cos"
      :initial="integration.cos"
      :fields="['secret_id', 'secret_key', 'bucket', 'region', 'AppId']"
      image="https://avatars3.githubusercontent.com/u/12334581?s=200&v=4"
    />
    <card
      label="Addthis"
      name="addthis"
      :initial="integration.addthis"
      :fields="['pubid']"
      image="https://icon-icons.com/icons2/1945/PNG/128/iconfinder-addthis-4661579_122447.png"
    />
  </div>
</template>

<script>
  import Card from './components/Card'
  import {mapState} from 'vuex'

  export default {
    name: 'Integration',
    components: {Card},
    computed: {
      ...mapState(['integration'])
    }
  }
</script>

<style lang="scss" scoped>
  .integration-container {
    padding: 20px;
  }

</style>
