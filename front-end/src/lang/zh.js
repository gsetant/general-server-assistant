export default {
  intro:{
    summary:"Gsetant 项目旨在为当前流行的媒体服务器(Plex, Emby, Jellyfin)提供一套通用的增强功能集合，使用API和插件等多种方式为与媒体服务器集成，并提供功能扩展。"
  },
   guide: {
    hplugin: '插件安装',
    plugin: '为了使用gsetant您需要为您的媒体服务器安装插件' +
      '\nPlex(https://github.com/gsetant/Gsetant.bundle/releases/)' +
      '\nEmby(release soon)' +
      '\nJellyfin(release soon)',
     hprofile: '插件设置',
     profile: '您需要为您的插件生成插件密函（plugin token），可从gsetant的个人中心中生成\n' +
      '复制插件密函到您的插件设置中\n' +
      '如果您使用公共Gsetant `https://www.gsetant.xyz` 做为Gsetant API地址，`433`做为Gsetant API port',
     hlibraries: '库设置',
    libraries: '进入gsetant的库管理界面设置为媒体服务器中的资料库设置匹配规则\n' +
      '下图为例子为使用网易云音乐插件为music库提供元数据搜刮 \n' +
      '您也可以同时为一个库开启多个插件，并更改开启插件的顺序',
  },
  route: {
    dashboard: '首页',
    plugin: '插件',
    pluginSetting: '插件设置',
    github: 'GitHub',
    log: '日志',
    adminPages: '管理员设置',
    userManagement: '用户管理',
    adminLog: '系统日志',
    pluginManagement: '插件管理',
    clusterManagement: '集群管理',
    profile: '个人中心',
    library: '库管理',
    manualSearch: '手动搜索',
    guide: '使用说明'
  },
  button:{
    save: '保存',
    cancel: '取消',
    setting: '操作',
    edit:'编辑',
    del:'删除',
    update: '升级'
  },
  library:{
    libraries: '资料库',
    plugins: '插件',
    enabled:'启用',
    disabled: '禁用',
  },
  manualSearch:{
    videoTitle: '视频名称',
    processing: '处理中',
    fileDir: '文件路径',
    usePlugin: '使用插件',
    search:'搜索',
    title: '标题',
    original_title: '原始标题',
    summary: '简介',
    studio: '发行商',
    collections: '集合',
    originally_available_at: '原始发布日期',
    year: '发布日期',
    directors: '导演',
    category: '分类',
    poster: '海报',
    thumbnail: '缩略图',
    actor: '演员'
  },
  pluginAdmin:{
    pluginName: '插件名称',
    version: '版本',
    content : '说明',
    install: '安装插件',
    pluginGithubAddress: '插件 Github 地址',
    finish: '安装完成',
    installing: '插件安装中',
    pleaseSelectVersion: '请选择版本'
  },
  clusterAdmin:{
    add: '添加节点',
    nodeSetting: '设置',
    nodeRole: '节点角色',
    nodeRoleMaster: 'master',
    nodeRoleMasterAndSlave: 'master&slave',
    nodeRoleSlave: 'slave',
    slaveName: '名称',
    slaveIP: 'IP',
    slavePort: 'Port',
    slaveStatus: '状态',
  },
  userManagement: {
    createUser:' 新建用户',
    updatePassword: '更新密码',
    deleteUser: '删除用户',
    userName: '用户名',
    authority: '权限',
    password: '密码',
    saveSuccess: '用户信息保存成功'
  },
  profile:{
    token: '插件密函',
    generateToken: '生成新密函'
  },
  navbar: {
    dashboard: '首页',
    github: '项目地址',
    logOut: '退出登录',
    profile: '个人中心',
    theme: '换肤',
    size: '布局大小'
  },
  login: {
    title: 'General Server Assistant',
    logIn: '登录',
    username: '账号',
    password: '密码',
    any: '随便填',
    thirdparty: '第三方登录',
    thirdpartyTips: '本地不能模拟，请结合自己业务进行模拟！！！'
  },
  documentation: {
    documentation: '文档',
    github: 'Github 地址'
  },
  permission: {
    addRole: '新增角色',
    editPermission: '编辑权限',
    roles: '你的权限',
    switchRoles: '切换权限',
    tips: '在某些情况下，不适合使用 v-permission。例如：Element-UI 的 el-tab 或 el-table-column 以及其它动态渲染 dom 的场景。你只能通过手动设置 v-if 来实现。',
    delete: '删除',
    confirm: '确定',
    cancel: '取消'
  },
  components: {
    documentation: '文档',
    tinymceTips: '富文本是管理后台一个核心的功能，但同时又是一个有很多坑的地方。在选择富文本的过程中我也走了不少的弯路，市面上常见的富文本都基本用过了，最终权衡了一下选择了Tinymce。更详细的富文本比较和介绍见',
    dropzoneTips: '由于我司业务有特殊需求，而且要传七牛 所以没用第三方，选择了自己封装。代码非常的简单，具体代码你可以在这里看到 @/components/Dropzone',
    stickyTips: '当页面滚动到预设的位置会吸附在顶部',
    backToTopTips1: '页面滚动到指定位置会在右下角出现返回顶部按钮',
    backToTopTips2: '可自定义按钮的样式、show/hide、出现的高度、返回的位置 如需文字提示，可在外部使用Element的el-tooltip元素',
    imageUploadTips: '由于我在使用时它只有vue@1版本，而且和mockjs不兼容，所以自己改造了一下，如果大家要使用的话，优先还是使用官方版本。'
  },
  table: {
    dynamicTips1: '固定表头, 按照表头顺序排序',
    dynamicTips2: '不固定表头, 按照点击顺序排序',
    dragTips1: '默认顺序',
    dragTips2: '拖拽后顺序',
    title: '标题',
    importance: '重要性',
    type: '类型',
    remark: '点评',
    search: '搜索',
    add: '添加',
    export: '导出',
    reviewer: '审核人',
    id: '序号',
    date: '时间',
    author: '作者',
    readings: '阅读数',
    status: '状态',
    actions: '操作',
    edit: '编辑',
    publish: '发布',
    draft: '草稿',
    delete: '删除',
    cancel: '取 消',
    confirm: '确 定'
  },
  example: {
    warning: '创建和编辑页面是不能被 keep-alive 缓存的，因为keep-alive 的 include 目前不支持根据路由来缓存，所以目前都是基于 component name 来进行缓存的。如果你想类似的实现缓存效果，可以使用 localStorage 等浏览器缓存方案。或者不要使用 keep-alive 的 include，直接缓存所有页面。详情见'
  },
  errorLog: {
    tips: '请点击右上角bug小图标',
    description: '现在的管理后台基本都是spa的形式了，它增强了用户体验，但同时也会增加页面出问题的可能性，可能一个小小的疏忽就导致整个页面的死锁。好在 Vue 官网提供了一个方法来捕获处理异常，你可以在其中进行错误处理或者异常上报。',
    documentation: '文档介绍'
  },
  excel: {
    export: '导出',
    selectedExport: '导出已选择项',
    placeholder: '请输入文件名(默认excel-list)'
  },
  zip: {
    export: '导出',
    placeholder: '请输入文件名(默认file)'
  },
  pdf: {
    tips: '这里使用   window.print() 来实现下载pdf的功能'
  },
  theme: {
    change: '换肤',
    documentation: '换肤文档',
    tips: 'Tips: 它区别于 navbar 上的 theme-pick, 是两种不同的换肤方法，各自有不同的应用场景，具体请参考文档。'
  },
  tagsView: {
    refresh: '刷新',
    close: '关闭',
    closeOthers: '关闭其它',
    closeAll: '关闭所有'
  },
  settings: {
    title: '系统布局配置',
    theme: '主题色',
    tagsView: '开启 Tags-View',
    fixedHeader: '固定 Header',
    sidebarLogo: '侧边栏 Logo'
  }
}
