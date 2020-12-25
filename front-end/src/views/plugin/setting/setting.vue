<template>
  <div>
    <el-form ref="form" :model="data" label-width="120px" >
      <el-form-item v-for="item in pluginSetting" :label=item.label >
        <!--text-->
        <el-input v-if="item.type==='text'" v-model="data[item.model]" :placeholder=item.placeholder />

        <!--select-->
        <el-select v-if="item.type==='select'" v-model="data[item.model]" >
          <el-option v-for="op in item.option" :label=op.label :value=op.value />
        </el-select>

        <!--switch-->
        <el-switch v-if="item.type==='switch'" v-model="data[item.model]" />

        <!--radio-->
        <el-radio-group v-if="item.type==='radio'" v-model="data[item.model]"  >
          <el-radio  v-for="op in item.option"  :label="op.label" />
        </el-radio-group>

      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">{{ $t('button.save') }}</el-button>
        <el-button @click="onCancel">{{ $t('button.cancel') }}</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
  import {getPluginSetting, savePluginSetting} from "@/api/plugin";
  import {getLanguage} from "@/lang";

  export default {
    name: "setting",
    data() {
      return {
        pluginName: this.$route.path.substring(8, this.$route.path.lastIndexOf('/')),
        pluginSetting: [],
        data:{},
        originalData:{}
      }
    },
    computed: {},
    mounted() {
      new Promise((resolve, reject) => {
        getPluginSetting(this.pluginName, getLanguage()).then(response => {
          this.pluginSetting= response.data.form
          if (response.data.userSetting){
            this.data= response.data.userSetting
          }
          this.originalData = JSON.parse(JSON.stringify(response.data.userSetting))
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    methods: {
      onSubmit() {
        new Promise((resolve, reject) => {
          savePluginSetting(this.pluginName, this.data).then(response => {
            this.$message(this.$t('button.save')+'!')
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      onCancel() {
        this.data = JSON.parse(JSON.stringify(this.originalData))
        this.$message({
          message: this.$t('button.cancel')+'!',
          type: 'warning'
        })
      }
    }
  }
</script>

<style scoped>

</style>
