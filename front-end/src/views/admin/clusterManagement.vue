<template>

  <div>
    <br>
    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleSetting">
      {{ $t('clusterAdmin.nodeSetting') }}
    </el-button>
    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleAdd">
      {{ $t('clusterAdmin.add') }}
    </el-button>
    <el-table
      :data="node_info.slaves"
      style="width: 100%">
      <el-table-column
        prop="name"
        :label="$t('clusterAdmin.slaveName')">
      </el-table-column>
      <el-table-column
        prop="IP"
        :label="$t('clusterAdmin.slaveIP')">
      </el-table-column>
      <el-table-column
        prop="port"
        :label="$t('clusterAdmin.slavePort')">
      </el-table-column>
      <el-table-column
        prop="status"
        :label="$t('clusterAdmin.slaveStatus')">
      </el-table-column>
      <el-table-column
        fixed="right"
        :label="$t('button.setting')"
        width="150">
        <template slot-scope="scope">
          <el-button @click="handleUpdate(scope.$index)" type="text" size="small">{{ $t('button.edit') }}</el-button>
          <el-button @click="del(scope.$index)" type="text" size="small">{{ $t('button.del') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="$t('clusterAdmin.nodeSetting')" :visible.sync="nodeSettingDialog" >
      <el-form ref="form" >
        <el-form-item  :label="$t('clusterAdmin.nodeRole')" >
          <el-radio-group  v-model="node_info.role" >
            <el-radio :label="$t('clusterAdmin.nodeRoleMaster')" value='master' />
            <el-radio :label="$t('clusterAdmin.nodeRoleMasterAndSlave')" value='master&slave' />
            <el-radio :label="$t('clusterAdmin.nodeRoleSlave')" value='slave' />
          </el-radio-group >
        </el-form-item>

        <el-button type="primary" @click="submitNodeSetting">{{ $t('button.save') }}</el-button>
      </el-form>
    </el-dialog>


    <el-dialog :title="slaveDialogTitle" :visible.sync="addDialog" >
      <el-form ref="form" >
        <el-form-item  :label="$t('clusterAdmin.slaveName')" >
            <el-input v-model="slaveInfo.name"/>
        </el-form-item>
        <el-form-item  :label="$t('clusterAdmin.slaveIP')" >
            <el-input v-model="slaveInfo.IP"/>
        </el-form-item>
        <el-form-item  :label="$t('clusterAdmin.slavePort')" >
            <el-input v-model="slaveInfo.port"/>
        </el-form-item>
        <el-form-item  label="Token" >
            <el-input v-model="slaveInfo.token"/>
        </el-form-item>
        <el-button type="primary" @click="submitSlaveInfoAdd">{{ $t('button.save') }}</el-button>
      </el-form>
    </el-dialog>
  </div>

</template>

<script>
  import Kanban from '@/components/Kanban/index'
  import {getLanguage} from "@/lang";
  import {deletePlugin, getAllPluginInfo, getPluginVersions, installPlugin, updatePlugin} from "@/api/plugin";
  import {getNodeInfo, saveNodeInfo} from "@/api/cluster";

  export default {
    name: "pluginManagement",
    components: {
      Kanban
    },
    data() {
      return {
        id : '',
        addDialog: false,
        nodeSettingDialog: false,
        node_info: {},
        slaveInfo: {},
        slaveDialogTitle: '',
        slaveSessionIndex: -1,
      }
    },
    mounted() {
      this.refresh()
      new Promise((resolve, reject) => {
          getNodeInfo().then(response => {
            this.node_info= response.data
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
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
      handleAdd() {
        this.addDialog = true
        this.slaveDialogTitle = this.$t('clusterAdmin.add')
        this.slaveSessionIndex = -1
        this.slaveInfo = {}
      },

      handleSetting() {
        this.nodeSettingDialog = true
      },
      handleUpdate(index){
        this.addDialog = true
        this.slaveInfo = this.node_info.slaves[index]
        this.slaveSessionIndex = index
        this.slaveDialogTitle = this.$t('button.edit')
      },
      submitSlaveInfoAdd(){
        if(this.slaveSessionIndex >= 0){
          this.node_info.slaves[this.slaveSessionIndex] = this.slaveInfo
        }else {
          this.node_info.slaves.push(this.slaveInfo)
        }
        this.submitNodeSetting()
        this.addDialog = false
      },
      submitNodeSetting() {
        new Promise((resolve, reject) => {
          saveNodeInfo(this.node_info).then(response => {
            this.nodeSettingDialog = false
          }).catch(error => {
            reject(error)
          })
        })
      },

      del(index) {
        this.node_info.slaves.splice(index, index)
        this.submitNodeSetting()
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
