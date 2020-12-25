<template>
  <div>

    <el-container style="width: 100%;height: auto">

      <el-header style="width: 100%">
        <p class="tittle">{{pluginInfo.tittle}}</p>
      </el-header>

    </el-container>


    <el-container style="width: 100%;height: auto">

      <el-aside>
        <el-image class="icon" :src="pluginInfo.icon"></el-image>
      </el-aside>

      <el-main style="padding-left: 20px">
        <p class="content">{{pluginInfo.content}}</p>
        <br>
        <p class="version">version:{{pluginInfo.version}}</p>
      </el-main>

    </el-container>


    <el-container style="width: 100%;height: auto">

      <el-footer>

      </el-footer>

    </el-container>
  </div>

</template>
<script>
  import {getPluginInfo} from "@/api/plugin";
  import {getLanguage} from "@/lang";

  export default {
    name: "dashboard",
    data(){
      return {
        pluginName: this.$route.path.substring(8,this.$route.path.lastIndexOf('/')),
        pluginInfo:{}
      }
    },
    computed: {

    },
    mounted() {
      new Promise((resolve, reject) => {
        getPluginInfo(this.pluginName,getLanguage()).then(response => {
          this.pluginInfo= response.data
          resolve()
        }).catch(error => {
          reject(error)
        })
      })
    }
  }
</script>

<style scoped>
.tittle{
  font-size: 40px;
  text-align: center;
  margin: 0;
}
</style>
