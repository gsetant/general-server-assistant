<template>

  <div>
    <br>
    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
      {{ $t('pluginAdmin.install') }}
    </el-button>

    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="tittle"
        :label="$t('pluginAdmin.pluginName')">
      </el-table-column>
      <el-table-column
        prop="version"
        :label="$t('pluginAdmin.version')">
      </el-table-column>
      <el-table-column
        prop="content"
        :label="$t('pluginAdmin.content')">
      </el-table-column>
      <el-table-column
        prop="github"
        label="Github">
      </el-table-column>
      <el-table-column
        fixed="right"
        :label="$t('button.setting')"
        width="150">
        <template slot-scope="scope">
          <el-button @click="handleUpdate(scope.row)" type="text" size="small">{{ $t('button.update') }}</el-button>
          <el-button @click="del(scope.row)"type="text" size="small">{{ $t('button.del') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="dialogTittle" :visible.sync="installDialog" >
      <el-form ref="form" v-loading="installLoading" :element-loading-text="$t('pluginAdmin.installing')" >
        <el-form-item :label="$t('pluginAdmin.pluginGithubAddress')" >
          <el-input v-model="installDialogData.github" />
        </el-form-item>

        <el-form-item style="text-align: center">
          <el-button v-if="!installFinish" type="primary" @click="installPlugin">{{ $t('pluginAdmin.install') }}</el-button>
          <el-button v-if="installFinish" type="primary" @click="closeInstall">{{ $t('pluginAdmin.finish') }}</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog :title="updateDialogTittle" :visible.sync="updateDialog" >
      <el-form ref="form" v-loading="updateLoading" :element-loading-text="$t('pluginAdmin.installing')" style="text-align: center; padding-bottom: 20px" >
        <el-select v-model="selectVersion" :placeholder="$t('pluginAdmin.pleaseSelectVersion')" style="padding-bottom: 40px">
          <el-option
            v-for="item in pluginVersions"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>

        <el-form-item >
          <el-button v-if="!updateFinish" type="primary" @click="updatePlugin">{{ $t('pluginAdmin.install') }}</el-button>
          <el-button v-if="updateFinish" type="primary" @click="closeUpdate">{{ $t('pluginAdmin.finish') }}</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>

</template>

<script>
  import Kanban from '@/components/Kanban/index'
  import {getLanguage} from "@/lang";
  import {deletePlugin, getAllPluginInfo, getPluginVersions, installPlugin, updatePlugin} from "@/api/plugin";

  export default {
    name: "pluginManagement",
    components: {
      Kanban
    },
    data() {
      return {
        id : '',
        installLoading: false,
        updateLoading: false,
        installFinish: false,
        updateFinish: false,
        dialogTittle: '',
        pluginVersions: [],
        selectVersion: '',
        pluginGit: '',
        updateDialogTittle: '',
        installDialog: false,
        updateDialog: false,
        dialogStatus: '',
        installDialogData:{},
        updateDialogData:{},
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
          getAllPluginInfo(getLanguage()).then(response => {
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
        this.installDialog = true
        this.installLoading = false
        this.installFinish = false
        this.installDialogData = {}
        this.id = ''
      },
      handleUpdate(row) {
        this.dialogStatus = 'create'
        this.updateDialogTittle = this.$t('button.update')
        this.updateDialog = true
        this.updateLoading = false
        this.updateFinish = false
        this.updateDialogData = {}
        this.pluginGit =row.github
        this.id = ''
        new Promise((resolve, reject) => {
          getPluginVersions(row).then(response => {
            this.pluginVersions = response.data
            resolve();
          }).catch(error => {
            reject(error)
          })
        })
      },
      installPlugin(){
        this.installLoading = true
        new Promise((resolve, reject) => {
          installPlugin(this.installDialogData).then(response => {
            let message = response.data
            if (message === 'success') {
              this.installLoading = false;
              this.installFinish = true;
              this.$message(this.$t('pluginAdmin.finish') + '!');
            } else {
              this.installLoading = false;
              this.$message(message + '!');
            }
            resolve();
          }).catch(error => {
            reject(error)
          })
        })
      },
      closeInstall(){
        this.installDialog = false
        this.installLoading = false
        this.installFinish = false
        this.installDialogData = {}
        this.refresh()
      },
      updatePlugin(){
        this.updateLoading = true
        let updateInfo ={
            'github': this.pluginGit,
            'version': this.selectVersion
        }
        new Promise((resolve, reject) => {
          updatePlugin(updateInfo).then(response => {
            let message = response.data
            if (message === 'success') {
              this.updateLoading = false;
              this.updateFinish = true;
              this.$message(this.$t('pluginAdmin.finish') + '!');
            } else {
              this.updateLoading = false;
              this.$message(message + '!');
            }
            resolve();
          }).catch(error => {
            reject(error)
          })
        })
      },
      closeUpdate(){
        this.updateDialog = false
        this.updateLoading = false
        this.updateFinish = false
        this.updateDialogData = {}
        this.selectVersion = ''
        this.pluginGit = ''
        this.refresh()
      },
      del(row) {
        new Promise((resolve, reject) => {
          deletePlugin(row).then(response => {
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
