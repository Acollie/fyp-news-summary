
const Settings = { template: '<div>Settings page</div>' }
Vue.component('text_summary',{
  props:['text_raw'],
  template:`<div>Summary:<strong>{{text]}}</strong></div>`,
  methods:{},
  data:function (){
    return {}
  }

});
Vue.component('text_item', {
  props: ['post'],
  template: `<div>
                <button v-on:click="toggle_display" class="btn btn-primary">Hide/show</button>
                <div v-if="display">{{post.body}}</div>
                </div>`,
  methods:{
    toggle_display(){
      this.display = !this.display
    }
  },
  data:function(){
    return {display: false, body:'', new_summary:false, array_items:[]}
  }
})

const Search_results = { template:
  `<div id="search_page">
    <h1>Search results</h1>
    <div class="form-check" style="width:450px;">
      <button v-on:click="back_page" class="btn btn-primary">Back</button>
      <button v-on:click="resend_data" class="btn btn-primary">Reload summary</button>
      <p>
      <label for="Temperature" class="form-label">Temperature: {{this.temperature}}</label>
      <input type="range" class="form-range" v-model="temperature" min="0" max="1" step="0.1" id="Temperature">
      </p>
      <label for="binning" class="form-label" @click="binning_setting">Use Binning</label>
      <input class="form-check-input" v-model="binning" type="checkbox" value="" id="binning">
    </div>
      <p>Auto generated summary <strong>{{summary_response}}</strong></p>
    
  <table class="table" style="width:100%;position:fixed;">
    <thead>
    <tr>
      <th scope="col" style="width: 20px;">#</th>
      <th scope="col" style="width: 20px;">Relevance</th>
      <th scope="col" style="width: 20px;">New Summary</th>
      <th>Headline</th>
      <th>Action</th>

    </tr>
  </thead>
  <tbody>
    <tr v-for="(result,index) in this.search_array">
      <th scope="row">{{index +1 }}</th>
      <td>{{ (result[0]*100).toFixed(2)+' %'  }}</td>
      <td><input type="checkbox" checked name="add_remove" @click="add_to_summary(index)"></td>
      <td>{{ result[1].title }}</td>
      <td><text_item v-bind:post="result[1]"></text_item></td>
    </tr>
  </tbody>
  </table>
  </div>`,
  data: function(){
    return {
      search_array:[],
      binning:true,
      summary_response:'' ,
      temperature: 0.9,
      summary_items:[],
      summary_set:new Set()}
  },
  mounted () {
    this.init()
  },
  methods:{
    add_to_summary(id){
      if (this.summary_set.has(id)){
        this.summary_set.delete(id)
      }else {
        this.summary_set.add(id)
      }
    },
    binning_setting(){
      this.binning = !this.binning
      console.log(this.binning)
    },
    resend_data: function (){
      console.log(this.summary_set)
      console.log(this.search_array[0])
      let items = []
      for (const entry of this.summary_set.entries()) {
        items.push(this.search_array[entry[0]][1]['body_tldr'])
      }
      axios.post('api/refresh_summary', {
        data:{'summary_items':items,'temperature':this.temperature,'binning':this.binning},
        // headers:{"X-CSRFToken": csrfToken}
      })
      .then((response)=>{
        // this.$set(this.text_summary, 'text', "Foo bar")
        // console.log(response.data);
        this.summary_response = response.data['summary_response']
        // router.push({name: 'search_page',params: { data: response.data }})
      })
      .catch(function (error) {
        this.summary_response ="foo"

        alert("An error occurred")
        console.log(error)
      });

    },
    back_page(){
      router.push({name: 'MainPage'})
    },
    init(){
      console.log('mounted')
      this.search_array = this.$route.params.data_returned.search_response
      this.summary_response = this.$route.params.data_returned.summary_response
      for (let i = 0; i < this.$route.params.data_returned.search_response.length; i++) {
        this.summary_items.push(this.$route.params.data_returned.search_response[i][1]['body_tldr'])
        this.summary_set.add(i)
      }

    }
  },


}

