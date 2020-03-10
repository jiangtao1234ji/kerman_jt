<template>
  <div class="app-container">
    <el-table v-loading="listLoading" :data="list" border fit highlight-current-row style="width: 100%">
      <el-table-column align="center" label="ID" width="80">
        <template slot-scope="scope">
          <span>{{ scope.row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column width="180px" align="center" :label="$t('blog.date')">
        <template slot-scope="scope">
          <span>{{ scope.row.date | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column width="120px" align="center" :label="$t('blog.author')">
        <template slot-scope="scope">
          <span>{{ scope.row.author }}</span>
        </template>
      </el-table-column>
      <el-table-column width="120px" align="center" :label="$t('blog.category')">
        <template slot-scope="scope">
          <span>{{ scope.row.category }}</span>
        </template>
      </el-table-column>

      <el-table-column min-width="300px" :label="$t('blog.title')">
        <template slot-scope="{row}">
          <router-link :to="'/blog/edit/'+row.id" class="link-type">
            <span>{{ row.title }}</span>
          </router-link>
        </template>
      </el-table-column>

      <el-table-column align="center" :label="$t('blog.actions')" width="220">
        <template slot-scope="scope">
          <router-link :to="'/blog/edit/'+scope.row.id">
            <el-button type="primary" size="small" icon="el-icon-edit">
              {{ $t('blog.edit') }}
            </el-button>
          </router-link>
          <el-button type="danger" size="small" icon="el-icon-delete" @click="handleDelete(scope.row)">
            {{ $t('blog.delete') }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />
  </div>
</template>

<script>
import { fetchList, deleteBlog } from '../api/blog'
import Pagination from '../components/Pagination' // Secondary package based on el-pagination

export default {
  name: 'BlogTab',
  components: { Pagination },
  props: {
    type: {
      type: String,
      default: 'published'
    }
  },
  data() {
    return {
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList({ type: this.type, ...this.listQuery }).then(response => {
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false
      })
    },
    handleDelete(row) {
      this.$confirm(this.$t('blog.confirmDelete'), this.$t('el.messagebox.title'), {
        type: 'warining'
      }).then(val => {
        if (val) {
          deleteBlog(row.id).then(_ => {
            this.list.splice(this.list.indexOf(row), 1)
            this.$message(this.$t('blog.delSuccess'))
          })
        }
      })
    }
  }
}
</script>

<style scoped>
  .edit-input {
    padding-right: 100px;
  }

  .cancel-btn {
    position: absolute;
    right: 15px;
    top: 10px;
  }
</style>
