
const Settings = { template: '<div>Settings page</div>' }
Vue.component('text_summary',{
  props:['text_raw'],
  template:`<div>Summary<strong>{{text]}}</strong></div>`,
  methods:{},
  data:function (){
    return {}
  }

});
Vue.component('text_item', {
  props: ['post'],
  template: `<div><input type="checkbox" name="vehicle1" value="Bike"><button v-on:click="toggle_display" class="btn btn-primary">Hide/show</button><div v-if="display">{{post.body}}</div></div>`,
  methods:{
    toggle_display(){
      this.display = !this.display
    }
  },
  data:function(){
    return {display: false, body:''}
  }
})

const Search_results = { template:
  `<div id="search_page">
    <h1>Search results</h1>
    <button v-on:click="back_page" class="btn btn-primary">Back</button>
    <button v-on:click="resend_data" class="btn btn-primary">Reload summary</button>
  <p>Auto generated summary <strong>{{this.summary_response}}</strong></p>
  <table class="table" style="width:100%;position:fixed;">
    <thead>
    <tr>
      <th scope="col" style="width: 20px;">#</th>
      <th scope="col" style="width: 20px;">Relevance</th>
      <th>Headline</th>
      <th>Action</th>

    </tr>
  </thead>
  <tbody>
    <tr v-for="(result,index) in this.search_array">
      <th scope="row">{{index +1 }}</th>
      <td>{{ (Math.round(result[0] * 100) / 100) * 100 +' %'  }}</td>
      <td>{{ result[1].title }}</td>
      <td><text_item v-bind:post="result[1]"></text_item></td>
    </tr>
  </tbody>
  </table>
  </div>`,
  data: function(){
    return {search_array:[]}
  },
  mounted () {
    this.init()
  },
  methods:{
    resend_data(){
        axios.post('search/', {
        data:{'search_string':this.search_string},
        // headers:{"X-CSRFToken": csrfToken}
      })
      .then(function (response) {
        console.log(response.data);
        router.push({name: 'search_page',params: { data: response.data }})
      })
      .catch(function (error) {
        alert("An error occurred")
        console.log(error)
      });
    },
    back_page(){
      router.push({name: 'MainPage'})
    },
    init(){
      this.search_array = this.$route.params.data.search_response
      this.summary_response = this.$route.params.data.summary_response
      console.log(this.summary_response)
    }
  },

}

let test_object = {
  "status": true,
  "search_response": [
  ],
  "summary_response": "Tories believe the prime minister is playing the fear card on this one so he can look tough in the run up to the general election. Lib Dems avoided suggesting anyone was playing politics with the issue."
}

const MainPage = { template: 
  `<div id="center_content">
  <h1 align='center'>Lucid</h1>
  <input v-model='search_string' type='text' placeholder='Enter search here' class="form-control"></input>
  <button v-on:click='send_data' class='btn btn-primary' style='width:100%'>Search</button></div>`
  ,
  methods:{
    send_data(){
      // router.push({name: 'search_page',params: { data: test_object }})
      axios.post('search/', {
        data:{'search_string':this.search_string},
        // headers:{"X-CSRFToken": csrfToken}
      })
      .then(function (response) {
        console.log(response.data);
        router.push({name: 'search_page',params: { data: response.data }})
      })
      .catch(function (error) {
        alert("An error occurred")
        console.log(error)
      });
      
    }
  },
  data:function(){
  return {"search_string":""}
}}




const routes = [
  { path: '/search_page', component: Search_results, name: 'search_page', },
  { path: '/', component: MainPage, name:'MainPage' },
  { path: '/settings', component: Settings },
  { path: '*', redirect: '/'}
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})


var app = new Vue({
    mode: 'history',
    router
}).$mount('#vue-app');