let test_object = {
  "status": true,
  "search_response": [
    [
      0.6226738095283508,
      {
        "title": "b'Wales make two changes for France\\n'",
        "body": "b'Wales make two changes for France\\n\\nWales coach Mike Ruddock has made two changes from the team that beat Italy 38-8 for Saturday\\'s trip to France.\\n\\nKevin Morgan takes over from his injured Newport-Gwent Dragons colleague Hal Luscombe on the right wing. And in the pack Neath-Swansea Ospreys forward Ryan Jones is preferred at blindside flanker to Jonathan Thomas. Thomas, a try-scorer in Rome, drops down to the bench instead of Ian Gough, while Cardiff back Rhys Williams steps up in place of Morgan. Luscombe is sidelined by a hamstring problem sustained during the Six Nations game against Italy last weekend.\\n\\nHowever, the experienced and in-form Morgan was already pushing hard for a start at Stade de France. \"Due to his impressive performances from the bench, Kevin was very much in the selection mix anyway, and the unfortunate injury to Hal gives him the chance to start,\" said Ruddock. \"Now that Ryan Jones has recovered from injury, we have increased the options in the back row. \"Jonathan Thomas is unlucky to lose his spot after performing well against Italy and scoring a try, but such is the competition for places that every position is debated in detail. \"For this particular game, we felt we might not always be afforded the open spaces out wide we were able to exploit against Italy, so an extra big ball-carrier in the back-row is thought to be necessary on this occasion. \"Obviously, it\\'s a 22-man game these days, and there is every chance that Jonathan will be making an impact from the bench.\" Wales have beaten France on two of their last three visits to Paris, and another victory this time around would keep them firmly on course for a first Five or Six Nations title triumph since 1994. \"Graham Henry (former Wales coach) said a couple of years ago that we should \\'be bold\\' when going to France, and he was proved right,\" said Ruddock. \"That is a great way to approach the game, and something we will further endorse with the players this week.\"\\n\\nG Thomas (Toulouse, capt); K Morgan (Newport-Gwent), T Shanklin (Cardiff), G Henson (Neath-Swansea), S Williams (Neath-Swansea); S Jones (Clermont Auvergne), D Peel (Llanelli); G Jenkins (Cardiff), M Davies (Gloucester), A Jones; (Neath-Swansea), B Cockbain (Neath-Swansea), R Sidoli (Cardiff); R Jones (Neath-Swansea), M Williams (Cardiff), M Owen (Newport-Gwent).\\n\\nReplacements: R McBryde (Llanelli), J Yapp (Cardiff), J Thomas (Neath-Swansea), R Sowden-Taylor (Cardiff), G Cooper (Newport-Gwent), C Sweeney Newport-Gwent), R Williams (Cardiff).\\n'",
        "body_tldr": "b'G Thomas (Toulouse, capt); K Morgan (Newport-Gwent), T Shanklin (Cardiff), G Henson (Neath-Swansea), S Williams (Neath-Swansea); S Jones (Clermont Auvergne), D Peel (Llanelli); G Jenkins (Cardiff), M Davies (Gloucester), A Jones; (Neath-Swansea), B Cockbain (Neath-Swansea), R Sidoli (Cardiff); R Jones (Neath-Swansea), M Williams (Cardiff), M Owen (Newport-Gwent).Thomas, a try-scorer in Rome, drops down to the bench instead of Ian Gough, while Cardiff back Rhys Williams steps up in place of Morgan.Replacements: R McBryde (Llanelli), J Yapp (Cardiff), J Thomas (Neath-Swansea), R Sowden-Taylor (Cardiff), G Cooper (Newport-Gwent), C Sweeney Newport-Gwent), R Williams (Cardiff).Wales coach Mike Ruddock has made two changes from the team that beat Italy 38-8 for Saturday\\'s trip to France.Luscombe is sidelined by a hamstring problem sustained during the Six Nations game against Italy last weekend.\"Due to his impressive performances from the bench, Kevin was very much in the selection mix anyway, and the unfortunate injury to Hal gives him the chance to start,\" said Ruddock.And in the pack Neath-Swansea Ospreys forward Ryan Jones is preferred at blindside flanker to Jonathan Thomas.'",
        "news_source": "BBC news"
      }
    ],
    [
      0.5870453715324402,
      {
        "title": "b'England 17-18 France\\n'",
        "body": "b\"England 17-18 France\\n\\nEngland suffered an eighth defeat in 11 Tests as scrum-half Dimitri Yachvili booted France to victory at Twickenham.\\n\\nTwo converted tries from Olly Barkley and Josh Lewsey helped the world champions to a 17-6 half-time lead. But Charlie Hodgson and Barkley missed six penalties between them, while Yachvili landed six for France to put the visitors in front. England could have won the game with three minutes left, but Hodgson pushed an easy drop goal opportunity wide. It was a dismal defeat for England, coming hard on the heels of an opening Six Nations loss in Wales. They should have put the game well beyond France's reach, but remarkably remained scoreless for the entire second half. A scrappy opening quarter saw both sides betray the lack of confidence engendered by poor opening displays against Wales and Scotland respectively. Hodgson had an early opportunity to settle English nerves but pushed a straightforward penalty attempt wide. But a probing kick from France centre Damien Traille saw Mark Cueto penalised for holding on to the ball in the tackle, Yachvili giving France the lead with a kick from wide out.\\n\\nFrance twice turned over England ball at the breakdown early on as the home side struggled to generate forward momentum, one Ben Kay charge apart. A spell of tit-for-tat kicking emphasised the caution on both sides, until England refused a possible three points to kick a penalty to the corner, only to botch the subsequent line-out. But England made the breakthrough after 19 minutes, when a faltering move off the back of a scrum led to the opening try. Jamie Noon took a short pass from Barkley and ran a good angle to plough through Yann Delaigue's flimsy tackle before sending his centre partner through to score at the posts.\\n\\nHodgson converted and added a penalty after one of several French infringements on the floor for a 10-3 lead. The fly-half failed to dispense punishment though with a scuffed attempt after France full-back Pepito Elhorga, scragged by Lewsey, threw the ball into touch. Barkley also missed two longer-range efforts as the first half drew to a close, but by then England had scored a second converted try. After a series of phases lock Danny Grewcock ran hard at the French defence and off-loaded out of Sylvain Marconnet's tackle to Lewsey. The industrious wing cut back in on an angle and handed off hooker Sebastien Bruno to sprint over. After a dire opening to the second half, France threw on three forward replacements in an attempt to rectify the situation, wing Jimmy Marlu having already departed injured. Yachvili nibbled away at the lead with a third penalty after 51 minutes.\\n\\nAnd when Lewis Moody was twice penalised - for handling in a ruck and then straying offside - the scrum-half's unerring left boot cut the deficit to two points. Barkley then missed his third long-range effort to increase the tension. And after seeing another attempt drop just short, Yachvili put France ahead with his sixth penalty with 11 minutes left.\\n\\nEngland sent on Ben Cohen and Matt Dawson, and after Barkley's kick saw Christophe Dominici take the ball over his own line, the stage was set for a victory platform. But even after a poor scrummage, Hodgson had the chance to seal victory but pushed his drop-goal attempt wide. England threw everything at the French in the final frantic moments, but the visitors held on for their first win at Twickenham since 1997.\\n\\nJ Robinson (capt); M Cueto, J Noon, O Barkley, J Lewsey; C Hodgson, H Ellis; G Rowntree, S Thompson, P Vickery; D Grewcock, B Kay; J Worsley, L Moody, M Corry.\\n\\nA Titterrell, A Sheridan, S Borthwick, A Hazell, M Dawson, H Paul, B Cohen.\\n\\nP Elhorga; C Dominici, B Liebenberg, D Traille, J Marlu; Y Delaigue, D Yachvili; S Marconnet, S Bruno, N Mas; F Pelous (capt), J Thion, S Betsen, J Bonnaire, S Chabal.\\n\\nW Servat, J Milloud, G Lamboley, Y Nyanga, P Mignoni, F Michalak, J-P Grandclaude.\\n\\nPaddy O'Brien (New Zealand)\\n\"",
        "body_tldr": "b\"But Charlie Hodgson and Barkley missed six penalties between them, while Yachvili landed six for France to put the visitors in front.But a probing kick from France centre Damien Traille saw Mark Cueto penalised for holding on to the ball in the tackle, Yachvili giving France the lead with a kick from wide out.And after seeing another attempt drop just short, Yachvili put France ahead with his sixth penalty with 11 minutes left.Barkley also missed two longer-range efforts as the first half drew to a close, but by then England had scored a second converted try.England could have won the game with three minutes left, but Hodgson pushed an easy drop goal opportunity wide.J Robinson (capt); M Cueto, J Noon, O Barkley, J Lewsey; C Hodgson, H Ellis; G Rowntree, S Thompson, P Vickery; D Grewcock, B Kay; J Worsley, L Moody, M Corry.England suffered an eighth defeat in 11 Tests as scrum-half Dimitri Yachvili booted France to victory at Twickenham.Hodgson had an early opportunity to settle English nerves but pushed a straightforward penalty attempt wide.After a dire opening to the second half, France threw on three forward replacements in an attempt to rectify the situation, wing Jimmy Marlu having already departed injured.Hodgson converted and added a penalty after one of several French infringements on the floor for a 10-3 lead.Yachvili nibbled away at the lead with a third penalty after 51 minutes.England sent on Ben Cohen and Matt Dawson, and after Barkley's kick saw Christophe Dominici take the ball over his own line, the stage was set for a victory platform.France twice turned over England ball at the breakdown early on as the home side struggled to generate forward momentum, one Ben Kay charge apart.\"",
        "news_source": "BBC news"
      }
    ],
    [
      0.5678454041481018,
      {
        "title": "b'Fear will help France - Laporte\\n'",
        "body": "b'Fear will help France - Laporte\\n\\nFrance coach Bernard Laporte believes his team will be scared going into their game with England on Sunday, but claims it will work in their favour.\\n\\nThe French turned in a stuttering performance as they limped to a 16-9 win against Scotland in the opening match of the Six Nations on Saturday. \"We will go to Twickenham with a little fear and it\\'ll give us a boost,\" said the French coach. He added: \"We are never good enough when we are favourites.\" Meanwhile, Perpignan centre Jean-Philippe Granclaude is delighted to have received his first call-up to the France squad. \"It\\'s incredible,\" the youngster said. \"I was not expecting it at all. \"Playing with the France team has always been a dream and now it has come true and I am about to face England at Twickenham in the Six Nations.\" Laporte will announce his starting line-up on Wednesday at the French team\\'s training centre in Marcoussis, near Paris.\\n'",
        "body_tldr": "b'\"We will go to Twickenham with a little fear and it\\'ll give us a boost,\" said the French coach.\"Playing with the France team has always been a dream and now it has come true and I am about to face England at Twickenham in the Six Nations.\"France coach Bernard Laporte believes his team will be scared going into their game with England on Sunday, but claims it will work in their favour.Laporte will announce his starting line-up on Wednesday at the French team\\'s training centre in Marcoussis, near Paris.'",
        "news_source": "BBC news"
      }
    ],
    [
      0.5327774882316589,
      {
        "title": "b'Dominici backs lacklustre France\\n'",
        "body": "b'Dominici backs lacklustre France\\n\\nWing Christophe Dominici says France can claim another Six Nations Grand Slam despite two lacklustre wins so far against Scotland and England.\\n\\nThe champions only just saw off the Scots in Paris, then needed England to self-destruct in last week\\'s 18-17 win. \"The English played better than us but lost, whereas we are still in the race for the Grand Slam,\" said Dominici. \"We know our display was not perfect, but we can still win the Grand Slam, along with Ireland and Wales.\" France , Ireland and Wales all remain unbeaten after two rounds of this year\\'s RBS Six Nations, with the two Celtic nations playing by far the more impressive rugby.\\n\\nFrance take on Wales at the Stade de France on 26 February and Ireland in Dublin on 12 March. But although France have yet to click, Dominici says that they can still win the hard way as long as scrum-half Dimitri Yachvili continues in his goalkicking form. \"If we have an efficient kicker on whom we can rely on, a solid defence and a team who play for their lives, we can achieve something,\" Dominici added. \"I said at the start of the competition that the winners would be clearer from the third matches, and that\\'s exactly what is going to happen.\" France coach Bernard Laporte will announce his starting line-up next Tuesday for the match against Wales.\\n\\nWing Jimmy Marlu is definitely out with the knee injury sustained at Twickenham, which is likely to sideline him for the rest of the tournament. Inspirational flanker Serge Betsen is a doubt with a thigh injury, but number eight Imanol Harinordoquy has shaken off his shoulder injury. In the backs, centre Yannick Jauzion and winger Aurelien Rougerie are all back in contention after injury, while Brive back Julien Laharrague has received his first call-up as a replacement for Pepito Elhorga.\\n'",
        "body_tldr": "b'Wing Christophe Dominici says France can claim another Six Nations Grand Slam despite two lacklustre wins so far against Scotland and England.\"We know our display was not perfect, but we can still win the Grand Slam, along with Ireland and Wales.\"But although France have yet to click, Dominici says that they can still win the hard way as long as scrum-half Dimitri Yachvili continues in his goalkicking form.France take on Wales at the Stade de France on 26 February and Ireland in Dublin on 12 March.\"The English played better than us but lost, whereas we are still in the race for the Grand Slam,\" said Dominici.France , Ireland and Wales all remain unbeaten after two rounds of this year\\'s RBS Six Nations, with the two Celtic nations playing by far the more impressive rugby.'",
        "news_source": "BBC news"
      }
    ],
    [
      0.5278875231742859,
      {
        "title": "b'Fit-again Betsen in France squad\\n'",
        "body": "b'Fit-again Betsen in France squad\\n\\nFrance have brought flanker Serge Betsen back into their squad to face England at Twickenham on Sunday.\\n\\nBut the player, who missed the victory over Scotland through injury, must attend a disciplinary hearing on Wednesday after being cited by Wasps. \"Serge has a good case so we are confident he will play,\" said France coach Bernard Laporte. The inexperienced Nicolas Mas, Jimmy Marlu and Jean-Philippe Grandclaude are also included in a 22-man squad. The trio have been called up after Pieter de Villiers, Ludovic Valbon and Aurelien Rougerie all picked up injuries in France\\'s 16-9 win on Saturday.\\n\\nLaporte said he was confident that Betsen would be cleared by the panel investigating his alleged trip that broke Wasps centre Stuart Abbott\\'s leg. \"If he was to be suspended, we would call up Imanol Harinordoquy or Thomas Lievremont,\" said Laporte, who has dropped Patrick Tabacco. \"We missed Serge badly against Scotland. He has now recovered from his thigh injury and played on Saturday with Biarritz.\" France\\'s regular back-row combination of Betsen, Harinordoquy and Olivier Magne were all missing from France\\'s side at the weekend because of injury. Laporte is expected to announce France\\'s starting line-up on Wednesday.\\n\\nForwards: Nicolas Mas, Sylvain Marconnet, Olivier Milloud, William Servat, Sebastien Bruno, Fabien Pelous, Jerome Thion, Gregory Lamboley, Serge Betsen, Julien Bonnaire, Sebastien Chabal, Yannick Nyanga. Backs: Dimitri Yachvili, Pierre Mignoni, Frederic Michalak, Yann Delaigue, Damien Traille, Brian Liebenberg, Jean-Philippe Grandclaude, Christophe Dominici, Jimmy Marlu, Pepito Elhorga.\\n'",
        "body_tldr": "b'\"Serge has a good case so we are confident he will play,\" said France coach Bernard Laporte.France\\'s regular back-row combination of Betsen, Harinordoquy and Olivier Magne were all missing from France\\'s side at the weekend because of injury.Laporte said he was confident that Betsen would be cleared by the panel investigating his alleged trip that broke Wasps centre Stuart Abbott\\'s leg.\"If he was to be suspended, we would call up Imanol Harinordoquy or Thomas Lievremont,\" said Laporte, who has dropped Patrick Tabacco.But the player, who missed the victory over Scotland through injury, must attend a disciplinary hearing on Wednesday after being cited by Wasps.France have brought flanker Serge Betsen back into their squad to face England at Twickenham on Sunday.'",
        "news_source": "BBC news"
      }
    ]
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
      // router.push({name: 'search_page',params: { data_returned: test_object }})
      axios.post('search/', {
        data:{'search_string':this.search_string},
        // headers:{"X-CSRFToken": csrfToken}
      })
      .then(function (response) {
        console.log(response.data);
        router.push({name: 'search_page',params: { data_returned: response.data }})
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