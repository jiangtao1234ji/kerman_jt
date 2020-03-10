import Mock from 'mockjs'

const List = []
const count = 100

const baseContent = '<p>I am testing data, I am testing data.</p><p><img src="https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943"></p>'
const image_uri = 'https://wpimg.wallstcn.com/e4558086-631c-425c-9430-56ffb46e70b3'

for (let i = 0; i < count; i++) {
  List.push(Mock.mock({
    id: '@increment',
    date: '@datetime',
    author: '@first',
    title: '@title(5, 10)',
    description: '@sentence',
    content: baseContent,
    'lang|1': ['zh', 'en'],
    type: Mock.Random.pick(['published', 'draft']),
    last_update: '@datetime',
    'comment|1': true,
    image: image_uri,
    slug: '@domain',
    category: Mock.Random.pick(['programming', 'essay']),
    tags: [Mock.Random.pick(['test', 'python', 'algorithm', 'reading'])]
  }))
}

export default [
  {
    url: '/blog/\\d+',
    type: 'get',
    response: config => {
      return {
        code: 20000,
        data: List[0]
      }
    }
  },

  {
    url: '/blog',
    type: 'get',
    response: config => {
      const {type, title, page = 1, limit = 10, sort} = config.query;

      let mocklist = List.filter(item => {
        if (type && type !== item.type) return false;
        if (title && item.title.indexOf(title) < 0) return false;
        return true
      })

      if (sort === '-id') {
        mocklist = mocklist.reverse()
      }

      const pagelist = mocklist.filter((item, index) => index < limit *
        page && index >= limit * (page - 1))

      return {
        code: 20000,
        data: {
          total: mockList.length,
          items: pageList
        }
      }
    }
  },

  {
    url: '/blog',
    type: 'post',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/blog',
    type: 'put',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  },

  {
    url: '/blog',
    type: 'delete',
    response: _ => {
      return {
        code: 20000,
        data: 'success'
      }
    }
  }



  // {
  //   url: '/article/detail',
  //   type: 'get',
  //   response: config => {
  //     const {id} = config.query
  //     for (const article of List) {
  //       if (article.id === +id) {
  //         return {
  //           code: 20000,
  //           data: article
  //         }
  //       }
  //     }
  //   }
  // },
  //
  // {
  //   url: '/article/pv',
  //   type: 'get',
  //   response: _ => {
  //     return {
  //       code: 20000,
  //       data: {
  //         pvData: [
  //           {key: 'PC', pv: 1024},
  //           {key: 'mobile', pv: 1024},
  //           {key: 'ios', pv: 1024},
  //           {key: 'android', pv: 1024}
  //         ]
  //       }
  //     }
  //   }
  // },
  //
  // {
  //   url: '/article/create',
  //   type: 'post',
  //   response: _ => {
  //     return {
  //       code: 20000,
  //       data: 'success'
  //     }
  //   }
  // },
  //
  // {
  //   url: '/article/update',
  //   type: 'post',
  //   response: _ => {
  //     return {
  //       code: 20000,
  //       data: 'success'
  //     }
  //   }
  // }
]

