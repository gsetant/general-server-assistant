<template>

  <div>
    <br>
    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
      {{ $t('table.add') }}
    </el-button>

    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="libraries"
        :label="$t('library.libraries')"
        width="180">
      </el-table-column>
      <el-table-column
        prop="active"
        :label="$t('library.plugins')">
      </el-table-column>
      <el-table-column
        fixed="right"
        :label="$t('button.setting')"
        width="150">
        <template slot-scope="scope">
          <el-button @click="edit(scope.row)" type="text" size="small">{{ $t('button.edit') }}</el-button>
          <el-button @click="del(scope.row)"type="text" size="small">{{ $t('button.del') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="dialogTittle" :visible.sync="dialogFormVisible">
      <el-form ref="form">
        <el-form-item :label="$t('library.libraries')" >
          <el-input v-model="dialogData.libraries" />
        </el-form-item>
        <Kanban :key="1" :list="dialogData.active" :group="group" class="kanban todo" :header-text="$t('library.enabled')"/>
        <Kanban :key="2" :list="dialogData.disable" :group="group" class="kanban working" :header-text="$t('library.disabled')"/>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">{{ $t('button.save') }}</el-button>
        </el-form-item>
      </el-form>

    </el-dialog>
  </div>

</template>

<script>
  import Kanban from '@/components/Kanban'
  import {getLanguage} from "@/lang";
  import {delLibrariesSetting, getLibrariesSettings, librariesDetail, saveLibrariesSetting} from "@/api/libraries";
  import {savePluginSetting} from "@/api/plugin";

  export default {
    name: "index",
    components: {
      Kanban
    },
    data() {
      return {
        id : '',
        dialogTittle: '',
        dialogFormVisible: false,
        dialogStatus: '',
        dialogData:{},
        tableData: [],
        group: 'plugins',
      }
    },
    mounted() {
      this.refresh()
    },
    methods: {
      refresh(){
        new Promise((resolve, reject) => {
          getLibrariesSettings().then(response => {
            this.tableData= response.data
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      handleCreate() {
        this.dialogStatus = 'create'
        this.dialogTittle = this.$t('table.add')
        this.dialogFormVisible = true
        this.id = ''
        new Promise((resolve, reject) => {
          librariesDetail().then(response => {
            this.dialogData= response.data
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      edit(row) {
        this.dialogStatus = 'create'
        this.dialogTittle= this.$t('button.edit')
        this.dialogFormVisible = true
        this.id = row.id
        new Promise((resolve, reject) => {
          librariesDetail(row).then(response => {
            this.dialogData= response.data
            this.dialogData.id = this.id
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      onSubmit() {
        new Promise((resolve, reject) => {
          saveLibrariesSetting(this.dialogData).then(response => {
            this.$message(this.$t('button.save')+'!')
            this.dialogFormVisible = false
            this.refresh()
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      del(row) {

        new Promise((resolve, reject) => {
          delLibrariesSetting(row).then(response => {
            this.$message(this.$t('button.save')+'!')
            this.refresh()
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
    }
  }
</script>

<style lang="scss">

  .kanban {
    &.todo {
      .board-column-header {
        background: #4A9FF9;
      }
    }

    &.working {
      .board-column-header {
        background: #f9944a;
      }
    }

    &.done {
      .board-column-header {
        background: #2ac06d;
      }
    }
  }
</style>
