<template>
  <el-form ref="blogForm" :model="blogForm" :rules="rules" class="form-container">
    <el-form-item prop="content">
      <markdown-editor
        ref="editor"
        v-model="blogForm.content"
        height="90vh"
        :upload-image="uploadImage"
        :options="{previewStyle: 'tab', hideModeSwitch: true}"
      />
    </el-form-item>

    <right-panel click-not-close>
      <el-form-item prop="title">
        <MDinput v-model="blogForm.title" :maxlength="100" name="name" required>
          {{ $t('blog.title') }}
        </MDinput>
      </el-form-item>
      <el-form-item prop="image" :label="$t('blog.coverImage')">
        <upload v-model="blogForm.image" :upload-image="uploadImage" />
      </el-form-item>

      <el-form-item :label="$t('blog.author')" class="blogInfo-container-item">
        <el-input v-model="blogForm.author" :placeholder="$t('blog.author')" />
      </el-form-item>
      <el-form-item :label="$t('blog.description')">
        <el-input
          v-model="blogForm.description"
          :rows="1"
          type="textarea"
          class="article-textarea"
          autosize
          :placeholder="$t('blog.description')"
        />
      </el-form-item>
      <el-form-item :label="$t('blog.slug')">
        <el-input v-model="blogForm.slug" />
      </el-form-item>
      <el-form-item :label="$t('blog.language')">
        <el-radio v-model="blogForm.lang" label="zh">中文</el-radio>
        <el-radio v-model="blogForm.lang" label="en">English</el-radio>
      </el-form-item>

      <el-form-item :label="$t('blog.category')">
        <el-select v-model="blogForm.category" style="width:100%" filterable allow-create>
          <el-option v-for="(item,id) in categoryOptions" :key="item+id" :label="item" :value="item" />
        </el-select>
      </el-form-item>

      <el-form-item :label="$t('blog.tags')">
        <el-select
          v-model="blogForm.tags"
          style="width:100%"
          multiple
          remote
          :remote-method="searchRemoteTags"
          filterable
          allow-create
        >
          <el-option v-for="(item,id) in tagOptions" :key="item+id" :label="item" :value="item" />
        </el-select>
      </el-form-item>

      <div style="margin-bottom:30px;">
        <el-checkbox v-model="blogForm.comment">{{ $t('blog.commentOn') }}</el-checkbox>
        <el-button v-loading="loading" style="margin-left: 10px;" type="success" @click="submitForm">
          {{ $t('blog.publish' ) }}
        </el-button>
        <el-button v-loading="loading" type="warning" @click="draftForm">
          {{ $t('blog.draft' ) }}
        </el-button>
      </div>
    </right-panel>
  </el-form>
</template>

<script>
import MarkdownEditor from '../components/MarkdownEditor'
import Upload from '../components/Upload/SingleImage'
import MDinput from '../components/MDinput'
import { fetchBlog, createBlog, updateBlog } from '../api/blog'
import { categoryList, tagList } from '../api/remote-search'
import RightPanel from '../components/RightPanel'
import uploadData from '../api/cos'

const defaultForm = {
  is_draft: true,
  title: '', // 文章题目
  content: '', // 文章内容
  description: '', // 文章摘要
  image: '', // 文章图片
  category: '',
  tags: [],
  lang: 'zh',
  comment: true
}

export default {
  name: 'ArticleDetail',
  components: { MarkdownEditor, MDinput, Upload, RightPanel },
  props: {
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  data() {
    const validateRequire = (rule, value, callback) => {
      if (value === '') {
        this.$message({
          message: rule.field + this.$t('blog.missing'),
          type: 'error'
        })
        callback(new Error(rule.field + this.$t('blog.missing')))
      } else {
        callback()
      }
    }
    return {
      blogForm: Object.assign({}, defaultForm),
      loading: false,
      rules: {
        title: [{ validator: validateRequire }],
        content: [{ validator: validateRequire }],
        author: [{ validator: validateRequire }],
        slug: [{ validator: validateRequire }],
        category: [{ validator: validateRequire }]
      },
      categoryOptions: [],
      tagOptions: [],
      tempRoute: {}
    }
  },
  computed: {
    contentShortLength() {
      return this.blogForm.description.length
    },
    lang() {
      return this.$store.getters.language
    }
  },
  created() {
    if (this.isEdit) {
      const id = this.$route.params && this.$route.params.id
      this.fetchData(id)
    } else {
      this.blogForm = Object.assign({}, defaultForm)
    }

    // Why need to make a copy of this.$route here?
    // Because if you enter this page and quickly switch tag, may be in the execution of the setTagsViewTitle function, this.$route is no longer pointing to the current page
    // https://github.com/PanJiaChen/vue-element-admin/issues/1221
    this.tempRoute = Object.assign({}, this.$route)
    this.fetchCategories()
  },
  methods: {
    fetchData(id) {
      fetchBlog(id).then(response => {
        this.blogForm = response.data
        // Set tagsview title
        this.setTagsViewTitle()
      }).catch(err => {
        console.log(err)
      })
    },
    setTagsViewTitle() {
      const title = this.lang === 'zh' ? '编辑文章' : 'Edit Article'
      const route = Object.assign({}, this.tempRoute, { title: `${title}-${this.blogForm.id}` })
      this.$store.dispatch('tagsView/updateVisitedView', route)
    },
    fetchCategories() {
      categoryList().then(resp => {
        if (!resp.data.items) return
        this.categoryOptions = resp.data.items.map(v => v.name)
      })
    },
    searchRemoteTags(query) {
      console.log(query)
      tagList(query).then(resp => {
        if (!resp.data.items) return
        this.tagOptions = resp.data.items.map(v => v.name)
      })
    },
    uploadImage(fileObj, callbacks) {
      uploadData(fileObj, callbacks)
    },
    sendBlog(data) {
      return (this.isEdit ? updateBlog(data) : createBlog(data))
    },
    submitForm() {
      this.$refs.blogForm.validate(valid => {
        if (!valid) return
        this.sendBlog({ ...this.blogForm, is_draft: false }).then(resp => {
          this.loading = true
          this.$notify({
            title: this.$t('blog.success'),
            message: this.$t('blog.successMessage'),
            type: 'success',
            duration: 2000
          })
          this.blogForm.status = 'published'
          this.loading = false
        })
      })
    },
    draftForm() {
      if (this.blogForm.content.length === 0 || this.blogForm.title.length === 0) {
        this.$message({
          message: this.$t('blog.missingField'),
          type: 'warning'
        })
        return
      }
      this.sendBlog({ ...this.blogForm, is_draft: true }).then(resp => {
        this.$message({
          message: this.$t('blog.saveSuccess'),
          type: 'success',
          showClose: true,
          duration: 1000
        })
        this.blogForm.status = 'draft'
      })
    }
  }
}
</script>

<style lang="scss">
  .sub-navbar {
    background: none;
  }

  .te-editor .CodeMirror {
    font-size: 16px;
  }

  .tui-editor-defaultUI {
    border-bottom: none;
  }

  @media (min-width: 980px) {
    .form-container {
      padding-right: 380px;
    }
  }
</style>
