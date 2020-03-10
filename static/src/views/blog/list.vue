<template>
  <div class="tab-container">
    <el-tabs v-model="activeName" style="margin-top:15px;" type="border-card">
      <el-tab-pane v-for="(name,key) in tabMapOptions" :key="key" :label="name" :name="key">
        <keep-alive>
          <blog-tab v-if="activeName===key" :type="key" />
        </keep-alive>
      </el-tab-pane>
      <el-tab-pane>
        <router-link slot="label" to="/blog/create/">
          <el-button type="primary" size="small" class="create-blog-btn" icon="el-icon-edit">
            {{ $t('blog.newBlog') }}
          </el-button>
        </router-link>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import BlogTab from '../../components/BlogTab'

export default {
  name: 'BlogList',
  components: { BlogTab },
  data() {
    return {
      tabMapOptions: {
        published: this.$t('blog.published'),
        draft: this.$t('blog.draft')
      },
      activeName: 'published'
    }
  }
}
</script>

<style scoped>
  .tab-container {
    margin: 30px;
  }
</style>
