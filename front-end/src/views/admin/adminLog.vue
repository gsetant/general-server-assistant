<template>
  <div>
    <textarea readonly style="width: 100%; height: 800px; resize: none; ">{{log}}</textarea>
  </div>
</template>

<script>
  import {getAdminLogFull, getAdminNewLog, getPluginLogFull, getPluginNewLog} from "@/api/log";

  export default {
    name: "log",
    data(){
      return {
        timer: '',
        pluginName: this.$route.path.substring(8,this.$route.path.lastIndexOf('/')),
        log: '',
        lineNumber: 0
      }
    },
    mounted() {
      new Promise((resolve, reject) => {
        getAdminLogFull().then(response => {
          this.log= response.data.log
          this.lineNumber= response.data.length
          this.timer = setInterval(this.getNewLog, 1000);
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    },
    methods:{
      getNewLog(){
        new Promise((resolve, reject) => {
          getAdminNewLog(this.lineNumber+1).then(response => {
            if (response.data.log !== ''){
              this.log = this.log + response.data.log
              this.lineNumber = response.data.length
            }
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      }
    },
    beforeDestroy() {
      clearInterval(this.timer);
    }
  }
</script>

<style scoped>

</style>
