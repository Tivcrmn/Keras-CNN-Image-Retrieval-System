<template>
  <div>
    <h1>keras-cnn-image-retrieval</h1>
    <el-button size="small" type="primary" class="description" @click="dialogVisible = true">说明</el-button>
    <el-button size="small" type="primary" class="random" @click="getRandomImgs">随机从库里取图</el-button>
    <el-upload
      class="upload"
      action="http://localhost:8000/cnn_vgg16"
      :show-file-list="false "
      :on-success="onSuccess"
      :on-progress="onProgress">
      <el-button size="small" type="primary">点击上传</el-button>
    </el-upload>

    <h1 v-if="loading">loading......</h1>
    <div v-else class="image_retrieval">
      <span v-for="(img, index) in imgs" :key="index" class="image">
        <img  @click="getRelativeImgs(img.name)" :src="'data:image/jpg;base64,' + img.base64">
      </span>
    </div>

    <el-dialog
      title="项目简介"
      :visible.sync="dialogVisible"
      width="80%">
      <p>本课题采用训练集为<em>caltech101</em>共有101类和8677张图片，具体可见
        <a href="http://www.vision.caltech.edu/Image_Datasets/Caltech101/" target="_blank">http://www.vision.caltech.edu/Image_Datasets/Caltech101/</a> <span>每张图片都有40-800张不等</span></p>
      <p>支持库内检索和上传检索， 系统会返回最接近的100张图片</p>
      <p>任取20次图片准确率分析<a href="https://plot.ly/~Tivcrmn/0" target="_blank">https://plot.ly/~Tivcrmn/0</a></p>
      <p>任取20次图片时间分析<a href="https://plot.ly/~Tivcrmn/2" target="_blank">https://plot.ly/~Tivcrmn/2</a></p>
      <h2>库内检索</h2>
      <img src="../assets/inDatabase.jpg">
      <h2>上传检索</h2>
      <img src="../assets/upload.jpg">
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
      </span>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data () {
    return {
      loading: false,
      imgs: [],
      dialogVisible: false
    }
  },
  created () {
    this.getRelativeImgs('airplanes/image_0002.jpg', true)
  },
  methods: {
    getRelativeImgs (name, isInDatabase) {
      this.loading = true
      this.$http.get('http://localhost:8000/cnn_vgg16', {params: {'name': name}}).then(res => {
        this.imgs = res.body.data
        this.loading = false
      }, res => {
        // error callback
      })
    },
    getRandomImgs () {
      this.loading = true
      this.$http.get('http://localhost:8000/cnn_vgg16_random').then(res => {
        this.imgs = res.body.data
        this.loading = false
      }, res => {
        // error callback
      })
    },
    onSuccess (res, file, fileList) {
      this.imgs = res.data
      this.loading = false
    },
    onProgress (event, file, fileList) {
      this.loading = true
    }
  }
}
</script>

<style lang="less">
h1 {
  font-weight: normal;
  text-align: center;
}
.image_retrieval {
  .image {
    padding-right: 15px;
  }
  img {
    width: 90px;
    height: 90px;
  }
  img:hover{
    cursor: pointer;
  }
}
.el-dialog {
  img {
    width: 100%;
    height: 80%;
  }
}
.upload {
  position: absolute;
  top: 80px;
  right: 55px;
}
.random {
  position: absolute;
  top: 80px;
  right: 150px;
}
.description {
  position: absolute;
  top: 80px;
  right: 280px;
}

</style>
