<template>
  <div>
    <el-form ref="form" :model="data" label-width="120px">
      <el-form-item style="width: 95%" :label="$t('manualSearch.videoTitle')">
        <el-input v-model="searchQuery.video_title"/>
      </el-form-item>
      <el-form-item style="width: 95%" :label="$t('manualSearch.fileDir')">
        <el-input v-model="searchQuery.part_file"/>
      </el-form-item>
      <el-form-item :label="$t('manualSearch.usePlugin')">
        <el-select v-model="searchQuery.selectPlugin">
          <el-option v-for="plugin in pluginList" :label="plugin.tittle" :value="plugin.name"/>
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="onSubmit">{{ $t('manualSearch.search')}}</el-button>
      </el-form-item>
      <div>
        <table v-for="item in result">
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.title')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.title}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.original_title')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.original_title}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.summary')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.summary}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.studio')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.studio}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.collections')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.collections}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.originally_available_at')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.originally_available_at}}</p>
            </td>
          </tr>
          <tr class="resultTrL">
            <td class="resultTdL">
              <p>{{$t('manualSearch.year')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.year}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.directors')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.directors}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.category')}}</p>
            </td>
            <td class="resultTdR">
              <p>{{item.category}}</p>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.poster')}}</p>
            </td>
            <td class="resultTdR">
              <el-image class="icon" :src="'data:image/jpeg;base64,' + item.poster"></el-image>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.thumbnail')}}</p>
            </td>
            <td class="resultTdR">
              <el-image class="icon" :src="'data:image/jpeg;base64,' + item.thumbnail"></el-image>
            </td>
          </tr>
          <tr class="resultTr">
            <td class="resultTdL">
              <p>{{$t('manualSearch.actor')}}</p>
            </td>
            <td class="resultTdR">
              <table>
                <tr v-for="(value, key) in item.actor" :key="key" class="actorTr">
                  <td style="width: 100px; text-align: right; padding: 10px">
                    <p>{{key}}</p>
                  </td>
                  <td >
                    <el-image class="icon" style="width: 100px" :src="'data:image/jpeg;base64,' + value"></el-image>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="height:1px;border:none;border-top:1px solid #555555;padding: 0"/>
            <td style="height:1px;border:none;border-top:1px solid #555555;padding: 0"/>
          </tr>
        </table>
      </div>
    </el-form>
    <el-dialog title="" :visible.sync="processing" >
      <div style="height: 100px; " v-loading="true" :element-loading-text="$t('manualSearch.processing')" >

      </div>
    </el-dialog>
  </div>
  </template>

  <script>
    import {getPluginInfo, getPluginInfos, getPluginSetting} from "@/api/plugin";
    import {getLanguage} from "@/lang";
    import {mapGetters} from "vuex";
    import {manualScan} from "@/api/scan";

    export default {
      name: "index",
      data() {
        return {
          pluginList: [],

          result: {},
          searchQuery: {
            video_title: '',
            part_file: '',
            selectPlugin: '',
          },
          video_title: '',
          processing: false,
        }
      }, computed: {
        ...mapGetters([
          'name',
          'roles'
        ])
      }, mounted() {
        new Promise((resolve, reject) => {
          getPluginInfos(this.roles, getLanguage()).then(response => {
            this.pluginList = response.data
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      },
      methods: {
        onSubmit() {
          this.processing = true;
          new Promise((resolve, reject) => {
            manualScan(this.searchQuery).then(response => {
              this.result = response.data;
              this.processing = false;
              resolve()
            }).catch(error => {
              this.processing = false;
              this.$message(error)
              reject(error)
            })
          })
        },
      }
    };
  </script>

  <style scoped>
    p {
      word-wrap: break-word;
      word-break: break-all;
      overflow: hidden;
    }

    .resultTdL {
      width: 150px;
      text-align: right;
      padding: 20px;
    }

    .resultTdR {
      padding: 20px;
    }

    .resultTr {
      padding: 50px;
    }
  </style>
