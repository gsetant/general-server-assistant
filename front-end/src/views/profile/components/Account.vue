<template>
  <div>
    <el-form>
      <el-form-item label="Name">
        <el-input v-model="user.name" />
      </el-form-item>
      <el-form-item label="Email">
        <el-input v-model="user.email" />
      </el-form-item>
      <el-form-item label="password">
        <el-input v-model="user.password" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit">{{ $t('button.save') }}</el-button>
      </el-form-item>
    </el-form>
    <el-form>
      <el-form-item :label="$t('profile.token')">
        <el-input v-model="token" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="generateToken">{{ $t('profile.generateToken') }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import {getPluginSetting} from "@/api/plugin";
import {getLanguage} from "@/lang";
import {generateToken, getInfo, updateUser} from "@/api/user";

export default {
  name: 'account',
  data() {
    return {
      user: {
        name: '',
        email: '',
        token: '',
        password:''
      },
      token: ''
    }
  },
  methods: {
    submit() {
      new Promise((resolve, reject) => {
        updateUser({user_info: this.user}).then(response => {
          this.$message({
            message: this.$t('userManagement.saveSuccess'),
            type: 'success',
            duration: 5 * 1000
          })
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    generateToken(){
      new Promise((resolve, reject) => {
        generateToken().then(response => {
          this.token= response.data.token
          this.user.token = this.token
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    }
  },
  mounted() {
    new Promise((resolve, reject) => {
      getInfo().then(response => {
        this.user= response.data
        this.user.password = ''
        if (this.user.token == null)
          this.token = 'click to generate'
        else this.token = this.user.token
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },
}
</script>
