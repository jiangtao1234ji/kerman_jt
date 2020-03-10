import request from '../utils/request'
import COS from 'cos-js-sdk-v5'
import store from '../store'

const cos = new COS({
  getAuthorization: (options, callback) => {
    request({
      url: '/token/cos',
      method: 'get'
    }).then(resp => {
      const {data} = resp
      console.log(data)
      callback({
        TmpSecretId: data.credentials.tmpSecretId,
        TmpSecretKey: data.credentials.tmpSecretKey,
        XCosSecurityToken: data.credentials.sessionToken,
        ExpiredTime: data.expiredTime
      })
    })
  }
})

export default (file, {success, error, progress}) => {
  if (!store.state.integration.cos.enabled) {
    error(new Error('COS is not configured yet'))
    return
  }
  cos.putObject({
    Bucket: store.state.integration.cos.bucket, /* 必须 */
    Region: store.state.integration.cos.region,     /* 存储桶所在地域，必须字段 */
    Key: (new Date()).toISOString().slice(0, 7) + '-' + file.name,              /* 必须 */
    Body: file, // 上传文件对象
    onProgress: function (progressData) {
      progress(progressData.percent)
    }
  }, function (err, data) {
    if (err) {
      error(err)
    } else {
      success('/images/' + data.Key)
    }
  })
  cos.sliceUploadFile({
    Bucket: store.state.integration.cos.bucket,
    Region: store.state.integration.cos.region,
    Key: (new Date()).toISOString().slice(0, 7) + '-' + file.name,
    Body: file,
    onProgress: function (progressData) {
      progress(progressData.percent)
    }

  }, function (err, data) {
    if (err) {
      error(err)
    } else {
      success('/images/' + data.Key)
    }
  })
}
