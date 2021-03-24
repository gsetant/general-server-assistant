<template>

  <div>
    <br>
    <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate()">
      {{ $t('userManagement.createUser') }}
    </el-button>

    <el-table
      :data="tableData"
      style="width: 100%">
      <el-table-column
        prop="name"
        :label="$t('userManagement.userName')">
      </el-table-column>
      <el-table-column
        prop="email"
        label="Email">
      </el-table-column>
      <el-table-column
        prop="roles"
        :label="$t('userManagement.authority')">
      </el-table-column>
      <el-table-column
        prop="token"
        :label="$t('profile.token')">
      </el-table-column>

      <el-table-column
        fixed="right"
        :label="$t('button.setting')"
        width="150">
        <template slot-scope="scope">
          <el-button @click="handleCreate(scope.row)" type="text" size="small">{{ $t('button.edit') }}</el-button>
          <el-button @click="del(scope.row)" type="text" size="small">{{ $t('button.del') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog :title="dialogTittle" :visible.sync="userDialog" >
      <el-form ref="form" >
        <el-form-item :label="$t('userManagement.userName')">
          <el-input v-model="dialogData.name" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="dialogData.email" />
        </el-form-item>
        <el-form-item :label="$t('userManagement.authority')">
          <el-checkbox-group v-model="selectRoles">
            <el-checkbox v-for="role in allRoles"  :label="role" name="role"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item :label="$t('userManagement.password')">
          <el-input v-model="dialogData.password" />
        </el-form-item>
        <el-form-item style="text-align: center">
          <el-button type="primary" @click="submit">{{ $t('button.save') }}</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

  </div>

</template>

<script>
  import Kanban from '@/components/Kanban/index'
  import {getLanguage} from "@/lang";
  import {deletePlugin, getAllPluginInfo, getPluginVersions, installPlugin, updatePlugin} from "@/api/plugin";
  import {delUser, getAllUserInfo, getInfo, updateUser} from "@/api/user";
  import store from "@/store";

  export default {
    name: "userManagement",
    components: {
      Kanban
    },
    data() {
      return {
        id : '',
        dialogTittle: '',
        dialogStatus: '',
        userDialog: false,
        dialogData:{},
        selectRoles: [],
        tableData: [],
        group: 'plugins',
        allRoles: [],
      }
    },
    async mounted() {
      this.refresh()
      new Promise((resolve, reject) => {
        getInfo().then(response => {
          this.allRoles = response.data.roles.split(',');
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    methods: {
      refresh(){
        new Promise((resolve, reject) => {
          getAllUserInfo().then(response => {
            this.tableData= response.data
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      handleCreate(userInfo = {roles:''}) {
        this.dialogStatus = 'create'
        this.dialogData = userInfo
        this.dialogTittle = this.$t('button.edit')
        this.id = ''
        this.selectRoles = userInfo.roles.split(',')
        this.userDialog = true
      },
      del(row) {
        new Promise((resolve, reject) => {
          delUser(row.name).then(response => {
            this.$message(this.$t('button.save')+'!')
            this.refresh()
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      submit() {
        let roles = this.selectRoles.filter(function (s) {
          return s && s.trim();
        });
        this.dialogData.roles = roles.toString();
        debugger
        new Promise((resolve, reject) => {
          updateUser({user_info: this.dialogData}).then(response => {
            this.$message({
              message: this.$t('userManagement.saveSuccess'),
              type: 'success',
              duration: 5 * 1000
            })
            this.userDialog = false;
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
